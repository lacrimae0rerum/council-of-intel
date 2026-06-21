"""FastAPI application factory."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

from council_of_intel.api.dry_run import (
    CachedOpenRouterModelProvider,
    ModelProvider,
    run_dry_run,
)
from council_of_intel.api.manager import NoopSessionRunner, SessionManager, SessionRunner
from council_of_intel.api.schemas import SessionCreateRequest, SessionCreateResponse
from council_of_intel.config import AppConfig
from council_of_intel.personalities.schema import Personality
from council_of_intel.storage.models import SessionRecord
from council_of_intel.storage.sessions import SessionStore
from council_of_intel.validation import validate_session_request


def create_app(
    config: AppConfig,
    catalog: dict[str, Personality],
    store: SessionStore,
    runner: SessionRunner | None = None,
    model_provider: ModelProvider | None = None,
) -> FastAPI:
    """Create the local FastAPI app with explicit dependencies."""
    app = FastAPI(title="council-of-intel", version="0.1.0")
    manager = SessionManager(store, runner or NoopSessionRunner())
    provider = model_provider or CachedOpenRouterModelProvider(str(config.openrouter.base_url))

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/sessions", response_model=SessionCreateResponse, status_code=202)
    async def create_session(payload: SessionCreateRequest) -> SessionCreateResponse:
        try:
            validate_session_request(
                payload.mode,
                payload.seats,
                payload.chairman_personality,
                config,
                catalog,
            )
        except ValueError as exc:
            raise _http_validation_error(exc) from exc

        session_id = manager.create(
            query=payload.query,
            mode=payload.mode,
            seats=payload.seats,
            chairman_personality=payload.chairman_personality,
        )
        return SessionCreateResponse(session_id=session_id, status="pending")

    @app.get("/sessions")
    async def list_sessions(
        status: str | None = Query(default=None),
        search: str | None = Query(default=None),
    ) -> dict[str, Any]:
        return {
            "sessions": [
                summary.model_dump(mode="json")
                for summary in store.list_sessions(status=status, search=search)
            ]
        }

    @app.get("/sessions/{session_id}")
    async def get_session(session_id: str) -> dict[str, Any]:
        return _load_or_404(store, session_id).model_dump(mode="json")

    @app.get("/sessions/{session_id}/status")
    async def get_session_status(session_id: str) -> dict[str, Any]:
        record = _load_or_404(store, session_id)
        return _status_payload(record)

    @app.post("/sessions/{session_id}/cancel")
    async def cancel_session(session_id: str) -> dict[str, Any]:
        try:
            record = await manager.cancel(session_id)
        except ValueError as exc:
            raise _http_validation_error(exc) from exc
        return record.model_dump(mode="json")

    @app.get("/sessions/{session_id}/export-md", response_class=PlainTextResponse)
    async def export_markdown(session_id: str) -> str:
        record = _load_or_404(store, session_id)
        return record.final_markdown or ""

    @app.get("/sessions/{session_id}/logs")
    async def get_logs(session_id: str) -> dict[str, Any]:
        record = _load_or_404(store, session_id)
        return {"logs": record.logs}

    @app.get("/personalities")
    async def personalities() -> dict[str, Any]:
        return {
            "personalities": [
                personality.model_dump(
                    include={
                        "id",
                        "name",
                        "family",
                        "polarity",
                        "recommended_model",
                        "sat_layer",
                        "can_be_chairman",
                        "description",
                    }
                )
                for personality in catalog.values()
            ]
        }

    @app.get("/modes")
    async def modes() -> dict[str, list[str]]:
        return {"modes": ["sats", "council"]}

    @app.get("/config")
    async def effective_config() -> dict[str, Any]:
        return config.model_dump(mode="json")

    @app.post("/sessions/dry-run")
    async def dry_run(payload: SessionCreateRequest | None = None, no_cache: bool = False) -> dict:
        if payload is None:
            return await run_dry_run(config, catalog, provider, no_cache=no_cache)
        return await run_dry_run(
            config,
            catalog,
            provider,
            mode=payload.mode,
            seats=payload.seats,
            chairman_personality=payload.chairman_personality,
            no_cache=no_cache,
        )

    return app


def _load_or_404(store: SessionStore, session_id: str) -> SessionRecord:
    try:
        return store.load(session_id)
    except ValueError as exc:
        raise _http_validation_error(exc, status_code=404) from exc


def _http_validation_error(exc: ValueError, status_code: int = 400) -> HTTPException:
    detail = exc.to_payload() if hasattr(exc, "to_payload") else {"message_human": str(exc)}
    return HTTPException(status_code=status_code, detail=detail)


def _status_payload(record: SessionRecord) -> dict[str, Any]:
    now = datetime.now(UTC)
    elapsed = max(0, int((now - record.created_at).total_seconds()))
    completed_rounds = list(range(record.current_round or 0))
    return {
        "session_id": record.session_id,
        "status": record.status,
        "current_round": record.current_round,
        "rounds_completed": completed_rounds,
        "seats_progress": [
            {
                "seat_idx": seat.seat_idx,
                "personality": seat.personality_id,
                "state": seat.state,
                **({"error": seat.error} if seat.error else {}),
            }
            for seat in record.seats
        ],
        "cost_so_far_eur": record.cost_eur,
        "elapsed_seconds": elapsed,
        "last_event_ts": record.updated_at.isoformat(),
    }
