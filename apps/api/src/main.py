"""FastAPI application entrypoint for Nagpur Krishi Data API."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.src.core.errors import register_error_handlers
from apps.api.src.core.middleware import ETagMiddleware
from apps.api.src.db.session import init_db

# Routers
from apps.api.src.api.v1.meta import router as meta_router
from apps.api.src.api.v1.tehsils import router as tehsils_router
from apps.api.src.api.v1.season import router as season_router
from apps.api.src.api.v1.rainfall import router as rainfall_router
from apps.api.src.api.v1.crops import router as crops_router
from apps.api.src.api.v1.markets import router as markets_router
from apps.api.src.api.v1.lab import router as lab_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Nagpur Krishi Data API (नागपूर शेती आकडे)",
    description="High-fidelity agricultural statistics, rainfall models, and market intelligence for farmers of Nagpur district.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ETag Middleware
app.add_middleware(ETagMiddleware)

# 3. RFC 7807 Error Handlers
register_error_handlers(app)

# 4. Include Routers
api_v1_prefix = "/api/v1"
app.include_router(meta_router, prefix=api_v1_prefix)
app.include_router(tehsils_router, prefix=api_v1_prefix)
app.include_router(season_router, prefix=api_v1_prefix)
app.include_router(rainfall_router, prefix=api_v1_prefix)
app.include_router(crops_router, prefix=api_v1_prefix)
app.include_router(markets_router, prefix=api_v1_prefix)
app.include_router(lab_router, prefix=api_v1_prefix)


@app.get("/healthz", tags=["System Health"])
def health_check():
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/readyz", tags=["System Health"])
def readiness_check():
    """Readiness probe."""
    return {"status": "ready"}
