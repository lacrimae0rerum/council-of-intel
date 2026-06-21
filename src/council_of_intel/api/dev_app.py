"""Development ASGI app with project dependencies wired in."""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from council_of_intel.api.app import create_app
from council_of_intel.api.manager import SessionExecutionRequest
from council_of_intel.api.runner import ProtocolSessionRunner
from council_of_intel.config import load_config
from council_of_intel.logging_config import configure_logging
from council_of_intel.openrouter.client import OpenRouterClient
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.storage.models import SeatRecord, SessionRecord
from council_of_intel.storage.sessions import SessionStore

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _load_root_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_root_env()
config = load_config(PROJECT_ROOT / "config.yaml")
log_path = PROJECT_ROOT / "logs" / f"council-web-dev-{os.getpid()}.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
try:
    configure_logging(
        str(log_path),
        level=config.logging.level,
    )
except PermissionError:
    logging.basicConfig(level=config.logging.level)
catalog = load_personalities(PROJECT_ROOT / "personalities")


def _build_store() -> SessionStore:
    preferred = Path(
        os.environ.get("COUNCIL_WEB_SESSIONS_DIR", PROJECT_ROOT / "test-artifacts/web-dev-sessions")
    )
    try:
        return SessionStore(preferred, preferred / "index.sqlite3")
    except PermissionError:
        fallback = Path(tempfile.gettempdir()) / "council-of-intel-web-dev-sessions"
        return SessionStore(fallback, fallback / "index.sqlite3")


store = _build_store()


class DemoSessionRunner:
    """Fast deterministic runner for Web HITO validation."""

    async def run(self, request: SessionExecutionRequest) -> None:
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
                logs=[{"event": "demo_session_started"}],
            )
        )
        await asyncio.sleep(1.2)
        now = datetime.now(UTC)
        request.store.save(
            SessionRecord(
                session_id=request.session_id,
                query=request.query,
                mode=request.mode,
                status="running",
                created_at=started_at,
                updated_at=now,
                current_round=2,
                cost_eur=0.01,
                seats=[
                    SeatRecord(
                        seat_idx=index,
                        personality_id=seat.personality_id,
                        model=seat.model,
                        state="completed" if index == 0 else "running",
                    )
                    for index, seat in enumerate(request.seats)
                ],
                logs=[{"event": "demo_session_started"}, {"event": "demo_round1_partial"}],
            )
        )
        await asyncio.sleep(1.2)
        finished_at = datetime.now(UTC)
        request.store.save(
            SessionRecord(
                session_id=request.session_id,
                query=request.query,
                mode=request.mode,
                status="completed",
                created_at=started_at,
                updated_at=finished_at,
                current_round=4,
                cost_eur=0.02,
                final_markdown=_demo_markdown(request),
                seats=[
                    SeatRecord(
                        seat_idx=index,
                        personality_id=seat.personality_id,
                        model=seat.model,
                        state="completed",
                    )
                    for index, seat in enumerate(request.seats)
                ],
                rounds={
                    "round1": ["Demo: hipotesis A", "Demo: hipotesis B"],
                    "round2": ["Demo: cross-examination"],
                    "round3": "Demo: counterfactual controlado",
                },
                logs=[
                    {"event": "demo_session_started"},
                    {"event": "demo_round1_partial"},
                    {"event": "demo_session_completed"},
                ],
            )
        )


def _demo_markdown(request: SessionExecutionRequest) -> str:
    seats = ", ".join(seat.personality_id for seat in request.seats)
    mode = "SATs" if request.mode == "sats" else "Council"
    return (
        "# Stage Final: Council Answer\n\n"
        f"**Modo:** {mode}\n\n"
        f"**Pregunta:** {request.query}\n\n"
        "## Evaluacion\n"
        "Demo Web HITO completada: la sesion arranco, avanzo por polling y cerro con Markdown.\n\n"
        "## Conclusion\n"
        "- El flujo UI/API funciona de punta a punta.\n"
        "- Sustituye este runner por OpenRouter real para deliberacion operativa.\n\n"
        "## Dissent registrado\n"
        f"- Seats demo ejecutados: {seats}\n"
    )


runner = (
    ProtocolSessionRunner(config, catalog, OpenRouterClient(config.openrouter))
    if os.environ.get("COUNCIL_WEB_REAL_OPENROUTER") == "1"
    else DemoSessionRunner()
)

app = create_app(config=config, catalog=catalog, store=store, runner=runner)
