"""Async REST client used by the Textual TUI."""

from __future__ import annotations

import httpx


class TuiApiClient:
    """Small API client for local backend endpoints."""

    def __init__(self, base_url: str, http_client: httpx.AsyncClient | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = http_client or httpx.AsyncClient(base_url=self.base_url, timeout=30)
        self._owns_client = http_client is None

    async def close(self) -> None:
        """Close owned HTTP resources."""
        if self._owns_client:
            await self._client.aclose()

    async def create_session(
        self,
        query: str,
        mode: str,
        chairman_personality: str,
        seats: list[dict],
    ) -> dict:
        """Create a one-shot session."""
        response = await self._client.post(
            "/sessions",
            json={
                "query": query,
                "mode": mode,
                "chairman_personality": chairman_personality,
                "seats": seats,
            },
        )
        response.raise_for_status()
        return response.json()

    async def get_status(self, session_id: str) -> dict:
        """Fetch lightweight session status."""
        response = await self._client.get(f"/sessions/{session_id}/status")
        response.raise_for_status()
        return response.json()

    async def get_session(self, session_id: str) -> dict:
        """Fetch full session record."""
        response = await self._client.get(f"/sessions/{session_id}")
        response.raise_for_status()
        return response.json()

    async def list_sessions(self) -> list[dict]:
        """List previous sessions."""
        response = await self._client.get("/sessions")
        response.raise_for_status()
        return response.json()["sessions"]

    async def list_personalities(self) -> list[dict]:
        """List available personalities."""
        response = await self._client.get("/personalities")
        response.raise_for_status()
        return response.json()["personalities"]

    async def cancel_session(self, session_id: str) -> dict:
        """Cancel a running session."""
        response = await self._client.post(f"/sessions/{session_id}/cancel")
        response.raise_for_status()
        return response.json()

    async def export_markdown(self, session_id: str) -> str:
        """Fetch Markdown export."""
        response = await self._client.get(f"/sessions/{session_id}/export-md")
        response.raise_for_status()
        return response.text

    async def get_logs(self, session_id: str) -> list[dict]:
        """Fetch structured session logs."""
        response = await self._client.get(f"/sessions/{session_id}/logs")
        response.raise_for_status()
        return response.json()["logs"]
