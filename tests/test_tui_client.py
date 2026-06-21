import json

import httpx
import pytest

from council_of_intel.tui.client import TuiApiClient


@pytest.mark.asyncio
async def test_tui_client_creates_session_and_polls_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/sessions" and request.method == "POST":
            payload = json.loads(request.content)
            assert payload["mode"] == "sats"
            return httpx.Response(202, json={"session_id": "sid-1", "status": "pending"})
        if request.url.path == "/sessions/sid-1/status":
            return httpx.Response(200, json={"session_id": "sid-1", "status": "running"})
        return httpx.Response(404)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://test",
    ) as http_client:
        client = TuiApiClient("http://test", http_client=http_client)
        created = await client.create_session(
            query="Evalua esto",
            mode="sats",
            chairman_personality="mclaughlin",
            seats=[
                {"personality_id": "ach-analyst", "model": "openai/gpt-5.5"},
                {"personality_id": "red-team", "model": "anthropic/claude-sonnet-4.6"},
                {
                    "personality_id": "devils-advocate",
                    "model": "google/gemini-3.1-pro-preview",
                },
            ],
        )
        status = await client.get_status("sid-1")

    assert created["session_id"] == "sid-1"
    assert status["status"] == "running"


@pytest.mark.asyncio
async def test_tui_client_cancel_and_export_markdown() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/sessions/sid-1/cancel":
            return httpx.Response(200, json={"session_id": "sid-1", "status": "cancelled_by_user"})
        if request.url.path == "/sessions/sid-1/export-md":
            return httpx.Response(200, text="# Stage Final: Council Answer")
        return httpx.Response(404)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://test",
    ) as http_client:
        client = TuiApiClient("http://test", http_client=http_client)
        cancelled = await client.cancel_session("sid-1")
        markdown = await client.export_markdown("sid-1")

    assert cancelled["status"] == "cancelled_by_user"
    assert markdown == "# Stage Final: Council Answer"


@pytest.mark.asyncio
async def test_tui_client_lists_personalities() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/personalities":
            return httpx.Response(
                200,
                json={
                    "personalities": [
                        {
                            "id": "ach-analyst",
                            "recommended_model": "anthropic/claude-sonnet-4.6",
                        }
                    ]
                },
            )
        return httpx.Response(404)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://test",
    ) as http_client:
        client = TuiApiClient("http://test", http_client=http_client)
        personalities = await client.list_personalities()

    assert personalities == [
        {"id": "ach-analyst", "recommended_model": "anthropic/claude-sonnet-4.6"}
    ]
