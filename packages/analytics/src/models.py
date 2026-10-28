"""Explainable statistical crop yield models for Nagpur District.

Implements:
1. OLS regression: Yield ~ Trend + Monsoon_Rainfall (mm)
2. Leave-One-Year-Out Cross-Validation (LOOCV) vs. Olympic 5-year Baseline.
3. Analytical Prediction Intervals (80% and 95% ranges).
4. Extrapolation boundary checks.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats
from packages.analytics.src.baseline import compute_olympic_average


class CropYieldRegressionModel:
    """Explainable Ordinary Least Squares regression model for crop yield."""

    def __init__(self, crop_id: str):
        self.crop_id = crop_id
        self.slope_trend: float = 0.0
        self.slope_rain: float = 0.0
        self.intercept: float = 0.0
        self.r_squared: float = 0.0
        self.p_value_rain: float = 1.0
        self.se_residual: float = 0.0
        self.degrees_of_freedom: int = 0
        self.min_historical_rain: float = 0.0
        self.max_historical_rain: float = 0.0
        self.loocv_mae_model: float = 0.0
        self.loocv_mae_baseline: float = 0.0
        self.loocv_mape_model: float = 0.0
        self.loocv_mape_baseline: float = 0.0
        self.beats_baseline: bool = False
        self.n_observations: int = 0
        self.xtx_inv: Optional[np.ndarray] = None
        self.X_mean: Optional[np.ndarray] = None

    def fit(self, df_merged: pd.DataFrame) -> "CropYieldRegressionModel":
        """Fit model on paired historical dataset.

        Expected columns:
        - crop_year (int)
        - yield_kg_ha (float)
        - monsoon_rf_mm (float)
        """
        clean_df = df_merged.dropna(subset=["crop_year", "yield_kg_ha", "monsoon_rf_mm"]).copy()
        clean_df = clean_df.sort_values("crop_year").reset_index(drop=True)
        self.n_observations = len(clean_df)

        if self.n_observations < 10:
            raise ValueError(f"Insufficient observations for {self.crop_id}: {self.n_observations}")

        # Features: [1, trend_index, monsoon_rf_mm]
        min_year = clean_df["crop_year"].min()
        clean_df["trend"] = clean_df["crop_year"] - min_year

        self.min_historical_rain = float(clean_df["monsoon_rf_mm"].min())
        self.max_historical_rain = float(clean_df["monsoon_rf_mm"].max())

        X = np.column_stack([
            np.ones(self.n_observations),
            clean_df["trend"].values,
            clean_df["monsoon_rf_mm"].values
        ])
        y = clean_df["yield_kg_ha"].values

        # OLS estimation: beta = (X'X)^-1 X'y
        xtx = X.T @ X
        self.xtx_inv = np.linalg.pinv(xtx)
        beta = self.xtx_inv @ X.T @ y

        self.intercept = float(beta[0])
        self.slope_trend = float(beta[1])
        self.slope_rain = float(beta[2])

        # Residuals and diagnostics
        y_pred = X @ beta
        residuals = y - y_pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)

        self.r_squared = float(1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0
        self.degrees_of_freedom = self.n_observations - 3
        self.se_residual = float(np.sqrt(ss_res / self.degrees_of_freedom))

        # Standard error of slope_rain and t-test
        var_beta = self.se_residual**2 * np.diag(self.xtx_inv)
        se_rain = np.sqrt(var_beta[2]) if var_beta[2] > 0 else 1.0
        t_stat_rain = self.slope_rain / se_rain
        self.p_value_rain = float(2.0 * (1.0 - stats.t.cdf(abs(t_stat_rain), df=self.degrees_of_freedom)))

        # Leave-One-Year-Out Cross-Validation (LOOCV)
        self._evaluate_loocv(clean_df, min_year)

        return self

    def _evaluate_loocv(self, df: pd.DataFrame, min_year: int):
        """Compute LOOCV MAE and MAPE for both Model and Olympic Baseline."""
        n = len(df)
        model_errors = []
        baseline_errors = []
        actuals = []

        for i in range(n):
            train_df = df.drop(index=i)
            test_row = df.iloc[i]

            actual_y = test_row["yield_kg_ha"]
            test_trend = test_row["crop_year"] - min_year
            test_rf = test_row["monsoon_rf_mm"]

            # Fit on n-1
            X_tr = np.column_stack([
                np.ones(n - 1),
                (train_df["crop_year"] - min_year).values,
                train_df["monsoon_rf_mm"].values
            ])
            y_tr = train_df["yield_kg_ha"].values
            b = np.linalg.pinv(X_tr.T @ X_tr) @ X_tr.T @ y_tr

            pred_y = b[0] + b[1] * test_trend + b[2] * test_rf
            model_errors.append(abs(actual_y - pred_y))

            # Baseline: Olympic average of prior 5 years (if available) or prior training years
            idx_in_train = train_df[train_df["crop_year"] < test_row["crop_year"]]["yield_kg_ha"].tolist()
            prior_vals = idx_in_train[-5:] if len(idx_in_train) >= 3 else train_df["yield_kg_ha"].tolist()
            baseline_y = compute_olympic_average(prior_vals)
            if baseline_y is not None:
                baseline_errors.append(abs(actual_y - baseline_y))
            else:
                baseline_errors.append(abs(actual_y - np.mean(y_tr)))

            actuals.append(actual_y)

        self.loocv_mae_model = float(np.mean(model_errors))
        self.loocv_mae_baseline = float(np.mean(baseline_errors))
        self.loocv_mape_model = float(np.mean([e / a for e, a in zip(model_errors, actuals) if a > 0]) * 100.0)
        self.loocv_mape_baseline = float(np.mean([e / a for e, a in zip(baseline_errors, actuals) if a > 0]) * 100.0)
        self.beats_baseline = bool(self.loocv_mae_model < self.loocv_mae_baseline)

    def predict_range(
        self,
        target_year: int,
        target_rain_mm: float,
        min_year: int = 1966
    ) -> Dict[str, Any]:
        """Predict yield point estimate and analytical prediction intervals (ranges)."""
        trend = target_year - min_year
        x0 = np.array([1.0, float(trend), float(target_rain_mm)])

        point_estimate = float(self.intercept + self.slope_trend * trend + self.slope_rain * target_rain_mm)

        # Standard error of prediction: se_pred = se_res * sqrt(1 + x0' (X'X)^-1 x0)
        leverage = float(x0.T @ self.xtx_inv @ x0) if self.xtx_inv is not None else 0.0
        se_prediction = float(self.se_residual * np.sqrt(max(0.0, 1.0 + leverage)))

        # Critical values for t-distribution
        t_80 = float(stats.t.ppf(0.90, df=self.degrees_of_freedom))
        t_95 = float(stats.t.ppf(0.975, df=self.degrees_of_freedom))

        ci_80_lower = max(0.0, point_estimate - t_80 * se_prediction)
        ci_80_upper = point_estimate + t_80 * se_prediction

        ci_95_lower = max(0.0, point_estimate - t_95 * se_prediction)
        ci_95_upper = point_estimate + t_95 * se_prediction

        # Extrapolation check: is target rainfall outside historical observed domain?
        is_extrapolated = bool(target_rain_mm < self.min_historical_rain or target_rain_mm > self.max_historical_rain)

        return {
            "crop_id": self.crop_id,
            "target_year": target_year,
            "target_rain_mm": target_rain_mm,
            "point_estimate_kg_ha": round(point_estimate, 1),
            "range_80": (round(ci_80_lower, 1), round(ci_80_upper, 1)),
            "range_95": (round(ci_95_lower, 1), round(ci_95_upper, 1)),
            "is_extrapolated": is_extrapolated,
            "historical_rain_domain": (self.min_historical_rain, self.max_historical_rain),
            "model_r_squared": round(self.r_squared, 3),
            "p_value_rain": round(self.p_value_rain, 4),
            "slope_per_100mm": round(self.slope_rain * 100.0, 1),
            "beats_baseline": self.beats_baseline,
            "loocv_mae": round(self.loocv_mae_model, 1),
            "baseline_mae": round(self.loocv_mae_baseline, 1),
            "confidence_disclaimer": "अंदाज (अधिकृत पीक कापणी प्रयोग अहवाल येईपर्यंत) / Estimate until official CCE publication"
        }

