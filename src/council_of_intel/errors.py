"""Structured errors surfaced by validation layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CouncilValidationError(ValueError):
    """Validation error with a stable client-facing payload."""

    error_code: str
    message_human: str
    context: dict[str, Any] = field(default_factory=dict)
    doc_ref: str | None = None

    def __post_init__(self) -> None:
        ValueError.__init__(self, self.message_human)
        if self.doc_ref is None:
            anchor = self.error_code.lower().replace("_", "-")
            self.doc_ref = f"docs/errors.md#{anchor}"

    def to_payload(self) -> dict[str, Any]:
        """Return the API-ready error payload."""
        return {
            "error_code": self.error_code,
            "message_human": self.message_human,
            "context": self.context,
            "doc_ref": self.doc_ref,
        }
