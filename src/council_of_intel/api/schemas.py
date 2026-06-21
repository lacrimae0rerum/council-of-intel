"""FastAPI request and response schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from council_of_intel.validation import SeatConfig


class SessionCreateRequest(BaseModel):
    """Create one one-shot session."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    mode: Literal["sats", "council"]
    seats: list[SeatConfig] = Field(min_length=3)
    chairman_personality: str = "mclaughlin"


class SessionCreateResponse(BaseModel):
    """Immediate session creation response."""

    session_id: str
    status: str


class ErrorPayload(BaseModel):
    """Structured validation or dry-run error."""

    error_code: str
    message_human: str
    context: dict
    doc_ref: str | None = None


class DryRunResponse(BaseModel):
    """Dry-run validation result."""

    valid: bool
    errors: list[ErrorPayload] = Field(default_factory=list)
    warnings: list[dict] = Field(default_factory=list)
    openrouter_models_validated: bool
    models_check: dict
