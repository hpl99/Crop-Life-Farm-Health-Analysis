"""Master Ingestion Pipeline Runner for Nagpur Krishi Data."""

import sys
from pathlib import Path

# Ensure repo root is on sys.path
ROOT_DIR = Path(__file__).resolve().parents[4]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import logging
from apps.api.src.db.session import init_db, SessionLocal
from packages.data_pipeline.ingestion.ingest_sources import ingest_sources, ingest_crops
from packages.data_pipeline.ingestion.ingest_tehsils import ingest_tehsils
from packages.data_pipeline.ingestion.ingest_crops import fetch_and_ingest_crops
from packages.data_pipeline.ingestion.ingest_rainfall import fetch_and_ingest_rainfall
from packages.data_pipeline.ingestion.ingest_mandi import fetch_and_ingest_mandi
from packages.data_pipeline.ingestion.ingest_events import ingest_events

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_all_ingestions():
    """Run all idempotent ingestion pipelines."""
    logger.info("Initializing database schema...")
    init_db()

    db = SessionLocal()
    try:
        logger.info("1/6 Ingesting Sources and Crop Dimensions...")
        ingest_sources(db)
        ingest_crops(db)

        logger.info("2/6 Ingesting 14 Tehsil Dimensions...")
        ingest_tehsils(db)

        logger.info("3/6 Ingesting Official 2026 Events...")
        ingest_events(db)

        logger.info("4/6 Ingesting Crop APY Data (1966-2024)...")
        crops_count = fetch_and_ingest_crops(db)
        logger.info(f"Loaded {crops_count} new crop yield records.")

        logger.info("5/6 Ingesting Historical & Normal Rainfall...")
        rain_count = fetch_and_ingest_rainfall(db)
        logger.info(f"Loaded {rain_count} new rainfall records.")

        logger.info("6/6 Ingesting Mandi Market Prices...")
        mandi_count = fetch_and_ingest_mandi(db)
        logger.info(f"Loaded {mandi_count} new mandi price records.")

        logger.info("All ingestion pipelines executed successfully!")

    except Exception as e:
        logger.error(f"Ingestion pipeline failed: {e}", exc_info=True)
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_all_ingestions()
