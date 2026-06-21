"""Command-line entrypoint."""

from __future__ import annotations

import argparse
import asyncio
import json

from council_of_intel.api.dry_run import CachedOpenRouterModelProvider, run_dry_run
from council_of_intel.config import load_config
from council_of_intel.env_file import load_env_file
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.tui.launcher import run_tui
from council_of_intel.web.launcher import run_web


def main(argv: list[str] | None = None) -> None:
    """Run the local launcher."""
    parser = argparse.ArgumentParser(prog="council-of-intel")
    parser.add_argument("--tui", action="store_true", help="Arranca la TUI Textual")
    parser.add_argument("--web", action="store_true", help="Arranca la Web TUI local")
    parser.add_argument(
        "--dry-run", action="store_true", help="Valida config/modelos sin deliberar"
    )
    parser.add_argument(
        "--no-cache", action="store_true", help="Fuerza recarga de modelos OpenRouter"
    )
    parser.add_argument("--config", default="config.yaml", help="Ruta de config.yaml")
    args = parser.parse_args(argv)
    load_env_file()

    selected = _selected_mode(args)
    if selected is None:
        selected = _prompt_mode()

    if selected == "tui":
        run_tui(args.config)
        return
    if selected == "web":
        run_web(args.config)
        return
    if selected == "dry-run":
        asyncio.run(_print_dry_run(args.config, no_cache=args.no_cache))
        return

    parser.print_help()


def _selected_mode(args: argparse.Namespace) -> str | None:
    selected = [
        mode
        for mode, enabled in (
            ("tui", args.tui),
            ("web", args.web),
            ("dry-run", args.dry_run),
        )
        if enabled
    ]
    if len(selected) > 1:
        raise SystemExit("Elige solo un modo: --tui, --web o --dry-run.")
    return selected[0] if selected else None


def _prompt_mode() -> str:
    print("[1] TUI · [2] Web · [3] Dry-run")
    choice = input("> ").strip()
    if choice == "1":
        return "tui"
    if choice == "2":
        return "web"
    if choice == "3":
        return "dry-run"
    raise SystemExit("Opcion invalida.")


async def _print_dry_run(config_path: str, no_cache: bool) -> None:
    config = load_config(config_path)
    catalog = load_personalities()
    provider = CachedOpenRouterModelProvider(str(config.openrouter.base_url))
    result = await run_dry_run(config, catalog, provider, no_cache=no_cache)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
