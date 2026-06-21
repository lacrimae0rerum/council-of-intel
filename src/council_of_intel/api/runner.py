"""Real protocol-backed API session runner."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from council_of_intel.api.manager import SessionExecutionRequest
from council_of_intel.config import AppConfig
from council_of_intel.openrouter.client import OpenRouterClient
from council_of_intel.personalities.schema import Personality
from council_of_intel.protocol.engine import DeliberationProtocol
from council_of_intel.storage.models import FailedSeatRecord, SeatRecord, SessionRecord


class ProtocolSessionRunner:
    """Run the deliberation protocol and persist a full SessionRecord."""

    def __init__(
        self,
        config: AppConfig,
        catalog: dict[str, Personality],
        client: OpenRouterClient,
    ) -> None:
        self._config = config
        self._catalog = catalog
        self._client = client

    async def run(self, request: SessionExecutionRequest) -> None:
        """Execute the protocol once and persist terminal state."""
        started_at = datetime.now(UTC)
        request.store.save(
            SessionRecord(
                session_id=request.session_id,
                query=request.query,
                mode=request.mode,
                status="running",
                created_at=started_at,
                updated_at=started_at,
                current_round=1,
                seats=[
                    SeatRecord(
                        seat_idx=index,
                        personality_id=seat.personality_id,
                        model=seat.model,
                        state="running",
                    )
                    for index, seat in enumerate(request.seats)
                ],
                logs=[{"event": "session_started"}],
            )
        )
        try:
            result = await DeliberationProtocol(
                self._config,
                self._catalog,
                self._client,
            ).run(
                query=request.query,
                mode=request.mode,
                seats=request.seats,
                chairman_personality_id=request.chairman_personality,
            )
        except asyncio.CancelledError:
            raise

        completed = result.round1.completed if result.round1 else []
        failed = result.round1.failed if result.round1 else []
        total_cost = sum(response.usage_cost for response in completed)
        if result.round2:
            total_cost += sum(evaluation.usage_cost for evaluation in result.round2.evaluations)
        if result.round3:
            total_cost += result.round3.usage_cost
        total_cost += result.final_answer_cost

        now = datetime.now(UTC)
        request.store.save(
            SessionRecord(
                session_id=request.session_id,
                query=request.query,
                mode=request.mode,
                status=result.status,
                created_at=started_at,
                updated_at=now,
                current_round=4 if result.status == "completed" else 1,
                cost_eur=round(total_cost, 4),
                final_markdown=result.final_answer,
                seats=[
                    SeatRecord(
                        seat_idx=index,
                        personality_id=seat.personality_id,
                        model=seat.model,
                        state="completed",
                    )
                    for index, seat in enumerate(request.seats)
                    if any(response.seat_idx == index for response in completed)
                ],
                failed_seats=[
                    FailedSeatRecord(
                        seat_idx=failure.seat_idx,
                        personality_id=request.seats[failure.seat_idx].personality_id,
                        model=failure.model,
                        reason=failure.message,
                    )
                    for failure in failed
                ],
                rounds={
                    "round1": [response.content for response in completed],
                    "round2": [
                        evaluation.content
                        for evaluation in (result.round2.evaluations if result.round2 else [])
                    ],
                    "round3": result.counterfactual,
                },
                logs=[{"event": "session_completed", "status": result.status}],
            )
        )
