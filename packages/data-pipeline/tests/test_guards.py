"""CI Guards that MUST fail the build if rules are violated.

Guards:
(a) A curated fact row with null source_id.
(b) faker, random, numpy.random used inside ingestion or API packages.
(c) Numeric statistics hard-coded in apps/web/src/** outside *.test.* and *.stories.*.
(d) Banned crop_data.csv file presence.
"""

import os
import re
from pathlib import Path
import pytest
from apps.api.src.db.session import SessionLocal
from apps.api.src.models.entities import FactCropYield, FactRainfall, FactMarketPrice

ROOT_DIR = Path(__file__).resolve().parents[3]


def test_guard_no_null_source_id():
    """CI Guard A: Every curated fact row must have a non-null source_id."""
    db = SessionLocal()
    try:
        null_yields = db.query(FactCropYield).filter(FactCropYield.source_id.is_(None)).count()
        assert null_yields == 0, f"Found {null_yields} fact_crop_yield rows with null source_id!"

        null_rain = db.query(FactRainfall).filter(FactRainfall.source_id.is_(None)).count()
        assert null_rain == 0, f"Found {null_rain} fact_rainfall rows with null source_id!"

        null_mandi = db.query(FactMarketPrice).filter(FactMarketPrice.source_id.is_(None)).count()
        assert null_mandi == 0, f"Found {null_mandi} fact_market_price rows with null source_id!"
    finally:
        db.close()


def test_guard_no_synthetic_generators_in_core():
    """CI Guard B: No faker, random, or numpy.random inside ingestion or API packages."""
    target_dirs = [
        ROOT_DIR / "apps" / "api" / "src",
        ROOT_DIR / "packages" / "data-pipeline" / "src",
        ROOT_DIR / "packages" / "analytics" / "src"
    ]

    forbidden_patterns = [
        re.compile(r"\bimport\s+faker\b"),
        re.compile(r"\bfrom\s+faker\b"),
        re.compile(r"\bimport\s+random\b"),
        re.compile(r"\bfrom\s+random\s+import\b"),
        re.compile(r"\bnumpy\.random\b"),
        re.compile(r"\bnp\.random\b")
    ]

    violations = []
    for t_dir in target_dirs:
        if not t_dir.exists():
            continue
        for py_file in t_dir.rglob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                matches = pattern.findall(text)
                if matches:
                    violations.append(f"{py_file}: contains forbidden pattern '{matches[0]}'")

    assert not violations, f"Synthetic generation guards failed:\n" + "\n".join(violations)


def test_guard_banned_crop_data_csv_not_present():
    """CI Guard D: Banned file crop_data.csv must not exist anywhere in the project."""
    matches = list(ROOT_DIR.rglob("crop_data.csv"))
    assert not matches, f"BANNED simulated file crop_data.csv found in repository: {matches}"


def test_guard_no_hardcoded_statistics_in_web():
    """CI Guard C: apps/web/src/** must not contain hard-coded statistics literals."""
    web_src = ROOT_DIR / "apps" / "web" / "src"
    if not web_src.exists():
        pytest.skip("apps/web/src does not exist yet (Phase 1)")

    banned_mockup_literals = [
        "650 mm",
        "286 mm",
        "936 mm",
        "R² = 0.76",
        "R^2 = 0.76",
        "120 kg/ha",
        "-400+ kg/ha",
        "Est. 650-900"
    ]

    violations = []
    for file_path in web_src.rglob("*"):
        if not file_path.is_file():
            continue
        # Skip tests, stories, and design references
        if any(skip in file_path.name for skip in [".test.", ".spec.", ".stories."]):
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for literal in banned_mockup_literals:
            if literal in text:
                violations.append(f"{file_path}: contains banned prototype mockup literal '{literal}'")

    assert not violations, "Hardcoded statistics guard failed:\n" + "\n".join(violations)
