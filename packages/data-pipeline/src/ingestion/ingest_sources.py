"""Ingest official sources and crop dimension records."""

from sqlalchemy.orm import Session
from apps.api.src.models.entities import Source, DimCrop

INITIAL_SOURCES = [
    {
        "source_id": "SRC_UPAG_DES",
        "name": "Unified Portal for Agricultural Statistics (UPAg) & DES",
        "url": "https://indiadataportal.com/p/area-production-yield-apy",
        "licence": "Open Data Commons Attribution License 1.0 (ODC-BY 1.0)",
        "trust_tier": "OFFICIAL_STATISTIC",
        "description": "District, Season and Crop wise Area, Production and Yield Statistics for Maharashtra published by DES, Ministry of Agriculture & Farmers Welfare."
    },
    {
        "source_id": "SRC_ICRISAT_DLD",
        "name": "ICRISAT District Level Database (DLD)",
        "url": "http://data.icrisat.org/dld/",
        "licence": "Public Agricultural Research Database (OGD India / ICRISAT)",
        "trust_tier": "OFFICIAL_STATISTIC",
        "description": "Historical district level agricultural database for India (1966-2015), ICRISAT-ICAR collaboration."
    },
    {
        "source_id": "SRC_IMD_RAINFALL",
        "name": "India Meteorological Department (IMD) District Climatology",
        "url": "https://mausam.imd.gov.in/",
        "licence": "Open Government Data (OGD India)",
        "trust_tier": "OFFICIAL_STATISTIC",
        "description": "Long-period historical monthly district rainfall and seasonal departures."
    },
    {
        "source_id": "SRC_OPEN_METEO",
        "name": "Open-Meteo Weather API & ERA5 Reanalysis",
        "url": "https://open-meteo.com/",
        "licence": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "trust_tier": "DERIVED",
        "description": "Hourly and daily weather forecast and ECMWF ERA5 atmospheric reanalysis."
    },
    {
        "source_id": "SRC_MSAMB_CMO",
        "name": "Maharashtra State Agricultural Marketing Board & CMO Mandi Portal",
        "url": "https://www.msamb.com/",
        "licence": "Open Government Data (OGD India / Govt. of Maharashtra)",
        "trust_tier": "OFFICIAL_STATISTIC",
        "description": "APMC mandi arrivals, minimum, maximum, and modal market prices."
    },
    {
        "source_id": "SRC_CRIDA_PLAN",
        "name": "ICAR-CRIDA Agriculture Contingency Plan for Nagpur",
        "url": "https://www.icar-crida.res.in/CP-2012/statewiseplans/Maharastra(Pdf)/PDKV,%20Akola/Nagpur.pdf",
        "licence": "Government of India / ICAR Official Research Publication",
        "trust_tier": "OFFICIAL_STATISTIC",
        "description": "District agro-climatic profile, taluka normal rainfall, soil mix, and 5-year baseline crop productivity."
    },
    {
        "source_id": "SRC_MAHA_GR",
        "name": "Government of Maharashtra Revenue & Forest Dept Resolutions",
        "url": "https://gr.maharashtra.gov.in/",
        "licence": "Official State Government Gazette / Executive Notification",
        "trust_tier": "OFFICIAL_ANNOUNCEMENT",
        "description": "Official government resolutions including 25 September 2026 drought declaration."
    },
    {
        "source_id": "SRC_CENSUS_LGD",
        "name": "Census of India 2011 / Local Government Directory",
        "url": "https://lgdirectory.gov.in/",
        "licence": "Open Database / Survey of India",
        "trust_tier": "OFFICIAL_STATISTIC",
        "description": "Sub-district administrative boundaries and centroids."
    }
]

INITIAL_CROPS = [
    {
        "crop_id": "soybean",
        "name_en": "Soybean",
        "name_mr": "सोयाबीन",
        "category": "Oilseeds",
        "aliases": "Soyabean, Bhat, Glycine max"
    },
    {
        "crop_id": "cotton",
        "name_en": "Cotton",
        "name_mr": "कापूस",
        "category": "Fibres",
        "aliases": "Cotton lint, Kapas, Gossypium"
    },
    {
        "crop_id": "rice",
        "name_en": "Rice (Paddy)",
        "name_mr": "भात / धान",
        "category": "Cereals",
        "aliases": "Paddy, Dhan, Oryza sativa"
    },
    {
        "crop_id": "wheat",
        "name_en": "Wheat",
        "name_mr": "गहू",
        "category": "Cereals",
        "aliases": "Gehun, Triticum"
    },
    {
        "crop_id": "gram",
        "name_en": "Gram (Chickpea)",
        "name_mr": "हरभरा (चना)",
        "category": "Pulses",
        "aliases": "Bengal Gram, Chana, Cicer arietinum"
    },
    {
        "crop_id": "tur",
        "name_en": "Pigeonpea (Tur/Arhar)",
        "name_mr": "तूर (अरहर)",
        "category": "Pulses",
        "aliases": "Tur, Arhar, Red Gram, Cajanus cajan"
    },
    {
        "crop_id": "jowar",
        "name_en": "Sorghum (Jowar)",
        "name_mr": "ज्वारी",
        "category": "Cereals",
        "aliases": "Jowar, Great Millet, Sorghum bicolor"
    }
]


def ingest_sources(db: Session):
    """Seed or update source metadata."""
    for s_data in INITIAL_SOURCES:
        existing = db.query(Source).filter_by(source_id=s_data["source_id"]).first()
        if not existing:
            source = Source(**s_data)
            db.add(source)
    db.commit()


def ingest_crops(db: Session):
    """Seed or update crop dimensions."""
    for c_data in INITIAL_CROPS:
        existing = db.query(DimCrop).filter_by(crop_id=c_data["crop_id"]).first()
        if not existing:
            crop = DimCrop(**c_data)
            db.add(crop)
    db.commit()

