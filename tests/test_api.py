import asyncio
import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from council_of_intel.api.app import create_app
from council_of_intel.api.manager import SessionExecutionRequest
from council_of_intel.config import load_config
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.storage.models import SeatRecord, SessionRecord
from council_of_intel.storage.sessions import SessionStore


class CancellableRunner:
    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.cancelled = asyncio.Event()

    async def run(self, request: SessionExecutionRequest) -> None:
        now = datetime.now(UTC)
        request.store.save(
            SessionRecord(
                session_id=request.session_id,
                query=request.query,
                mode=request.mode,
                status="running",
                created_at=now,
                updated_at=now,
                current_round=1,
                cost_eur=0.21,
                seats=[
                    SeatRecord(
                        seat_idx=index,
                        personality_id=seat.personality_id,
                        model=seat.model,
                        state="completed" if index == 0 else "running",
                    )
                    for index, seat in enumerate(request.seats)
                ],
                rounds={"round1": {"completed": [0]}},
                logs=[{"event": "round1_partial"}],
            )
        )
        self.started.set()
        try:
            await asyncio.sleep(3600)
        except asyncio.CancelledError:
            self.cancelled.set()
            request.store.save(
                SessionRecord(
                    session_id=request.session_id,
                    query=request.query,
                    mode=request.mode,
                    status="cancelled_by_user",
                    created_at=now,
                    updated_at=datetime.now(UTC),
                    current_round=1,
                    cost_eur=0.21,
                    seats=[
                        SeatRecord(
                            seat_idx=0,
                            personality_id=request.seats[0].personality_id,
                            model=request.seats[0].model,
                            state="completed",
                        )
                    ],
                    rounds={"round1": {"completed": [0]}},
                    logs=[{"event": "cancelled_by_user"}],
                )
            )
            raise


class StaticModelProvider:
    def __init__(self, model_ids: list[str]) -> None:
        self._model_ids = model_ids

    async def list_model_ids(self, no_cache: bool = False) -> list[str]:
        return self._model_ids


class NonCooperativeRunner:
    def __init__(self) -> None:
        self.started = asyncio.Event()

    async def run(self, request: SessionExecutionRequest) -> None:
        now = datetime.now(UTC)
        request.store.save(
            SessionRecord(
                session_id=request.session_id,
                query=request.query,
                mode=request.mode,
                status="running",
                created_at=now,
                updated_at=now,
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
            )
        )
        self.started.set()
        await asyncio.sleep(3600)


@pytest.fixture
def runtime_dir() -> Path:
    path = Path("test-artifacts") / f"api-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def app_context(runtime_dir: Path):
    config = load_config()
    catalog = load_personalities()
    store = SessionStore(runtime_dir / "sessions", runtime_dir / "index.sqlite3")
    runner = CancellableRunner()
    app = create_app(
        config=config,
        catalog=catalog,
        store=store,
        runner=runner,
        model_provider=StaticModelProvider(config.allowed_models),
    )
    return app, runner


def _payload() -> dict:
    return {
        "query": "Evalua esta intrusión",
        "mode": "sats",
        "chairman_personality": "mclaughlin",
        "seats": [
            {"personality_id": "ach-analyst", "model": "openai/gpt-5.5"},
            {"personality_id": "red-team", "model": "anthropic/claude-sonnet-4.6"},
            {
                "personality_id": "devils-advocate",
                "model": "google/gemini-3.1-pro-preview",
            },
        ],
    }


@pytest.mark.asyncio
async def test_sessions_lifecycle_cancel_and_status(app_context) -> None:
    app, runner = app_context
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        created = await client.post("/sessions", json=_payload())
        assert created.status_code == 202
        session_id = created.json()["session_id"]

        await asyncio.wait_for(runner.started.wait(), timeout=2)
        status = await client.get(f"/sessions/{session_id}/status")
        assert status.json()["status"] == "running"
        assert status.json()["cost_so_far_eur"] == 0.21

        cancelled = await client.post(f"/sessions/{session_id}/cancel")
        assert cancelled.status_code == 200
        assert cancelled.json()["status"] == "cancelled_by_user"
        assert cancelled.json()["cost_eur"] == 0.21
        assert runner.cancelled.is_set()


@pytest.mark.asyncio
async def test_cancel_marks_non_terminal_seats_failed(runtime_dir: Path) -> None:
    config = load_config()
    runner = NonCooperativeRunner()
    app = create_app(
        config=config,
        catalog=load_personalities(),
        store=SessionStore(runtime_dir / "sessions", runtime_dir / "index.sqlite3"),
        runner=runner,
        model_provider=StaticModelProvider(config.allowed_models),
    )
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        created = await client.post("/sessions", json=_payload())
        session_id = created.json()["session_id"]
        await asyncio.wait_for(runner.started.wait(), timeout=2)

        cancelled = await client.post(f"/sessions/{session_id}/cancel")
        status = await client.get(f"/sessions/{session_id}/status")

    assert cancelled.json()["status"] == "cancelled_by_user"
    assert status.json()["status"] == "cancelled_by_user"
    assert {seat["state"] for seat in status.json()["seats_progress"]} == {"failed"}
    assert {seat["error"] for seat in status.json()["seats_progress"]} == {"cancelled_by_user"}


@pytest.mark.asyncio
async def test_core_catalog_config_and_export_endpoints(app_context) -> None:
    app, _runner = app_context
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        health = await client.get("/health")
        modes = await client.get("/modes")
        personalities = await client.get("/personalities")
        config = await client.get("/config")

    assert health.json() == {"status": "ok"}
    assert modes.json()["modes"] == ["sats", "council"]
    assert len(personalities.json()["personalities"]) == 17
    assert "allowed_models" in config.json()


@pytest.mark.asyncio
async def test_dry_run_invalid_model_returns_did_you_mean(app_context) -> None:
    app, _runner = app_context
    payload = _payload()
    payload["seats"][0]["model"] = "openai/gpt-9"
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/sessions/dry-run", json=payload)

    body = response.json()
    assert response.status_code == 200
    assert body["valid"] is False
    assert body["errors"][0]["error_code"] == "MODEL_NOT_FOUND"
    assert "openai/gpt-5.5" in body["errors"][0]["context"]["did_you_mean"]


@pytest.mark.asyncio
async def test_openapi_contains_expected_paths(app_context) -> None:
    app, _runner = app_context
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        openapi = (await client.get("/openapi.json")).json()

    assert "/sessions/{session_id}/cancel" in openapi["paths"]
    assert "/sessions/dry-run" in openapi["paths"]
    assert "/health" in openapi["paths"]
