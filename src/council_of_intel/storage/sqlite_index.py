"""SQLite index for persisted session files."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

from council_of_intel.storage.models import (
    SessionRecord,
    SessionStatus,
    SessionSummary,
)


class SQLiteSessionIndex:
    """Small SQLite index for session listing and search."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def upsert(self, record: SessionRecord) -> None:
        """Insert or update one session summary row."""
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    """
                    insert into sessions (
                        session_id, query, mode, status, created_at, updated_at, cost_eur,
                        current_round
                    )
                    values (?, ?, ?, ?, ?, ?, ?, ?)
                    on conflict(session_id) do update set
                        query=excluded.query,
                        mode=excluded.mode,
                        status=excluded.status,
                        created_at=excluded.created_at,
                        updated_at=excluded.updated_at,
                        cost_eur=excluded.cost_eur,
                        current_round=excluded.current_round
                    """,
                    (
                        record.session_id,
                        record.query,
                        record.mode,
                        record.status,
                        record.created_at.isoformat(),
                        record.updated_at.isoformat(),
                        record.cost_eur,
                        record.current_round,
                    ),
                )

    def list_sessions(
        self,
        status: SessionStatus | None = None,
        search: str | None = None,
        limit: int = 100,
    ) -> list[SessionSummary]:
        """List indexed sessions, newest first."""
        clauses: list[str] = []
        params: list[object] = []
        if status is not None:
            clauses.append("status = ?")
            params.append(status)
        if search:
            clauses.append("query like ?")
            params.append(f"%{search}%")

        where = f"where {' and '.join(clauses)}" if clauses else ""
        params.append(limit)
        with closing(self._connect()) as connection:
            rows = connection.execute(
                f"""
                select
                    session_id, query, mode, status, created_at, updated_at, cost_eur,
                    current_round
                from sessions
                {where}
                order by created_at desc
                limit ?
                """,
                params,
            ).fetchall()

        return [
            SessionSummary(
                session_id=row["session_id"],
                query=row["query"],
                mode=row["mode"],
                status=row["status"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                cost_eur=row["cost_eur"],
                current_round=row["current_round"],
            )
            for row in rows
        ]

    def _ensure_schema(self) -> None:
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    """
                    create table if not exists sessions (
                        session_id text primary key,
                        query text not null,
                        mode text not null,
                        status text not null,
                        created_at text not null,
                        updated_at text not null,
                        cost_eur real not null,
                        current_round integer
                    )
                    """
                )
                connection.execute(
                    "create index if not exists idx_sessions_created_at "
                    "on sessions(created_at desc)"
                )
                connection.execute(
                    "create index if not exists idx_sessions_status on sessions(status)"
                )
                connection.execute(
                    "create index if not exists idx_sessions_query on sessions(query)"
                )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection
