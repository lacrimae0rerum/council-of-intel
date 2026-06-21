"""Structured models for Stage Final Markdown generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

SessionStatus = Literal["completed", "cancelled_by_user", "aborted_insufficient_seats"]
OutputMode = Literal["sats", "council"]


@dataclass(frozen=True, slots=True)
class DiscardedOption:
    """Rejected option in the Stage Final reasoning."""

    name: str
    problem: str
    reasoning: str


@dataclass(frozen=True, slots=True)
class FinalAnswerSections:
    """Structured content for the Stage Final core."""

    chairman_personality: str
    chosen_answer: str
    intro: str
    discarded_options: list[DiscardedOption]
    why_chosen: str
    recommended_formulation: str
    conclusion_bullets: list[str]
    dissent: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SatAnnex:
    """SAT annex content produced by a seat."""

    personality_id: str
    seat_idx: int
    content: str


@dataclass(frozen=True, slots=True)
class SeatMetadata:
    """Metadata for one analytical seat."""

    seat_idx: int
    personality_id: str
    model: str


@dataclass(frozen=True, slots=True)
class FailedSeat:
    """Metadata for a failed seat."""

    seat_idx: int
    personality_id: str
    model: str
    reason: str


@dataclass(frozen=True, slots=True)
class SessionMetadata:
    """Session metadata rendered in every Stage Final."""

    mode: OutputMode
    status: SessionStatus
    seats: list[SeatMetadata]
    chairman_synthesis_model: str
    chairman_personality: str
    chairman_counterfactual_model: str | None
    counterfactual_triggered: bool
    cost_eur: float
    duration_seconds: int
    session_id: str
    failed_seats: list[FailedSeat] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class RoundExportAnnexes:
    """Round details appended only to Markdown exports."""

    round1: str
    round2: str
    round3: str | None = None
