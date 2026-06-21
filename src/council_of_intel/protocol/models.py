"""Shared deliberation protocol models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from council_of_intel.openrouter.anonymizer import AnonymizedResponses
from council_of_intel.openrouter.client import ChatCompletionResult, SeatFailure
from council_of_intel.validation import SeatConfig, ValidationWarning


@dataclass(frozen=True, slots=True)
class Round1Result:
    """Blind-first individual responses."""

    status: Literal["completed", "aborted_insufficient_seats"]
    completed: list[ChatCompletionResult]
    failed: list[SeatFailure]


@dataclass(frozen=True, slots=True)
class Round2Evaluation:
    """One seat's cross-examination output."""

    seat_idx: int
    personality_id: str
    model: str
    content: str
    winner_label: str | None
    usage_cost: float = 0.0
    retried_for_anti_recursion: bool = False


@dataclass(frozen=True, slots=True)
class Round2Result:
    """Cross-examination result and private anonymization map."""

    anonymized: AnonymizedResponses
    evaluations: list[Round2Evaluation]


@dataclass(frozen=True, slots=True)
class Round3Result:
    """Anti-convergence decision."""

    triggered: bool
    consensus_label: str | None = None
    agreement_ratio: float = 0.0
    counterfactual: str | None = None
    usage_cost: float = 0.0


@dataclass(frozen=True, slots=True)
class ProtocolResult:
    """Full protocol result before Phase 4 output formatting."""

    status: Literal["completed", "aborted_insufficient_seats"]
    warnings: list[ValidationWarning] = field(default_factory=list)
    round1: Round1Result | None = None
    round2: Round2Result | None = None
    round3: Round3Result | None = None
    final_answer: str | None = None
    final_answer_cost: float = 0.0
    counterfactual_triggered: bool = False
    counterfactual: str | None = None
    seats: list[SeatConfig] = field(default_factory=list)
