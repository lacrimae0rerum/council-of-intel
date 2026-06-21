import shutil
import sys
import uuid
from pathlib import Path

import pytest

from council_of_intel.errors import CouncilValidationError
from council_of_intel.personalities.loader import load_personalities

EXPECTED_PERSONALITIES = {
    "ach-analyst",
    "red-team",
    "attribution-skeptic",
    "devils-advocate",
    "key-assumptions-checker",
    "quality-of-info-auditor",
    "indicators-of-change",
    "kent",
    "heuer",
    "clark",
    "lowenthal",
    "grabo",
    "feynman",
    "socrates",
    "sun-tzu",
    "lao-tzu",
    "mclaughlin",
}


def test_load_personalities_loads_closed_catalog() -> None:
    catalog = load_personalities(Path("personalities"))

    assert set(catalog) == EXPECTED_PERSONALITIES
    assert len(catalog) == 17


def test_mclaughlin_is_only_default_chairman() -> None:
    catalog = load_personalities(Path("personalities"))

    chairmen = [personality.id for personality in catalog.values() if personality.can_be_chairman]

    assert chairmen == ["mclaughlin"]


def test_loader_rejects_missing_required_file() -> None:
    with pytest.raises(CouncilValidationError) as exc_info:
        load_personalities(Path("tests/fixtures/broken_personalities"))

    assert exc_info.value.error_code == "PERSONALITY_FILE_MISSING"
    assert exc_info.value.context["personality"] == "broken"


def test_load_personalities_falls_back_to_bundled_path(monkeypatch: pytest.MonkeyPatch) -> None:
    empty_cwd = Path("test-artifacts") / f"personalities-cwd-{uuid.uuid4().hex}"
    empty_cwd.mkdir(parents=True)
    monkeypatch.chdir(empty_cwd)
    monkeypatch.setattr(sys, "_MEIPASS", str(Path.cwd().parents[1]), raising=False)

    catalog = load_personalities()

    assert set(catalog) == EXPECTED_PERSONALITIES
    shutil.rmtree(empty_cwd, ignore_errors=True)
