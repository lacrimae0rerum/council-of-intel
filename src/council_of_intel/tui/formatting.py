"""TUI formatting helpers and static defaults."""

from __future__ import annotations

DEFAULT_SATS_PERSONALITY_IDS = ("ach-analyst", "red-team", "devils-advocate")

STATE_INDICATORS = {
    "pending": "○",
    "running": "⣾",
    "completed": "✓",
    "failed": "✗",
}


def anthropic_palette() -> dict[str, str]:
    """Return the strict TUI palette from spec/07."""
    return {
        "anthropic": "#D97757",
        "ink": "#F5F5F5",
        "success": "#00B050",
        "danger": "#D63F3F",
    }


def default_sats_seats(personalities: list[dict]) -> list[dict]:
    """Build default SATs seats from the backend personality catalog."""
    by_id = {personality["id"]: personality for personality in personalities}
    seats: list[dict] = []
    for personality_id in DEFAULT_SATS_PERSONALITY_IDS:
        personality = by_id.get(personality_id)
        if personality is None:
            continue
        seats.append(
            {
                "personality_id": personality_id,
                "model": personality["recommended_model"],
            }
        )
    return seats


def seat_indicator(state: str) -> str:
    """Return the TUI symbol for a seat state."""
    return STATE_INDICATORS.get(state, "○")


def round_cells(current_round: int | None, rounds_completed: list[int]) -> list[str]:
    """Return fixed round cells for display."""
    cells: list[str] = []
    completed = set(rounds_completed)
    for round_idx in range(5):
        if round_idx in completed:
            indicator = "✓"
        elif current_round == round_idx:
            indicator = "⣾"
        else:
            indicator = "○"
        cells.append(f"Round {round_idx}: {indicator}")
    return cells
