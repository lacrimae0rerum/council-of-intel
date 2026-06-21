from pathlib import Path

import pytest

from council_of_intel.config import load_config
from council_of_intel.errors import CouncilValidationError
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.validation import SeatConfig, validate_session_request


@pytest.fixture
def config_and_catalog():
    return load_config(Path("config.yaml")), load_personalities(Path("personalities"))


def test_sats_mode_allows_reused_models(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    seats = [
        SeatConfig(personality_id="ach-analyst", model="openai/gpt-5.5"),
        SeatConfig(personality_id="red-team", model="openai/gpt-5.5"),
        SeatConfig(personality_id="key-assumptions-checker", model="anthropic/claude-sonnet-4.6"),
    ]

    result = validate_session_request("sats", seats, "mclaughlin", config, catalog)

    assert result.valid is True
    assert [warning.warning_code for warning in result.warnings] == ["PROVIDER_DIVERSITY_LOW"]


def test_council_mode_rejects_reused_models(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    seats = [
        SeatConfig(personality_id="kent", model="openai/gpt-5.5"),
        SeatConfig(personality_id="heuer", model="openai/gpt-5.5"),
        SeatConfig(personality_id="feynman", model="anthropic/claude-sonnet-4.6"),
    ]

    with pytest.raises(CouncilValidationError) as exc_info:
        validate_session_request("council", seats, "mclaughlin", config, catalog)

    assert exc_info.value.error_code == "DUPLICATE_MODEL_COUNCIL_MODE"


def test_any_mode_rejects_same_personality_same_model(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    seats = [
        SeatConfig(personality_id="ach-analyst", model="openai/gpt-5.5"),
        SeatConfig(personality_id="ach-analyst", model="openai/gpt-5.5"),
        SeatConfig(personality_id="red-team", model="anthropic/claude-sonnet-4.6"),
    ]

    with pytest.raises(CouncilValidationError) as exc_info:
        validate_session_request("sats", seats, "mclaughlin", config, catalog)

    assert exc_info.value.error_code == "SAME_PERSONALITY_SAME_MODEL"


def test_sats_mode_rejects_council_family_personality(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    seats = [
        SeatConfig(personality_id="kent", model="openai/gpt-5.5"),
        SeatConfig(personality_id="red-team", model="anthropic/claude-sonnet-4.6"),
        SeatConfig(personality_id="ach-analyst", model="google/gemini-3.1-pro-preview"),
    ]

    with pytest.raises(CouncilValidationError) as exc_info:
        validate_session_request("sats", seats, "mclaughlin", config, catalog)

    assert exc_info.value.error_code == "PERSONALITY_MODE_MISMATCH"


def test_chairman_must_be_chairman_capable(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    seats = [
        SeatConfig(personality_id="kent", model="openai/gpt-5.5"),
        SeatConfig(personality_id="heuer", model="anthropic/claude-sonnet-4.6"),
        SeatConfig(personality_id="feynman", model="google/gemini-3.1-pro-preview"),
    ]

    with pytest.raises(CouncilValidationError) as exc_info:
        validate_session_request("council", seats, "kent", config, catalog)

    assert exc_info.value.error_code == "CHAIRMAN_NOT_ALLOWED"
