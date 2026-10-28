"""Train explainable models, perform LOOCV, record metrics, and generate Model Cards."""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
import hashlib
from datetime import datetime
import pandas as pd
from sqlalchemy import func
from apps.api.src.db.session import SessionLocal
from apps.api.src.models.entities import FactCropYield, FactRainfall, ModelRegistry, ModelMetrics
from packages.analytics.src.models import CropYieldRegressionModel

DOCS_MODELS_DIR = ROOT_DIR / "docs" / "models"
DOCS_MODELS_DIR.mkdir(parents=True, exist_ok=True)


def get_paired_crop_rainfall_df(db, crop_id: str) -> pd.DataFrame:
    """Retrieve paired annual crop yields and monsoon rainfall (June-Sept total) for Nagpur."""
    # 1. Yields
    yield_records = db.query(
        FactCropYield.crop_year,
        FactCropYield.yield_kg_ha
    ).filter_by(
        district="Nagpur",
        crop_id=crop_id
    ).filter(FactCropYield.yield_kg_ha.isnot(None)).all()

    df_yields = pd.DataFrame(yield_records, columns=["crop_year", "yield_kg_ha"])

    # 2. Monsoon Rainfall (June-September sum per year)
    rain_records = db.query(
        FactRainfall.year,
        func.sum(FactRainfall.rainfall_mm).label("monsoon_rf_mm")
    ).filter_by(
        district="Nagpur"
    ).filter(
        FactRainfall.month.between(6, 9)
    ).group_by(FactRainfall.year).all()

    df_rain = pd.DataFrame(rain_records, columns=["crop_year", "monsoon_rf_mm"])

    # Merge on crop_year
    df_merged = pd.merge(df_yields, df_rain, on="crop_year", how="inner").sort_values("crop_year").reset_index(drop=True)
    return df_merged


def generate_model_card(model: CropYieldRegressionModel, df_train: pd.DataFrame, data_hash: str) -> str:
    """Generate Markdown Model Card compliant with scientific transparency standards."""
    card = f"""# Model Card: Nagpur {model.crop_id.capitalize()} Yield Response Model

**Version:** 1.0.0  
**Trained Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}  
**Target Crop:** `{model.crop_id}` (Nagpur District)  
**Algorithm:** Explainable Ordinary Least Squares (OLS) with Trend & Monsoon Rainfall  
**Training Data Hash (SHA-256):** `{data_hash}`  
**Number of Paired Historical Seasons:** {model.n_observations} (Years: {int(df_train['crop_year'].min())}–{int(df_train['crop_year'].max())})

---

## Model Specification

$$\\text{{Yield}}_t = \\beta_0 + \\beta_1 \\cdot (\\text{{Year}}_t - {int(df_train['crop_year'].min())}) + \\beta_2 \\cdot \\text{{MonsoonRF}}_t + \\epsilon_t$$

| Parameter | Coefficient | Description |
|---|---:|---|
| **Intercept ($\\beta_0$)** | {model.intercept:.2f} kg/ha | Base yield at start of series |
| **Trend Slope ($\\beta_1$)** | {model.slope_trend:+.2f} kg/ha/year | Annual technological & varietal progress |
| **Rainfall Response ($\\beta_2$)** | {model.slope_rain:+.3f} kg/ha per mm | **{model.slope_rain * 100:+.1f} kg/ha per 100mm** monsoon rainfall |

---

## Statistical Diagnostics & Significance

- **Coefficient of Determination ($R^2$):** **{model.r_squared:.3f}** (Explains {model.r_squared * 100:.1f}% of historical yield variance)
- **Rainfall p-value:** **{model.p_value_rain:.4f}** ({'Statistically significant (p < 0.05)' if model.p_value_rain < 0.05 else 'Not statistically significant at 5% level'})
- **Residual Standard Error ($s_e$):** {model.se_residual:.1f} kg/ha
- **Degrees of Freedom:** {model.degrees_of_freedom}

---

## Validation & Benchmark Evaluation (Leave-One-Year-Out Cross-Validation)

Evaluated against the naive **5-Year Olympic Average Baseline** (WFP/PMFBY standard):

| Metric | OLS Regression Model | 5-Year Olympic Baseline | Evaluation Verdict |
|---|---:|---:|---|
| **LOOCV Mean Absolute Error (MAE)** | **{model.loocv_mae_model:.1f} kg/ha** | {model.loocv_mae_baseline:.1f} kg/ha | **{'BEATS BASELINE' if model.beats_baseline else 'DOES NOT BEAT BASELINE'}** |
| **LOOCV Mean Absolute % Error (MAPE)** | **{model.loocv_mape_model:.1f}%** | {model.loocv_mape_baseline:.1f}% | {'Exposed in API' if model.beats_baseline else 'Analog matching prioritized'} |

---

## Prediction Boundaries & Extrapolation Checks

- **Observed Monsoon Rainfall Domain:** {model.min_historical_rain:.1f} mm to {model.max_historical_rain:.1f} mm.
- **Extrapolation Policy:** Predictions for seasons with rainfall below {model.min_historical_rain:.1f} mm or above {model.max_historical_rain:.1f} mm are explicitly flagged in the API with `is_extrapolated: true`.
- **Confidence Intervals:** Analytical Student's t prediction intervals (80% and 95%) are provided for all points. Point predictions are never returned in isolation.

---

## Limitations

1. **District-Level Aggregation:** Official yield statistics are compiled and reported only at the district level. This model cannot predict individual field or plot-level microclimate yields.
2. **Current-Season Status:** Any estimate for the ongoing season is labelled *"Estimate until official Crop Cutting Experiments (CCE) are released"*.
"""
    return card


def train_and_register_all():
    """Train models for main crops, store metrics, and generate model cards."""
    db = SessionLocal()
    try:
        crops = ["soybean", "cotton", "rice"]
        for crop_id in crops:
            df = get_paired_crop_rainfall_df(db, crop_id)
            if len(df) < 10:
                print(f"Skipping {crop_id}: insufficient paired data ({len(df)} rows)")
                continue

            # Data hash
            data_bytes = df.to_csv(index=False).encode("utf-8")
            data_hash = hashlib.sha256(data_bytes).hexdigest()

            # Fit model
            model = CropYieldRegressionModel(crop_id)
            model.fit(df)

            # Register in database
            model_id = f"MODEL_{crop_id.upper()}_V1"
            existing_model = db.query(ModelRegistry).filter_by(model_id=model_id).first()
            params = {
                "intercept": model.intercept,
                "slope_trend": model.slope_trend,
                "slope_rain": model.slope_rain,
                "r_squared": model.r_squared,
                "p_value_rain": model.p_value_rain,
                "se_residual": model.se_residual,
                "df": model.degrees_of_freedom,
                "min_rain": model.min_historical_rain,
                "max_rain": model.max_historical_rain,
                "min_year": int(df["crop_year"].min())
            }

            if not existing_model:
                db.add(ModelRegistry(
                    model_id=model_id,
                    crop_id=crop_id,
                    model_type="OLS_TREND_RAIN",
                    trained_at=datetime.utcnow(),
                    data_hash=data_hash,
                    parameters_json=json.dumps(params)
                ))

            # Store metrics
            metric_id = f"METRIC_{crop_id.upper()}_V1"
            existing_metric = db.query(ModelMetrics).filter_by(metric_id=metric_id).first()
            if not existing_metric:
                db.add(ModelMetrics(
                    metric_id=metric_id,
                    model_id=model_id,
                    loocv_mae=model.loocv_mae_model,
                    loocv_mape=model.loocv_mape_model,
                    r_squared=model.r_squared,
                    p_value=model.p_value_rain,
                    baseline_mae=model.loocv_mae_baseline,
                    beats_baseline=model.beats_baseline
                ))

            db.commit()

            # Write Model Card
            card_md = generate_model_card(model, df, data_hash)
            card_path = DOCS_MODELS_DIR / f"{crop_id}_model_card.md"
            card_path.write_text(card_md, encoding="utf-8")
            print(f"Model Card written: {card_path} | R² = {model.r_squared:.3f} | Beats Baseline: {model.beats_baseline}")

    finally:
        db.close()


if __name__ == "__main__":
    train_and_register_all()
