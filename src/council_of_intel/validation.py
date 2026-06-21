"""Round 0 session validation rules."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, ConfigDict

from council_of_intel.config import AppConfig
from council_of_intel.errors import CouncilValidationError
from council_of_intel.personalities.schema import Personality

Mode = Literal["sats", "council"]


class SeatConfig(BaseModel):
    """Requested analytical seat."""

    model_config = ConfigDict(extra="forbid")

    personality_id: str
    model: str


@dataclass(slots=True)
class ValidationWarning:
    """Non-blocking validation warning."""

    warning_code: str
    message_human: str
    context: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class SessionValidationResult:
    """Successful validation result."""

    valid: bool
    warnings: list[ValidationWarning] = field(default_factory=list)


def validate_session_request(
    mode: str,
    seats: list[SeatConfig],
    chairman_personality_id: str,
    config: AppConfig,
    catalog: dict[str, Personality],
) -> SessionValidationResult:
    """Validate Round 0 constraints before any OpenRouter call."""
    if mode not in ("sats", "council"):
        raise CouncilValidationError(
            error_code="INVALID_MODE",
            message_human=f"Modo `{mode}` inválido. Usa `sats` o `council`.",
            context={"mode": mode},
        )
    if len(seats) < config.validation.min_seats_to_continue_after_failures:
        raise CouncilValidationError(
            error_code="INSUFFICIENT_SEATS",
            message_human="Mete al menos 3 seats analíticos. Con menos esto no es un council.",
            context={"seat_count": len(seats)},
        )

    _validate_chairman(chairman_personality_id, catalog)
    _validate_allowed_models(seats, config)
    _validate_personalities_exist(seats, catalog)
    _validate_mode_families(mode, seats, catalog)
    _validate_same_personality_same_model(seats, config)
    _validate_model_uniqueness(mode, seats, config)
    warnings = _validate_personality_uniqueness(seats, config)
    warnings.extend(_provider_diversity_warnings(seats, config))
    return SessionValidationResult(valid=True, warnings=warnings)


def _validate_chairman(chairman_personality_id: str, catalog: dict[str, Personality]) -> None:
    chairman = catalog.get(chairman_personality_id)
    if chairman is None:
        raise CouncilValidationError(
            error_code="PERSONALITY_NOT_FOUND",
            message_human=f"Chairman `{chairman_personality_id}` no existe.",
            context={"personality": chairman_personality_id},
        )
    if not chairman.can_be_chairman:
        raise CouncilValidationError(
            error_code="CHAIRMAN_NOT_ALLOWED",
            message_human=f"`{chairman_personality_id}` no puede ser Chairman.",
            context={"personality": chairman_personality_id},
        )


def _validate_allowed_models(seats: list[SeatConfig], config: AppConfig) -> None:
    allowed = set(config.allowed_models)
    for index, seat in enumerate(seats):
        if seat.model not in allowed:
            raise CouncilValidationError(
                error_code="MODEL_NOT_ALLOWED",
                message_human=f"El modelo `{seat.model}` no está en `allowed_models`.",
                context={"seat_idx": index, "model": seat.model},
            )


def _validate_personalities_exist(
    seats: list[SeatConfig], catalog: dict[str, Personality]
) -> None:
    for index, seat in enumerate(seats):
        if seat.personality_id not in catalog:
            raise CouncilValidationError(
                error_code="PERSONALITY_NOT_FOUND",
                message_human=f"La personalidad `{seat.personality_id}` no existe.",
                context={"seat_idx": index, "personality": seat.personality_id},
            )


def _validate_mode_families(
    mode: str, seats: list[SeatConfig], catalog: dict[str, Personality]
) -> None:
    allowed_families = {"sats": {"A"}, "council": {"B", "C"}}[mode]
    for index, seat in enumerate(seats):
        personality = catalog[seat.personality_id]
        if personality.family not in allowed_families:
            raise CouncilValidationError(
                error_code="PERSONALITY_MODE_MISMATCH",
                message_human=(
                    f"`{seat.personality_id}` es Familia {personality.family} y no encaja "
                    f"en modo `{mode}`."
                ),
                context={
                    "seat_idx": index,
                    "personality": seat.personality_id,
                    "family": personality.family,
                    "mode": mode,
                },
            )


def _validate_same_personality_same_model(seats: list[SeatConfig], config: AppConfig) -> None:
    if not config.validation.block_same_personality_same_model:
        return
    pairs: dict[tuple[str, str], list[int]] = {}
    for index, seat in enumerate(seats):
        pairs.setdefault((seat.personality_id, seat.model), []).append(index)
    for (personality_id, model), indices in pairs.items():
        if len(indices) > 1:
            raise CouncilValidationError(
                error_code="SAME_PERSONALITY_SAME_MODEL",
                message_human=(
                    f"No puedes asignar `{personality_id}` con `{model}` a dos seats. "
                    "Es duplicado total y no aporta señal."
                ),
                context={"seat_idx": indices, "personality": personality_id, "model": model},
            )


def _validate_model_uniqueness(mode: str, seats: list[SeatConfig], config: AppConfig) -> None:
    enforce = (
        config.validation.enforce_unique_models_council_mode
        if mode == "council"
        else config.validation.enforce_unique_models_sats_mode
    )
    if not enforce:
        return
    seen: dict[str, list[int]] = {}
    for index, seat in enumerate(seats):
        seen.setdefault(seat.model, []).append(index)
    for model, indices in seen.items():
        if len(indices) > 1:
            raise CouncilValidationError(
                error_code="DUPLICATE_MODEL_COUNCIL_MODE",
                message_human=f"Modo Council exige modelos únicos. `{model}` está repetido.",
                context={"model": model, "seat_idx": indices},
            )


def _validate_personality_uniqueness(
    seats: list[SeatConfig], config: AppConfig
) -> list[ValidationWarning]:
    policy = config.validation.enforce_unique_personality
    if policy == "allow":
        return []

    repeated = {
        personality_id: indices
        for personality_id, indices in _indices_by_personality(seats).items()
        if len(indices) > 1
    }
    if not repeated:
        return []
    if policy == "block":
        personality_id, indices = next(iter(repeated.items()))
        raise CouncilValidationError(
            error_code="DUPLICATE_PERSONALITY_BLOCKED",
            message_human=f"`{personality_id}` está repetida y la config lo bloquea.",
            context={"personality": personality_id, "seat_idx": indices},
        )

    return [
        ValidationWarning(
            warning_code="DUPLICATE_PERSONALITY_WARN",
            message_human=(
                "Hay personalidades repetidas. Permitido por config, pero ojo con la señal."
            ),
            context={"repeated": repeated},
        )
    ]


def _indices_by_personality(seats: list[SeatConfig]) -> dict[str, list[int]]:
    indices: dict[str, list[int]] = {}
    for index, seat in enumerate(seats):
        indices.setdefault(seat.personality_id, []).append(index)
    return indices


def _provider_diversity_warnings(
    seats: list[SeatConfig], config: AppConfig
) -> list[ValidationWarning]:
    providers = [_provider_from_model(seat.model) for seat in seats]
    provider, count = Counter(providers).most_common(1)[0]
    ratio = count / len(seats)
    if ratio <= config.validation.provider_diversity_warn_threshold:
        return []
    return [
        ValidationWarning(
            warning_code="PROVIDER_DIVERSITY_LOW",
            message_human=(
                f"{count} de {len(seats)} seats usan provider `{provider}`. "
                "Considera diversificar."
            ),
            context={"provider": provider, "count": count, "total": len(seats), "ratio": ratio},
        )
    ]


def _provider_from_model(model: str) -> str:
    return model.split("/", 1)[0]
