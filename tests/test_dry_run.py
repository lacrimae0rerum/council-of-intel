import json
import shutil
import uuid
from pathlib import Path

import httpx
import pytest

from council_of_intel.api.dry_run import CachedOpenRouterModelProvider


@pytest.fixture
def runtime_dir() -> Path:
    path = Path("test-artifacts") / f"dry-run-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.mark.asyncio
async def test_openrouter_models_provider_caches_for_subsequent_calls(runtime_dir: Path) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert request.url.path == "/api/v1/models"
        return httpx.Response(
            200,
            json={"data": [{"id": "openai/gpt-5.5"}, {"id": "anthropic/claude-sonnet-4.6"}]},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://openrouter.ai/api/v1",
    ) as client:
        provider = CachedOpenRouterModelProvider(
            base_url="https://openrouter.ai/api/v1",
            cache_path=runtime_dir / "models.json",
            client=client,
        )
        first = await provider.list_model_ids()
        second = await provider.list_model_ids()

    assert first == ["openai/gpt-5.5", "anthropic/claude-sonnet-4.6"]
    assert second == first
    assert calls == 1
    cache_payload = json.loads((runtime_dir / "models.json").read_text(encoding="utf-8"))
    assert cache_payload["models"] == first


@pytest.mark.asyncio
async def test_openrouter_models_provider_no_cache_forces_reload(runtime_dir: Path) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json={"data": [{"id": f"model/{calls}"}]})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://openrouter.ai/api/v1",
    ) as client:
        provider = CachedOpenRouterModelProvider(
            base_url="https://openrouter.ai/api/v1",
            cache_path=runtime_dir / "models.json",
            client=client,
        )
        await provider.list_model_ids()
        reloaded = await provider.list_model_ids(no_cache=True)

    assert reloaded == ["model/2"]
    assert calls == 2
