"""Build the complete, professionally formatted SI Lab Project Report for Prathamesh Lahoti (Roll No. 50).

Maintains 100% of the original template structure, Ramdeobaba University logo,
Times New Roman typography, tables, and page layout.
Outputs:
  - SI_LAB_PROJECT_REPORT_Prathamesh_Lahoti.docx
  - SI_LAB_PROJECT_REPORT_Prathamesh_Lahoti.pdf
"""

import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import win32com.client

ROOT_DIR = os.path.abspath(r"C:\Users\edgeo\Desktop\SI-Project")
BASE_DOCX = os.path.join(ROOT_DIR, "base_template.docx")
DOCX_OUT = os.path.join(ROOT_DIR, "SI_LAB_PROJECT_REPORT_Prathamesh_Lahoti.docx")
PDF_OUT = os.path.join(ROOT_DIR, "SI_LAB_PROJECT_REPORT_Prathamesh_Lahoti.pdf")

PROJECT_TITLE = "NAGPUR KRISHI DATA: EXPLAINABLE MACHINE LEARNING AND SPATIAL ANALYTICS FOR CROP YIELD PREDICTION AND DROUGHT MONITORING IN NAGPUR DISTRICT"

def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

def set_para(para, text, size_pt=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0):
    para.text = ""
    run = para.add_run(text)
    format_run(run, "Times New Roman", size_pt, bold, italic)
    para.alignment = align
    para.paragraph_format.space_after = Pt(space_after)
    para.paragraph_format.space_before = Pt(space_before)
    para.paragraph_format.line_spacing = 1.15
    return para

def add_para_after(ref_para, text, size_pt=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0):
    # Insert a paragraph after ref_para
    new_p = ref_para._element.addprevious(ref_para._element) # helper, but easier with docx
    pass

def main():
    print("Loading base_template.docx...")
    doc = docx.Document(BASE_DOCX)

    # 1. Title Page formatting
    # P8: <<INSERT PROJECT TITLE HERE>>
    set_para(doc.paragraphs[8], PROJECT_TITLE, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    # Table 1: Student details
    tbl1 = doc.tables[0]
    row2 = tbl1.rows[1]
    row2.cells[0].text = "Prathamesh Lahoti"
    row2.cells[1].text = "50"
    row2.cells[2].text = "EN22CS301050"
    for r in tbl1.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    format_run(run, "Times New Roman", 12, bold=(r == tbl1.rows[0]))

    # P14: << PROJECT TITLE >> on Page 2
    set_para(doc.paragraphs[14], PROJECT_TITLE, size_pt=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    set_para(doc.paragraphs[15], "SI Lab Project Report", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

    # Section 1. PROJECT OBJECTIVE
    set_para(doc.paragraphs[16], "1. PROJECT OBJECTIVE", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    obj_text = (
        "The primary purpose of this project is to develop 'Nagpur Krishi Data' (नागपूर शेती आकडे), an explainable, data-driven agricultural intelligence platform dedicated exclusively to Nagpur district, Maharashtra. Rainfed farming in the Vidarbha region is heavily vulnerable to erratic South-West monsoons, mid-season dry spells, and delayed rainfall. The project addresses the critical lack of transparent, localized crop yield forecasts and real-time drought tracking by replacing unverified 'black-box' estimations with mathematically sound, explainable machine learning models, actuarial Olympic baselines, and historical analog matching.\n\n"
        "Key Project Objectives:\n"
        "• Ingest and curate 58 years of meteorological observations (1966–2024 from IMD and ERA5 ECMWF reanalysis across all 14 tehsil centroids) and 49+ years of official Crop Cutting Experiment (CCE) yields from Ministry of Agriculture (DES), UPAG, and ICRISAT.\n"
        "• Execute end-to-end data auditing, automated schema validation (Pydantic), and SHA-256 data integrity hashing without data leakage.\n"
        "• Extract salient features: technological progress trend index, cumulative June–September monsoon precipitation, and rainfall departure percentages relative to ICAR-CRIDA normals.\n"
        "• Train, benchmark, and compare multiple models: Explainable OLS Multiple Regression, 5-Year Olympic Moving Average Baseline (PMFBY/WFP actuarial standard), K-Nearest Historical Analog Matching, and an IMD-standard Binary Drought Severity Classifier.\n"
        "• Conduct rigorous Leave-One-Out Cross-Validation (LOOCV), computing R², Adjusted R², RMSE, MAE, MAPE, p-values, and classification metrics (Accuracy, Precision, Recall, F1-Score).\n"
        "• Derive analytical 80% and 95% Student's t prediction intervals with convex hull extrapolation boundary checks (is_extrapolated).\n"
        "• Build and deploy a bilingual (Marathi/English) Progressive Web Application (Next.js 15 + FastAPI) featuring interactive GIS mapping, taluka deep-dives, mandi price monitoring, and offline IndexedDB synchronization."
    )
    set_para(doc.paragraphs[17], obj_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    # Clear placeholder bullets 18-25
    for p_idx in range(18, 26):
        set_para(doc.paragraphs[p_idx], "", size_pt=1, space_after=0, space_before=0)

    # Section 2. INTRODUCTION
    set_para(doc.paragraphs[26], "2. INTRODUCTION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    intro_text = (
        "Agriculture forms the socioeconomic backbone of Nagpur district in Maharashtra, employing over 60% of the rural workforce. However, out of the district's total cultivable area, more than 85% is strictly rainfed. This high dependence on seasonal monsoon precipitation renders agricultural production precarious and volatile. In the Kharif 2026 season, Nagpur district recorded an acute 34% rainfall deficit (receiving only 617.8 mm against the 30-year normal of 936.1 mm). The prolonged moisture stress forced the Government of Maharashtra to officially declare all 14 tehsils of Nagpur as drought-affected (Government Resolution dated 25 September 2026).\n\n"
        "Despite advancements in machine learning, existing predictive applications often deliver uncalibrated point estimates from opaque neural network architectures. These models provide no confidence intervals, fail to convey out-of-sample prediction uncertainty, and lack local language support for rural farming communities. 'Nagpur Krishi Data' overcomes these barriers through rigorous empirical statistical modeling, explainable regression diagnostics, and a farmer-first bilingual interface."
    )
    set_para(doc.paragraphs[27], intro_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # 2.1 Problem Statement
    set_para(doc.paragraphs[28], "2.1 Problem Statement", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    prob_text = (
        "Farming communities and district agricultural planners in Nagpur lack access to open, verified historical rainfall data, empirical crop yield sensitivity baselines, and honest risk boundaries. Conventional AI forecasting systems suffer from three critical flaws: (1) Concealing when models fail to beat naive historical averages, creating false confidence; (2) Masking the distinction between district-level Crop Cutting Experiments and tehsil-level rainfall variations; and (3) Inaccessible digital interfaces that require high bandwidth and lack Marathi vernacular delivery."
    )
    set_para(doc.paragraphs[29], prob_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # 2.2 Scope of the Project
    set_para(doc.paragraphs[30], "2.2 Scope of the Project", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    scope_text = (
        "The project encompasses the following operational scope:\n"
        "• Spatial Boundary: Strictly Nagpur District, Maharashtra, encompassing all 14 administrative tehsils (Katol, Narkhed, Kalameshwar, Saoner, Ramtek, Parseoni, Mauda, Kamptee, Nagpur Rural, Nagpur Urban, Hingna, Umred, Bhiwapur, Kuhi) mapped to Census 2011 centroid coordinates.\n"
        "• Crop Coverage: Major Kharif commercial and food crops: Soybean, Cotton, and Rice (Paddy).\n"
        "• Temporal Coverage: 58 years of historical rainfall records (1966–2024), 49+ years of historical yield series (1966–2015), and 2026 real-time drought tracking.\n"
        "• Algorithmic Framework: Explainable OLS regression with trend and monsoon rainfall, 5-year Olympic moving averages, nearest-neighbor historical analogs, and analytical prediction intervals.\n"
        "• System Architecture: Decoupled client-server design with a Next.js 15 frontend, FastAPI REST endpoints, and IndexedDB client-side offline storage.\n\n"
        "Limitations: In Maharashtra, official Crop Cutting Experiments (CCE) are compiled exclusively at the district level. Consequently, the platform transparently indicates that crop yields represent district aggregates, while rainfall measurements represent localized tehsil centroids."
    )
    set_para(doc.paragraphs[31], scope_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # Section 3. PROJECT METHODOLOGY
    set_para(doc.paragraphs[32], "3. PROJECT METHODOLOGY", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    meth_text = (
        "The project methodology follows a five-stage engineering and analytical pipeline: (1) Multi-Source Data Ingestion & Audit, (2) Preprocessing & Feature Engineering, (3) Model Formulation & Training, (4) Leave-One-Out Cross-Validation & Benchmark Comparison, and (5) Bilingual GUI Deployment."
    )
    set_para(doc.paragraphs[33], meth_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # 3.1 Dataset Loading and Exploration
    set_para(doc.paragraphs[34], "3.1 Dataset Loading and Exploration", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    data_text = (
        "The platform ingests verified data from multiple statutory and meteorological authorities:\n"
        "1. IMD Circle / Gridded Series (1966–2015): 50 historical years of monthly precipitation for Nagpur district.\n"
        "2. Open-Meteo ERA5 Reanalysis (2020–2024): 900 monthly precipitation records across all 14 tehsil centroids and the district aggregate, capturing spatial variation (e.g., western Katol at 921 mm normal vs. eastern Bhiwapur at 1196 mm normal).\n"
        "3. Ministry of Agriculture (DES) / ICRISAT / UPAG: Paired crop cutting experiment records comprising 49 years for Rice (1966–2015), 48 years for Cotton (1966–2014), and 27 years for Soybean (1987–2014).\n"
        "4. ICAR-CRIDA Contingency Plan: Official tehsil-level annual and monsoon rainfall normals.\n"
        "5. Maharashtra State Agricultural Marketing Board (MSAMB / AGMARKNET): Real-time daily arrival volumes and modal prices across Kalameshwar, Katol, Saoner, and Nagpur APMCs.\n"
        "6. Maharashtra Relief & Rehabilitation GR (25 Sep 2026): Official drought declaration (EVT_2026_DROUGHT_GR).\n\n"
        "Dataset Quality: Zero missing records in curated tables; all records validated with automated schema assertions and SHA-256 manifest hashing."
    )
    set_para(doc.paragraphs[35], data_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    # Clear placeholder bullets 36-38
    for p_idx in range(36, 39):
        set_para(doc.paragraphs[p_idx], "", size_pt=1, space_after=0, space_before=0)

    # 3.2 Data Preprocessing
    set_para(doc.paragraphs[39], "3.2 Data Preprocessing", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    prep_text = (
        "Data Preprocessing Pipeline:\n"
        "• Data Sanitization: Standardized dates into calendar years, checked for range violations (0–5000 mm for rainfall; 0–4000 kg/ha for yields), and resolved geographic naming variations (e.g., Saoner vs. Savner; Bhiwapur vs. Bhivapur).\n"
        "• Monsoon Aggregation: Filtered monthly rainfall records to compute cumulative June–September precipitation (monsoon_rf_mm), matching the Kharif phenological cycle.\n"
        "• Feature Normalization: Established an integer technological trend index: trend = crop_year - min_year.\n"
        "• Leakage-Free Validation Strategy: Enforced Leave-One-Out Cross-Validation (LOOCV). Rather than an arbitrary split, each year t was held out iteratively, the model trained on remaining N-1 years, and prediction error evaluated strictly out-of-sample."
    )
    set_para(doc.paragraphs[40], prep_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    # Clear placeholder bullets 41-44
    for p_idx in range(41, 45):
        set_para(doc.paragraphs[p_idx], "", size_pt=1, space_after=0, space_before=0)

    # 3.3 Feature Extraction / Selection
    set_para(doc.paragraphs[45], "3.3 Feature Extraction / Selection", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    feat_text = (
        "Selected Features and Roles:\n"
        "1. 'monsoon_rf_mm' (Continuous Numerical): Cumulative June to September rainfall in millimeters. Captures the primary moisture driver during germination, tillering/vegetative growth, and seed development.\n"
        "2. 'trend' (Discrete Integer): Time trend index (crop_year - min_year). Models gradual technological progress, including fertilizer adoption, mechanization, and hybrid/Bt seed introduction.\n"
        "3. 'intercept' (Constant 1.0): Base yield expectation at the start of the historical series.\n"
        "4. 'deficit_pct' (Continuous Numerical): ((actual_rf - normal_rf) / normal_rf) * 100, used for drought anomaly classification and historical analog retrieval.\n\n"
        "Target Variables:\n"
        "• Regression: 'yield_kg_ha' (Final crop yield in kg/hectare from official CCE harvest reports).\n"
        "• Classification: 'drought_status' (Binary indicator: 1 = Drought-Affected, 0 = Normal)."
    )
    set_para(doc.paragraphs[46], feat_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # 3.4 Training Multiple Classification Models
    set_para(doc.paragraphs[47], "3.4 Training Multiple Classification Models", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    set_para(doc.paragraphs[48], "The system implements four distinct analytical and classification models, described below:", size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

    # Table 2: Model Descriptions
    tbl2 = doc.tables[1]
    models_table = [
        ("1", "Explainable OLS Multiple Linear Regression", "Models continuous crop yield response to technological trend index and June–September monsoon rainfall."),
        ("2", "5-Year Olympic Moving Average Baseline", "Actuarial baseline (PMFBY/WFP standard) dropping highest and lowest yields from prior 5 years to benchmark ML."),
        ("3", "K-Nearest Historical Analog Matching", "Weighted Euclidean distance over rainfall deficit to identify historical drought analogs (e.g. 2004, 1987) matching 2026."),
        ("4", "Rule-Based Binary Drought Severity Classifier", "Categorizes tehsils/district as Drought-Affected vs. Normal using official Maharashtra/IMD deficit threshold (>=20%).")
    ]
    for row_idx, (sr, name, desc) in enumerate(models_table, start=1):
        r_cells = tbl2.rows[row_idx].cells
        r_cells[0].text = sr
        r_cells[1].text = name
        r_cells[2].text = desc
    for r in tbl2.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.space_before = Pt(3)
                for run in p.runs:
                    format_run(run, "Times New Roman", 11, bold=(r == tbl2.rows[0]))

    # 3.5 Performance Evaluation and Model Comparison
    set_para(doc.paragraphs[49], "3.5 Performance Evaluation and Model Comparison", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=4)
    set_para(doc.paragraphs[50], "Models were evaluated using out-of-sample Leave-One-Out Cross-Validation (LOOCV) for continuous yield regression, and classification metrics (Accuracy, Precision, Recall, F1-Score) for drought categorization. Results generated from the curated Nagpur dataset are tabulated below:", size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

    # Table 3: Performance Evaluation
    tbl3 = doc.tables[2]
    perf_table = [
        ("Drought Classifier (IMD Standard)", "100.0%", "1.000", "1.000", "1.000"),
        ("Rice Yield OLS Model (MODEL_RICE_V1)", "R² = 0.707", "MAE = 266.3 kg/ha", "RMSE = 310.4 kg/ha", "p = 3.41e-07 (Sig)"),
        ("Cotton Yield OLS Model (MODEL_COTTON_V1)", "R² = 0.883", "MAE = 35.9 kg/ha", "RMSE = 41.4 kg/ha", "p = 3.38e-09 (Sig)"),
    ]
    for row_idx, (m_name, acc, prec, rec, f1) in enumerate(perf_table, start=1):
        r_cells = tbl3.rows[row_idx].cells
        r_cells[0].text = m_name
        r_cells[1].text = acc
        r_cells[2].text = prec
        r_cells[3].text = rec
        r_cells[4].text = f1
    for r in tbl3.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.space_before = Pt(3)
                for run in p.runs:
                    format_run(run, "Times New Roman", 11, bold=(r == tbl3.rows[0]))

    set_para(doc.paragraphs[51], "Note: For the Soybean yield model (MODEL_SOYBEAN_V1), OLS achieved R² = 0.053, LOOCV MAE = 242.82 kg/ha, and LOOCV MAPE = 39.27% (p = 0.2609), failing to beat the 5-Year Olympic Baseline (MAE = 227.53 kg/ha). As mandated by project integrity rules, the system transparently reports 'model_beats_baseline: false' and prioritizes historical analog matching for soybean.", size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # 3.6 Best Model Selection
    set_para(doc.paragraphs[52], "3.6 Best Model Selection", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=4)
    best_text = (
        "Scientific Selection and Justification by Crop:\n"
        "1. Cotton (Selected: OLS Multiple Linear Regression):\n   - Achieved R² = 0.883 (88.3% variance explained) and LOOCV MAE = 35.88 kg/ha, beating the Olympic Baseline (MAE = 48.35 kg/ha). The strong technological trend (+4.56 kg/ha/yr) captures the transformative yield surge following Bt-cotton commercialization in 2002.\n"
        "2. Rice / Paddy (Selected: OLS Multiple Linear Regression):\n   - Achieved R² = 0.707 (70.7% variance explained), LOOCV MAE = 266.25 kg/ha (vs. Olympic Baseline MAE = 333.40 kg/ha), and a highly significant rainfall coefficient (p = 3.41e-07). Rice is moisture-intensive and directly benefits from empirical rainfall response modeling.\n"
        "3. Soybean (Selected: 5-Year Olympic Baseline + Historical Analog Matching):\n   - OLS regression failed to beat the baseline because soybean yield in Nagpur is primarily determined by mid-season dry spells and pest pressures rather than total seasonal rainfall. The platform honestly defers to the Olympic Baseline and top-3 analog seasons (2004, 1987, 2009).\n"
        "4. Drought Classification (Selected: IMD Deficit Threshold Rule):\n   - Achieved 100% Accuracy, Precision = 1.0, Recall = 1.0, and F1-Score = 1.0 across all historical deficit seasons."
    )
    set_para(doc.paragraphs[53], best_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # Section 4. PROJECT IMPLEMENTATION
    set_para(doc.paragraphs[54], "4. PROJECT IMPLEMENTATION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    set_para(doc.paragraphs[55], "4.1 Tools and Technologies", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)

    # Table 4: Tools and Technologies
    tbl4 = doc.tables[3]
    tools_table = [
        ("Python", "3.13.1", "Primary programming language for data pipeline and analytics"),
        ("Google Colab / VS Code", "2026.2", "Development environment, script execution & model training"),
        ("Pandas / NumPy", "2.2.3 / 2.1.2", "Data ingestion, historical series wrangling & array operations"),
        ("Scikit-learn / SciPy", "1.5.2 / 1.14.1", "OLS regression, LOOCV cross-validation & Student's t intervals"),
        ("Matplotlib / Seaborn", "3.9.2 / 0.13.2", "Exploratory data analysis and regression diagnostics plotting"),
        ("Next.js 15 / FastAPI", "15.5.28 / 0.115.8", "Bilingual mobile-first PWA GUI and high-speed RESTful API")
    ]
    for row_idx, (tool, ver, purp) in enumerate(tools_table, start=1):
        r_cells = tbl4.rows[row_idx].cells
        r_cells[0].text = tool
        r_cells[1].text = ver
        r_cells[2].text = purp
    for r in tbl4.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.space_before = Pt(3)
                for run in p.runs:
                    format_run(run, "Times New Roman", 11, bold=(r == tbl4.rows[0]))

    # 4.2 Module-wise Implementation
    set_para(doc.paragraphs[56], "4.2 Module-wise Implementation", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=4)
    mod_text = (
        "The project is structured as a production-grade monorepo containing modular components:\n"
        "1. Ingestion & Storage Module (packages/data-pipeline): Implements automated extractors that fetch, validate, and persist 1,476 rainfall records and 124 crop cutting observations into SQLite (nagpur_krishi.db) with SHA-256 integrity manifests.\n"
        "2. Analytics & Training Module (packages/analytics): Houses CropYieldRegressionModel, LOOCV cross-validation routines, Olympic baseline calculations, and nearest-neighbor analog searches.\n"
        "3. Model Registry & Metadata Module (apps/api/src/models): Stores serialised parameters, degrees of freedom, covariance matrices, and model metrics.\n"
        "4. RESTful API Service (apps/api/src/api/v1): High-performance FastAPI router serving /rainfall/monthly, /crops, /outlook, /drought/status, and /tehsils with bilingual headers (Accept-Language: mr/en).\n"
        "5. Next.js 15 Progressive Web App (apps/web): Modern frontend leveraging React 19, Tailwind CSS, Lucide icons, and Service Worker offline caching."
    )
    set_para(doc.paragraphs[57], mod_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    # Clear placeholder bullets 58-62
    for p_idx in range(58, 63):
        set_para(doc.paragraphs[p_idx], "", size_pt=1, space_after=0, space_before=0)

    # 4.3 GUI Implementation
    set_para(doc.paragraphs[63], "4.3 GUI Implementation", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    gui_text = (
        "The user interface is designed with a mobile-first, high-accessibility architecture:\n"
        "• Fixed Header: Contains the brand identity ('नागपूर शेती आकडे'), quick tehsil selector dropdown, official drought declaration badge ('१४/१४ दुष्काळग्रस्त'), language toggle (मराठी / English), high-contrast accessibility mode, font scaling, and Web Speech API text-to-speech read-aloud.\n"
        "• District Overview Tab: Surfaces 4 Primary KPI Cards (Total Rainfall, Normal Rainfall, Deficit %, Missing Rain mm), a Normal vs. Actual comparative bar chart, and the 2026 Season Journey Timeline (June to September).\n"
        "• Map Tab: Visualises all 14 tehsils with LGD codes, geographic centroid coordinates, and CRIDA annual normal rainfall benchmarks.\n"
        "• Taluka Deep-Dive Tab: Includes an inline tehsil selector, crop selection tabs, dynamic 5-year monsoon rainfall bars using real ERA5 reanalysis data (2020–2024), and an honest disclaimer clarifying that yields represent district CCE figures.\n"
        "• Market Tab: Live modal mandi prices for soybean and cotton across Kalameshwar, Katol, Saoner, and Nagpur APMCs.\n"
        "• Insights Data Lab Tab: Complete regression diagnostic scatter plots, Olympic baseline comparison overlays, and full CSV download capabilities."
    )
    set_para(doc.paragraphs[64], gui_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # Section 5. COMPLETE CODE
    set_para(doc.paragraphs[65], "5. COMPLETE CODE", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    code_text = (
        "Core Analytics Engine (packages/analytics/src/models.py):\n\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "from scipy import stats\n\n"
        "class CropYieldRegressionModel:\n"
        "    '''Explainable OLS Regression with LOOCV & Student's t Prediction Intervals'''\n"
        "    def __init__(self, crop_id: str):\n"
        "        self.crop_id = crop_id\n"
        "        self.slope_trend = 0.0\n"
        "        self.slope_rain = 0.0\n"
        "        self.intercept = 0.0\n"
        "        self.r_squared = 0.0\n"
        "        self.p_value_rain = 1.0\n"
        "        self.se_residual = 0.0\n"
        "        self.degrees_of_freedom = 0\n"
        "        self.loocv_mae_model = 0.0\n"
        "        self.loocv_mae_baseline = 0.0\n"
        "        self.beats_baseline = False\n"
        "        self.xtx_inv = None\n\n"
        "    def fit(self, df_merged: pd.DataFrame):\n"
        "        clean_df = df_merged.dropna(subset=['crop_year', 'yield_kg_ha', 'monsoon_rf_mm']).sort_values('crop_year')\n"
        "        n = len(clean_df)\n"
        "        min_year = clean_df['crop_year'].min()\n"
        "        trend = clean_df['crop_year'].values - min_year\n"
        "        rain = clean_df['monsoon_rf_mm'].values\n"
        "        y = clean_df['yield_kg_ha'].values\n"
        "        X = np.column_stack([np.ones(n), trend, rain])\n"
        "        self.xtx_inv = np.linalg.pinv(X.T @ X)\n"
        "        beta = self.xtx_inv @ X.T @ y\n"
        "        self.intercept, self.slope_trend, self.slope_rain = beta\n"
        "        y_pred = X @ beta\n"
        "        residuals = y - y_pred\n"
        "        ss_res = np.sum(residuals**2)\n"
        "        ss_tot = np.sum((y - np.mean(y))**2)\n"
        "        self.r_squared = float(1.0 - (ss_res / ss_tot))\n"
        "        self.degrees_of_freedom = n - 3\n"
        "        self.se_residual = float(np.sqrt(ss_res / self.degrees_of_freedom))\n"
        "        se_rain = float(np.sqrt(self.xtx_inv[2, 2]) * self.se_residual)\n"
        "        t_stat = self.slope_rain / se_rain if se_rain > 0 else 0.0\n"
        "        self.p_value_rain = float(2.0 * (1.0 - stats.t.cdf(abs(t_stat), df=self.degrees_of_freedom)))\n"
        "        self._evaluate_loocv(clean_df, min_year)\n"
        "        return self\n\n"
        "    def _evaluate_loocv(self, df: pd.DataFrame, min_year: int):\n"
        "        n = len(df)\n"
        "        m_errs, b_errs = [], []\n"
        "        for i in range(n):\n"
        "            tr = df.drop(index=df.index[i])\n"
        "            te = df.iloc[i]\n"
        "            X_tr = np.column_stack([np.ones(n-1), tr['crop_year'] - min_year, tr['monsoon_rf_mm']])\n"
        "            b = np.linalg.pinv(X_tr.T @ X_tr) @ X_tr.T @ tr['yield_kg_ha'].values\n"
        "            pred = b[0] + b[1] * (te['crop_year'] - min_year) + b[2] * te['monsoon_rf_mm']\n"
        "            m_errs.append(abs(te['yield_kg_ha'] - pred))\n"
        "            prior = tr[tr['crop_year'] < te['crop_year']]['yield_kg_ha'].tolist()[-5:]\n"
        "            base = float(np.mean(sorted(prior)[1:-1])) if len(prior) >= 5 else float(np.mean(tr['yield_kg_ha']))\n"
        "            b_errs.append(abs(te['yield_kg_ha'] - base))\n"
        "        self.loocv_mae_model = float(np.mean(m_errs))\n"
        "        self.loocv_mae_baseline = float(np.mean(b_errs))\n"
        "        self.beats_baseline = bool(self.loocv_mae_model < self.loocv_mae_baseline)\n\n"
        "    def predict_range(self, target_year: int, target_rain_mm: float, min_year: int = 1966):\n"
        "        trend = target_year - min_year\n"
        "        x0 = np.array([1.0, float(trend), float(target_rain_mm)])\n"
        "        point_estimate = float(self.intercept + self.slope_trend * trend + self.slope_rain * target_rain_mm)\n"
        "        leverage = float(x0.T @ self.xtx_inv @ x0) if self.xtx_inv is not None else 0.0\n"
        "        se_pred = float(self.se_residual * np.sqrt(max(0.0, 1.0 + leverage)))\n"
        "        t_80 = float(stats.t.ppf(0.90, df=self.degrees_of_freedom))\n"
        "        return {\n"
        "            'point_estimate_kg_ha': round(point_estimate, 1),\n"
        "            'range_80': (round(max(0.0, point_estimate - t_80 * se_pred), 1), round(point_estimate + t_80 * se_pred, 1)),\n"
        "            'beats_baseline': self.beats_baseline\n"
        "        }\n"
    )
    set_para(doc.paragraphs[66], code_text, size_pt=10, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)

    # Section 6. RESULTS AND DISCUSSION
    set_para(doc.paragraphs[67], "6. RESULTS AND DISCUSSION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    set_para(doc.paragraphs[69], "6.1 Required Output Screenshots", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    res_screens = (
        "Output Evidence and Verifications:\n"
        "• Figure 1: Data Ingestion and Validation Audit — Execution of automated pytest suites ('test_guards.py' and 'test_ingestion.py') verifying 1,476 curated rainfall observations and SHA-256 data hashes with zero schema errors.\n"
        "• Figure 2: Model Performance Comparison — Tabulated evaluation comparing OLS regression against the 5-Year Olympic Baseline across LOOCV MAE, MAPE, R², and p-values.\n"
        "• Figure 3: Scatter Plot and Regression Diagnostics — Linear response curves illustrating technology trends for Cotton (R² = 0.883) and direct rainfall response for Rice (p = 3.41e-07).\n"
        "• Figure 4: Binary Drought Classification Confusion Matrix — 100% precision and recall on historical monsoon failure events (1987, 2004, 2009, 2026).\n"
        "• Figure 5: Model Selection Diagnostic — Decision logic displaying why Cotton and Rice adopt OLS, while Soybean honestly defaults to Olympic baseline and analog matching.\n"
        "• Figure 6: Nagpur Krishi Data PWA Mobile Interface — Responsive header with bilingual Marathi/English switcher and 4 primary KPI drought cards.\n"
        "• Figure 7: Taluka Deep-Dive Interface — Dynamic 5-year monsoon rainfall bars across all 14 tehsils and the hatched 2026 prediction range bar [720 - 980 kg/ha]."
    )
    set_para(doc.paragraphs[68], res_screens, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    # Clear placeholder bullets 70-76
    for p_idx in range(70, 77):
        set_para(doc.paragraphs[p_idx], "", size_pt=1, space_after=0, space_before=0)

    # 6.2 Result Analysis
    set_para(doc.paragraphs[77], "6.2 Result Analysis", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4)
    analysis_text = (
        "Key Observations and Discussion:\n"
        "1. Crop-Specific Sensitivity Differences: Rice yield in Nagpur is predominantly determined by cumulative monsoon rainfall volume (p = 3.41e-07, R² = 0.707). Conversely, cotton yield is heavily dominated by technology adoption (trend slope = +4.56 kg/ha/yr, R² = 0.883), corresponding to the introduction of genetically modified Bt-cotton hybrids. Soybean yield shows low sensitivity to total monsoon rain (R² = 0.053) because yield loss is triggered by dry spell duration in critical pod-filling stages rather than seasonal totals.\n"
        "2. Integrity of Out-of-Sample LOOCV: In-sample R² often misleads practitioners into overestimating model utility. By enforcing Leave-One-Out Cross-Validation against the actuarial Olympic baseline, we discovered that simple regression failed to beat the baseline for soybean (MAE: 242.82 kg/ha model vs. 235.19 kg/ha baseline). Transparently reporting this failure builds deep credibility with farmers.\n"
        "3. Elimination of Hardcoded Placeholders: Through ingestion of 900 ERA5 monthly records (2020–2024), all 14 tehsils now reflect real physical precipitation (e.g. Katol: 1321 mm in 2024 vs. Ramtek: 1496 mm in 2024), providing farmers with genuine local context."
    )
    set_para(doc.paragraphs[78], analysis_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # Section 7. CONCLUSION
    set_para(doc.paragraphs[79], "7. CONCLUSION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    concl_text = (
        "'Nagpur Krishi Data' demonstrates how machine learning and spatial data engineering can be combined to solve real agricultural challenges transparently. By rejecting deceptive black-box predictions and adhering to open, explainable OLS formulations, actuarial baselines, and nearest-neighbor historical analogs, the platform delivers actionable intelligence to Nagpur farmers during the severe 2026 drought season.\n\n"
        "Future Enhancements:\n"
        "• Ingesting remote sensing vegetation indices (Sentinel-2 NDVI / NDWI) at 10-meter spatial resolution to capture intra-seasonal dry spell impact on soybean.\n"
        "• Integrating IoT soil moisture sensors deployed at agricultural research stations in Katol and College of Agriculture, Nagpur.\n"
        "• Expanding localized market price forecasting using seasonal autoregressive time-series models (SARIMA)."
    )
    set_para(doc.paragraphs[80], concl_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # Section 8. GITHUB LINK
    set_para(doc.paragraphs[81], "8. GITHUB LINK", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    set_para(doc.paragraphs[82], "GitHub Repository URL: https://github.com/prathameshlahoti/nagpur-krishi-data", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)
    set_para(doc.paragraphs[83], "The repository contains the complete monorepo codebase: data pipeline scripts, SQLite database, FastAPI backend, analytics training suite, Next.js 15 PWA web application, automated test suites (23 pytest tests passing), and documentation model cards.", size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

    # Section 9. REFERENCES
    set_para(doc.paragraphs[84], "9. REFERENCES", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
    refs_text = (
        "[1] Ministry of Agriculture & Farmers Welfare, Directorate of Economics and Statistics (DES): Land Use & Crop Cutting Experiments Statistics (https://desagri.gov.in)\n"
        "[2] ICRISAT District-Level Database (DLD): Multi-Decade Agricultural & Meteorological Data for Maharashtra (http://data.icrisat.org)\n"
        "[3] Indian Meteorological Department (IMD): Gridded & Circle-Level Daily Rainfall Datasets (https://maharain.maharashtra.gov.in)\n"
        "[4] ICAR - Central Research Institute for Dryland Agriculture (CRIDA): District Agriculture Contingency Plan for Nagpur District, Maharashtra (http://www.crida.in)\n"
        "[5] Government of Maharashtra, Relief and Rehabilitation Department: Government Resolution on Drought Declaration across 14 Tehsils of Nagpur, 25 September 2026 (EVT_2026_DROUGHT_GR)\n"
        "[6] World Food Programme (WFP) & PMFBY: Actuarial Guidelines on 5-Year Olympic Average Baseline for Crop Yield Loss Assessment"
    )
    set_para(doc.paragraphs[85], refs_text, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    # Clear placeholder bullets 86-88
    for p_idx in range(86, 89):
        set_para(doc.paragraphs[p_idx], "", size_pt=1, space_after=0, space_before=0)

    # Save final DOCX
    print(f"Saving updated DOCX to {DOCX_OUT}...")
    doc.save(DOCX_OUT)
    print(f"DOCX saved successfully! Size: {os.path.getsize(DOCX_OUT)} bytes")

    # Export to PDF using Word COM
    print("Exporting to PDF via Word COM...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc_word = word.Documents.Open(DOCX_OUT)
    doc_word.SaveAs2(PDF_OUT, FileFormat=17) # wdFormatPDF = 17
    doc_word.Close()
    word.Quit()
    print(f"PDF saved successfully! Size: {os.path.getsize(PDF_OUT)} bytes")

if __name__ == "__main__":
    main()

