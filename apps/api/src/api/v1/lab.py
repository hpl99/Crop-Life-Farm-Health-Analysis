"""Analysis Lab endpoints for educational and statistical exploration."""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from apps.api.src.db.session import get_db
from apps.api.src.models.entities import DimCrop, FactCropYield, FactRainfall
from apps.api.src.schemas.common import ResponseMeta
from apps.api.src.schemas.tehsils import LabDescribeResponse, LabCorrelationResponse, LabRegressionResponse
from packages.analytics.src.lab import (
    compute_descriptive_stats, compute_correlation_analysis, compute_two_way_anova
)
from packages.analytics.src.train_and_register import get_paired_crop_rainfall_df
from packages.analytics.src.models import CropYieldRegressionModel

router = APIRouter(tags=["Analysis Lab"])


@router.get("/lab/describe", response_model=LabDescribeResponse)
def get_lab_descriptive_stats(
    crop: Optional[str] = Query("soybean", description="Crop ID to analyze"),
    db: Session = Depends(get_db)
):
    """Retrieve complete descriptive statistics for crop yields and rainfall."""
    crop_rec = db.query(DimCrop).filter_by(crop_id=crop.lower()).first()
    if not crop_rec:
        raise HTTPException(status_code=404, detail=f"Crop '{crop}' not found.")

    df = get_paired_crop_rainfall_df(db, crop_rec.crop_id)
    if len(df) == 0:
        raise HTTPException(status_code=400, detail="No paired data available.")

    stats_yield = compute_descriptive_stats(df["yield_kg_ha"].tolist(), label=f"{crop_rec.name_en} Yield (kg/ha)")
    stats_rain = compute_descriptive_stats(df["monsoon_rf_mm"].tolist(), label="Monsoon Rainfall (mm)")

    return LabDescribeResponse(
        metrics=[stats_yield, stats_rain],
        meta=ResponseMeta(
            sources=["SRC_UPAG_DES", "SRC_ICRISAT_DLD", "SRC_IMD_RAINFALL"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="DERIVED",
            n_observations=len(df)
        )
    )


@router.get("/lab/correlation", response_model=LabCorrelationResponse)
def get_lab_correlation(
    crop: Optional[str] = Query("soybean", description="Crop ID to analyze"),
    db: Session = Depends(get_db)
):
    """Compute Pearson & Spearman correlation and R² with significance."""
    crop_rec = db.query(DimCrop).filter_by(crop_id=crop.lower()).first()
    if not crop_rec:
        raise HTTPException(status_code=404, detail=f"Crop '{crop}' not found.")

    df = get_paired_crop_rainfall_df(db, crop_rec.crop_id)
    corr = compute_correlation_analysis(
        df["monsoon_rf_mm"].tolist(),
        df["yield_kg_ha"].tolist(),
        label_x="मान्सून पाऊस (Monsoon Rainfall)",
        label_y=f"{crop_rec.name_mr} उत्पादन ({crop_rec.name_en} Yield)"
    )

    return LabCorrelationResponse(
        crop_id=crop_rec.crop_id,
        analysis=corr,
        meta=ResponseMeta(
            sources=["SRC_UPAG_DES", "SRC_ICRISAT_DLD", "SRC_IMD_RAINFALL"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="DERIVED",
            n_observations=len(df)
        )
    )


@router.get("/lab/regression", response_model=LabRegressionResponse)
def get_lab_regression(
    crop: Optional[str] = Query("soybean", description="Crop ID to analyze"),
    db: Session = Depends(get_db)
):
    """Retrieve regression coefficients, diagnostics, and ANOVA breakdown."""
    crop_rec = db.query(DimCrop).filter_by(crop_id=crop.lower()).first()
    if not crop_rec:
        raise HTTPException(status_code=404, detail=f"Crop '{crop}' not found.")

    df = get_paired_crop_rainfall_df(db, crop_rec.crop_id)
    model = CropYieldRegressionModel(crop_rec.crop_id).fit(df)

    diagnostics = {
        "crop_id": crop_rec.crop_id,
        "n_observations": model.n_observations,
        "intercept": round(model.intercept, 2),
        "slope_trend_per_year": round(model.slope_trend, 2),
        "slope_rainfall_per_100mm": round(model.slope_rain * 100.0, 1),
        "r_squared": round(model.r_squared, 3),
        "residual_standard_error": round(model.se_residual, 1),
        "degrees_of_freedom": model.degrees_of_freedom,
        "p_value_rainfall": round(model.p_value_rain, 4),
        "loocv_mae_model": round(model.loocv_mae_model, 1),
        "loocv_mae_baseline": round(model.loocv_mae_baseline, 1),
        "beats_baseline": model.beats_baseline
    }

    return LabRegressionResponse(
        crop_id=crop_rec.crop_id,
        diagnostics=diagnostics,
        meta=ResponseMeta(
            sources=["SRC_UPAG_DES", "SRC_ICRISAT_DLD", "SRC_IMD_RAINFALL"],
            as_of=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            trust_tier="DERIVED",
            n_observations=len(df)
        )
    )
