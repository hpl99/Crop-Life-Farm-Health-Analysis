"""Monthly rainfall and normals endpoints."""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Header
from sqlalchemy.orm import Session
from apps.api.src.db.session import get_db
from apps.api.src.models.entities import FactRainfall, FactRainfallNormal, DimTehsil
from apps.api.src.schemas.common import ResponseMeta
from apps.api.src.schemas.rainfall import (
    MonthlyRainfallResponse, MonthlyRainfallItem,
    RainfallNormalResponse, RainfallNormalItem
)
from apps.api.src.core.middleware import get_requested_language

router = APIRouter(tags=["Rainfall"])

MONTH_NAMES = {
    1: ("January", "जानेवारी"),
    2: ("February", "फेब्रुवारी"),
    3: ("March", "मार्च"),
    4: ("April", "एप्रिल"),
    5: ("May", "मे"),
    6: ("June", "जून"),
    7: ("July", "जुलै"),
    8: ("August", "ऑगस्ट"),
    9: ("September", "सप्टेंबर"),
    10: ("October", "ऑक्टोबर"),
    11: ("November", "नोव्हेंबर"),
    12: ("December", "डिसेंबर"),
}


@router.get("/rainfall/monthly", response_model=MonthlyRainfallResponse)
def get_monthly_rainfall(
    tehsil_id: Optional[int] = Query(None, description="Tehsil ID (omit for district total)"),
    year: Optional[int] = Query(None, description="Filter specific year"),
    db: Session = Depends(get_db)
):
    """Retrieve historical monthly rainfall observations."""
    query = db.query(FactRainfall)
    if tehsil_id is not None:
        query = query.filter(FactRainfall.tehsil_id == tehsil_id)
    else:
        query = query.filter(FactRainfall.tehsil_id.is_(None))

    if year is not None:
        query = query.filter(FactRainfall.year == year)

    records = query.order_by(FactRainfall.year.desc(), FactRainfall.month.asc()).all()

    items = []
    for r in records:
        en_name, mr_name = MONTH_NAMES.get(r.month, ("", ""))
        items.append(MonthlyRainfallItem(
            year=r.year,
            month=r.month,
            month_name_en=en_name,
            month_name_mr=mr_name,
            rainfall_mm=r.rainfall_mm,
            normal_mm=None,
            departure_pct=None,
            source_id=r.source_id,
            trust_tier=r.trust_tier
        ))

    return MonthlyRainfallResponse(
        tehsil_id=tehsil_id,
        district="Nagpur",
        data=items,
        meta=ResponseMeta(
            sources=["SRC_IMD_RAINFALL"],
            as_of=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=len(items)
        )
    )


@router.get("/rainfall/normal", response_model=RainfallNormalResponse)
def get_rainfall_normals(db: Session = Depends(get_db)):
    """Retrieve district and taluka rainfall normals from ICAR-CRIDA Contingency Plan."""
    normals = db.query(FactRainfallNormal).all()
    tehsils = {t.tehsil_id: t for t in db.query(DimTehsil).all()}

    items = []
    for n in normals:
        t = tehsils.get(n.tehsil_id) if n.tehsil_id else None
        items.append(RainfallNormalItem(
            tehsil_id=n.tehsil_id,
            tehsil_name_en=t.name_en if t else "Nagpur District",
            tehsil_name_mr=t.name_mr if t else "नागपूर जिल्हा",
            period_type=n.period_type,
            period_index=n.period_index,
            normal_rf_mm=n.normal_rf_mm,
            normal_rainy_days=n.normal_rainy_days,
            basis_period=n.basis_period
        ))

    return RainfallNormalResponse(
        normals=items,
        meta=ResponseMeta(
            sources=["SRC_CRIDA_PLAN"],
            as_of=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=len(items)
        )
    )

