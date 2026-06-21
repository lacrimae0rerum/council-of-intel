"""Anonymous response shuffling for Round 2."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SeatResponse:
    """Raw seat response with private metadata."""

    seat_idx: int
    personality_id: str
    model: str
    content: str


@dataclass(frozen=True, slots=True)
class AnonymousItem:
    """Public anonymous response shown to evaluators."""

    label: str
    content: str

    def to_public_dict(self) -> dict[str, str]:
        """Return metadata-free public payload."""
        return {"label": self.label, "content": self.content}


@dataclass(frozen=True, slots=True)
class AnonymousMappingEntry:
    """Private mapping from anonymous label back to original seat."""

    seat_idx: int
    personality_id: str
    model: str


@dataclass(frozen=True, slots=True)
class AnonymizedResponses:
    """Anonymized public items plus private reverse mapping."""

    items: list[AnonymousItem]
    mapping: dict[str, AnonymousMappingEntry]


def anonymize_responses(
    responses: list[SeatResponse], seed: int | None = None
) -> AnonymizedResponses:
    """Shuffle responses and label them Response A/B/C without exposing metadata."""
    shuffled = list(responses)
    rng = random.Random(seed)
    rng.shuffle(shuffled)

    items: list[AnonymousItem] = []
    mapping: dict[str, AnonymousMappingEntry] = {}
    for offset, response in enumerate(shuffled):
        label = f"Response {chr(ord('A') + offset)}"
        items.append(AnonymousItem(label=label, content=response.content))
        mapping[label] = AnonymousMappingEntry(
            seat_idx=response.seat_idx,
            personality_id=response.personality_id,
            model=response.model,
        )
    return AnonymizedResponses(items=items, mapping=mapping)
