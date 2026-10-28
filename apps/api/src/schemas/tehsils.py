"""Tehsil, Drought Status, Mandi, and Lab schemas."""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from apps.api.src.schemas.common import ResponseMeta


class TehsilProperty(BaseModel):
    tehsil_id: int
    lgd_code: Optional[str]
    name_en: str
    name_mr: str
    centroid_lat: float
    centroid_lon: float
    drought_status: str = "DROUGHT_AFFECTED"
    annual_normal_rf_mm: Optional[float]


class TehsilFeature(BaseModel):
    type: str = "Feature"
    properties: TehsilProperty
    geometry: Optional[Dict[str, Any]] = None


class TehsilGeoJSONResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[TehsilFeature]
    meta: ResponseMeta


class DroughtStatusResponse(BaseModel):
    season_year: int = 2026
    total_talukas: int = 14
    affected_talukas: int = 14
    ratio_str: str = "14/14"
    status_label_en: str = "14/14 Drought-Affected"
    status_label_mr: str = "१४/१४ दुष्काळग्रस्त"
    declaration_date: str = "2026-09-25"
    resolution_citation: str
    meta: ResponseMeta


class MandiPriceItem(BaseModel):
    market_id: str
    apmc_name_en: str
    apmc_name_mr: str
    crop_id: str
    price_date: str
    arrivals_qtl: Optional[float]
    min_price: Optional[float]
    max_price: Optional[float]
    modal_price: float


class MandiPricesResponse(BaseModel):
    data: List[MandiPriceItem]
    meta: ResponseMeta


class LabDescribeResponse(BaseModel):
    metrics: List[Dict[str, Any]]
    meta: ResponseMeta


class LabCorrelationResponse(BaseModel):
    crop_id: str
    analysis: Dict[str, Any]
    meta: ResponseMeta


class LabRegressionResponse(BaseModel):
    crop_id: str
    diagnostics: Dict[str, Any]
    meta: ResponseMeta
