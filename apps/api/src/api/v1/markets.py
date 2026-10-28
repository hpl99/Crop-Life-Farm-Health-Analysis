"""Mandi Market Prices API endpoint."""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from apps.api.src.db.session import get_db
from apps.api.src.models.entities import FactMarketPrice, DimMarket, DimCrop
from apps.api.src.schemas.common import ResponseMeta
from apps.api.src.schemas.tehsils import MandiPricesResponse, MandiPriceItem

router = APIRouter(tags=["Market & Mandi"])


@router.get("/market/prices", response_model=MandiPricesResponse)
def get_market_prices(
    crop: Optional[str] = Query(None, description="Filter by crop_id (e.g. soybean, cotton, rice)"),
    market: Optional[str] = Query(None, description="Filter by market_id or APMC name"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Retrieve verified mandi prices and arrivals across Nagpur APMCs."""
    query = db.query(FactMarketPrice, DimMarket).join(
        DimMarket, FactMarketPrice.market_id == DimMarket.market_id
    )

    if crop:
        query = query.filter(FactMarketPrice.crop_id == crop.lower())

    if market:
        query = query.filter(
            (DimMarket.market_id.ilike(f"%{market}%")) | (DimMarket.apmc_name_en.ilike(f"%{market}%"))
        )

    records = query.order_by(FactMarketPrice.price_date.desc()).limit(limit).all()

    items = []
    for price, mkt in records:
        items.append(MandiPriceItem(
            market_id=mkt.market_id,
            apmc_name_en=mkt.apmc_name_en,
            apmc_name_mr=mkt.apmc_name_mr,
            crop_id=price.crop_id,
            price_date=str(price.price_date),
            arrivals_qtl=price.arrivals_qtl,
            min_price=price.min_price,
            max_price=price.max_price,
            modal_price=price.modal_price
        ))

    return MandiPricesResponse(
        data=items,
        meta=ResponseMeta(
            sources=["SRC_MSAMB_CMO"],
            as_of=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=len(items)
        )
    )

