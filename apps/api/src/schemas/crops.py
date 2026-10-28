"""Crop, Yield, and Outlook Pydantic v2 schemas."""

from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
from apps.api.src.schemas.common import ResponseMeta


class CropItem(BaseModel):
    crop_id: str
    name_en: str
    name_mr: str
    category: str
    has_history: bool


class CropListResponse(BaseModel):
    crops: List[CropItem]
    meta: ResponseMeta


class YieldDataPoint(BaseModel):
    crop_year: int
    fiscal_year: Optional[str]
    season: str
    yield_kg_ha: Optional[float]
    area_ha: Optional[float]
    production_t: Optional[float]
    source_id: str
    trust_tier: str


class YieldHistoryResponse(BaseModel):
    crop_id: str
    crop_name_en: str
    crop_name_mr: str
    spatial_level: str = "district"
    spatial_disclaimer_mr: str = "जिल्हा पातळीवरील अधिकृत आकडेवारी"
    data: List[YieldDataPoint]
    meta: ResponseMeta


class AnalogYearItem(BaseModel):
    year: int
    monsoon_rf_mm: float
    deficit_mm: float
    deficit_pct: float
    yield_kg_ha: float
    similarity_rank: int
    summary: str


class OutlookResponse(BaseModel):
    crop_id: str
    crop_name_en: str
    crop_name_mr: str
    season_year: int = 2026
    rainfall_deficit_pct: float
    model_beats_baseline: bool
    point_estimate_kg_ha: Optional[float]
    range_80_kg_ha: Optional[Tuple[float, float]]
    range_95_kg_ha: Optional[Tuple[float, float]]
    is_extrapolated: bool
    confidence_disclaimer: str
    analog_years: List[AnalogYearItem]
    meta: ResponseMeta


class RainfallResponseResult(BaseModel):
    crop_id: str
    crop_name_en: str
    crop_name_mr: str
    r_squared: float
    p_value: float
    is_significant: bool
    slope_per_100mm: float
    interpretation: str
    scatter_points: List[dict]
    trend_line: List[dict]
    meta: ResponseMeta

