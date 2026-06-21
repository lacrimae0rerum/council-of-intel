"""JSON session persistence backed by a SQLite listing index."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from council_of_intel.errors import CouncilValidationError
from council_of_intel.storage.models import SessionRecord, SessionStatus, SessionSummary
from council_of_intel.storage.sqlite_index import SQLiteSessionIndex


class SessionStore:
    """Persist full session JSON files and maintain a SQLite index."""

    def __init__(
        self,
        sessions_dir: Path | str = "sessions",
        index_path: Path | str | None = None,
    ) -> None:
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.index = SQLiteSessionIndex(index_path or self.sessions_dir / "sessions.sqlite3")

    def save(self, record: SessionRecord) -> None:
        """Write one full session JSON file and upsert its index row."""
        path = self._session_path(record.session_id)
        payload = record.model_dump(mode="json")
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        self.index.upsert(record)

    def load(self, session_id: str) -> SessionRecord:
        """Load one persisted session by id."""
        path = self._session_path(session_id)
        if not path.exists():
            raise CouncilValidationError(
                error_code="SESSION_NOT_FOUND",
                message_human=f"No encuentro la sesión `{session_id}`.",
                context={"session_id": session_id},
            )

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return SessionRecord.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise CouncilValidationError(
                error_code="SESSION_RECORD_INVALID",
                message_human=f"La sesión `{session_id}` está corrupta o no pasa schema.",
                context={"session_id": session_id, "path": str(path)},
            ) from exc

    def list_sessions(
        self,
        status: SessionStatus | None = None,
        search: str | None = None,
        limit: int = 100,
    ) -> list[SessionSummary]:
        """Return session summaries from the SQLite index."""
        return self.index.list_sessions(status=status, search=search, limit=limit)

    def _session_path(self, session_id: str) -> Path:
        return self.sessions_dir / f"{session_id}.json"
