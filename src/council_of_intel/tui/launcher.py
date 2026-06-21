"""Launch local backend plus Textual TUI."""

from __future__ import annotations

import threading
import time
from pathlib import Path

import uvicorn

from council_of_intel.api.app import create_app
from council_of_intel.api.ports import choose_port
from council_of_intel.api.runner import ProtocolSessionRunner
from council_of_intel.config import load_config
from council_of_intel.logging_config import configure_logging
from council_of_intel.openrouter.client import OpenRouterClient
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.storage.sessions import SessionStore
from council_of_intel.tui.app import CouncilTuiApp
from council_of_intel.tui.client import TuiApiClient


def run_tui(config_path: Path | str = "config.yaml") -> None:
    """Start the local API backend and run the Textual TUI."""
    config = load_config(config_path)
    configure_logging(config.logging.path, level=config.logging.level)
    catalog = load_personalities()
    store = SessionStore("sessions", "sessions/index.sqlite3")
    runner = ProtocolSessionRunner(
        config=config,
        catalog=catalog,
        client=OpenRouterClient(config.openrouter),
    )
    port = choose_port(config.server.preferred_port, config.server.port_range_fallback)
    app = create_app(config=config, catalog=catalog, store=store, runner=runner)
    server = _start_api_server(app, port)

    try:
        api_client = TuiApiClient(f"http://127.0.0.1:{port}")
        CouncilTuiApp(api_client, polling_interval=config.polling.status_interval_seconds).run()
    finally:
        server.should_exit = True


def _start_api_server(app, port: int) -> uvicorn.Server:
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 5
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.05)
    return server
