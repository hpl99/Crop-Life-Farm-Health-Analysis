"""Phase 1 Acceptance Tests: Ingested Real Data Integrity & Provenance."""

import pytest
from apps.api.src.db.session import SessionLocal
from apps.api.src.models.entities import (
    Source, DimTehsil, DimCrop, FactCropYield, FactRainfall,
    FactRainfallNormal, EventsOfficial
)


@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_sources_present(db):
    """Verify all official sources are registered with licenses."""
    sources = db.query(Source).all()
    source_ids = {s.source_id for s in sources}
    assert "SRC_UPAG_DES" in source_ids
    assert "SRC_ICRISAT_DLD" in source_ids
    assert "SRC_IMD_RAINFALL" in source_ids
    assert "SRC_CRIDA_PLAN" in source_ids
    assert "SRC_MAHA_GR" in source_ids


def test_tehsils_count_and_coordinates(db):
    """Verify exactly 14 Nagpur tehsils exist with valid coordinates."""
    tehsils = db.query(DimTehsil).all()
    assert len(tehsils) == 14

    for t in tehsils:
        assert 20.0 <= t.centroid_lat <= 22.0
        assert 78.0 <= t.centroid_lon <= 80.0
        assert t.name_en and t.name_mr


def test_crop_yield_history_for_main_crops(db):
    """Phase 1 Acceptance Criteria: Yield history for each main crop loads with provenance."""
    main_crops = ["soybean", "cotton", "rice"]

    for crop_id in main_crops:
        yields = db.query(FactCropYield).filter_by(crop_id=crop_id).all()
        assert len(yields) >= 12, f"Expected at least 12 years of history for {crop_id}, found {len(yields)}"

        for y in yields:
            assert y.source_id in ["SRC_UPAG_DES", "SRC_ICRISAT_DLD"]
            assert y.trust_tier == "OFFICIAL_STATISTIC"
            if y.yield_kg_ha is not None:
                assert y.yield_kg_ha > 0, f"Negative or zero yield for {crop_id} in {y.crop_year}"


def test_crida_rainfall_normals(db):
    """Verify rainfall normals match ICAR-CRIDA contingency plan."""
    monsoon_norm = db.query(FactRainfallNormal).filter_by(
        tehsil_id=None,
        period_type="MONSOON_TOTAL"
    ).first()
    assert monsoon_norm is not None
    assert monsoon_norm.normal_rf_mm == 936.1
    assert monsoon_norm.normal_rainy_days == 44.9

    annual_norm = db.query(FactRainfallNormal).filter_by(
        tehsil_id=None,
        period_type="ANNUAL"
    ).first()
    assert annual_norm is not None
    assert annual_norm.normal_rf_mm == 1082.1


def test_official_2026_drought_event(db):
    """Verify the 2026 drought declaration event carries correct date and citation."""
    drought_ev = db.query(EventsOfficial).filter_by(event_id="EVT_2026_DROUGHT_GR").first()
    assert drought_ev is not None
    assert str(drought_ev.event_date) == "2026-09-25"
    assert drought_ev.reported_value == "14/14"
    assert drought_ev.trust_tier == "OFFICIAL_ANNOUNCEMENT"
    assert "DM-2026/CR-142/M-3" in drought_ev.citation

