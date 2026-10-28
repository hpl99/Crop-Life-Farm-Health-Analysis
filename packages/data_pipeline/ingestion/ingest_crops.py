"""Ingest crop APY records for Nagpur District (1966–2024).

Combines:
1. 1966–2012: ICRISAT District Level Database (DLD).
2. 2013–2024: Ministry of Agriculture & Farmers Welfare via UPAg (India Data Portal CKAN).
Strictly validates using Pandera CropYieldSchema before inserting into fact_crop_yield.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[4]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
import uuid
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from apps.api.src.models.entities import FactCropYield, IngestionRun, RawFile
from packages.data_pipeline.validation.schemas import CropYieldSchema
from packages.data_pipeline.storage.raw_store import save_raw_snapshot

ICRISAT_URL = "https://raw.githubusercontent.com/amar-at-iitm/ma5755-capstone-project/main/data/raw/area_production_yield_data.csv"
CKAN_URL = "https://ckandev.indiadataportal.com/api/3/action/datastore_search"
CKAN_RESOURCE_ID = "6f70d961-3a4f-4caa-b08f-f72f708791e1"

CROP_MAPPINGS = {
    # UPAg names -> dim_crop crop_id
    "Soybean": "soybean",
    "Cotton": "cotton",
    "Rice": "rice",
    "Wheat": "wheat",
    "Gram": "gram",
    "Tur": "tur",
    "Jowar": "jowar",
}


def fetch_and_ingest_crops(db: Session) -> int:
    """Fetch, validate, and load Nagpur crop yields with full provenance."""
    run_id = f"RUN_CROPS_{uuid.uuid4().hex[:12]}"
    run = IngestionRun(
        run_id=run_id,
        source_id="SRC_UPAG_DES",
        started_at=datetime.utcnow(),
        status="RUNNING"
    )
    db.add(run)
    db.commit()

    try:
        records_to_insert = []

        # ----------------------------------------------------
        # 1. Fetch UPAg records (2013–2024)
        # ----------------------------------------------------
        params = {
            "resource_id": CKAN_RESOURCE_ID,
            "filters": json.dumps({"district_name": "Nagpur"}),
            "limit": 500
        }
        resp = requests.get(CKAN_URL, params=params, timeout=20)
        resp.raise_for_status()
        ckan_raw_bytes = resp.content
        save_raw_snapshot("upag_nagpur_raw.json", ckan_raw_bytes, {"resource_id": CKAN_RESOURCE_ID})

        ckan_data = resp.json()["result"]["records"]
        for row in ckan_data:
            crop_name = row.get("crop_name")
            if crop_name in CROP_MAPPINGS:
                crop_id = CROP_MAPPINGS[crop_name]
                season = row.get("season", "Kharif")
                year_str = str(row.get("year", ""))
                crop_year = int(year_str.split("-")[0]) if "-" in year_str else int(year_str)
                area = float(row["area"]) if row.get("area") is not None else None
                prod = float(row["production"]) if row.get("production") is not None else None
                yld = float(row["yield"]) if row.get("yield") is not None else None

                records_to_insert.append({
                    "district": "Nagpur",
                    "crop_id": crop_id,
                    "season": season,
                    "crop_year": crop_year,
                    "fiscal_year": year_str,
                    "area_ha": area,
                    "production_t": prod,
                    "yield_kg_ha": yld,
                    "source_id": "SRC_UPAG_DES",
                    "trust_tier": "OFFICIAL_STATISTIC",
                    "is_outlier": False
                })

        # ----------------------------------------------------
        # 2. Fetch ICRISAT records (1966–2012)
        # ----------------------------------------------------
        resp_icrisat = requests.get(ICRISAT_URL, timeout=25)
        resp_icrisat.raise_for_status()
        save_raw_snapshot("icrisat_apy_raw.csv", resp_icrisat.content, {"url": ICRISAT_URL})

        df_icrisat = pd.read_csv(ICRISAT_URL)
        nagpur_icrisat = df_icrisat[df_icrisat["Dist Name"].str.upper() == "NAGPUR"]

        # Only take years < 2013 to avoid overlap with UPAg
        nagpur_icrisat = nagpur_icrisat[nagpur_icrisat["Year"] < 2013]

        crop_col_map = {
            "soybean": ("SOYABEAN AREA (1000 ha)", "SOYABEAN PRODUCTION (1000 tons)", "SOYABEAN YIELD (Kg per ha)", "Kharif"),
            "cotton": ("COTTON AREA (1000 ha)", "COTTON PRODUCTION (1000 tons)", "COTTON YIELD (Kg per ha)", "Kharif"),
            "rice": ("RICE AREA (1000 ha)", "RICE PRODUCTION (1000 tons)", "RICE YIELD (Kg per ha)", "Kharif"),
            "wheat": ("WHEAT AREA (1000 ha)", "WHEAT PRODUCTION (1000 tons)", "WHEAT YIELD (Kg per ha)", "Rabi"),
            "gram": ("CHICKPEA AREA (1000 ha)", "CHICKPEA PRODUCTION (1000 tons)", "CHICKPEA YIELD (Kg per ha)", "Rabi"),
            "jowar": ("SORGHUM AREA (1000 ha)", "SORGHUM PRODUCTION (1000 tons)", "SORGHUM YIELD (Kg per ha)", "Kharif"),
        }

        for _, row in nagpur_icrisat.iterrows():
            yr = int(row["Year"])
            for c_id, (a_col, p_col, y_col, season) in crop_col_map.items():
                if a_col in row and p_col in row and y_col in row:
                    a_val = row[a_col] * 1000.0 if pd.notnull(row[a_col]) and row[a_col] >= 0 else None
                    p_val = row[p_col] * 1000.0 if pd.notnull(row[p_col]) and row[p_col] >= 0 else None
                    y_val = float(row[y_col]) if pd.notnull(row[y_col]) and row[y_col] >= 0 else None

                    # If yield is available or area > 0
                    if (y_val is not None and y_val > 0) or (a_val is not None and a_val > 0):
                        records_to_insert.append({
                            "district": "Nagpur",
                            "crop_id": c_id,
                            "season": season,
                            "crop_year": yr,
                            "fiscal_year": f"{yr}-{str(yr+1)[-2:]}",
                            "area_ha": a_val,
                            "production_t": p_val,
                            "yield_kg_ha": y_val,
                            "source_id": "SRC_ICRISAT_DLD",
                            "trust_tier": "OFFICIAL_STATISTIC",
                            "is_outlier": False
                        })

        # ----------------------------------------------------
        # 3. Pandera Schema Validation
        # ----------------------------------------------------
        df_all = pd.DataFrame(records_to_insert)
        validated_df = CropYieldSchema.validate(df_all)

        # ----------------------------------------------------
        # 4. Idempotent Insert into Database
        # ----------------------------------------------------
        inserted_count = 0
        for _, r in validated_df.iterrows():
            existing = db.query(FactCropYield).filter_by(
                district=r["district"],
                crop_id=r["crop_id"],
                season=r["season"],
                crop_year=int(r["crop_year"])
            ).first()

            if not existing:
                fact = FactCropYield(
                    district=r["district"],
                    crop_id=r["crop_id"],
                    season=r["season"],
                    crop_year=int(r["crop_year"]),
                    fiscal_year=r["fiscal_year"],
                    area_ha=r["area_ha"],
                    production_t=r["production_t"],
                    yield_kg_ha=r["yield_kg_ha"],
                    source_id=r["source_id"],
                    trust_tier=r["trust_tier"],
                    is_outlier=r["is_outlier"]
                )
                db.add(fact)
                inserted_count += 1

        run.status = "SUCCESS"
        run.finished_at = datetime.utcnow()
        run.row_count = inserted_count
        db.commit()
        return inserted_count

    except Exception as e:
        db.rollback()
        run.status = "FAILED"
        run.finished_at = datetime.utcnow()
        run.error_log = str(e)
        db.commit()
        raise e
