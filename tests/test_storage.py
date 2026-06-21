import json
import shutil
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from council_of_intel.errors import CouncilValidationError
from council_of_intel.storage.models import FailedSeatRecord, SeatRecord, SessionRecord
from council_of_intel.storage.sessions import SessionStore


@pytest.fixture
def runtime_dir() -> Path:
    path = Path("test-artifacts") / f"storage-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


def _session(
    session_id: str,
    query: str = "atribucion intrusion",
    status: str = "completed",
    created_at: datetime | None = None,
) -> SessionRecord:
    now = created_at or datetime(2026, 5, 7, 12, 0, tzinfo=UTC)
    return SessionRecord(
        session_id=session_id,
        query=query,
        mode="sats",
        status=status,
        created_at=now,
        updated_at=now + timedelta(seconds=30),
        current_round=4,
        cost_eur=0.42,
        final_markdown="# Stage Final: Council Answer",
        seats=[
            SeatRecord(
                seat_idx=0,
                personality_id="ach-analyst",
                model="anthropic/claude-sonnet-4.6",
                state="completed",
            ),
            SeatRecord(
                seat_idx=1,
                personality_id="red-team",
                model="x-ai/grok-4.3",
                state="completed",
            ),
            SeatRecord(
                seat_idx=2,
                personality_id="devils-advocate",
                model="openai/gpt-chat-latest",
                state="completed",
            ),
        ],
        failed_seats=[
            FailedSeatRecord(
                seat_idx=3,
                personality_id="quality-of-info-auditor",
                reason="timeout",
            )
        ],
        rounds={"round1": {"seat0": "raw"}},
        logs=[{"event": "session_completed"}],
    )


def test_session_store_saves_json_and_loads_roundtrip(runtime_dir: Path) -> None:
    store = SessionStore(runtime_dir / "sessions", runtime_dir / "index.sqlite3")
    record = _session("01HZROUNDTRIP")

    store.save(record)
    loaded = store.load("01HZROUNDTRIP")

    assert loaded == record
    payload = json.loads((runtime_dir / "sessions" / "01HZROUNDTRIP.json").read_text())
    assert payload["status"] == "completed"
    assert payload["cost_eur"] == 0.42


def test_session_store_indexes_and_lists_latest_first(runtime_dir: Path) -> None:
    store = SessionStore(runtime_dir / "sessions", runtime_dir / "index.sqlite3")
    older = _session("older", created_at=datetime(2026, 5, 7, 10, 0, tzinfo=UTC))
    newer = _session("newer", created_at=datetime(2026, 5, 7, 11, 0, tzinfo=UTC))

    store.save(older)
    store.save(newer)

    summaries = store.list_sessions()
    assert [summary.session_id for summary in summaries] == ["newer", "older"]
    assert summaries[0].status == "completed"
    assert summaries[0].cost_eur == 0.42


def test_session_store_filters_by_status_and_search(runtime_dir: Path) -> None:
    store = SessionStore(runtime_dir / "sessions", runtime_dir / "index.sqlite3")
    store.save(_session("one", query="atribucion intrusion", status="completed"))
    store.save(_session("two", query="warning ransomware", status="cancelled_by_user"))

    by_status = store.list_sessions(status="cancelled_by_user")
    by_search = store.list_sessions(search="intrusion")

    assert [summary.session_id for summary in by_status] == ["two"]
    assert [summary.session_id for summary in by_search] == ["one"]


def test_session_store_persists_index_across_instances(runtime_dir: Path) -> None:
    sessions_dir = runtime_dir / "sessions"
    index_path = runtime_dir / "index.sqlite3"
    SessionStore(sessions_dir, index_path).save(_session("persisted"))

    reopened = SessionStore(sessions_dir, index_path)

    assert [summary.session_id for summary in reopened.list_sessions()] == ["persisted"]


def test_session_store_load_missing_raises_structured_error(runtime_dir: Path) -> None:
    store = SessionStore(runtime_dir / "sessions", runtime_dir / "index.sqlite3")

    with pytest.raises(CouncilValidationError) as exc_info:
        store.load("missing")

    assert exc_info.value.error_code == "SESSION_NOT_FOUND"


def test_session_record_rejects_invalid_status() -> None:
    with pytest.raises(ValueError):
        _session("bad", status="done")
