"""Metadata and Data Export API endpoints."""

import io
import csv
from datetime import datetime, timezone
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from apps.api.src.db.session import get_db
from apps.api.src.models.entities import Source, FactCropYield, FactRainfall, DimCrop
from apps.api.src.schemas.common import ResponseMeta

router = APIRouter(tags=["Metadata"])


@router.get("/meta/sources")
def get_sources(db: Session = Depends(get_db)):
    """Retrieve list of active data sources and licenses."""
    sources = db.query(Source).all()
    as_of = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "sources": [
            {
                "source_id": s.source_id,
                "name": s.name,
                "url": s.url,
                "licence": s.licence,
                "trust_tier": s.trust_tier,
                "description": s.description
            }
            for s in sources
        ],
        "meta": ResponseMeta(
            sources=[s.source_id for s in sources],
            as_of=as_of,
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=len(sources)
        )
    }


@router.get("/export.csv")
def export_dataset_csv(db: Session = Depends(get_db)):
    """Download full paired crop yield and rainfall dataset with provenance columns."""
    yields = db.query(FactCropYield).all()
    crops = {c.crop_id: c.name_en for c in db.query(DimCrop).all()}

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "district", "crop_id", "crop_name", "season", "crop_year",
        "fiscal_year", "area_ha", "production_t", "yield_kg_ha",
        "source_id", "trust_tier"
    ])

    for y in yields:
        writer.writerow([
            y.district,
            y.crop_id,
            crops.get(y.crop_id, y.crop_id),
            y.season,
            y.crop_year,
            y.fiscal_year,
            y.area_ha,
            y.production_t,
            y.yield_kg_ha,
            y.source_id,
            y.trust_tier
        ])

    csv_data = output.getvalue()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="nagpur_krishi_data_verified.csv"'}
    )
