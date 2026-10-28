"""SQLAlchemy 2 database models for Nagpur Krishi Data.

Strict provenance: every fact row links to sources(source_id) and declares trust_tier.
"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    String, Integer, Float, Date, DateTime, Boolean, Text, ForeignKey,
    Index, UniqueConstraint, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    source_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    licence: Mapped[str] = mapped_column(String(255), nullable=False)
    trust_tier: Mapped[str] = mapped_column(String(32), nullable=False)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    ingestion_runs: Mapped[List["IngestionRun"]] = relationship(back_populates="source")
    raw_files: Mapped[List["RawFile"]] = relationship(back_populates="source")


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.source_id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(32), default="RUNNING", nullable=False)  # RUNNING, SUCCESS, FAILED
    row_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    checksum: Mapped[Optional[str]] = mapped_column(String(128))
    error_log: Mapped[Optional[str]] = mapped_column(Text)

    source: Mapped["Source"] = relationship(back_populates="ingestion_runs")


class RawFile(Base):
    __tablename__ = "raw_files"

    file_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.source_id"), nullable=False)
    filepath: Mapped[str] = mapped_column(Text, nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    file_format: Mapped[str] = mapped_column(String(16), nullable=False)  # csv, json, pdf

    source: Mapped["Source"] = relationship(back_populates="raw_files")


class DimTehsil(Base):
    __tablename__ = "dim_tehsil"

    tehsil_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lgd_code: Mapped[Optional[str]] = mapped_column(String(32), unique=True)
    name_en: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name_mr: Mapped[str] = mapped_column(String(64), nullable=False)
    centroid_lat: Mapped[float] = mapped_column(Float, nullable=False)
    centroid_lon: Mapped[float] = mapped_column(Float, nullable=False)
    geojson_geom: Mapped[Optional[str]] = mapped_column(Text)  # GeoJSON polygon/multipolygon string


class DimCrop(Base):
    __tablename__ = "dim_crop"

    crop_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name_en: Mapped[str] = mapped_column(String(64), nullable=False)
    name_mr: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)  # Oilseeds, Fibres, Cereals, Pulses
    aliases: Mapped[Optional[str]] = mapped_column(Text)  # JSON or comma-separated list of alternative names


class DimMarket(Base):
    __tablename__ = "dim_market"

    market_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    apmc_name_en: Mapped[str] = mapped_column(String(128), nullable=False)
    apmc_name_mr: Mapped[str] = mapped_column(String(128), nullable=False)
    district: Mapped[str] = mapped_column(String(64), default="Nagpur", nullable=False)
    tehsil_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dim_tehsil.tehsil_id"))


class FactCropYield(Base):
    __tablename__ = "fact_crop_yield"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district: Mapped[str] = mapped_column(String(64), default="Nagpur", nullable=False)
    crop_id: Mapped[str] = mapped_column(ForeignKey("dim_crop.crop_id"), nullable=False)
    season: Mapped[str] = mapped_column(String(32), nullable=False)  # Kharif, Rabi, Summer
    crop_year: Mapped[int] = mapped_column(Integer, nullable=False)
    fiscal_year: Mapped[Optional[str]] = mapped_column(String(16))   # e.g. "2023-2024"
    area_ha: Mapped[Optional[float]] = mapped_column(Float)
    production_t: Mapped[Optional[float]] = mapped_column(Float)
    yield_kg_ha: Mapped[Optional[float]] = mapped_column(Float)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.source_id"), nullable=False)
    trust_tier: Mapped[str] = mapped_column(String(32), nullable=False)
    is_outlier: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("district", "crop_id", "season", "crop_year", name="uq_crop_yield_obs"),
        Index("idx_crop_yield_lookup", "crop_id", "crop_year"),
    )


class FactRainfall(Base):
    __tablename__ = "fact_rainfall"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tehsil_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dim_tehsil.tehsil_id"))  # None for district-aggregate
    district: Mapped[str] = mapped_column(String(64), default="Nagpur", nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    rainfall_mm: Mapped[float] = mapped_column(Float, nullable=False)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.source_id"), nullable=False)
    trust_tier: Mapped[str] = mapped_column(String(32), nullable=False)

    __table_args__ = (
        UniqueConstraint("tehsil_id", "district", "record_date", name="uq_rainfall_obs"),
        Index("idx_rainfall_year_month", "year", "month"),
    )


class FactRainfallNormal(Base):
    __tablename__ = "fact_rainfall_normal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tehsil_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dim_tehsil.tehsil_id"))
    period_type: Mapped[str] = mapped_column(String(32), nullable=False)  # MONSOON_TOTAL, ANNUAL, MONTH
    period_index: Mapped[Optional[int]] = mapped_column(Integer)          # 6 for June, etc.
    normal_rf_mm: Mapped[float] = mapped_column(Float, nullable=False)
    normal_rainy_days: Mapped[Optional[float]] = mapped_column(Float)
    basis_period: Mapped[str] = mapped_column(String(64), default="ICAR-CRIDA/IMD", nullable=False)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.source_id"), nullable=False)


class FactMarketPrice(Base):
    __tablename__ = "fact_market_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    market_id: Mapped[str] = mapped_column(ForeignKey("dim_market.market_id"), nullable=False)
    crop_id: Mapped[str] = mapped_column(ForeignKey("dim_crop.crop_id"), nullable=False)
    price_date: Mapped[date] = mapped_column(Date, nullable=False)
    arrivals_qtl: Mapped[Optional[float]] = mapped_column(Float)
    min_price: Mapped[Optional[float]] = mapped_column(Float)
    max_price: Mapped[Optional[float]] = mapped_column(Float)
    modal_price: Mapped[float] = mapped_column(Float, nullable=False)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.source_id"), nullable=False)

    __table_args__ = (
        Index("idx_market_price_lookup", "crop_id", "price_date"),
    )


class EventsOfficial(Base):
    __tablename__ = "events_official"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)
    title_mr: Mapped[str] = mapped_column(String(255), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(64), nullable=False)
    reported_value: Mapped[str] = mapped_column(String(64), nullable=False)
    trust_tier: Mapped[str] = mapped_column(String(32), nullable=False)
    citation: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)


class ModelRegistry(Base):
    __tablename__ = "model_registry"

    model_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    crop_id: Mapped[str] = mapped_column(ForeignKey("dim_crop.crop_id"), nullable=False)
    model_type: Mapped[str] = mapped_column(String(64), nullable=False)  # OLS_TREND_RAIN, OLYMPIC_5YR, ANALOG_MATCH
    trained_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    data_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    parameters_json: Mapped[str] = mapped_column(Text, nullable=False)


class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    metric_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    model_id: Mapped[str] = mapped_column(ForeignKey("model_registry.model_id"), nullable=False)
    loocv_mae: Mapped[float] = mapped_column(Float, nullable=False)
    loocv_mape: Mapped[float] = mapped_column(Float, nullable=False)
    r_squared: Mapped[Optional[float]] = mapped_column(Float)
    p_value: Mapped[Optional[float]] = mapped_column(Float)
    baseline_mae: Mapped[float] = mapped_column(Float, nullable=False)
    beats_baseline: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
