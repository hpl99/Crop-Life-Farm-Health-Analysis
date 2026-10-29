"""Ingest real historical monthly rainfall for all 14 Nagpur Tehsils (2020-2024).

Source: Open-Meteo ERA5 / ECMWF High-Resolution Historical Reanalysis Archive (CC BY 4.0).
Coordinates: Exact Census 2011 centroids of each of the 14 tehsils in Nagpur district.
"""

import sys
import time
import requests
import pandas as pd
from pathlib import Path
from datetime import date
from sqlalchemy.orm import Session

ROOT_DIR = Path(__file__).resolve().parents[4]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from apps.api.src.db.session import SessionLocal
from apps.api.src.models.entities import DimTehsil, FactRainfall, FactRainfallNormal
from packages.data_pipeline.storage.raw_store import save_raw_snapshot


def ingest_tehsil_monthly_rainfall(db: Session) -> int:
    """Fetch real 2020-2024 monthly rainfall observations for each of the 14 tehsils."""
    tehsils = db.query(DimTehsil).order_by(DimTehsil.tehsil_id).all()
    total_inserted = 0

    print(f"Fetching real historical monthly rainfall for {len(tehsils)} tehsils...")

    for t in tehsils:
        lat = t.centroid_lat
        lon = t.centroid_lon
        t_id = t.tehsil_id

        # Delete any existing tehsil records for 2020-2024
        db.query(FactRainfall).filter(
            FactRainfall.tehsil_id == t_id,
            FactRainfall.year.between(2020, 2024)
        ).delete()

        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={lat:.4f}&longitude={lon:.4f}&"
            f"start_date=2020-01-01&end_date=2024-12-31&"
            f"daily=precipitation_sum&timezone=Asia%2FKolkata"
        )

        try:
            resp = requests.get(url, timeout=25)
            resp.raise_for_status()
            data = resp.json()

            # Save raw archive snapshot for provenance
            save_raw_snapshot(
                f"tehsil_rainfall_raw_{t.name_en.lower().replace(' ', '_')}.json",
                resp.content,
                {"url": url, "tehsil_id": t_id, "name_en": t.name_en}
            )

            daily = data.get("daily", {})
            times = daily.get("time", [])
            precips = daily.get("precipitation_sum", [])

            df = pd.DataFrame({"time": pd.to_datetime(times), "precip": precips})
            df["year"] = df["time"].dt.year
            df["month"] = df["time"].dt.month

            # Aggregate by year and month
            monthly_agg = df.groupby(["year", "month"])["precip"].sum().reset_index()

            for _, row in monthly_agg.iterrows():
                yr = int(row["year"])
                mo = int(row["month"])
                rf = round(float(row["precip"]), 1)

                rec = FactRainfall(
                    district="Nagpur",
                    tehsil_id=t_id,
                    record_date=date(yr, mo, 1),
                    year=yr,
                    month=mo,
                    rainfall_mm=rf,
                    source_id="SRC_OPEN_METEO",
                    trust_tier="OFFICIAL_STATISTIC"
                )
                db.add(rec)
                total_inserted += 1

            db.commit()
            print(f"  [{t_id:2d}/14] {t.name_en:15s}: Ingested {len(monthly_agg)} monthly records ({lat:.2f}N, {lon:.2f}E)")
            time.sleep(0.3)

        except Exception as e:
            db.rollback()
            print(f"  Error fetching tehsil {t.name_en}: {e}")

    # Also ensure district-level has 2020-2024 records as average of tehsils
    print("Calculating district-level monthly series for 2020-2024...")
    db.query(FactRainfall).filter(
        FactRainfall.tehsil_id.is_(None),
        FactRainfall.year.between(2020, 2024)
    ).delete()

    df_all = pd.read_sql(
        "SELECT year, month, AVG(rainfall_mm) as avg_rf FROM fact_rainfall WHERE tehsil_id IS NOT NULL AND year BETWEEN 2020 AND 2024 GROUP BY year, month",
        db.bind
    )
    for _, row in df_all.iterrows():
        yr = int(row["year"])
        mo = int(row["month"])
        db.add(FactRainfall(
            district="Nagpur",
            tehsil_id=None,
            record_date=date(yr, mo, 1),
            year=yr,
            month=mo,
            rainfall_mm=round(float(row["avg_rf"]), 1),
            source_id="SRC_OPEN_METEO",
            trust_tier="DERIVED"
        ))
        total_inserted += 1

    db.commit()
    print(f"Successfully loaded {total_inserted} real monthly rainfall records!")
    return total_inserted


if __name__ == "__main__":
    db = SessionLocal()
    try:
        ingest_tehsil_monthly_rainfall(db)
    finally:
        db.close()
