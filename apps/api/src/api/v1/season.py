"""Season summary and Weather Forecast API endpoints."""

from datetime import datetime
from typing import Optional
import requests
from fastapi import APIRouter, Depends, Query, Header, HTTPException
from sqlalchemy.orm import Session
from apps.api.src.db.session import get_db
from apps.api.src.models.entities import DimTehsil, FactRainfallNormal, EventsOfficial
from apps.api.src.schemas.common import ResponseMeta
from apps.api.src.schemas.rainfall import SeasonSummaryResponse
from apps.api.src.core.middleware import get_requested_language

router = APIRouter(tags=["Season & Forecast"])

# Unified mathematical basis for 2026 Season KPIs
# Normal SW Monsoon = 936.1 mm (ICAR-CRIDA Section 1.2)
# Reported Deficit = -34.0% (IMD Regional Met Centre Nagpur)
# Derived Actual = 936.1 * (1 - 0.34) = 617.8 mm
# Missing Rain = 936.1 - 617.8 = 318.3 mm
NORMAL_SW_MONSOON_MM = 936.1
DEFICIT_2026_PCT = -34.0
ACTUAL_2026_MM = round(NORMAL_SW_MONSOON_MM * (1.0 + (DEFICIT_2026_PCT / 100.0)), 1)
MISSING_RAIN_2026_MM = round(NORMAL_SW_MONSOON_MM - ACTUAL_2026_MM, 1)


@router.get("/season/current/summary", response_model=SeasonSummaryResponse)
def get_season_summary(
    accept_language: str = Header(None),
    db: Session = Depends(get_db)
):
    """Retrieve 2026 Monsoon Season summary KPIs."""
    lang = get_requested_language(accept_language)
    as_of = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    return SeasonSummaryResponse(
        season_year=2026,
        period="Jun-Sep",
        normal_rf_mm=NORMAL_SW_MONSOON_MM,
        actual_rf_mm=ACTUAL_2026_MM,
        deficit_pct=DEFICIT_2026_PCT,
        missing_rf_mm=MISSING_RAIN_2026_MM,
        drought_talukas_count=14,
        total_talukas_count=14,
        drought_status_mr="१४/१४ दुष्काळग्रस्त (शासकीय निर्णय २५ सप्टें २०२६)",
        drought_status_en="14/14 Drought-Affected (Govt Resolution 25 Sep 2026)",
        meta=ResponseMeta(
            sources=["SRC_CRIDA_PLAN", "SRC_IMD_RAINFALL", "SRC_MAHA_GR"],
            as_of=as_of,
            trust_tier="OFFICIAL_STATISTIC",
            n_observations=14
        )
    )


@router.get("/forecast")
def get_weather_forecast(
    tehsil: Optional[str] = Query("Nagpur (Rural)", description="Name of tehsil"),
    db: Session = Depends(get_db)
):
    """Retrieve live 7-day weather forecast from Open-Meteo API for selected tehsil centroid."""
    tehsil_rec = db.query(DimTehsil).filter(
        (DimTehsil.name_en.ilike(tehsil)) | (DimTehsil.name_mr.ilike(tehsil))
    ).first()

    if not tehsil_rec:
        tehsil_rec = db.query(DimTehsil).filter_by(name_en="Nagpur (Rural)").first()

    lat, lon = tehsil_rec.centroid_lat, tehsil_rec.centroid_lon
    open_meteo_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,weather_code"
        f"&timezone=Asia%2FKolkata"
    )

    try:
        resp = requests.get(open_meteo_url, timeout=10)
        resp.raise_for_status()
        forecast_data = resp.json()

        daily = forecast_data.get("daily", {})
        time_list = daily.get("time", [])
        days = []
        for i, t in enumerate(time_list):
            days.append({
                "date": t,
                "t_max_c": daily.get("temperature_2m_max", [0])[i],
                "t_min_c": daily.get("temperature_2m_min", [0])[i],
                "precipitation_mm": daily.get("precipitation_sum", [0])[i],
                "wind_speed_kmh": daily.get("wind_speed_10m_max", [0])[i],
                "weather_code": daily.get("weather_code", [0])[i],
            })

        return {
            "tehsil": tehsil_rec.name_en,
            "tehsil_mr": tehsil_rec.name_mr,
            "centroid": {"lat": lat, "lon": lon},
            "forecast_days": days,
            "meta": ResponseMeta(
                sources=["SRC_OPEN_METEO"],
                as_of=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                trust_tier="DERIVED",
                n_observations=len(days)
            )
        }
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Upstream weather service temporarily unavailable: {str(e)}"
        )

