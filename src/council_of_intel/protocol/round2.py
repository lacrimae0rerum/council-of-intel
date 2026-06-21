"""Round 2 cross-examination and anti-recursion."""

from __future__ import annotations

import asyncio
import re
from typing import Protocol

from council_of_intel.config import AppConfig
from council_of_intel.openrouter.anonymizer import SeatResponse, anonymize_responses
from council_of_intel.openrouter.client import (
    ChatCompletionRequest,
    ChatCompletionResult,
    ChatMessage,
)
from council_of_intel.openrouter.sanitizer import sanitize_model_self_references
from council_of_intel.personalities.schema import Personality
from council_of_intel.protocol.models import Round1Result, Round2Evaluation, Round2Result
from council_of_intel.validation import SeatConfig


class CompletionClient(Protocol):
    """Protocol for anything that can complete a chat request."""

    async def complete_chat(self, request: ChatCompletionRequest) -> ChatCompletionResult: ...


async def run_round2(
    query: str,
    seats: list[SeatConfig],
    round1: Round1Result,
    config: AppConfig,
    catalog: dict[str, Personality],
    client: CompletionClient,
    anonymizer_seed: int | None = None,
) -> Round2Result:
    """Run anonymous cross-examination for surviving seats."""
    seat_by_index = {index: seat for index, seat in enumerate(seats)}
    sanitized = [
        SeatResponse(
            seat_idx=response.seat_idx,
            personality_id=seat_by_index[response.seat_idx].personality_id,
            model=response.model,
            content=sanitize_model_self_references(response.content),
        )
        for response in round1.completed
    ]
    anonymized = anonymize_responses(sanitized, seed=anonymizer_seed)
    evaluations = await asyncio.gather(
        *[
            _evaluate_one(
                query=query,
                seat=seat_by_index[response.seat_idx],
                seat_idx=response.seat_idx,
                anonymized_payload="\n\n".join(
                    f"{item.label}:\n{item.content}" for item in anonymized.items
                ),
                config=config,
                catalog=catalog,
                client=client,
            )
            for response in round1.completed
        ]
    )
    return Round2Result(anonymized=anonymized, evaluations=evaluations)


async def _evaluate_one(
    query: str,
    seat: SeatConfig,
    seat_idx: int,
    anonymized_payload: str,
    config: AppConfig,
    catalog: dict[str, Personality],
    client: CompletionClient,
) -> Round2Evaluation:
    personality = catalog[seat.personality_id]
    request = _cross_exam_request(
        query,
        seat,
        seat_idx,
        personality,
        anonymized_payload,
        extra_user_text=None,
    )
    result = await client.complete_chat(request)
    retried = False

    if _needs_anti_recursion(personality, result.content):
        retry_request = _cross_exam_request(
            query,
            seat,
            seat_idx,
            personality,
            anonymized_payload,
            extra_user_text="toma postura, no solo preguntes",
        )
        result = await client.complete_chat(retry_request)
        retried = True

    return Round2Evaluation(
        seat_idx=seat_idx,
        personality_id=personality.id,
        model=seat.model,
        content=result.content,
        winner_label=parse_winner_label(result.content),
        usage_cost=result.usage_cost,
        retried_for_anti_recursion=retried,
    )


def _cross_exam_request(
    query: str,
    seat: SeatConfig,
    seat_idx: int,
    personality: Personality,
    anonymized_payload: str,
    extra_user_text: str | None,
) -> ChatCompletionRequest:
    user_parts = [
        f"Pregunta original:\n{query}",
        f"Respuestas anonimizadas:\n{anonymized_payload}",
        (
            "Produce ranking de las respuestas, declara una linea `Winner: Response X`, "
            "y engage con al menos 2 otras respuestas con argumento sustantivo. "
            "Maximo 300 palabras."
        ),
    ]
    if extra_user_text:
        user_parts.append(extra_user_text)
    return ChatCompletionRequest(
        seat_idx=seat_idx,
        model=seat.model,
        messages=[
            ChatMessage(
                role="system",
                content="\n\n".join(
                    [personality.agent_prompt, personality.skill, personality.knowledge]
                ),
            ),
            ChatMessage(role="user", content="\n\n".join(user_parts)),
        ],
    )


def parse_winner_label(content: str) -> str | None:
    """Extract `Winner: Response X` from a cross-examination response."""
    match = re.search(r"\bWinner\s*:\s*(Response\s+[A-Z])\b", content, flags=re.IGNORECASE)
    if not match:
        return None
    response, letter = match.group(1).split()
    return f"{response.title()} {letter.upper()}"


def _needs_anti_recursion(personality: Personality, content: str) -> bool:
    if not personality.requires_anti_recursion:
        return False
    if re.search(r"\b(Winner|Postura|Conclusion|Juicio)\b", content, flags=re.IGNORECASE):
        return False
    stripped = content.strip()
    if not stripped:
        return False
    sentence_marks = re.findall(r"[?.!]", stripped)
    return bool(sentence_marks) and all(mark == "?" for mark in sentence_marks)
