"""Dry-run validation with OpenRouter model catalog checks."""

from __future__ import annotations

import difflib
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Protocol

import httpx

from council_of_intel.config import AppConfig
from council_of_intel.personalities.schema import Personality
from council_of_intel.validation import SeatConfig, validate_session_request


class ModelProvider(Protocol):
    """Provider of OpenRouter model identifiers."""

    async def list_model_ids(self, no_cache: bool = False) -> list[str]: ...


class CachedOpenRouterModelProvider:
    """Fetch and cache OpenRouter `/models` ids for dry-run."""

    def __init__(
        self,
        base_url: str,
        cache_path: Path | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._cache_path = cache_path or Path.home() / ".cache" / "council-of-intel" / "models.json"
        self._client = client

    async def list_model_ids(self, no_cache: bool = False) -> list[str]:
        if not no_cache:
            cached = self._read_cache()
            if cached is not None:
                return cached

        client = self._client or httpx.AsyncClient(base_url=self._base_url, timeout=30)
        close_client = self._client is None
        try:
            response = await client.get("models")
            response.raise_for_status()
            payload = response.json()
        finally:
            if close_client:
                await client.aclose()

        model_ids = [item["id"] for item in payload.get("data", []) if "id" in item]
        self._write_cache(model_ids)
        return model_ids

    def _read_cache(self) -> list[str] | None:
        if not self._cache_path.exists():
            return None
        payload = json.loads(self._cache_path.read_text(encoding="utf-8"))
        fetched_at = datetime.fromisoformat(payload["fetched_at"])
        if datetime.now(UTC) - fetched_at > timedelta(hours=1):
            return None
        return list(payload["models"])

    def _write_cache(self, model_ids: list[str]) -> None:
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_path.write_text(
            json.dumps(
                {"fetched_at": datetime.now(UTC).isoformat(), "models": model_ids},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


async def run_dry_run(
    config: AppConfig,
    catalog: dict[str, Personality],
    model_provider: ModelProvider,
    mode: str | None = None,
    seats: list[SeatConfig] | None = None,
    chairman_personality: str | None = None,
    no_cache: bool = False,
) -> dict:
    """Validate config/catalog and optional session request without running deliberation."""
    model_ids = await model_provider.list_model_ids(no_cache=no_cache)
    model_set = set(model_ids)
    requested_models = set(config.allowed_models)
    requested_models.add(config.chairman_model_synthesis)
    requested_models.add(config.chairman_model_counterfactual)
    if seats:
        requested_models.update(seat.model for seat in seats)

    invalid_models = sorted(model for model in requested_models if model not in model_set)
    errors = []
    for model in invalid_models:
        suggestions = suggest(model, model_ids)
        errors.append(
            {
                "error_code": "MODEL_NOT_FOUND",
                "message_human": (
                    f"El modelo {model} no existe en OpenRouter. ¿Quizás {suggestions[0]}?"
                ),
                "context": {"requested": model, "did_you_mean": suggestions},
                "doc_ref": "docs/errors.md#model-not-found",
            }
        )
    warnings: list[dict] = []

    if not errors and mode and seats:
        try:
            result = validate_session_request(
                mode,
                seats,
                chairman_personality or config.defaults.chairman_personality,
                config,
                catalog,
            )
            warnings = [
                {
                    "warning_code": warning.warning_code,
                    "message_human": warning.message_human,
                    "context": warning.context,
                }
                for warning in result.warnings
            ]
        except ValueError as exc:
            payload = exc.to_payload() if hasattr(exc, "to_payload") else {"error_code": "INVALID"}
            errors.append(payload)

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "openrouter_models_validated": True,
        "models_check": {
            "valid": sorted(model for model in requested_models if model in model_set),
            "invalid": [
                {"requested": model, "did_you_mean": suggest(model, model_ids)}
                for model in invalid_models
            ],
        },
    }


def suggest(model: str, model_ids: list[str]) -> list[str]:
    """Return closest model id suggestions."""
    provider = model.split("/", 1)[0]
    same_provider = [model_id for model_id in model_ids if model_id.startswith(f"{provider}/")]
    candidates = same_provider or model_ids
    return difflib.get_close_matches(model, candidates, n=3, cutoff=0.2) or candidates[:3]
