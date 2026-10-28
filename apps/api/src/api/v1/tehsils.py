"""Tehsils and Drought status endpoints."""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from apps.api.src.db.session import get_db
from apps.api.src.models.entities import DimTehsil, EventsOfficial, FactRainfallNormal
from apps.api.src.schemas.common import ResponseMeta
from apps.api.src.schemas.tehsils import TehsilGeoJSONResponse, DroughtStatusResponse, TehsilFeature, TehsilProperty
from apps.api.src.core.middleware import get_requested_language

router = APIRouter(tags=["Tehsils & Geography"])


@router.get("/tehsils", response_model=TehsilGeoJSONResponse)
def get_tehsils(db: Session = Depends(get_db)):
    """Retrieve GeoJSON features for all 14 Nagpur tehsils."""
    tehsils = db.query(DimTehsil).order_by(DimTehsil.name_en).all()
    normals = {n.tehsil_id: n.normal_rf_mm for n in db.query(FactRainfallNormal).filter_by(period_type="ANNUAL").all() if n.tehsil_id}

    features = []
    for t in tehsils:
        prop = TehsilProperty(
            tehsil_id=t.tehsil_id,
            lgd_code=t.lgd_code,
            name_en=t.name_en,
            name_mr=t.name_mr,
            centroid_lat=t.centroid_lat,
            centroid_lon=t.centroid_lon,
            drought_status="DROUGHT_AFFECTED",
            annual_normal_rf_mm=normals.get(t.tehsil_id)
        )
        geom = {
            "type": "Point",
            "coordinates": [t.centroid_lon, t.centroid_lat]
        }
        features.append(TehsilFeature(properties=prop, geometry=geom))

    return TehsilGeoJSONResponse(
        features=features,
        meta=ResponseMeta(
            sources=["SRC_CENSUS_LGD", "SRC_CRIDA_PLAN"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=len(tehsils)
        )
    )


@router.get("/drought/status", response_model=DroughtStatusResponse)
def get_drought_status(
    accept_language: str = Header(None),
    db: Session = Depends(get_db)
):
    """Retrieve official 2026 drought declaration status."""
    lang = get_requested_language(accept_language)
    event = db.query(EventsOfficial).filter_by(event_id="EVT_2026_DROUGHT_GR").first()

    citation = event.citation if event else "Government Resolution dated 25 September 2026"
    return DroughtStatusResponse(
        season_year=2026,
        total_talukas=14,
        affected_talukas=14,
        ratio_str="14/14",
        status_label_en="14/14 Drought-Affected",
        status_label_mr="१४/१४ दुष्काळग्रस्त",
        declaration_date="2026-09-25",
        resolution_citation=citation,
        meta=ResponseMeta(
            sources=["SRC_MAHA_GR"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="OFFICIAL_ANNOUNCEMENT",
            n_observations=14
        )
    )
