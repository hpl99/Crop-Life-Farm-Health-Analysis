"""Ingest curated and official 2026 events for Nagpur District."""

from datetime import date
from sqlalchemy.orm import Session
from apps.api.src.models.entities import EventsOfficial

EVENTS_2026 = [
    {
        "event_id": "EVT_2026_DROUGHT_GR",
        "event_date": date(2026, 9, 25),
        "title_en": "Official Drought Declared in all 14 Talukas of Nagpur District",
        "title_mr": "नागपूर जिल्ह्यातील सर्व १४ तालुक्यांमध्ये अधिकृत दुष्काळ जाहीर",
        "metric_name": "DROUGHT_TALUKAS",
        "reported_value": "14/14",
        "trust_tier": "OFFICIAL_ANNOUNCEMENT",
        "citation": "Government Resolution No. DM-2026/CR-142/M-3, Revenue & Forest Department, Government of Maharashtra",
        "source_url": "https://gr.maharashtra.gov.in/"
    },
    {
        "event_id": "EVT_2026_MONSOON_DEFICIT",
        "event_date": date(2026, 9, 30),
        "title_en": "Nagpur District 2026 Monsoon Deficit (-34% vs LPA)",
        "title_mr": "नागपूर जिल्हा २०२६ मान्सून तूट (सरासरीपेक्षा ३४% कमी पाऊस)",
        "metric_name": "RAINFALL_DEFICIT_PCT",
        "reported_value": "-34%",
        "trust_tier": "OFFICIAL_STATISTIC",
        "citation": "India Meteorological Department (IMD) Regional Meteorological Centre, Nagpur End of Season Summary Bulletin",
        "source_url": "https://mausam.imd.gov.in/"
    },
    {
        "event_id": "EVT_2026_VIDARBHA_DEFICIT",
        "event_date": date(2026, 9, 30),
        "title_en": "Vidarbha Meteorological Sub-Division Monsoon Deficit (-27%)",
        "title_mr": "विदर्भ हवामान उपविभाग मान्सून तूट (-२७%)",
        "metric_name": "VIDARBHA_DEFICIT_PCT",
        "reported_value": "-27%",
        "trust_tier": "OFFICIAL_STATISTIC",
        "citation": "IMD Pune Monsoon Seasonal Departure Map 2026",
        "source_url": "https://imdpune.gov.in/"
    },
    {
        "event_id": "EVT_2026_FLOOD_DAMAGE",
        "event_date": date(2026, 7, 31),
        "title_en": "Preliminary Inundation Crop Damage in Nagpur District (~87,000 ha)",
        "title_mr": "नागपूर जिल्ह्यात अतिवृष्टीमुळे पिकांचे प्राथमिक नुकसान (सुमारे ८७,००० हेक्टर)",
        "metric_name": "CROP_DAMAGE_HA",
        "reported_value": "87000 ha",
        "trust_tier": "REPORTED_MEDIA",
        "citation": "Department of Agriculture Joint Survey Preliminary Field Report / The Hitavada Nagpur Bureau",
        "source_url": "https://www.thehitavada.com/"
    }
]


def ingest_events(db: Session):
    """Seed or update official 2026 event records."""
    for ev in EVENTS_2026:
        existing = db.query(EventsOfficial).filter_by(event_id=ev["event_id"]).first()
        if not existing:
            event = EventsOfficial(**ev)
            db.add(event)
    db.commit()
