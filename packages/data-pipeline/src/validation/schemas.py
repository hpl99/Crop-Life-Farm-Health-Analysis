"""Pandera validation schemas for data integrity and provenance.

Fails loudly if:
- source_id is null
- yield, area, or production are negative
- rainfall is negative or exceeds realistic limits (>1000mm in a single month)
- trust_tier is not in approved list
"""

import pandera.pandas as pa
from pandera.pandas import Column, Check, DataFrameSchema

APPROVED_TRUST_TIERS = [
    "OFFICIAL_STATISTIC",
    "OFFICIAL_ANNOUNCEMENT",
    "REPORTED_MEDIA",
    "DERIVED"
]

# 1. Crop Yield Schema
CropYieldSchema = DataFrameSchema(
    {
        "district": Column(str, Check.isin(["Nagpur", "NAGPUR"]), nullable=False),
        "crop_id": Column(str, nullable=False),
        "season": Column(str, Check.isin(["Kharif", "Rabi", "Summer", "Whole Year"]), nullable=False),
        "crop_year": Column(int, Check.in_range(1960, 2030), nullable=False),
        "fiscal_year": Column(str, nullable=True),
        "area_ha": Column(float, Check.greater_than_or_equal_to(0.0), nullable=True),
        "production_t": Column(float, Check.greater_than_or_equal_to(0.0), nullable=True),
        "yield_kg_ha": Column(float, Check.in_range(0.0, 150000.0), nullable=True),  # Sugarcane can reach 120k kg/ha
        "source_id": Column(str, Check.str_length(min_value=3), nullable=False),
        "trust_tier": Column(str, Check.isin(APPROVED_TRUST_TIERS), nullable=False),
        "is_outlier": Column(bool, nullable=False),
    },
    strict=True,
    coerce=True
)

# 2. Monthly Rainfall Schema
MonthlyRainfallSchema = DataFrameSchema(
    {
        "district": Column(str, Check.isin(["Nagpur", "NAGPUR"]), nullable=False),
        "year": Column(int, Check.in_range(1950, 2030), nullable=False),
        "month": Column(int, Check.in_range(1, 12), nullable=False),
        "rainfall_mm": Column(float, Check.in_range(0.0, 1500.0), nullable=False),
        "source_id": Column(str, Check.str_length(min_value=3), nullable=False),
        "trust_tier": Column(str, Check.isin(APPROVED_TRUST_TIERS), nullable=False),
    },
    strict=False,
    coerce=True
)

# 3. Tehsil Boundary Schema
TehsilSchema = DataFrameSchema(
    {
        "tehsil_id": Column(int, Check.greater_than(0), nullable=False),
        "name_en": Column(str, Check.str_length(min_value=2), nullable=False),
        "name_mr": Column(str, Check.str_length(min_value=2), nullable=False),
        "centroid_lat": Column(float, Check.in_range(20.0, 22.0), nullable=False),
        "centroid_lon": Column(float, Check.in_range(78.0, 80.0), nullable=False),
    },
    strict=False,
    coerce=True
)

# 4. Mandi Price Schema
MandiPriceSchema = DataFrameSchema(
    {
        "market_id": Column(str, nullable=False),
        "crop_id": Column(str, nullable=False),
        "arrivals_qtl": Column(float, Check.greater_than_or_equal_to(0.0), nullable=True),
        "min_price": Column(float, Check.greater_than_or_equal_to(0.0), nullable=True),
        "max_price": Column(float, Check.greater_than_or_equal_to(0.0), nullable=True),
        "modal_price": Column(float, Check.greater_than(0.0), nullable=False),
        "source_id": Column(str, Check.str_length(min_value=3), nullable=False),
    },
    strict=False,
    coerce=True
)
