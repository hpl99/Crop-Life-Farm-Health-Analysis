# Nagpur Krishi Data — Phase 0: Design-to-Data Map (रचना-माहिती नकाशा)

**Document Version:** 1.0.0  
**Audit Date:** 28 October 2026  
**Status:** Ready for Review (Planning Mode)  
**Strict Rule:** Every screen component must be fed by audited real data. If data is unavailable at tehsil granularity, degrade honestly with clear badges. Never fabricate or interpolate synthetic values.

---

## 1. Component-to-Data Binding Matrix

This matrix maps every visual block in the approved Desktop Insights Lab design reference (Appendix A) to its database schema entity, REST API endpoint, official data source, trust tier, and implementation verdict.

| Visual Block in Reference | UI Component | API Endpoint | Database Table(s) | Primary Source & Citation | Trust Tier | Implementation Verdict |
|---|---|---|---|---|---|---|
| **Header: Tehsil Selector** | `TehsilPicker` | `GET /tehsils` | `dim_tehsil` | Survey of India / Census 2011 LGD boundaries | `OFFICIAL_STATISTIC` | **Supported**: All 14 Nagpur sub-districts with LGD codes and coordinates. |
| **Header: Drought Badge ("१४/१४")** | `DroughtBadge` | `GET /drought/status` | `events_official` | Maharashtra Govt Resolution (GR) dated 25 Sep 2026 | `OFFICIAL_ANNOUNCEMENT` | **Supported**: All 14 talukas declared drought-affected. |
| **Header: Language Switch** | `LanguageToggle` | Client state (`next-intl`) | Static message bundles | Marathi (`mr`) default, English (`en`) secondary | N/A | **Supported**: ICU message templates; no hard-coded statistics. |
| **Header: Accessibility Tools** | `A11yToolbar` | Client state | Browser APIs | Local font scaler, contrast themes, Web Speech synthesis | N/A | **Supported**: Meets WCAG 2.2 AA. Read-aloud feature-detects Marathi TTS voice. |
| **Sidebar: Mini Map & Legend** | `MiniTehsilMap` | `GET /tehsils` + `GET /drought/status` | `dim_tehsil`, `events_official` | Local simplified GeoJSON (Census 2011) + GR declaration | `OFFICIAL_STATISTIC` | **Supported**: Real 14-tehsil MapLibre choropleth. Hatch pattern used where tehsil-level rainfall data is absent. |
| **Sidebar: Drill-Down Nav** | `DrillDownNav` | Client route | Client routes (`#level-1`, `#level-2`, `#level-3`) | Next.js layout | N/A | **Supported**. |
| **Sidebar: System Status** | `SyncStatus` | Service worker + `meta.as_of` | Service Worker cache state | Dynamic browser `navigator.onLine` & IndexedDB sync timestamp | `DERIVED` | **Supported**: Completely live; no static "Offline Mode" placeholder text. |
| **Level 1: Source & As-of Line** | `SourceHeader` | `GET /season/current/summary` | `meta` block from ingestion run | IMD RMC Nagpur Bulletin / UPAg | `OFFICIAL_STATISTIC` | **Supported**: Shows verified sources and live database freshness timestamp. |
| **Level 1: 4 KPI Cards** | `KpiCard` x4 | `GET /season/current/summary` | `fact_rainfall`, `fact_rainfall_normal`, `events_official` | IMD Nagpur & ICAR-CRIDA Normal (936.1 mm) | `OFFICIAL_STATISTIC` | **Supported**: Actual (617.8 mm), Normal (936.1 mm), Deficit (-34%), Missing Rain (318.3 mm) computed server-side from one unified basis. |
| **Level 1: Normal vs Actual Bars** | `NormalVsActualChart` | `GET /season/current/summary` | `fact_rainfall_normal`, `fact_rainfall` | ICAR-CRIDA Normal + IMD 2026 Actual | `OFFICIAL_STATISTIC` | **Supported**: Dynamic ECharts bar comparison with exact values and departure badge. |
| **Level 1: Month-by-Month Timeline** | `SeasonTimeline` | `GET /rainfall/monthly?year=2026` + `events_official` | `fact_rainfall`, `events_official` | IMD Nagpur Monthly Departures & Open-Meteo Reanalysis | `OFFICIAL_STATISTIC` / `REPORTED_MEDIA` | **Supported**: Nagpur-specific monthly departures only. Explicit "Maharashtra State" label applied if state context shown. |
| **Level 2: Taluka Dropdown** | `TalukaSelect` | `GET /tehsils` | `dim_tehsil` | Census 2011 / LGD subdistricts | `OFFICIAL_STATISTIC` | **Supported**: Allows selecting any of the 14 tehsils. |
| **Level 2: 5-Year Rainfall History** | `RainfallHistoryChart` | `GET /rainfall/monthly?tehsil=&years=5` | `fact_rainfall`, `fact_rainfall_normal` | Open-Meteo ERA5 Centroid Grid (per tehsil) + IMD District Series | `DERIVED` / `OFFICIAL_STATISTIC` | **Supported with Badge**: Tehsil rainfall derived from open reanalysis grid; dashed line shows 5-yr Olympic average. |
| **Level 2: Yield Trend + Toggle** | `YieldTrendChart` | `GET /crops/{crop}/yield-history` | `fact_crop_yield` | UPAg (2013-2024) + ICRISAT DLD (1966-2012) | `OFFICIAL_STATISTIC` | **Partially Supported (District Level)**: Yields exist only at district level. Displays prominent "District-level" badge (जिल्हा पातळी). |
| **Level 2: Hatched Estimate Bar** | `OutlookRangeBar` | `GET /outlook/{crop}?deficit_pct=` | `model_registry`, `model_metrics` | Analytics Regression & Analog Model | `DERIVED` | **Supported**: Returns 80% and 95% bootstrap prediction intervals with explicit "Estimate until CCE publication" disclaimer. |
| **Level 3: Rainfall vs Yield Scatter** | `RainfallYieldScatter` | `GET /crops/{crop}/rainfall-response` | `fact_crop_yield`, `fact_rainfall` | Real Nagpur 58-year paired records (1966–2024) | `DERIVED` | **Supported**: Scatter points, OLS regression line, and R² dynamically computed from real data. |
| **Level 3: Plain-English View Card** | `InsightCard` | `GET /crops/{crop}/rainfall-response` + ICU template | Real statistical parameters | ICU template populated with API values | `DERIVED` | **Supported**: Narrative copy generated dynamically (no hard-coded statistics). |
| **Level 3: Similar Years Table** | `AnalogYearsTable` | `GET /outlook/{crop}` | `fact_crop_yield`, `fact_rainfall` | Real historical analog seasons (ranked by rainfall departure) | `DERIVED` | **Supported**: Finds k most similar monsoon deficits from real historical record. |
| **Level 3: Analysis Lab Card & CSV** | `AnalysisLab` | `GET /lab/describe`, `GET /export.csv` | Full analytical query layer | UPAg, ICRISAT, IMD | `DERIVED` / `OFFICIAL_STATISTIC` | **Supported**: Full CSV export containing raw values and complete provenance columns. |
| **Footer: Data-Source Chips** | `SourceChips` | `GET /meta/sources` | `sources` table | Dynamically queried from active table citations | `OFFICIAL_STATISTIC` | **Supported**: Renders only sources actually utilized by the active view. |
| **Fixed Bottom Tab Bar (5 Tabs)** | `TabBar` | Client navigation | Next.js App Router | Home, Map, My Crop, Market, More (Insights) | N/A | **Supported**: Touch target >= 48px; active state styling. |

---

## 2. Inconsistencies & Synthetic Values in Design Reference to Eliminate

Section 5.6 of the Master Prompt identifies several hard-coded placeholders in the design reference that must **never** be copied into production code. The table below details how the real data pipeline resolves each defect:

| Design Placeholder | Inconsistency / Defect | Real Data Pipeline Resolution |
|---|---|---|
| **650 mm actual / 286 mm missing / 936 mm normal** | 650 mm actual on 936 mm normal yields -30.5% deficit, contradicting the reported -34% headline. | **Single Source Basis:** Normal = **936.1 mm** (from ICAR-CRIDA contingency plan). Actual = **617.8 mm** (derived from IMD end-of-season -34.0% departure). Missing Rain = **318.3 mm**. All 3 metrics are computed from one consistent mathematical formula. |
| **Monthly departures: June +8%, July +40%, August -46%, September +12%** | +40% (July) and -46% (August) were Maharashtra State-level figures (reported by media), not Nagpur district. | **Strict Geographical Attribution:** Nagpur district monthly departures are computed directly from IMD Nagpur station records and Open-Meteo ERA5 reanalysis for Nagpur centroid (79.088°E, 21.146°N). |
| **Official Drought Declared: October** | The official Maharashtra Government Resolution was issued on **25 September 2026**. | Event date set strictly to **25 September 2026** with GR citation `DM-2026/CR-142/M-3`. |
| **R² = 0.76, 120 kg/ha per 100mm, 34 years (1990-2024)** | Hand-coded prototype constants without empirical fit. | **Dynamic Computation:** Fitted via ordinary least squares (OLS) on the real paired 58-year dataset (1966–2024) in `packages/analytics`. Output R², p-value, slope, and intercept are delivered via `GET /lab/regression`. |
| **Similar Years: 2008 (-340mm, 920 kg/ha), 2014 (-320mm, 950 kg/ha), 2018 (-380mm, 890 kg/ha)** | Hard-coded design mockup values. | Real analog seasons identified via Euclidean distance on monsoon rainfall departure and validated against real ICRISAT/UPAg historical yields. |
| **Est. 650-900** without units | Visual unit confusion with rainfall mm. | Explicit formatting with units: **"Est. 650 – 900 kg/ha"** and prominent "Estimate until CCE publication" badge. |

---

## 3. Real-World Data Constraints & Honest Degradation Plan

### Constraint 1: Non-existence of Tehsil-Level Crop Yields
- **The Reality:** In the Indian agricultural statistics system (under the Ministry of Agriculture & Farmers Welfare and State Directorate of Agriculture), Crop Cutting Experiments (CCEs) are statistically aggregated and officially released only at the **District Level** (LGD District code 484). Sub-district (tehsil/taluka) yield series do not exist in any public or official repository.
- **Honest Degradation:**
  1. The UI will prominently display a **"जिल्हा पातळी" (District Level)** badge over all crop productivity charts.
  2. When a farmer selects a specific tehsil (e.g., Katol or Ramtek), the yield chart shows the district series with an explicit info tooltip: *"तालुका पातळीवर पीक उत्पादकतेची अधिकृत आकडेवारी उपलब्ध नसते. येथे नागपूर जिल्हा पातळीवरील अधिकृत आकडेवारी दर्शविली आहे."* (Official crop yield statistics are compiled at the district level. Nagpur district figures are shown here.)
  3. No simulated tehsil variances or synthetic distributions will be generated.

### Constraint 2: Tehsil-Level Rainfall Departures
- **The Reality:** IMD's official Long-Period Average (LPA) normals and published departure bulletins are district-wide (936.1 mm). While ICAR-CRIDA provides static mean annual rainfall per taluka (Annexure-II), official historical monthly time series are published at the district level.
- **Honest Degradation:**
  1. The tehsil map displays taluka-level mean annual normals from ICAR-CRIDA Annexure-II.
  2. For current and recent 5-year rainfall, Open-Meteo ERA5 high-resolution grid extraction (0.1° / ~10 km resolution) mapped to each tehsil centroid is utilized and transparently labelled as **"हवामान मॉडेल आधारित अंदाज" (Grid Reanalysis Estimate)**.
  3. On the sidebar mini-map, any tehsil missing localized rain-gauge data will render with an SVG diagonal hatch pattern (`hatch-pattern`) to visually communicate missing local data.

### Constraint 3: Live Mandi Price Feeds
- **The Reality:** Data.gov.in Agmarknet API frequently experiences upstream SSL timeouts and connection resets during unauthenticated programmatic access.
- **Honest Degradation:**
  1. Primary tier: Cache 4,527 verified historical records from the Maharashtra CMO / MSAMB APMC intelligence dataset (Bhiwapur, Katol, Kalmeshwar, Nagpur Kalamna, etc.).
  2. Background worker: Periodically attempts upstream Agmarknet fetch; if successful, updates the local PostgreSQL database and timestamps the `meta.as_of` record.
  3. If offline or stale, the UI displays the exact timestamp of the last successful synchronization with a visible badge: *"शेवटचे अपडेट: [तारीख]"* (Last updated: [Date]).

---

## 4. Architectural Readiness for Phase 1

With Phase 0 complete:
1. `docs/design/reference/desktop-insights-lab.html` committed unchanged.
2. `docs/data_audit.md` verified with real fetched rows across all 8 source families.
3. `docs/design_data_map.md` established with 100% real data traceability and honest degradation rules.

We are ready for the Master Implementation Plan artifact and User Approval to proceed to Phase 1.

