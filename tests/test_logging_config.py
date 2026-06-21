import json
import shutil
import uuid
from pathlib import Path

import pytest

from council_of_intel.logging_config import configure_logging, get_logger


@pytest.fixture
def runtime_dir() -> Path:
    path = Path("test-artifacts") / f"logs-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


def test_structured_logger_writes_json_with_session_context(runtime_dir: Path) -> None:
    log_path = runtime_dir / "logs" / "council.log"

    configure_logging(log_path=log_path, level="INFO", max_bytes=512, backup_count=1)
    logger = get_logger("test").bind(session_id="01HZLOG", round=1)
    logger.info("seat_completed", seat_idx=2, cost_eur=0.12)

    line = log_path.read_text(encoding="utf-8").strip()
    payload = json.loads(line)
    assert payload["event"] == "seat_completed"
    assert payload["session_id"] == "01HZLOG"
    assert payload["round"] == 1
    assert payload["seat_idx"] == 2
    assert payload["cost_eur"] == 0.12


def test_structured_logger_uses_rotation(runtime_dir: Path) -> None:
    log_path = runtime_dir / "logs" / "council.log"

    configure_logging(log_path=log_path, level="INFO", max_bytes=120, backup_count=1)
    logger = get_logger("rotation")
    for index in range(20):
        logger.info("large_event", index=index, payload="x" * 80)

    assert log_path.exists()
    assert log_path.with_name("council.log.1").exists()
