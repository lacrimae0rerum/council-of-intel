"""Launch FastAPI plus packaged React frontend."""

from __future__ import annotations

import sys
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from council_of_intel.api.app import create_app
from council_of_intel.api.ports import choose_port
from council_of_intel.api.runner import ProtocolSessionRunner
from council_of_intel.config import load_config
from council_of_intel.logging_config import configure_logging
from council_of_intel.openrouter.client import OpenRouterClient
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.storage.sessions import SessionStore


def build_web_app(
    config_path: Path | str = "config.yaml",
    static_dir: Path | str | None = None,
    sessions_dir: Path | str = "sessions",
) -> FastAPI:
    """Build the API app and mount packaged React static assets when present."""
    config = load_config(config_path)
    configure_logging(config.logging.path, level=config.logging.level)
    catalog = load_personalities()
    sessions_path = Path(sessions_dir)
    store = SessionStore(sessions_path, sessions_path / "index.sqlite3")
    runner = ProtocolSessionRunner(
        config=config,
        catalog=catalog,
        client=OpenRouterClient(config.openrouter),
    )
    api_app = create_app(config=config, catalog=catalog, store=store, runner=runner)
    app = FastAPI(title="council-of-intel-web", version="0.1.0")
    app.mount("/api", api_app)

    resolved_static_dir = _resolve_static_dir(static_dir)
    if resolved_static_dir is not None:
        _mount_spa_static(app, resolved_static_dir)
    return app


def run_web(
    config_path: Path | str = "config.yaml",
    static_dir: Path | str | None = None,
    open_browser: bool = True,
) -> None:
    """Run the packaged web server with configured port fallback."""
    config = load_config(config_path)
    port = choose_port(config.server.preferred_port, config.server.port_range_fallback)
    app = build_web_app(config_path=config_path, static_dir=static_dir)
    url = f"http://127.0.0.1:{port}"
    print(f"Web lista en {url}")
    if open_browser:
        webbrowser.open(url)
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


def _resolve_static_dir(static_dir: Path | str | None = None) -> Path | None:
    candidates: list[Path] = []
    if static_dir is not None:
        candidates.append(Path(static_dir))
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        candidates.append(Path(sys._MEIPASS) / "static")
    candidates.append(Path(__file__).resolve().parents[1] / "static")
    candidates.append(Path("frontend") / "dist")

    for candidate in candidates:
        if (candidate / "index.html").exists():
            return candidate
    return None


def _mount_spa_static(app: FastAPI, static_dir: Path) -> None:
    root = static_dir.resolve()
    index_path = root / "index.html"

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        requested = (root / full_path).resolve()
        if requested.is_file() and requested.is_relative_to(root):
            return FileResponse(requested)
        if index_path.exists():
            return FileResponse(index_path)
        raise HTTPException(status_code=404)
