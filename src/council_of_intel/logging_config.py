"""Structured JSON logging setup."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog


def configure_logging(
    log_path: Path | str,
    level: str = "INFO",
    max_bytes: int = 5_000_000,
    backup_count: int = 5,
) -> None:
    """Configure structlog to write JSON lines through a rotating file handler."""
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(message)s"))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(_level_value(level))

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(ensure_ascii=False),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(_level_value(level)),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=False,
    )


def get_logger(name: str | None = None):
    """Return a configured structlog logger."""
    return structlog.get_logger(name)


def _level_value(level: str) -> int:
    return logging.getLevelNamesMapping().get(level.upper(), logging.INFO)
