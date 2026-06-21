from council_of_intel.tui.formatting import (
    anthropic_palette,
    default_sats_seats,
    round_cells,
    seat_indicator,
)


def test_tui_palette_uses_only_allowed_colors() -> None:
    assert set(anthropic_palette().values()) == {"#D97757", "#F5F5F5", "#00B050", "#D63F3F"}


def test_seat_indicator_maps_states() -> None:
    assert seat_indicator("pending") == "○"
    assert seat_indicator("running") == "⣾"
    assert seat_indicator("completed") == "✓"
    assert seat_indicator("failed") == "✗"


def test_round_cells_show_completed_current_and_pending() -> None:
    assert round_cells(current_round=2, rounds_completed=[0, 1]) == [
        "Round 0: ✓",
        "Round 1: ✓",
        "Round 2: ⣾",
        "Round 3: ○",
        "Round 4: ○",
    ]


def test_default_sats_seats_are_three_valid_entries() -> None:
    seats = default_sats_seats(
        [
            {"id": "ach-analyst", "recommended_model": "anthropic/claude-sonnet-4.6"},
            {"id": "red-team", "recommended_model": "x-ai/grok-4.3"},
            {"id": "devils-advocate", "recommended_model": "openai/gpt-chat-latest"},
        ]
    )

    assert len(seats) == 3
    assert [seat["personality_id"] for seat in seats] == [
        "ach-analyst",
        "red-team",
        "devils-advocate",
    ]
    assert [seat["model"] for seat in seats] == [
        "anthropic/claude-sonnet-4.6",
        "x-ai/grok-4.3",
        "openai/gpt-chat-latest",
    ]
