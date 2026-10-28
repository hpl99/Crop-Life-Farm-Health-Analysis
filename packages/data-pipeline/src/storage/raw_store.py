"""Raw snapshot storage and provenance hashing.

Saves raw data files into data/raw/ and calculates SHA-256 checksums.
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


ROOT_DIR = Path(__file__).resolve().parents[4]
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def calculate_sha256(content: bytes) -> str:
    """Calculate hex SHA-256 digest of binary content."""
    return hashlib.sha256(content).hexdigest()


def save_raw_snapshot(filename: str, content: bytes, source_meta: Dict[str, Any]) -> Path:
    """Save an immutable raw file snapshot along with its provenance JSON manifest."""
    filepath = RAW_DATA_DIR / filename
    filepath.write_bytes(content)

    checksum = calculate_sha256(content)
    manifest = {
        "filename": filename,
        "filepath": str(filepath),
        "sha256": checksum,
        "byte_size": len(content),
        "saved_at_utc": datetime.utcnow().isoformat() + "Z",
        "source_meta": source_meta
    }

    manifest_path = RAW_DATA_DIR / f"{filename}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    return filepath
