"""Rainfall and Season summary Pydantic schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from apps.api.src.schemas.common import ResponseMeta


class SeasonSummaryResponse(BaseModel):
    season_year: int = 2026
    period: str = "Jun-Sep"
    normal_rf_mm: float
    actual_rf_mm: float
    deficit_pct: float
    missing_rf_mm: float
    drought_talukas_count: int
    total_talukas_count: int = 14
    drought_status_mr: str
    drought_status_en: str
    meta: ResponseMeta


class MonthlyRainfallItem(BaseModel):
    year: int
    month: int
    month_name_en: str
    month_name_mr: str
    rainfall_mm: float
    rainfall_actual_mm: Optional[float] = None
    normal_mm: Optional[float] = None
    departure_pct: Optional[float] = None
    is_monsoon: bool = False
    source_id: str
    trust_tier: str


class MonthlyRainfallResponse(BaseModel):
    tehsil_id: Optional[int]
    district: str
    data: List[MonthlyRainfallItem]
    meta: ResponseMeta


class RainfallNormalItem(BaseModel):
    tehsil_id: Optional[int]
    tehsil_name_en: Optional[str]
    tehsil_name_mr: Optional[str]
    period_type: str
    period_index: Optional[int]
    normal_rf_mm: float
    normal_rainy_days: Optional[float]
    basis_period: str


class RainfallNormalResponse(BaseModel):
    normals: List[RainfallNormalItem]
    meta: ResponseMeta

