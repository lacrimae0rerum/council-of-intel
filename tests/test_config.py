import shutil
import sys
import uuid
from pathlib import Path

import pytest

from council_of_intel.config import AppConfig, load_config
from council_of_intel.errors import CouncilValidationError


def test_load_config_reads_project_yaml() -> None:
    config = load_config(Path("config.yaml"))

    assert isinstance(config, AppConfig)
    assert config.defaults.mode == "sats"
    assert "openai/gpt-5.5" in config.allowed_models
    assert config.chairman_model_synthesis in config.allowed_models
    assert config.chairman_model_counterfactual in config.allowed_models


def test_load_config_rejects_invalid_chairman_model() -> None:
    with pytest.raises(CouncilValidationError) as exc_info:
        load_config(Path("tests/fixtures/invalid_chairman_config.yaml"))

    assert exc_info.value.error_code == "CHAIRMAN_MODEL_NOT_ALLOWED"
    assert exc_info.value.context["model"] == "anthropic/missing"


def test_load_config_falls_back_to_bundled_path(monkeypatch: pytest.MonkeyPatch) -> None:
    empty_cwd = Path("test-artifacts") / f"config-cwd-{uuid.uuid4().hex}"
    empty_cwd.mkdir(parents=True)
    monkeypatch.chdir(empty_cwd)
    monkeypatch.setattr(sys, "_MEIPASS", str(Path.cwd().parents[1]), raising=False)

    config = load_config()

    assert config.defaults.mode == "sats"
    shutil.rmtree(empty_cwd, ignore_errors=True)
