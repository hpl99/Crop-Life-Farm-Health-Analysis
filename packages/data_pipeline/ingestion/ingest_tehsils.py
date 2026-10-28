"""Ingest the 14 sub-districts (tehsils) of Nagpur District."""

from sqlalchemy.orm import Session
from apps.api.src.models.entities import DimTehsil

# Verified 14 Nagpur subdistricts from Census 2011 / LGD
NAGPUR_TEHSILS = [
    {"tehsil_id": 1, "lgd_code": "04018", "name_en": "Ramtek", "name_mr": "रामटेक", "centroid_lat": 21.51508, "centroid_lon": 79.34985},
    {"tehsil_id": 2, "lgd_code": "04019", "name_en": "Umred", "name_mr": "उमरेड", "centroid_lat": 20.85107, "centroid_lon": 79.19023},
    {"tehsil_id": 3, "lgd_code": "04020", "name_en": "Nagpur (Rural)", "name_mr": "नागपूर (ग्रामीण)", "centroid_lat": 21.02600, "centroid_lon": 78.99752},
    {"tehsil_id": 4, "lgd_code": "04021", "name_en": "Hingna", "name_mr": "हिंगणा", "centroid_lat": 21.00230, "centroid_lon": 78.86729},
    {"tehsil_id": 5, "lgd_code": "04022", "name_en": "Katol", "name_mr": "काटोल", "centroid_lat": 21.23028, "centroid_lon": 78.63156},
    {"tehsil_id": 6, "lgd_code": "04023", "name_en": "Bhiwapur", "name_mr": "भिवापूर", "centroid_lat": 20.72717, "centroid_lon": 79.37088},
    {"tehsil_id": 7, "lgd_code": "04024", "name_en": "Kalameshwar", "name_mr": "कळमेश्वर", "centroid_lat": 21.27613, "centroid_lon": 78.85215},
    {"tehsil_id": 8, "lgd_code": "04025", "name_en": "Kuhi", "name_mr": "कुही", "centroid_lat": 20.98193, "centroid_lon": 79.44755},
    {"tehsil_id": 9, "lgd_code": "04026", "name_en": "Savner", "name_mr": "सावनेर", "centroid_lat": 21.41714, "centroid_lon": 78.94767},
    {"tehsil_id": 10, "lgd_code": "04027", "name_en": "Kamptee", "name_mr": "कामठी", "centroid_lat": 21.14488, "centroid_lon": 79.24463},
    {"tehsil_id": 11, "lgd_code": "04028", "name_en": "Parseoni", "name_mr": "पारशिवणी", "centroid_lat": 21.43279, "centroid_lon": 79.14782},
    {"tehsil_id": 12, "lgd_code": "04029", "name_en": "Nagpur (Urban)", "name_mr": "नागपूर (शहर)", "centroid_lat": 21.14466, "centroid_lon": 79.07992},
    {"tehsil_id": 13, "lgd_code": "04030", "name_en": "Narkhed", "name_mr": "नरखेड", "centroid_lat": 21.38584, "centroid_lon": 78.48836},
    {"tehsil_id": 14, "lgd_code": "04031", "name_en": "Mauda", "name_mr": "मौदा", "centroid_lat": 21.22788, "centroid_lon": 79.43532},
]


def ingest_tehsils(db: Session):
    """Seed or update tehsil dimensions."""
    for t in NAGPUR_TEHSILS:
        existing = db.query(DimTehsil).filter_by(name_en=t["name_en"]).first()
        if not existing:
            tehsil = DimTehsil(**t)
            db.add(tehsil)
    db.commit()

