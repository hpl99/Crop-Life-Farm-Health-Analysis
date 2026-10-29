# Statistical Models, Features, Parameters & Results Summary
**Project:** Nagpur Krishi Data (नागपूर शेती आकडे)  
**District Scope:** Nagpur District, Maharashtra, India (Exclusively)  
**Evaluation Standard:** Leave-One-Out Cross-Validation (LOOCV) vs. 5-Year Olympic Baseline  

---

## 1. Overview of Models Used

| Model Family | Role / Purpose | Mechanism |
|---|---|---|
| **Explainable OLS Multiple Linear Regression** | Yield Trend & Monsoon Sensitivity | $\text{Yield}_t = \beta_0 + \beta_1 \cdot \text{Trend}_t + \beta_2 \cdot \text{Rainfall}_t + \epsilon_t$ |
| **5-Year Olympic Average Baseline** | Agricultural Actuarial Benchmark | Drops min & max of preceding 5 years, averages middle 3 (PMFBY / WFP standard) |
| **Analytical Prediction Intervals** | Uncertainty Quantification | 80% & 95% intervals via Student's $t$ with design matrix variance scaling |
| **Historical Analog Matching** | Transparent Scenario Exploration | Nearest-neighbor matching over rainfall deficit & drought characteristics |

---

## 2. Features Used

| Feature Name | Type | Description | Source |
|---|---|---|---|
| **`monsoon_rf_mm`** | Continuous (float) | Total June–September cumulative rainfall (mm) | IMD Nagpur & Open-Meteo ERA5 Reanalysis |
| **`trend`** | Discrete integer | Year index: $(\text{crop\_year} - \min(\text{historical\_year}))$ | Captures technological adoption, mechanization, and seed varieties |
| **`intercept`** | Constant ($1.0$) | Base regression intercept | Model constant |
| **`yield_kg_ha`** *(Target)* | Continuous (float) | Final crop yield in kg/ha | Official Crop Cutting Experiments (DES / UPAG / ICRISAT) |

---

## 3. Fitted Model Parameters & Coefficients

All parameters are fitted using Ordinary Least Squares on paired historical seasons for Nagpur district:

| Crop | Model ID | Seasons ($N$) | Intercept ($\beta_0$) | Trend Slope ($\beta_1$) | Rain Slope ($\beta_2$) | Rainfall Sensitivity (per 100mm) | Residual SE ($s_e$) | Degrees of Freedom |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Soybean** | `MODEL_SOYBEAN_V1` | 27 (1987–2014) | 567.62 kg/ha | -1.16 kg/ha/yr | +0.330 kg/ha/mm | **+33.0 kg/ha** | 290.49 kg/ha | 24 |
| **Cotton** | `MODEL_COTTON_V1` | 48 (1966–2014) | 21.88 kg/ha | +4.56 kg/ha/yr | +0.021 kg/ha/mm | **+2.1 kg/ha** | 37.59 kg/ha | 45 |
| **Rice (Paddy)** | `MODEL_RICE_V1` | 49 (1966–2015) | 159.12 kg/ha | +10.15 kg/ha/yr | +0.828 kg/ha/mm | **+82.8 kg/ha** | 227.86 kg/ha | 46 |

---

## 4. Empirical Results & LOOCV Performance

Every model was tested out-of-sample using **Leave-One-Out Cross-Validation (LOOCV)** and compared against the **5-Year Olympic Baseline**:

| Crop | $R^2$ Variance Explained | Rainfall $p$-value | Statistical Significance ($\alpha=0.05$) | Model LOOCV MAE | Baseline Olympic MAE | LOOCV MAPE | Beats Baseline? | System Behavior |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Soybean** | **0.053** (5.3%) | 0.2609 | Not Significant ($p > 0.05$) | 255.46 kg/ha | **227.53 kg/ha** | 42.3% | ❌ **No** | System honestly marks `model_beats_baseline: false`; displays Olympic baseline alongside range; prioritizes Analog matching |
| **Cotton** | **0.759** (75.9%) | 0.4693 | Trend driven (Bt-cotton tech) | **31.11 kg/ha** | 33.79 kg/ha | 26.6% | ✅ **Yes** | Model outperforms naive baseline by 2.68 kg/ha |
| **Rice (Paddy)** | **0.518** (51.8%) | $7.79 \times 10^{-6}$ | **Highly Significant ($p < 0.001$)** | **193.11 kg/ha** | 257.51 kg/ha | 19.9% | ✅ **Yes** | Model outperforms baseline significantly (25.0% error reduction) |

---

## 5. Analytical Prediction Intervals & Extrapolation Bounds

For any scenario rainfall $x_0 = [1, \text{trend}, \text{rainfall}]$, the prediction range is computed as:

$$\hat{y} \pm t_{\alpha/2, \text{df}} \cdot s_e \sqrt{1 + x_0^T (X^T X)^{-1} x_0}$$

- **Domain Range:** $559.5\text{ mm}$ to $1406.3\text{ mm}$.
- **Extrapolation Safety Rule:** If input rainfall $< 559.5\text{ mm}$ or $> 1406.3\text{ mm}$, the API sets `is_extrapolated = True` and displays an explicit cautionary badge.
- **Uncertainty Tiers:** 80% interval (primary range for planning) and 95% interval (wide risk range).

---

## 6. Historical Analog Matching Results (2026 Drought Season)

For the **2026 Season** (Nagpur District: ~618 mm rainfall, **-34% deficit**, 14/14 tehsils drought-affected under GR dated 25 Sep 2026), the top matched historical analogs are:

| Rank | Historical Season | Monsoon Rainfall | Deficit % | Soybean Yield | Cotton Yield | Rice Yield | Historical Recorded Event |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **#1** | **2004** | 623.2 mm | -33.4% | 617 kg/ha | 88 kg/ha | 610 kg/ha | Severe dry spells in July & August across Vidarbha |
| **#2** | **1987** | 559.5 mm | -40.2% | 789 kg/ha | 41 kg/ha | 394 kg/ha | Historic pan-India monsoon failure & major drought |
| **#3** | **2009** | 665.4 mm | -28.9% | 960 kg/ha | 109 kg/ha | 1023 kg/ha | Late monsoon onset followed by prolonged August dry spell |

---

## 7. Model Persistence & API Access

All model artifacts and LOOCV validation metrics are stored in the curated database:
- **Registry Table:** `model_registry` (`MODEL_SOYBEAN_V1`, `MODEL_COTTON_V1`, `MODEL_RICE_V1`)
- **Metrics Table:** `model_metrics` (LOOCV MAE, MAPE, $R^2$, $p$-value, baseline comparison)
- **API Endpoints:**
  - `GET /api/v1/crops/{crop}/rainfall-response`
  - `GET /api/v1/outlook/{crop}?deficit_pct=-34.0`
  - `GET /api/v1/lab/regression?crop=soybean`

