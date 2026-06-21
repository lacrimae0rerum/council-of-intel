import json
from argparse import Namespace
from types import SimpleNamespace

import pytest

from council_of_intel import cli


def test_selected_mode_rejects_multiple_flags() -> None:
    args = Namespace(tui=True, web=True, dry_run=False)

    with pytest.raises(SystemExit):
        cli._selected_mode(args)


def test_selected_mode_returns_none_without_flags() -> None:
    args = Namespace(tui=False, web=False, dry_run=False)

    assert cli._selected_mode(args) is None


def test_prompt_mode_maps_choices(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _prompt: "2")

    assert cli._prompt_mode() == "web"


def test_main_dispatches_web(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {}

    def fake_run_web(config_path: str) -> None:
        called["config"] = config_path

    monkeypatch.setattr(cli, "load_env_file", lambda: called.setdefault("env_loaded", True))
    monkeypatch.setattr(cli, "run_web", fake_run_web)

    cli.main(["--web", "--config", "custom.yaml"])

    assert called == {"env_loaded": True, "config": "custom.yaml"}


@pytest.mark.asyncio
async def test_print_dry_run_outputs_json(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    class Provider:
        async def list_model_ids(self, no_cache: bool = False) -> list[str]:
            return ["model"]

    config = SimpleNamespace(openrouter=SimpleNamespace(base_url="https://openrouter.ai/api/v1"))
    monkeypatch.setattr(cli, "load_config", lambda path: config)
    monkeypatch.setattr(cli, "load_personalities", lambda: {})
    monkeypatch.setattr(cli, "CachedOpenRouterModelProvider", lambda base_url: Provider())

    async def fake_run_dry_run(*_args, **_kwargs):
        return {"valid": True, "errors": []}

    monkeypatch.setattr(cli, "run_dry_run", fake_run_dry_run)

    await cli._print_dry_run("config.yaml", no_cache=True)

    assert json.loads(capsys.readouterr().out) == {"valid": True, "errors": []}
