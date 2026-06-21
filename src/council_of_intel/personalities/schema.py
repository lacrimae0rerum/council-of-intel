"""Schema for personality metadata loaded from agent.md frontmatter."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Personality(BaseModel):
    """Validated personality metadata plus prompt file bodies."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    family: Literal["A", "B", "C", "D"]
    polarity: Literal[
        "structured",
        "adversarial",
        "first-principles",
        "emergent",
        "doctrinal",
        "director",
    ]
    recommended_model: str
    sat_layer: Literal[
        "ach",
        "kac",
        "iof",
        "qoi",
        "red_team",
        "devils",
        "attribution",
        "none",
    ]
    can_be_chairman: bool
    requires_anti_recursion: bool = False
    description: str = Field(min_length=1)
    agent_prompt: str = Field(min_length=1)
    skill: str = Field(min_length=1)
    knowledge: str = Field(min_length=1)
