"""Async OpenRouter client and seat failure policy."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field

from council_of_intel.config import OpenRouterConfig
from council_of_intel.errors import CouncilValidationError

SleepCallable = Callable[[float], Awaitable[None]]


class ChatMessage(BaseModel):
    """OpenRouter chat message."""

    model_config = ConfigDict(extra="forbid")

    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    """Seat-specific chat completion request."""

    model_config = ConfigDict(extra="forbid")

    seat_idx: int = Field(ge=0)
    model: str
    messages: list[ChatMessage] = Field(min_length=1)
    temperature: float | None = Field(default=None, ge=0, le=2)
    max_tokens: int | None = Field(default=None, gt=0)


@dataclass(frozen=True, slots=True)
class ChatCompletionResult:
    """Successful seat completion."""

    seat_idx: int
    model: str
    content: str
    usage_cost: float
    raw_response: dict


@dataclass(frozen=True, slots=True)
class SeatFailure:
    """Seat failure after retries are exhausted."""

    seat_idx: int
    model: str
    error_code: str
    message: str


@dataclass(frozen=True, slots=True)
class BatchCompletionResult:
    """Batch result for parallel seat completions."""

    status: Literal["completed", "aborted_insufficient_seats"]
    completed: list[ChatCompletionResult] = field(default_factory=list)
    failed: list[SeatFailure] = field(default_factory=list)


class OpenRouterRequestError(RuntimeError):
    """OpenRouter call failed after retry policy."""

    def __init__(self, seat_idx: int, model: str, message: str) -> None:
        super().__init__(message)
        self.seat_idx = seat_idx
        self.model = model


class OpenRouterClient:
    """Small async client for OpenRouter chat completions."""

    def __init__(
        self,
        config: OpenRouterConfig,
        http_client: httpx.AsyncClient | None = None,
        sleep: SleepCallable = asyncio.sleep,
    ) -> None:
        self._config = config
        self._http_client = http_client
        self._sleep = sleep

    async def complete_chat(self, request: ChatCompletionRequest) -> ChatCompletionResult:
        """Run one non-streaming chat completion with configured retry policy."""
        last_error: OpenRouterRequestError | None = None
        for attempt in range(self._config.retry_attempts + 1):
            try:
                return await self._post_chat_completion(request)
            except asyncio.CancelledError:
                raise
            except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError) as exc:
                last_error = OpenRouterRequestError(
                    seat_idx=request.seat_idx,
                    model=request.model,
                    message=str(exc),
                )
                if attempt >= self._config.retry_attempts:
                    raise last_error from exc
                await self._sleep(self._config.retry_backoff_base_seconds * (2**attempt))

        raise last_error or OpenRouterRequestError(
            request.seat_idx,
            request.model,
            "unknown failure",
        )

    async def _post_chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResult:
        payload = {
            "model": request.model,
            "messages": [message.model_dump() for message in request.messages],
            "stream": False,
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        client = self._http_client or httpx.AsyncClient(
            base_url=str(self._config.base_url),
            timeout=self._config.timeout_seconds,
        )
        close_client = self._http_client is None
        try:
            response = await client.post(
                "chat/completions",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            raw = response.json()
            return _parse_completion(request, raw)
        finally:
            if close_client:
                await client.aclose()

    def _headers(self) -> dict[str, str]:
        api_key = os.environ.get(self._config.api_key_env)
        if not api_key:
            raise CouncilValidationError(
                error_code="OPENROUTER_API_KEY_MISSING",
                message_human=(
                    f"No encuentro `{self._config.api_key_env}` en el entorno. "
                    "Sin key no llamo a OpenRouter."
                ),
                context={"env": self._config.api_key_env},
            )
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


async def run_seat_completions(
    client: OpenRouterClient,
    requests: list[ChatCompletionRequest],
    min_survivors: int,
) -> BatchCompletionResult:
    """Run seats concurrently and abort only if fewer than min_survivors complete."""
    raw_results = await asyncio.gather(
        *[_complete_or_fail(client, request) for request in requests]
    )

    completed = [result for result in raw_results if isinstance(result, ChatCompletionResult)]
    failed = [result for result in raw_results if isinstance(result, SeatFailure)]
    status: Literal["completed", "aborted_insufficient_seats"] = (
        "completed" if len(completed) >= min_survivors else "aborted_insufficient_seats"
    )
    return BatchCompletionResult(status=status, completed=completed, failed=failed)


async def _complete_or_fail(
    client: OpenRouterClient, request: ChatCompletionRequest
) -> ChatCompletionResult | SeatFailure:
    try:
        return await client.complete_chat(request)
    except asyncio.CancelledError:
        raise
    except OpenRouterRequestError as exc:
        return SeatFailure(
            seat_idx=exc.seat_idx,
            model=exc.model,
            error_code="OPENROUTER_REQUEST_FAILED",
            message=str(exc),
        )


def _parse_completion(
    request: ChatCompletionRequest, raw: dict
) -> ChatCompletionResult:
    try:
        content = raw["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise OpenRouterRequestError(
            request.seat_idx,
            request.model,
            "OpenRouter response missing choices[0].message.content",
        ) from exc

    usage = raw.get("usage") or {}
    cost = usage.get("cost", 0.0)
    return ChatCompletionResult(
        seat_idx=request.seat_idx,
        model=raw.get("model", request.model),
        content=str(content),
        usage_cost=float(cost or 0.0),
        raw_response=raw,
    )
