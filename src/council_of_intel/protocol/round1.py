"""Round 1 blind-first individual responses."""

from __future__ import annotations

from typing import Protocol

from council_of_intel.config import AppConfig
from council_of_intel.openrouter.client import (
    BatchCompletionResult,
    ChatCompletionRequest,
    ChatMessage,
    run_seat_completions,
)
from council_of_intel.personalities.schema import Personality
from council_of_intel.protocol.models import Round1Result
from council_of_intel.validation import SeatConfig


class CompletionClient(Protocol):
    """Protocol for anything that can complete a chat request."""

    async def complete_chat(self, request: ChatCompletionRequest): ...


async def run_round1(
    query: str,
    seats: list[SeatConfig],
    config: AppConfig,
    catalog: dict[str, Personality],
    client: CompletionClient,
) -> Round1Result:
    """Send blind individual prompts in parallel."""
    requests = [
        ChatCompletionRequest(
            seat_idx=index,
            model=seat.model,
            messages=[
                ChatMessage(
                    role="system",
                    content=_seat_system_prompt(catalog[seat.personality_id]),
                ),
                ChatMessage(role="user", content=query),
            ],
        )
        for index, seat in enumerate(seats)
    ]
    batch: BatchCompletionResult = await run_seat_completions(
        client,
        requests,
        min_survivors=config.validation.min_seats_to_continue_after_failures,
    )
    return Round1Result(status=batch.status, completed=batch.completed, failed=batch.failed)


def _seat_system_prompt(personality: Personality) -> str:
    return "\n\n".join([personality.agent_prompt, personality.skill, personality.knowledge])
