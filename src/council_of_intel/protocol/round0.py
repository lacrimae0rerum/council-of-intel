"""Round 0 routing and validation."""

from __future__ import annotations

from council_of_intel.config import AppConfig
from council_of_intel.personalities.schema import Personality
from council_of_intel.validation import (
    SeatConfig,
    SessionValidationResult,
    validate_session_request,
)


def run_round0(
    mode: str,
    seats: list[SeatConfig],
    chairman_personality_id: str,
    config: AppConfig,
    catalog: dict[str, Personality],
) -> SessionValidationResult:
    """Validate all routing constraints before any model call."""
    return validate_session_request(mode, seats, chairman_personality_id, config, catalog)
