"""Ingest Mandi prices and markets for Nagpur District."""

import uuid
import requests
import io
import pandas as pd
from datetime import datetime, date
from sqlalchemy.orm import Session
from apps.api.src.models.entities import DimMarket, FactMarketPrice, IngestionRun, DimCrop
from packages.data_pipeline.validation.schemas import MandiPriceSchema
from packages.data_pipeline.storage.raw_store import save_raw_snapshot

CMO_MANDI_URL = "https://raw.githubusercontent.com/joshi-vipul/maharashtra_mandi/master/Monthly_data_cmo.csv"

COMMODITY_MAP = {
    "Soybean": "soybean",
    "SOYBEAN": "soybean",
    "Cotton": "cotton",
    "COTTON": "cotton",
    "Paddy-Unhusked": "rice",
    "PADDY-UNHUSKED": "rice",
    "Rice(Paddy-Hus)": "rice",
    "RICE(PADDY-HUS)": "rice",
    "Wheat(Husked)": "wheat",
    "WHEAT(HUSKED)": "wheat",
    "Gram": "gram",
    "GRAM": "gram",
    "Pigeon Pea (Tur)": "tur",
    "PIGEON PEA (TUR)": "tur",
    "Sorgum(Jawar)": "jowar",
    "SORGUM(JAWAR)": "jowar",
}


def fetch_and_ingest_mandi(db: Session) -> int:
    """Fetch, validate, and load Mandi market prices for Nagpur."""
    run_id = f"RUN_MANDI_{uuid.uuid4().hex[:12]}"
    run = IngestionRun(
        run_id=run_id,
        source_id="SRC_MSAMB_CMO",
        started_at=datetime.utcnow(),
        status="RUNNING"
    )
    db.add(run)
    db.commit()

    try:
        resp = requests.get(CMO_MANDI_URL, timeout=30)
        resp.raise_for_status()
        save_raw_snapshot("cmo_mandi_raw.csv", resp.content, {"url": CMO_MANDI_URL})

        df = pd.read_csv(io.StringIO(resp.text))
        nagpur_df = df[df["district_name"].astype(str).str.upper() == "NAGPUR"]

        # 1. Populate dim_market
        unique_apmcs = nagpur_df["APMC"].unique()
        for apmc in unique_apmcs:
            mkt_id = f"MKT_{apmc.upper().replace(' ', '_')}"
            existing = db.query(DimMarket).filter_by(market_id=mkt_id).first()
            if not existing:
                db.add(DimMarket(
                    market_id=mkt_id,
                    apmc_name_en=apmc,
                    apmc_name_mr=apmc,  # Can be localized
                    district="Nagpur"
                ))
        db.commit()

        # 2. Extract price records for tracked crops
        records_to_insert = []
        for _, row in nagpur_df.iterrows():
            comm = str(row["Commodity"]).strip()
            if comm in COMMODITY_MAP:
                c_id = COMMODITY_MAP[comm]
                apmc = str(row["APMC"]).strip()
                mkt_id = f"MKT_{apmc.upper().replace(' ', '_')}"
                date_str = str(row["date"]).strip()  # e.g. "2015-04"
                parts = date_str.split("-")
                p_date = date(int(parts[0]), int(parts[1]), 1)

                arrivals = float(row["arrivals_in_qtl"]) if pd.notnull(row["arrivals_in_qtl"]) else None
                min_p = float(row["min_price"]) if pd.notnull(row["min_price"]) else None
                max_p = float(row["max_price"]) if pd.notnull(row["max_price"]) else None
                modal_p = float(row["modal_price"]) if pd.notnull(row["modal_price"]) else None

                if modal_p is not None and modal_p > 0:
                    records_to_insert.append({
                        "market_id": mkt_id,
                        "crop_id": c_id,
                        "price_date": p_date,
                        "arrivals_qtl": arrivals,
                        "min_price": min_p,
                        "max_price": max_p,
                        "modal_price": modal_p,
                        "source_id": "SRC_MSAMB_CMO"
                    })

        df_records = pd.DataFrame(records_to_insert)
        validated_df = MandiPriceSchema.validate(df_records)

        inserted_count = 0
        for _, r in validated_df.iterrows():
            fact = FactMarketPrice(
                market_id=r["market_id"],
                crop_id=r["crop_id"],
                price_date=r["price_date"],
                arrivals_qtl=r["arrivals_qtl"],
                min_price=r["min_price"],
                max_price=r["max_price"],
                modal_price=r["modal_price"],
                source_id=r["source_id"]
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
