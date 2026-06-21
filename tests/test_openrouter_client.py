import asyncio
import json

import httpx
import pytest

from council_of_intel.config import OpenRouterConfig
from council_of_intel.openrouter.client import (
    ChatCompletionRequest,
    ChatMessage,
    OpenRouterClient,
    run_seat_completions,
)


def _config(retry_attempts: int = 1) -> OpenRouterConfig:
    return OpenRouterConfig(
        api_key_env="OPENROUTER_API_KEY",
        base_url="https://openrouter.ai/api/v1",
        timeout_seconds=10,
        retry_attempts=retry_attempts,
        retry_backoff_base_seconds=2,
    )


def _request(seat_idx: int, model: str = "openai/gpt-5.5") -> ChatCompletionRequest:
    return ChatCompletionRequest(
        seat_idx=seat_idx,
        model=model,
        messages=[ChatMessage(role="user", content=f"query {seat_idx}")],
    )


def _completion_response(content: str = "respuesta", cost: float = 0.42) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "gen-test",
            "choices": [{"message": {"role": "assistant", "content": content}}],
            "model": "openai/gpt-5.5",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15,
                "cost": cost,
            },
        },
    )


@pytest.mark.asyncio
async def test_complete_chat_posts_openrouter_payload_and_reads_usage_cost(monkeypatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    seen_payloads: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_payloads.append(json.loads(request.content))
        assert request.headers["Authorization"] == "Bearer test-key"
        assert request.url.path == "/api/v1/chat/completions"
        return _completion_response(content="final", cost=0.31)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://openrouter.ai/api/v1",
    ) as http_client:
        client = OpenRouterClient(
            _config(),
            http_client=http_client,
            sleep=lambda _: asyncio.sleep(0),
        )
        result = await client.complete_chat(_request(2))

    assert seen_payloads == [
        {
            "model": "openai/gpt-5.5",
            "messages": [{"role": "user", "content": "query 2"}],
            "stream": False,
        }
    ]
    assert result.seat_idx == 2
    assert result.content == "final"
    assert result.usage_cost == 0.31


@pytest.mark.asyncio
async def test_complete_chat_retries_http_failures_once(monkeypatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(503, json={"error": {"message": "upstream down"}})
        return _completion_response(content="after retry")

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://openrouter.ai/api/v1",
    ) as http_client:
        client = OpenRouterClient(
            _config(retry_attempts=1),
            http_client=http_client,
            sleep=lambda _: asyncio.sleep(0),
        )
        result = await client.complete_chat(_request(0))

    assert calls == 2
    assert result.content == "after retry"


@pytest.mark.asyncio
async def test_complete_chat_propagates_cancelled_error(monkeypatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        raise asyncio.CancelledError

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://openrouter.ai/api/v1",
    ) as http_client:
        client = OpenRouterClient(
            _config(),
            http_client=http_client,
            sleep=lambda _: asyncio.sleep(0),
        )
        with pytest.raises(asyncio.CancelledError):
            await client.complete_chat(_request(0))


@pytest.mark.asyncio
async def test_run_seat_completions_continues_when_one_of_four_fails(monkeypatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        if payload["messages"][0]["content"] == "query 3":
            return httpx.Response(500, json={"error": {"message": "boom"}})
        return _completion_response(content=payload["messages"][0]["content"])

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://openrouter.ai/api/v1",
    ) as http_client:
        client = OpenRouterClient(
            _config(retry_attempts=0),
            http_client=http_client,
            sleep=lambda _: asyncio.sleep(0),
        )
        result = await run_seat_completions(
            client,
            [_request(0), _request(1), _request(2), _request(3)],
            min_survivors=3,
        )

    assert result.status == "completed"
    assert len(result.completed) == 3
    assert [failure.seat_idx for failure in result.failed] == [3]


@pytest.mark.asyncio
async def test_run_seat_completions_aborts_when_fewer_than_three_survive(monkeypatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        seat_idx = int(payload["messages"][0]["content"].split()[-1])
        if seat_idx < 5:
            return httpx.Response(500, json={"error": {"message": "boom"}})
        return _completion_response(content=f"ok {seat_idx}")

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://openrouter.ai/api/v1",
    ) as http_client:
        client = OpenRouterClient(
            _config(retry_attempts=0),
            http_client=http_client,
            sleep=lambda _: asyncio.sleep(0),
        )
        result = await run_seat_completions(
            client,
            [_request(index) for index in range(7)],
            min_survivors=3,
        )

    assert result.status == "aborted_insufficient_seats"
    assert len(result.completed) == 2
    assert len(result.failed) == 5
