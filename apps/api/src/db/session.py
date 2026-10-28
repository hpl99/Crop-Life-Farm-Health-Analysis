"""Database engine and session management.

Supports both PostgreSQL + PostGIS (via DATABASE_URL) and local SQLite fallback.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from apps.api.src.models.entities import Base

# Default to local SQLite database in data/curated/ if DATABASE_URL is not set
ROOT_DIR = Path(__file__).resolve().parents[4]
DEFAULT_DB_PATH = ROOT_DIR / "data" / "curated" / "nagpur_krishi.db"
DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Set connect_args for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables in the database if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI route handlers."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

