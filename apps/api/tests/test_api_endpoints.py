"""Comprehensive API contract, RFC 7807, and caching tests."""

import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app

client = TestClient(app)


def test_health_and_readiness():
    res1 = client.get("/healthz")
    assert res1.status_code == 200
    assert res1.json() == {"status": "ok"}

    res2 = client.get("/readyz")
    assert res2.status_code == 200
    assert res2.json() == {"status": "ready"}


def test_meta_sources():
    res = client.get("/api/v1/meta/sources")
    assert res.status_code == 200
    data = res.json()
    assert "sources" in data
    assert "meta" in data
    assert data["meta"]["trust_tier"] == "OFFICIAL_STATISTIC"
    assert len(data["sources"]) >= 5


def test_tehsils_geojson():
    res = client.get("/api/v1/tehsils")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 14
    for f in data["features"]:
        assert f["properties"]["name_en"]
        assert f["properties"]["name_mr"]
        assert f["geometry"]["type"] == "Point"


def test_drought_status():
    res = client.get("/api/v1/drought/status")
    assert res.status_code == 200
    data = res.json()
    assert data["total_talukas"] == 14
    assert data["affected_talukas"] == 14
    assert data["declaration_date"] == "2026-09-25"
    assert data["meta"]["trust_tier"] == "OFFICIAL_ANNOUNCEMENT"


def test_season_current_summary():
    res = client.get("/api/v1/season/current/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["normal_rf_mm"] == 936.1
    assert data["deficit_pct"] == -34.0
    assert data["actual_rf_mm"] == 617.8
    assert data["missing_rf_mm"] == 318.3
    assert data["drought_talukas_count"] == 14


def test_crops_list():
    res = client.get("/api/v1/crops")
    assert res.status_code == 200
    data = res.json()
    crop_ids = [c["crop_id"] for c in data["crops"]]
    assert "soybean" in crop_ids
    assert "cotton" in crop_ids
    assert "rice" in crop_ids


def test_crop_yield_history():
    res = client.get("/api/v1/crops/soybean/yield-history")
    assert res.status_code == 200
    data = res.json()
    assert data["crop_id"] == "soybean"
    assert len(data["data"]) >= 25
    assert data["spatial_level"] == "district"


def test_crop_rainfall_response():
    res = client.get("/api/v1/crops/cotton/rainfall-response")
    assert res.status_code == 200
    data = res.json()
    assert data["crop_id"] == "cotton"
    assert data["r_squared"] > 0.5
    assert len(data["scatter_points"]) >= 30
    assert len(data["trend_line"]) >= 2


def test_crop_outlook_with_ranges_and_analogs():
    """Phase 2 Acceptance: API returns ranges and analogs."""
    res = client.get("/api/v1/outlook/soybean?deficit_pct=-34")
    assert res.status_code == 200
    data = res.json()
    assert data["crop_id"] == "soybean"
    assert "range_80_kg_ha" in data
    assert "range_95_kg_ha" in data
    assert len(data["analog_years"]) == 5
    assert "confidence_disclaimer" in data


def test_market_prices():
    res = client.get("/api/v1/market/prices?limit=10")
    assert res.status_code == 200
    data = res.json()
    assert len(data["data"]) > 0
    assert data["data"][0]["modal_price"] > 0


def test_lab_regression_diagnostics():
    res = client.get("/api/v1/lab/regression?crop=rice")
    assert res.status_code == 200
    data = res.json()
    assert data["crop_id"] == "rice"
    diag = data["diagnostics"]
    assert "r_squared" in diag
    assert "loocv_mae_model" in diag


def test_export_csv():
    res = client.get("/api/v1/export.csv")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/csv")
    assert "district,crop_id,crop_name" in res.text


def test_rfc_7807_error_format_on_404():
    res = client.get("/api/v1/crops/nonexistent_crop/yield-history")
    assert res.status_code == 404
    assert res.headers["content-type"] == "application/problem+json"
    err = res.json()
    assert err["status"] == 404
    assert "title" in err
    assert "instance" in err


def test_etag_caching():
    res1 = client.get("/api/v1/season/current/summary")
    assert res1.status_code == 200
    etag = res1.headers.get("etag")
    assert etag is not None

    res2 = client.get("/api/v1/season/current/summary", headers={"if-none-match": etag})
    assert res2.status_code == 304
