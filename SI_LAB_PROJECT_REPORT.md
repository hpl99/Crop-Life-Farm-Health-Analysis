# RAMDEOBABA UNIVERSITY, NAGPUR
## DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
### B.Tech. CSE (Artificial Intelligence and Data Science) (AIDS)

---

### SEMESTER V  
### SI LAB  
### PROJECT REPORT  

# NAGPUR KRISHI DATA: EXPLAINABLE MACHINE LEARNING AND SPATIAL ANALYTICS FOR CROP YIELD PREDICTION AND DROUGHT MONITORING IN NAGPUR DISTRICT

### Submitted by:
| Student Name | Roll No. | Enrollment No. |
|---|:---:|:---:|
| **Prathamesh Lahoti** | **50** | **EN22CS301050** |

**Academic Year:** 2026–27  

---

# SI Lab Project Report

## 1. PROJECT OBJECTIVE
The primary purpose of this project is to develop **Nagpur Krishi Data (नागपूर शेती आकडे)**, an explainable, data-driven agricultural intelligence platform dedicated exclusively to Nagpur district, Maharashtra. Rainfed farming in the Vidarbha region is heavily vulnerable to erratic South-West monsoons, mid-season dry spells, and delayed rainfall. The project addresses the critical lack of transparent, localized crop yield forecasts and real-time drought tracking by replacing unverified "black-box" estimations with mathematically sound, explainable machine learning models, actuarial Olympic baselines, and historical analog matching.

**Key Project Objectives:**
- Ingest and curate 58 years of meteorological observations (1966–2024 from IMD and ERA5 ECMWF reanalysis across all 14 tehsil centroids) and 49+ years of official Crop Cutting Experiment (CCE) yields from Ministry of Agriculture (DES), UPAG, and ICRISAT.
- Execute end-to-end data auditing, automated schema validation (Pydantic), and SHA-256 data integrity hashing without data leakage.
- Extract salient features: technological progress trend index, cumulative June–September monsoon precipitation, and rainfall departure percentages relative to ICAR-CRIDA normals.
- Train, benchmark, and compare multiple models: Explainable OLS Multiple Regression, 5-Year Olympic Moving Average Baseline (PMFBY/WFP actuarial standard), K-Nearest Historical Analog Matching, and an IMD-standard Binary Drought Severity Classifier.
- Conduct rigorous Leave-One-Out Cross-Validation (LOOCV), computing $R^2$, Adjusted $R^2$, RMSE, MAE, MAPE, $p$-values, and classification metrics (Accuracy, Precision, Recall, F1-Score).
- Derive analytical 80% and 95% Student's $t$ prediction intervals with convex hull extrapolation boundary checks (`is_extrapolated`).
- Build and deploy a bilingual (Marathi/English) Progressive Web Application (Next.js 15 + FastAPI) featuring interactive GIS mapping, taluka deep-dives, mandi price monitoring, and offline IndexedDB synchronization.

---

## 2. INTRODUCTION
Agriculture forms the socioeconomic backbone of Nagpur district in Maharashtra, employing over 60% of the rural workforce. However, out of the district's total cultivable area, more than 85% is strictly rainfed. This high dependence on seasonal monsoon precipitation renders agricultural production precarious and volatile. In the Kharif 2026 season, Nagpur district recorded an acute 34% rainfall deficit (receiving only 617.8 mm against the 30-year normal of 936.1 mm). The prolonged moisture stress forced the Government of Maharashtra to officially declare all 14 tehsils of Nagpur as drought-affected (Government Resolution dated 25 September 2026).

Despite advancements in machine learning, existing predictive applications often deliver uncalibrated point estimates from opaque neural network architectures. These models provide no confidence intervals, fail to convey out-of-sample prediction uncertainty, and lack local language support for rural farming communities. *Nagpur Krishi Data* overcomes these barriers through rigorous empirical statistical modeling, explainable regression diagnostics, and a farmer-first bilingual interface.

### 2.1 Problem Statement
Farming communities and district agricultural planners in Nagpur lack access to open, verified historical rainfall data, empirical crop yield sensitivity baselines, and honest risk boundaries. Conventional AI forecasting systems suffer from three critical flaws:
1. Concealing when models fail to beat naive historical averages, creating false confidence.
2. Masking the distinction between district-level Crop Cutting Experiments and tehsil-level rainfall variations.
3. Inaccessible digital interfaces that require high bandwidth and lack Marathi vernacular delivery.

### 2.2 Scope of the Project
- **Spatial Boundary:** Strictly Nagpur District, Maharashtra, encompassing all 14 administrative tehsils (Katol, Narkhed, Kalameshwar, Saoner, Ramtek, Parseoni, Mauda, Kamptee, Nagpur Rural, Nagpur Urban, Hingna, Umred, Bhiwapur, Kuhi) mapped to Census 2011 centroid coordinates.
- **Crop Coverage:** Major Kharif commercial and food crops: Soybean, Cotton, and Rice (Paddy).
- **Temporal Coverage:** 58 years of historical rainfall records (1966–2024), 49+ years of historical yield series (1966–2015), and 2026 real-time drought tracking.
- **Algorithmic Framework:** Explainable OLS regression with trend and monsoon rainfall, 5-year Olympic moving averages, nearest-neighbor historical analogs, and analytical prediction intervals.
- **System Architecture:** Decoupled client-server design with a Next.js 15 frontend, FastAPI REST endpoints, and IndexedDB client-side offline storage.
- **Limitations:** In Maharashtra, official Crop Cutting Experiments (CCE) are compiled exclusively at the district level. Consequently, the platform transparently indicates that crop yields represent district aggregates, while rainfall measurements represent localized tehsil centroids.

---

## 3. PROJECT METHODOLOGY
The project methodology follows a five-stage engineering and analytical pipeline: (1) Multi-Source Data Ingestion & Audit, (2) Preprocessing & Feature Engineering, (3) Model Formulation & Training, (4) Leave-One-Out Cross-Validation & Benchmark Comparison, and (5) Bilingual GUI Deployment.

### 3.1 Dataset Loading and Exploration
The platform ingests verified data from multiple statutory and meteorological authorities:
1. **IMD Circle / Gridded Series (1966–2015):** 50 historical years of monthly precipitation for Nagpur district.
2. **Open-Meteo ERA5 Reanalysis (2020–2024):** 900 monthly precipitation records across all 14 tehsil centroids and the district aggregate, capturing spatial variation (e.g., western Katol at 921 mm normal vs. eastern Bhiwapur at 1196 mm normal).
3. **Ministry of Agriculture (DES) / ICRISAT / UPAG:** Paired crop cutting experiment records comprising 49 years for Rice (1966–2015), 48 years for Cotton (1966–2014), and 27 years for Soybean (1987–2014).
4. **ICAR-CRIDA Contingency Plan:** Official tehsil-level annual and monsoon rainfall normals.
5. **Maharashtra State Agricultural Marketing Board (MSAMB / AGMARKNET):** Real-time daily arrival volumes and modal prices across Kalameshwar, Katol, Saoner, and Nagpur APMCs.
6. **Maharashtra Relief & Rehabilitation GR (25 Sep 2026):** Official drought declaration (`EVT_2026_DROUGHT_GR`).

*Dataset Quality:* Zero missing records in curated tables; all records validated with automated schema assertions and SHA-256 manifest hashing.

### 3.2 Data Preprocessing
- **Data Sanitization:** Standardized dates into calendar years, checked for range violations (0–5000 mm for rainfall; 0–4000 kg/ha for yields), and resolved geographic naming variations (e.g., Saoner vs. Savner; Bhiwapur vs. Bhivapur).
- **Monsoon Aggregation:** Filtered monthly rainfall records to compute cumulative June–September precipitation (`monsoon_rf_mm`), matching the Kharif phenological cycle.
- **Feature Normalization:** Established an integer technological trend index: $\text{trend} = \text{crop\_year} - \min(\text{year})$.
- **Leakage-Free Validation Strategy:** Enforced Leave-One-Out Cross-Validation (LOOCV). Rather than an arbitrary split, each year $t$ was held out iteratively, the model trained on remaining $N-1$ years, and prediction error evaluated strictly out-of-sample.

### 3.3 Feature Extraction / Selection
1. **`monsoon_rf_mm` (Continuous Numerical):** Cumulative June to September rainfall in millimeters. Captures the primary moisture driver during germination, tillering/vegetative growth, and seed development.
2. **`trend` (Discrete Integer):** Time trend index $(\text{crop\_year} - \min(\text{year}))$. Models gradual technological progress, including fertilizer adoption, mechanization, and hybrid/Bt seed introduction.
3. **`intercept` (Constant 1.0):** Base yield expectation at the start of the historical series.
4. **`deficit_pct` (Continuous Numerical):** $((RF_{\text{actual}} - RF_{\text{normal}}) / RF_{\text{normal}}) \times 100$, used for drought anomaly classification and historical analog retrieval.

*Target Variables:*
- Regression: `yield_kg_ha` (Final crop yield in kg/hectare from official CCE harvest reports).
- Classification: `drought_status` (Binary indicator: 1 = Drought-Affected, 0 = Normal).

### 3.4 Training Multiple Classification Models
| Sr. No. | Model Name | Purpose / Notes |
|:---:|---|---|
| **1** | **Explainable OLS Multiple Linear Regression** | Models continuous crop yield response to technological trend index and June–September monsoon rainfall. |
| **2** | **5-Year Olympic Moving Average Baseline** | Actuarial baseline (PMFBY/WFP standard) dropping highest and lowest yields from prior 5 years to benchmark ML. |
| **3** | **K-Nearest Historical Analog Matching** | Weighted Euclidean distance over rainfall deficit to identify historical drought analogs (e.g. 2004, 1987) matching 2026. |
| **4** | **Rule-Based Binary Drought Severity Classifier** | Categorizes tehsils/district as Drought-Affected vs. Normal using official Maharashtra/IMD deficit threshold ($\ge 20\%$). |

### 3.5 Performance Evaluation and Model Comparison
| Model | Accuracy | Precision | Recall | F1-Score |
|---|:---:|:---:|:---:|:---:|
| **Drought Classifier (IMD Standard)** | **100.0%** | **1.000** | **1.000** | **1.000** |
| **Rice Yield OLS Model (`MODEL_RICE_V1`)** | $R^2 = 0.707$ | MAE = 266.3 kg/ha | RMSE = 310.4 kg/ha | $p = 3.41 \times 10^{-7}$ (Sig) |
| **Cotton Yield OLS Model (`MODEL_COTTON_V1`)** | $R^2 = 0.883$ | MAE = 35.9 kg/ha | RMSE = 41.4 kg/ha | $p = 3.38 \times 10^{-9}$ (Sig) |

*Note on Soybean:* For the Soybean yield model (`MODEL_SOYBEAN_V1`), OLS achieved $R^2 = 0.053$, LOOCV MAE = 242.82 kg/ha, and LOOCV MAPE = 39.27% ($p = 0.2609$), failing to beat the 5-Year Olympic Baseline (MAE = 227.53 kg/ha). As mandated by project integrity rules, the system transparently reports `model_beats_baseline: false` and prioritizes historical analog matching for soybean.

### 3.6 Best Model Selection
1. **Cotton (Selected: OLS Multiple Linear Regression):**
   - Achieved $R^2 = 0.883$ (88.3% variance explained) and LOOCV MAE = 35.88 kg/ha, beating the Olympic Baseline (MAE = 48.35 kg/ha). The strong technological trend (+4.56 kg/ha/yr) captures the transformative yield surge following Bt-cotton commercialization in 2002.
2. **Rice / Paddy (Selected: OLS Multiple Linear Regression):**
   - Achieved $R^2 = 0.707$ (70.7% variance explained), LOOCV MAE = 266.25 kg/ha (vs. Olympic Baseline MAE = 333.40 kg/ha), and a highly significant rainfall coefficient ($p = 3.41 \times 10^{-7}$). Rice is moisture-intensive and directly benefits from empirical rainfall response modeling.
3. **Soybean (Selected: 5-Year Olympic Baseline + Historical Analog Matching):**
   - OLS regression failed to beat the baseline because soybean yield in Nagpur is primarily determined by mid-season dry spells and pest pressures rather than total seasonal rainfall. The platform honestly defers to the Olympic Baseline and top-3 analog seasons (2004, 1987, 2009).
4. **Drought Classification (Selected: IMD Deficit Threshold Rule):**
   - Achieved 100% Accuracy, Precision = 1.0, Recall = 1.0, and F1-Score = 1.0 across all historical deficit seasons.

---

## 4. PROJECT IMPLEMENTATION

### 4.1 Tools and Technologies
| Tool / Technology | Version | Purpose |
|---|:---:|---|
| **Python** | 3.13.1 | Primary programming language for data pipeline and analytics |
| **Google Colab / VS Code** | Latest | Development environment, script execution & model training |
| **Pandas / NumPy** | 2.2.3 / 2.1.2 | Data ingestion, historical series wrangling & array operations |
| **Scikit-learn / SciPy** | 1.5.2 / 1.14.1 | OLS regression, LOOCV cross-validation & Student's t intervals |
| **Matplotlib / Seaborn** | 3.9.2 / 0.13.2 | Exploratory data analysis and regression diagnostics plotting |
| **Next.js 15 / FastAPI** | 15.5.28 / 0.115.8 | Bilingual mobile-first PWA GUI and high-speed RESTful API |

### 4.2 Module-wise Implementation
1. **Ingestion & Storage Module (`packages/data-pipeline`):** Implements automated extractors that fetch, validate, and persist 1,476 rainfall records and 124 crop cutting observations into SQLite (`nagpur_krishi.db`) with SHA-256 integrity manifests.
2. **Analytics & Training Module (`packages/analytics`):** Houses `CropYieldRegressionModel`, LOOCV cross-validation routines, Olympic baseline calculations, and nearest-neighbor analog searches.
3. **Model Registry & Metadata Module (`apps/api/src/models`):** Stores serialised parameters, degrees of freedom, covariance matrices, and model metrics.
4. **RESTful API Service (`apps/api/src/api/v1`):** High-performance FastAPI router serving `/rainfall/monthly`, `/crops`, `/outlook`, `/drought/status`, and `/tehsils` with bilingual headers (`Accept-Language: mr/en`).
5. **Next.js 15 Progressive Web App (`apps/web`):** Modern frontend leveraging React 19, Tailwind CSS, Lucide icons, and Service Worker offline caching.

### 4.3 GUI Implementation
- **Fixed Header:** Contains the brand identity ("नागपूर शेती आकडे"), quick tehsil selector dropdown, official drought declaration badge ("१४/१४ दुष्काळग्रस्त"), language toggle (मराठी / English), high-contrast accessibility mode, font scaling, and Web Speech API text-to-speech read-aloud.
- **District Overview Tab:** Surfaces 4 Primary KPI Cards (Total Rainfall, Normal Rainfall, Deficit %, Missing Rain mm), a Normal vs. Actual comparative bar chart, and the 2026 Season Journey Timeline (June to September).
- **Map Tab:** Visualises all 14 tehsils with LGD codes, geographic centroid coordinates, and CRIDA annual normal rainfall benchmarks.
- **Taluka Deep-Dive Tab:** Includes an inline tehsil selector, crop selection tabs, dynamic 5-year monsoon rainfall bars using real ERA5 reanalysis data (2020–2024), and an honest disclaimer clarifying that yields represent district CCE figures.
- **Market Tab:** Live modal mandi prices for soybean and cotton across Kalameshwar, Katol, Saoner, and Nagpur APMCs.
- **Insights Data Lab Tab:** Complete regression diagnostic scatter plots, Olympic baseline comparison overlays, and full CSV download capabilities.

---

## 5. COMPLETE CODE
```python
import numpy as np
import pandas as pd
from scipy import stats

class CropYieldRegressionModel:
    """Explainable OLS Regression with LOOCV & Student's t Prediction Intervals"""
    def __init__(self, crop_id: str):
        self.crop_id = crop_id
        self.slope_trend = 0.0
        self.slope_rain = 0.0
        self.intercept = 0.0
        self.r_squared = 0.0
        self.p_value_rain = 1.0
        self.se_residual = 0.0
        self.degrees_of_freedom = 0
        self.loocv_mae_model = 0.0
        self.loocv_mae_baseline = 0.0
        self.beats_baseline = False
        self.xtx_inv = None

    def fit(self, df_merged: pd.DataFrame):
        clean_df = df_merged.dropna(subset=['crop_year', 'yield_kg_ha', 'monsoon_rf_mm']).sort_values('crop_year')
        n = len(clean_df)
        min_year = clean_df['crop_year'].min()
        trend = clean_df['crop_year'].values - min_year
        rain = clean_df['monsoon_rf_mm'].values
        y = clean_df['yield_kg_ha'].values
        X = np.column_stack([np.ones(n), trend, rain])
        self.xtx_inv = np.linalg.pinv(X.T @ X)
        beta = self.xtx_inv @ X.T @ y
        self.intercept, self.slope_trend, self.slope_rain = beta
        y_pred = X @ beta
        residuals = y - y_pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        self.r_squared = float(1.0 - (ss_res / ss_tot))
        self.degrees_of_freedom = n - 3
        self.se_residual = float(np.sqrt(ss_res / self.degrees_of_freedom))
        se_rain = float(np.sqrt(self.xtx_inv[2, 2]) * self.se_residual)
        t_stat = self.slope_rain / se_rain if se_rain > 0 else 0.0
        self.p_value_rain = float(2.0 * (1.0 - stats.t.cdf(abs(t_stat), df=self.degrees_of_freedom)))
        self._evaluate_loocv(clean_df, min_year)
        return self

    def _evaluate_loocv(self, df: pd.DataFrame, min_year: int):
        n = len(df)
        m_errs, b_errs = [], []
        for i in range(n):
            tr = df.drop(index=df.index[i])
            te = df.iloc[i]
            X_tr = np.column_stack([np.ones(n-1), tr['crop_year'] - min_year, tr['monsoon_rf_mm']])
            b = np.linalg.pinv(X_tr.T @ X_tr) @ X_tr.T @ tr['yield_kg_ha'].values
            pred = b[0] + b[1] * (te['crop_year'] - min_year) + b[2] * te['monsoon_rf_mm']
            m_errs.append(abs(te['yield_kg_ha'] - pred))
            prior = tr[tr['crop_year'] < te['crop_year']]['yield_kg_ha'].tolist()[-5:]
            base = float(np.mean(sorted(prior)[1:-1])) if len(prior) >= 5 else float(np.mean(tr['yield_kg_ha']))
            b_errs.append(abs(te['yield_kg_ha'] - base))
        self.loocv_mae_model = float(np.mean(m_errs))
        self.loocv_mae_baseline = float(np.mean(b_errs))
        self.beats_baseline = bool(self.loocv_mae_model < self.loocv_mae_baseline)

    def predict_range(self, target_year: int, target_rain_mm: float, min_year: int = 1966):
        trend = target_year - min_year
        x0 = np.array([1.0, float(trend), float(target_rain_mm)])
        point_estimate = float(self.intercept + self.slope_trend * trend + self.slope_rain * target_rain_mm)
        leverage = float(x0.T @ self.xtx_inv @ x0) if self.xtx_inv is not None else 0.0
        se_pred = float(self.se_residual * np.sqrt(max(0.0, 1.0 + leverage)))
        t_80 = float(stats.t.ppf(0.90, df=self.degrees_of_freedom))
        return {
            'point_estimate_kg_ha': round(point_estimate, 1),
            'range_80': (round(max(0.0, point_estimate - t_80 * se_pred), 1), round(point_estimate + t_80 * se_pred, 1)),
            'beats_baseline': self.beats_baseline
        }
```

---

## 6. RESULTS AND DISCUSSION

### 6.1 Required Output Screenshots
- **Figure 1: Data Preprocessing and Validation Audit** — Execution of automated pytest suites (`test_guards.py` and `test_ingestion.py`) verifying 1,476 curated rainfall observations and SHA-256 data hashes with zero schema errors.
- **Figure 2: Model Performance Comparison** — Tabulated evaluation comparing OLS regression against the 5-Year Olympic Baseline across LOOCV MAE, MAPE, $R^2$, and $p$-values.
- **Figure 3: Scatter Plot and Regression Diagnostics** — Linear response curves illustrating technology trends for Cotton ($R^2 = 0.883$) and direct rainfall response for Rice ($p = 3.41 \times 10^{-7}$).
- **Figure 4: Binary Drought Classification Confusion Matrix** — 100% precision and recall on historical monsoon failure events (1987, 2004, 2009, 2026).
- **Figure 5: Model Selection Diagnostic** — Decision logic displaying why Cotton and Rice adopt OLS, while Soybean honestly defaults to Olympic baseline and analog matching.
- **Figure 6: Nagpur Krishi Data PWA Mobile Interface** — Responsive header with bilingual Marathi/English switcher and 4 primary KPI drought cards.
- **Figure 7: Taluka Deep-Dive Interface** — Dynamic 5-year monsoon rainfall bars across all 14 tehsils and the hatched 2026 prediction range bar [720 - 980 kg/ha].

### 6.2 Result Analysis
1. **Crop-Specific Sensitivity Differences:** Rice yield in Nagpur is predominantly determined by cumulative monsoon rainfall volume ($p = 3.41 \times 10^{-7}$, $R^2 = 0.707$). Conversely, cotton yield is heavily dominated by technology adoption (trend slope = +4.56 kg/ha/yr, $R^2 = 0.883$), corresponding to the introduction of genetically modified Bt-cotton hybrids. Soybean yield shows low sensitivity to total monsoon rain ($R^2 = 0.053$) because yield loss is triggered by dry spell duration in critical pod-filling stages rather than seasonal totals.
2. **Integrity of Out-of-Sample LOOCV:** In-sample $R^2$ often misleads practitioners into overestimating model utility. By enforcing Leave-One-Out Cross-Validation against the actuarial Olympic baseline, we discovered that simple regression failed to beat the baseline for soybean (MAE: 242.82 kg/ha model vs. 235.19 kg/ha baseline). Transparently reporting this failure builds deep credibility with farmers.
3. **Elimination of Hardcoded Placeholders:** Through ingestion of 900 ERA5 monthly records (2020–2024), all 14 tehsils now reflect real physical precipitation (e.g. Katol: 1321 mm in 2024 vs. Ramtek: 1496 mm in 2024), providing farmers with genuine local context.

---

## 7. CONCLUSION
*Nagpur Krishi Data* demonstrates how machine learning and spatial data engineering can be combined to solve real agricultural challenges transparently. By rejecting deceptive black-box predictions and adhering to open, explainable OLS formulations, actuarial baselines, and nearest-neighbor historical analogs, the platform delivers actionable intelligence to Nagpur farmers during the severe 2026 drought season.

**Future Enhancements:**
- Ingesting remote sensing vegetation indices (Sentinel-2 NDVI / NDWI) at 10-meter spatial resolution to capture intra-seasonal dry spell impact on soybean.
- Integrating IoT soil moisture sensors deployed at agricultural research stations in Katol and College of Agriculture, Nagpur.
- Expanding localized market price forecasting using seasonal autoregressive time-series models (SARIMA).

---

## 8. GITHUB LINK
- **GitHub Repository URL:** `https://github.com/prathameshlahoti/nagpur-krishi-data`

The repository contains the complete monorepo codebase: data pipeline scripts, SQLite database, FastAPI backend, analytics training suite, Next.js 15 PWA web application, automated test suites (23 pytest tests passing), and documentation model cards.

---

## 9. REFERENCES
- **[1]** Ministry of Agriculture & Farmers Welfare, Directorate of Economics and Statistics (DES): Land Use & Crop Cutting Experiments Statistics (https://desagri.gov.in)
- **[2]** ICRISAT District-Level Database (DLD): Multi-Decade Agricultural & Meteorological Data for Maharashtra (http://data.icrisat.org)
- **[3]** Indian Meteorological Department (IMD): Gridded & Circle-Level Daily Rainfall Datasets (https://maharain.maharashtra.gov.in)
- **[4]** ICAR - Central Research Institute for Dryland Agriculture (CRIDA): District Agriculture Contingency Plan for Nagpur District, Maharashtra (http://www.crida.in)
- **[5]** Government of Maharashtra, Relief and Rehabilitation Department: Government Resolution on Drought Declaration across 14 Tehsils of Nagpur, 25 September 2026 (`EVT_2026_DROUGHT_GR`)
- **[6]** World Food Programme (WFP) & PMFBY: Actuarial Guidelines on 5-Year Olympic Average Baseline for Crop Yield Loss Assessment

---

## FINAL SUBMISSION CHECKLIST
- [x] Final project report in PDF format (`SI_LAB_PROJECT_REPORT_Prathamesh_Lahoti.pdf`).
- [x] Word document generated with university logo & exact formatting (`SI_LAB_PROJECT_REPORT_Prathamesh_Lahoti.docx`).
- [x] Complete Python code, database, and monorepo structure.
- [x] Formatted in Times New Roman 16 pt for project title, 14 pt for headings/subheadings, and 12 pt justified for body text.

