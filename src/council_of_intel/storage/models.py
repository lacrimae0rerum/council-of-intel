"""Persistent session storage models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

SessionStatus = Literal[
    "pending",
    "running",
    "completed",
    "cancelled_by_user",
    "aborted_insufficient_seats",
]
SeatState = Literal["pending", "running", "completed", "failed"]
SessionMode = Literal["sats", "council"]


class SeatRecord(BaseModel):
    """Persistent metadata for one analytical seat."""

    model_config = ConfigDict(extra="forbid")

    seat_idx: int = Field(ge=0)
    personality_id: str
    model: str
    state: SeatState
    error: str | None = None


class FailedSeatRecord(BaseModel):
    """Persistent metadata for a failed seat."""

    model_config = ConfigDict(extra="forbid")

    seat_idx: int = Field(ge=0)
    personality_id: str
    reason: str
    model: str | None = None


class SessionRecord(BaseModel):
    """Complete persisted session record."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    query: str
    mode: SessionMode
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    current_round: int | None = Field(default=None, ge=0, le=4)
    cost_eur: float = Field(default=0.0, ge=0)
    final_markdown: str | None = None
    seats: list[SeatRecord] = Field(default_factory=list)
    failed_seats: list[FailedSeatRecord] = Field(default_factory=list)
    rounds: dict[str, Any] = Field(default_factory=dict)
    logs: list[dict[str, Any]] = Field(default_factory=list)


class SessionSummary(BaseModel):
    """SQLite-backed lightweight session listing row."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    query: str
    mode: SessionMode
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    cost_eur: float
    current_round: int | None = None
