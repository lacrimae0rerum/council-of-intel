"""Background session execution and cancellation manager."""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal, Protocol

from council_of_intel.storage.models import SeatRecord, SessionRecord
from council_of_intel.storage.sessions import SessionStore
from council_of_intel.validation import SeatConfig


@dataclass(frozen=True, slots=True)
class SessionExecutionRequest:
    """Execution context passed to the session runner."""

    session_id: str
    query: str
    mode: Literal["sats", "council"]
    seats: list[SeatConfig]
    chairman_personality: str
    store: SessionStore


class SessionRunner(Protocol):
    """Protocol for background protocol execution."""

    async def run(self, request: SessionExecutionRequest) -> None: ...


class NoopSessionRunner:
    """Default runner placeholder until API is wired to full protocol in later integration."""

    async def run(self, request: SessionExecutionRequest) -> None:
        now = datetime.now(UTC)
        request.store.save(
            SessionRecord(
                session_id=request.session_id,
                query=request.query,
                mode=request.mode,
                status="completed",
                created_at=now,
                updated_at=now,
                current_round=4,
                cost_eur=0.0,
                final_markdown="# Stage Final: Council Answer\n\nPendiente de runner real.",
            )
        )


class SessionManager:
    """Own in-process background tasks and cooperative cancellation."""

    def __init__(self, store: SessionStore, runner: SessionRunner) -> None:
        self._store = store
        self._runner = runner
        self._tasks: dict[str, asyncio.Task[None]] = {}

    def create(
        self,
        query: str,
        mode: Literal["sats", "council"],
        seats: list[SeatConfig],
        chairman_personality: str,
    ) -> str:
        """Create a pending session and schedule background execution."""
        session_id = uuid.uuid4().hex
        now = datetime.now(UTC)
        self._store.save(
            SessionRecord(
                session_id=session_id,
                query=query,
                mode=mode,
                status="pending",
                created_at=now,
                updated_at=now,
                current_round=0,
                seats=[],
            )
        )
        request = SessionExecutionRequest(
            session_id=session_id,
            query=query,
            mode=mode,
            seats=seats,
            chairman_personality=chairman_personality,
            store=self._store,
        )
        self._tasks[session_id] = asyncio.create_task(self._runner.run(request))
        return session_id

    async def cancel(self, session_id: str) -> SessionRecord:
        """Cancel a running task, idempotently returning the persisted session."""
        current = self._store.load(session_id)
        if current.status in {"completed", "cancelled_by_user", "aborted_insufficient_seats"}:
            return current

        task = self._tasks.get(session_id)
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        latest = self._store.load(session_id)
        if latest.status != "cancelled_by_user":
            now = datetime.now(UTC)
            latest = _cancelled_record(latest, now)
            self._store.save(latest)
        return latest


def _cancelled_record(record: SessionRecord, now: datetime) -> SessionRecord:
    seats = [
        seat
        if seat.state in {"completed", "failed"}
        else SeatRecord(
            seat_idx=seat.seat_idx,
            personality_id=seat.personality_id,
            model=seat.model,
            state="failed",
            error="cancelled_by_user",
        )
        for seat in record.seats
    ]
    return record.model_copy(
        update={
            "status": "cancelled_by_user",
            "updated_at": now,
            "seats": seats,
            "logs": [*record.logs, {"event": "cancelled_by_user"}],
        }
    )
