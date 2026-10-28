# Model Card: Nagpur Rice Yield Response Model

**Version:** 1.0.0  
**Trained Date:** 2026-10-28 17:52:33 UTC  
**Target Crop:** `rice` (Nagpur District)  
**Algorithm:** Explainable Ordinary Least Squares (OLS) with Trend & Monsoon Rainfall  
**Training Data Hash (SHA-256):** `1f516b77b74fa609c69ac6217a0ea750881048c7953438c7bd21ba6e553e44a2`  
**Number of Paired Historical Seasons:** 49 (Years: 1966–2015)

---

## Model Specification

$$\text{Yield}_t = \beta_0 + \beta_1 \cdot (\text{Year}_t - 1966) + \beta_2 \cdot \text{MonsoonRF}_t + \epsilon_t$$

| Parameter | Coefficient | Description |
|---|---:|---|
| **Intercept ($\beta_0$)** | 159.12 kg/ha | Base yield at start of series |
| **Trend Slope ($\beta_1$)** | +10.15 kg/ha/year | Annual technological & varietal progress |
| **Rainfall Response ($\beta_2$)** | +0.828 kg/ha per mm | **+82.8 kg/ha per 100mm** monsoon rainfall |

---

## Statistical Diagnostics & Significance

- **Coefficient of Determination ($R^2$):** **0.518** (Explains 51.8% of historical yield variance)
- **Rainfall p-value:** **0.0000** (Statistically significant (p < 0.05))
- **Residual Standard Error ($s_e$):** 227.9 kg/ha
- **Degrees of Freedom:** 46

---

## Validation & Benchmark Evaluation (Leave-One-Year-Out Cross-Validation)

Evaluated against the naive **5-Year Olympic Average Baseline** (WFP/PMFBY standard):

| Metric | OLS Regression Model | 5-Year Olympic Baseline | Evaluation Verdict |
|---|---:|---:|---|
| **LOOCV Mean Absolute Error (MAE)** | **193.1 kg/ha** | 257.5 kg/ha | **BEATS BASELINE** |
| **LOOCV Mean Absolute % Error (MAPE)** | **19.9%** | 27.4% | Exposed in API |

---

## Prediction Boundaries & Extrapolation Checks

- **Observed Monsoon Rainfall Domain:** 559.5 mm to 1406.3 mm.
- **Extrapolation Policy:** Predictions for seasons with rainfall below 559.5 mm or above 1406.3 mm are explicitly flagged in the API with `is_extrapolated: true`.
- **Confidence Intervals:** Analytical Student's t prediction intervals (80% and 95%) are provided for all points. Point predictions are never returned in isolation.

---

## Limitations

1. **District-Level Aggregation:** Official yield statistics are compiled and reported only at the district level. This model cannot predict individual field or plot-level microclimate yields.
2. **Current-Season Status:** Any estimate for the ongoing season is labelled *"Estimate until official Crop Cutting Experiments (CCE) are released"*.
