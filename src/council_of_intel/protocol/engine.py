"""End-to-end deliberation protocol orchestration."""

from __future__ import annotations

from typing import Protocol

from council_of_intel.config import AppConfig
from council_of_intel.openrouter.client import ChatCompletionRequest, ChatCompletionResult
from council_of_intel.personalities.schema import Personality
from council_of_intel.protocol.models import ProtocolResult
from council_of_intel.protocol.round0 import run_round0
from council_of_intel.protocol.round1 import run_round1
from council_of_intel.protocol.round2 import run_round2
from council_of_intel.protocol.round3 import run_round3
from council_of_intel.protocol.round4 import run_round4
from council_of_intel.validation import SeatConfig


class CompletionClient(Protocol):
    """Protocol for the injected LLM client."""

    async def complete_chat(self, request: ChatCompletionRequest) -> ChatCompletionResult: ...


class DeliberationProtocol:
    """Run Round 0 through Round 4 for one one-shot session."""

    def __init__(
        self,
        config: AppConfig,
        catalog: dict[str, Personality],
        client: CompletionClient,
        anonymizer_seed: int | None = None,
    ) -> None:
        self._config = config
        self._catalog = catalog
        self._client = client
        self._anonymizer_seed = anonymizer_seed

    async def run(
        self,
        query: str,
        mode: str,
        seats: list[SeatConfig],
        chairman_personality_id: str,
    ) -> ProtocolResult:
        """Execute the full deliberation protocol."""
        round0 = run_round0(mode, seats, chairman_personality_id, self._config, self._catalog)
        round1 = await run_round1(query, seats, self._config, self._catalog, self._client)
        if round1.status == "aborted_insufficient_seats":
            return ProtocolResult(
                status="aborted_insufficient_seats",
                warnings=round0.warnings,
                round1=round1,
                seats=seats,
            )

        round2 = await run_round2(
            query,
            seats,
            round1,
            self._config,
            self._catalog,
            self._client,
            anonymizer_seed=self._anonymizer_seed,
        )
        round3 = await run_round3(round2, self._config, self._client)
        final_response = await run_round4(
            query,
            self._catalog[chairman_personality_id],
            round1,
            round2,
            round3,
            self._config,
            self._client,
        )
        return ProtocolResult(
            status="completed",
            warnings=round0.warnings,
            round1=round1,
            round2=round2,
            round3=round3,
            final_answer=final_response.content,
            final_answer_cost=final_response.usage_cost,
            counterfactual_triggered=round3.triggered,
            counterfactual=round3.counterfactual,
            seats=seats,
        )
