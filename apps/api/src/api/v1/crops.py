"""Crops, Yields, Rainfall-Response, and Outlook API endpoints."""

import json
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Header, HTTPException
from sqlalchemy.orm import Session
from apps.api.src.db.session import get_db
from apps.api.src.models.entities import DimCrop, FactCropYield, ModelRegistry, ModelMetrics
from apps.api.src.schemas.common import ResponseMeta
from apps.api.src.schemas.crops import (
    CropListResponse, CropItem, YieldHistoryResponse, YieldDataPoint,
    RainfallResponseResult, OutlookResponse, AnalogYearItem
)
from packages.analytics.src.train_and_register import get_paired_crop_rainfall_df
from packages.analytics.src.models import CropYieldRegressionModel
from packages.analytics.src.analog import find_analog_years
from apps.api.src.core.middleware import get_requested_language

router = APIRouter(tags=["Crops & Yields"])


@router.get("/crops", response_model=CropListResponse)
def get_crops(db: Session = Depends(get_db)):
    """Retrieve list of tracked crops with Marathi and English names."""
    crops = db.query(DimCrop).all()
    items = []
    for c in crops:
        has_history = db.query(FactCropYield).filter_by(crop_id=c.crop_id).count() > 0
        items.append(CropItem(
            crop_id=c.crop_id,
            name_en=c.name_en,
            name_mr=c.name_mr,
            category=c.category,
            has_history=has_history
        ))

    return CropListResponse(
        crops=items,
        meta=ResponseMeta(
            sources=["SRC_UPAG_DES", "SRC_ICRISAT_DLD"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=len(items)
        )
    )


@router.get("/crops/{crop}/yield-history", response_model=YieldHistoryResponse)
def get_crop_yield_history(
    crop: str,
    db: Session = Depends(get_db)
):
    """Retrieve multi-decade historical yield observations for a crop."""
    crop_rec = db.query(DimCrop).filter_by(crop_id=crop.lower()).first()
    if not crop_rec:
        raise HTTPException(status_code=404, detail=f"Crop '{crop}' not found.")

    records = db.query(FactCropYield).filter_by(
        district="Nagpur",
        crop_id=crop.lower()
    ).order_by(FactCropYield.crop_year.asc()).all()

    items = [
        YieldDataPoint(
            crop_year=r.crop_year,
            fiscal_year=r.fiscal_year,
            season=r.season,
            yield_kg_ha=r.yield_kg_ha,
            area_ha=r.area_ha,
            production_t=r.production_t,
            source_id=r.source_id,
            trust_tier=r.trust_tier
        )
        for r in records
    ]

    return YieldHistoryResponse(
        crop_id=crop_rec.crop_id,
        crop_name_en=crop_rec.name_en,
        crop_name_mr=crop_rec.name_mr,
        spatial_level="district",
        spatial_disclaimer_mr="जिल्हा पातळीवरील अधिकृत आकडेवारी",
        data=items,
        meta=ResponseMeta(
            sources=["SRC_UPAG_DES", "SRC_ICRISAT_DLD"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=len(items)
        )
    )


@router.get("/crops/{crop}/rainfall-response", response_model=RainfallResponseResult)
def get_crop_rainfall_response(
    crop: str,
    accept_language: str = Header(None),
    db: Session = Depends(get_db)
):
    """Retrieve paired rainfall vs yield scatter points, regression line, and diagnostics."""
    crop_rec = db.query(DimCrop).filter_by(crop_id=crop.lower()).first()
    if not crop_rec:
        raise HTTPException(status_code=404, detail=f"Crop '{crop}' not found.")

    lang = get_requested_language(accept_language)
    df = get_paired_crop_rainfall_df(db, crop_rec.crop_id)
    if len(df) < 10:
        raise HTTPException(status_code=400, detail=f"Insufficient paired data for '{crop}'.")

    model = CropYieldRegressionModel(crop_rec.crop_id).fit(df)

    scatter_points = [
        {
            "year": int(row["crop_year"]),
            "rainfall_mm": round(float(row["monsoon_rf_mm"]), 1),
            "yield_kg_ha": round(float(row["yield_kg_ha"]), 1)
        }
        for _, row in df.iterrows()
    ]

    # Generate regression line across observed rainfall range
    min_rf, max_rf = model.min_historical_rain, model.max_historical_rain
    rf_grid = [min_rf, (min_rf + max_rf) / 2.0, max_rf]
    recent_trend = int(df["crop_year"].max()) - int(df["crop_year"].min())
    trend_line = [
        {
            "rainfall_mm": round(rf, 1),
            "yield_kg_ha": round(model.intercept + model.slope_trend * recent_trend + model.slope_rain * rf, 1)
        }
        for rf in rf_grid
    ]

    # Dynamic plain language interpretation
    slope_100 = model.slope_rain * 100.0
    if lang == "mr":
        interp = (
            f"नागपुरात मागील {model.n_observations} वर्षांच्या आकडेवारीनुसार: "
            f"जून-सप्टेंबर पावसातील प्रत्येक १०० मिमी फरकाने {crop_rec.name_mr} उत्पादनात सरासरी {slope_100:+.1f} किग्रा/हेक्टर बदल होतो. "
            f"(R² = {model.r_squared:.2f}, स्पष्टीकरण: {model.r_squared*100:.1f}%)."
        )
    else:
        interp = (
            f"Based on {model.n_observations} years of Nagpur historical records: "
            f"each 100mm change in June-September monsoon rainfall is associated with a {slope_100:+.1f} kg/ha change in {crop_rec.name_en} yield. "
            f"(R² = {model.r_squared:.2f}, explains {model.r_squared*100:.1f}% of variance)."
        )

    return RainfallResponseResult(
        crop_id=crop_rec.crop_id,
        crop_name_en=crop_rec.name_en,
        crop_name_mr=crop_rec.name_mr,
        r_squared=round(model.r_squared, 3),
        p_value=round(model.p_value_rain, 4),
        is_significant=bool(model.p_value_rain < 0.05),
        slope_per_100mm=round(slope_100, 1),
        interpretation=interp,
        scatter_points=scatter_points,
        trend_line=trend_line,
        meta=ResponseMeta(
            sources=["SRC_UPAG_DES", "SRC_ICRISAT_DLD", "SRC_IMD_RAINFALL"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="DERIVED",
            n_observations=len(scatter_points)
        )
    )


@router.get("/outlook/{crop}", response_model=OutlookResponse)
def get_crop_outlook(
    crop: str,
    deficit_pct: float = Query(-34.0, description="Monsoon deficit percentage"),
    accept_language: str = Header(None),
    db: Session = Depends(get_db)
):
    """Retrieve yield prediction ranges and analog historical seasons for a crop."""
    crop_rec = db.query(DimCrop).filter_by(crop_id=crop.lower()).first()
    if not crop_rec:
        raise HTTPException(status_code=404, detail=f"Crop '{crop}' not found.")

    lang = get_requested_language(accept_language)
    df = get_paired_crop_rainfall_df(db, crop_rec.crop_id)
    if len(df) < 10:
        raise HTTPException(status_code=400, detail=f"Insufficient paired data for '{crop}'.")

    # Fit model and predict
    normal_rf = 936.1
    implied_rf = normal_rf * (1.0 + (deficit_pct / 100.0))

    model = CropYieldRegressionModel(crop_rec.crop_id).fit(df)
    min_year = int(df["crop_year"].min())
    pred = model.predict_range(target_year=2026, target_rain_mm=implied_rf, min_year=min_year)

    # Find Top 5 Analog Years
    analogs = find_analog_years(df, target_monsoon_rf_mm=implied_rf, normal_rf_mm=normal_rf, top_k=5)
    analog_items = [
        AnalogYearItem(
            year=a["year"],
            monsoon_rf_mm=a["monsoon_rf_mm"],
            deficit_mm=a["deficit_mm"],
            deficit_pct=a["deficit_pct"],
            yield_kg_ha=a["yield_kg_ha"],
            similarity_rank=a["similarity_rank"],
            summary=a["summary_mr"] if lang == "mr" else a["summary_en"]
        )
        for a in analogs
    ]

    return OutlookResponse(
        crop_id=crop_rec.crop_id,
        crop_name_en=crop_rec.name_en,
        crop_name_mr=crop_rec.name_mr,
        season_year=2026,
        rainfall_deficit_pct=deficit_pct,
        model_beats_baseline=model.beats_baseline,
        point_estimate_kg_ha=pred["point_estimate_kg_ha"],
        range_80_kg_ha=pred["range_80"],
        range_95_kg_ha=pred["range_95"],
        is_extrapolated=pred["is_extrapolated"],
        confidence_disclaimer="अंदाज (अधिकृत पीक कापणी प्रयोग अहवाल येईपर्यंत) / Estimate until official CCE release",
        analog_years=analog_items,
        meta=ResponseMeta(
            sources=["SRC_UPAG_DES", "SRC_ICRISAT_DLD", "SRC_IMD_RAINFALL", "SRC_CRIDA_PLAN"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="DERIVED",
            n_observations=len(df)
        )
    )
