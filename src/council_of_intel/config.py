"""Application configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, ValidationError, model_validator

from council_of_intel.errors import CouncilValidationError
from council_of_intel.runtime_paths import resolve_runtime_path


class OpenRouterConfig(BaseModel):
    """OpenRouter transport configuration."""

    model_config = ConfigDict(extra="forbid")

    api_key_env: str
    base_url: AnyHttpUrl
    timeout_seconds: int = Field(gt=0)
    retry_attempts: int = Field(ge=0)
    retry_backoff_base_seconds: int = Field(gt=0)


class DefaultsConfig(BaseModel):
    """Default UI/session choices."""

    model_config = ConfigDict(extra="forbid")

    mode: Literal["sats", "council"]
    chairman_personality: str


class ValidationConfig(BaseModel):
    """Round 0 validation policy."""

    model_config = ConfigDict(extra="forbid")

    enforce_unique_models_council_mode: bool
    enforce_unique_models_sats_mode: bool
    block_same_personality_same_model: bool
    enforce_unique_personality: Literal["warn", "block", "allow"]
    provider_diversity_warn_threshold: float = Field(ge=0, le=1)
    min_seats_to_continue_after_failures: int = Field(ge=1)


class AntiConvergenceConfig(BaseModel):
    """Counterfactual trigger settings."""

    model_config = ConfigDict(extra="forbid")

    agreement_threshold: float = Field(gt=0, le=1)
    counterfactual_max_words: int = Field(gt=0)


class CrossExaminationConfig(BaseModel):
    """Round 2 cross-examination settings."""

    model_config = ConfigDict(extra="forbid")

    min_engaged_seats: int = Field(ge=1)
    max_words: int = Field(gt=0)
    anti_recursion_retries: int = Field(ge=0)


class PollingConfig(BaseModel):
    """Client polling settings."""

    model_config = ConfigDict(extra="forbid")

    status_interval_seconds: float = Field(gt=0)


class ServerConfig(BaseModel):
    """Local server settings."""

    model_config = ConfigDict(extra="forbid")

    preferred_port: int = Field(ge=1, le=65535)
    port_range_fallback: tuple[int, int]

    @model_validator(mode="after")
    def validate_port_range(self) -> ServerConfig:
        start, end = self.port_range_fallback
        if start > end:
            raise ValueError("port_range_fallback start must be <= end")
        return self


class LoggingConfig(BaseModel):
    """Structured logging settings."""

    model_config = ConfigDict(extra="forbid")

    level: str
    format: Literal["json"]
    path: str


class AppConfig(BaseModel):
    """Root application config."""

    model_config = ConfigDict(extra="forbid")

    openrouter: OpenRouterConfig
    allowed_models: list[str] = Field(min_length=1)
    chairman_model_synthesis: str
    chairman_model_counterfactual: str
    defaults: DefaultsConfig
    validation: ValidationConfig
    anticonvergence: AntiConvergenceConfig
    cross_examination: CrossExaminationConfig
    polling: PollingConfig
    server: ServerConfig
    logging: LoggingConfig

    @model_validator(mode="after")
    def validate_chairman_models_allowed(self) -> AppConfig:
        allowed = set(self.allowed_models)
        for field_name in ("chairman_model_synthesis", "chairman_model_counterfactual"):
            model = getattr(self, field_name)
            if model not in allowed:
                raise ValueError(f"{field_name} must be present in allowed_models")
        return self


def load_config(path: Path | str = Path("config.yaml")) -> AppConfig:
    """Load and validate the project config."""
    config_path = resolve_runtime_path(path)
    if not config_path.exists():
        raise CouncilValidationError(
            error_code="CONFIG_FILE_NOT_FOUND",
            message_human=f"No encuentro `{config_path}`. Sin config no hay council.",
            context={"path": str(config_path)},
        )

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    try:
        return AppConfig.model_validate(raw)
    except ValidationError as exc:
        chairman_error = _chairman_model_error(raw)
        if chairman_error is not None:
            raise chairman_error from exc
        raise CouncilValidationError(
            error_code="CONFIG_INVALID",
            message_human="`config.yaml` no pasa schema. Revisa el contexto del error.",
            context={"errors": exc.errors(include_url=False)},
        ) from exc
    except ValueError as exc:
        chairman_error = _chairman_model_error(raw)
        if chairman_error is not None:
            raise chairman_error from exc
        raise


def _chairman_model_error(raw: object) -> CouncilValidationError | None:
    if not isinstance(raw, dict):
        return None

    allowed = set(raw.get("allowed_models", []))
    for key in ("chairman_model_synthesis", "chairman_model_counterfactual"):
        model = raw.get(key)
        if isinstance(model, str) and model not in allowed:
            return CouncilValidationError(
                error_code="CHAIRMAN_MODEL_NOT_ALLOWED",
                message_human=f"El modelo Chairman `{model}` no está en `allowed_models`.",
                context={"field": key, "model": model},
            )
    return None
