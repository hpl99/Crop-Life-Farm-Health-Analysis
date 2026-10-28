"""Common Pydantic v2 schemas and RFC 7807 Problem Details."""

from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ResponseMeta(BaseModel):
    """Metadata block required on every API response."""
    sources: List[str] = Field(..., description="List of source_ids cited in this payload")
    as_of: str = Field(..., description="Freshness timestamp (ISO 8601 UTC)")
    trust_tier: str = Field(..., description="Highest trust tier: OFFICIAL_STATISTIC, OFFICIAL_ANNOUNCEMENT, REPORTED_MEDIA, DERIVED")
    n_observations: Optional[int] = Field(None, description="Number of underlying real observations")


class ProblemDetails(BaseModel):
    """RFC 7807 compliant problem details error payload."""
    type: str = Field("about:blank", description="URI reference identifying the problem type")
    title: str = Field(..., description="Short, human-readable summary of the problem")
    status: int = Field(..., description="HTTP status code")
    detail: str = Field(..., description="Human-readable explanation specific to this occurrence")
    instance: Optional[str] = Field(None, description="URI reference identifying the specific occurrence")

