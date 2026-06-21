import shutil
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from council_of_intel.web import launcher


@pytest.fixture
def runtime_dir() -> Path:
    path = Path("test-artifacts") / f"web-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


def test_build_web_app_serves_static_index(runtime_dir: Path) -> None:
    static_dir = runtime_dir / "static"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<div id='root'>ok</div>", encoding="utf-8")

    app = launcher.build_web_app(static_dir=static_dir, sessions_dir=runtime_dir / "sessions")
    client = TestClient(app)

    assert client.get("/api/health").json() == {"status": "ok"}
    assert len(client.get("/api/personalities").json()["personalities"]) == 17
    assert "root" in client.get("/").text
    assert "root" in client.get("/deep/react/route").text
    assert client.get("/api/does-not-exist").status_code == 404


def test_run_web_uses_configured_port_and_browser(
    monkeypatch: pytest.MonkeyPatch, runtime_dir: Path
) -> None:
    calls = {}
    app_obj = object()

    class Config:
        class Server:
            preferred_port = 1234
            port_range_fallback = (1235, 1236)

        server = Server()

    monkeypatch.setattr(launcher, "load_config", lambda path: Config())
    monkeypatch.setattr(launcher, "choose_port", lambda preferred, fallback: 1235)
    monkeypatch.setattr(launcher, "build_web_app", lambda config_path, static_dir: app_obj)
    monkeypatch.setattr(launcher.webbrowser, "open", lambda url: calls.setdefault("url", url))

    def fake_uvicorn_run(app, host: str, port: int, log_level: str) -> None:
        calls["uvicorn"] = (app, host, port, log_level)

    monkeypatch.setattr(launcher.uvicorn, "run", fake_uvicorn_run)

    launcher.run_web("config.yaml", static_dir=runtime_dir, open_browser=True)

    assert calls["url"] == "http://127.0.0.1:1235"
    assert calls["uvicorn"] == (app_obj, "127.0.0.1", 1235, "warning")
