"""Runtime path helpers for source and PyInstaller builds."""

from __future__ import annotations

import sys
from pathlib import Path


def bundled_path(relative_path: Path | str) -> Path:
    """Return a path inside PyInstaller's bundle, or the project cwd in source runs."""
    base = Path(getattr(sys, "_MEIPASS", Path.cwd()))
    return base / relative_path


def resolve_runtime_path(path: Path | str) -> Path:
    """Resolve a user path, falling back to bundled data if the path is missing."""
    requested = Path(path)
    if requested.exists() or requested.is_absolute():
        return requested

    bundled = bundled_path(requested)
    if bundled.exists():
        return bundled
    return requested
