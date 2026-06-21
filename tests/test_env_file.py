import os
import uuid
from pathlib import Path

from council_of_intel.env_file import load_env_file


def test_load_env_file_sets_missing_values(monkeypatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    env_path = _env_path()
    env_path.write_text(
        "\n".join(
            [
                "# local secrets",
                "OPENROUTER_API_KEY='sk-test'",
                'COUNCIL_OTHER="value with spaces"',
            ]
        ),
        encoding="utf-8",
    )

    assert load_env_file(env_path) is True

    assert os.environ["OPENROUTER_API_KEY"] == "sk-test"
    assert os.environ["COUNCIL_OTHER"] == "value with spaces"


def test_load_env_file_does_not_override_existing_value(monkeypatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "from-shell")
    env_path = _env_path()
    env_path.write_text("OPENROUTER_API_KEY=from-file", encoding="utf-8")

    assert load_env_file(env_path) is True

    assert os.environ["OPENROUTER_API_KEY"] == "from-shell"


def test_load_env_file_ignores_missing_file() -> None:
    assert load_env_file(_env_path()) is False


def _env_path() -> Path:
    path = Path("test-artifacts") / f"env-{uuid.uuid4().hex}" / ".env"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
