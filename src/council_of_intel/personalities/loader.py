"""Load personality folders from disk."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from council_of_intel.errors import CouncilValidationError
from council_of_intel.personalities.schema import Personality
from council_of_intel.runtime_paths import resolve_runtime_path

REQUIRED_FILES = ("agent.md", "skill.md", "knowledge.md")


def load_personalities(root: Path | str = Path("personalities")) -> dict[str, Personality]:
    """Load every personality directory under `root`."""
    catalog_root = resolve_runtime_path(root)
    if not catalog_root.exists():
        raise CouncilValidationError(
            error_code="PERSONALITY_CATALOG_NOT_FOUND",
            message_human=f"No encuentro el catálogo `{catalog_root}`.",
            context={"path": str(catalog_root)},
        )

    personalities: dict[str, Personality] = {}
    for personality_dir in sorted(path for path in catalog_root.iterdir() if path.is_dir()):
        personality = _load_personality(personality_dir)
        if personality.id != personality_dir.name:
            raise CouncilValidationError(
                error_code="PERSONALITY_ID_MISMATCH",
                message_human=(
                    f"La carpeta `{personality_dir.name}` no coincide con el id "
                    f"`{personality.id}` del frontmatter."
                ),
                context={"folder": personality_dir.name, "id": personality.id},
            )
        personalities[personality.id] = personality

    return personalities


def _load_personality(personality_dir: Path) -> Personality:
    for filename in REQUIRED_FILES:
        if not (personality_dir / filename).exists():
            raise CouncilValidationError(
                error_code="PERSONALITY_FILE_MISSING",
                message_human=f"`{personality_dir.name}` no tiene `{filename}`.",
                context={"personality": personality_dir.name, "file": filename},
            )

    metadata, prompt_body = _split_frontmatter(personality_dir / "agent.md")
    payload = {
        **metadata,
        "agent_prompt": prompt_body.strip(),
        "skill": (personality_dir / "skill.md").read_text(encoding="utf-8").strip(),
        "knowledge": (personality_dir / "knowledge.md").read_text(encoding="utf-8").strip(),
    }
    try:
        return Personality.model_validate(payload)
    except ValidationError as exc:
        raise CouncilValidationError(
            error_code="PERSONALITY_FRONTMATTER_INVALID",
            message_human=f"`{personality_dir.name}/agent.md` tiene frontmatter inválido.",
            context={"personality": personality_dir.name, "errors": exc.errors(include_url=False)},
        ) from exc


def _split_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise CouncilValidationError(
            error_code="PERSONALITY_FRONTMATTER_INVALID",
            message_human=f"`{path}` no empieza con frontmatter YAML.",
            context={"path": str(path)},
        )

    try:
        _, metadata_text, body = text.split("---", 2)
    except ValueError as exc:
        raise CouncilValidationError(
            error_code="PERSONALITY_FRONTMATTER_INVALID",
            message_human=f"`{path}` no cierra el frontmatter YAML.",
            context={"path": str(path)},
        ) from exc

    metadata = yaml.safe_load(metadata_text)
    if not isinstance(metadata, dict):
        raise CouncilValidationError(
            error_code="PERSONALITY_FRONTMATTER_INVALID",
            message_human=f"`{path}` tiene frontmatter vacío o inválido.",
            context={"path": str(path)},
        )
    return metadata, body
