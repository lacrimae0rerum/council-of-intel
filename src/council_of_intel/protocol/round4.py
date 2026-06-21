"""Round 4 Chairman synthesis call."""

from __future__ import annotations

import re
from typing import Protocol

from council_of_intel.config import AppConfig
from council_of_intel.errors import CouncilValidationError
from council_of_intel.openrouter.client import (
    ChatCompletionRequest,
    ChatCompletionResult,
    ChatMessage,
)
from council_of_intel.personalities.schema import Personality
from council_of_intel.protocol.models import Round1Result, Round2Result, Round3Result

SELF_REFERENCE_PATTERNS = [
    r"como dije antes en mi argumento adversarial",
    r"como mencion[eé] antes en mi argumento adversarial",
    r"as I said earlier in my adversarial argument",
    r"as I mentioned in my counterfactual",
    r"mi counterfactual anterior",
]


class CompletionClient(Protocol):
    """Protocol for anything that can complete a chat request."""

    async def complete_chat(self, request: ChatCompletionRequest) -> ChatCompletionResult: ...


async def run_round4(
    query: str,
    chairman: Personality,
    round1: Round1Result,
    round2: Round2Result,
    round3: Round3Result,
    config: AppConfig,
    client: CompletionClient,
) -> ChatCompletionResult:
    """Ask the Chairman for final synthesis."""
    request = ChatCompletionRequest(
        seat_idx=0,
        model=config.chairman_model_synthesis,
        messages=[
            ChatMessage(role="system", content=chairman.agent_prompt),
            ChatMessage(role="user", content=_synthesis_context(query, round1, round2, round3)),
        ],
    )
    response = await client.complete_chat(request)
    validate_no_counterfactual_self_reference(response.content)
    return ChatCompletionResult(
        seat_idx=response.seat_idx,
        model=response.model,
        content=normalize_stage_final(response.content),
        usage_cost=response.usage_cost,
        raw_response=response.raw_response,
    )


def normalize_stage_final(content: str) -> str:
    """Keep the Chairman answer but enforce the public Stage Final entry point."""
    stripped = content.strip()
    if stripped.startswith("# Stage Final: Council Answer"):
        return stripped
    return "# Stage Final: Council Answer\n\n" + stripped


def validate_no_counterfactual_self_reference(content: str) -> None:
    """Block self-references that reveal the Chairman dual-call split."""
    for pattern in SELF_REFERENCE_PATTERNS:
        if re.search(pattern, content, flags=re.IGNORECASE):
            raise CouncilValidationError(
                error_code="CHAIRMAN_COUNTERFACTUAL_SELF_REFERENCE",
                message_human=(
                    "La síntesis del Chairman se auto-referencia al counterfactual. "
                    "Eso rompe la separación de llamadas."
                ),
                context={"pattern": pattern},
            )


def _synthesis_context(
    query: str, round1: Round1Result, round2: Round2Result, round3: Round3Result
) -> str:
    round1_text = "\n\n".join(
        f"Seat {response.seat_idx} ({response.model}):\n{response.content}"
        for response in round1.completed
    )
    round2_text = "\n\n".join(
        f"Seat {evaluation.seat_idx} winner={evaluation.winner_label}:\n{evaluation.content}"
        for evaluation in round2.evaluations
    )
    parts = [
        f"Pregunta original:\n{query}",
        f"Round 1 completo:\n{round1_text}",
        f"Round 2 anonimizado:\n{round2_text}",
    ]
    if round3.triggered and round3.counterfactual:
        parts.append(f"Round 3 - argumento contrario externo:\n{round3.counterfactual}")
    else:
        parts.append("Round 3 - argumento contrario externo: no aplicó")
    parts.append("Produce el Stage Final con el formato definido para council-of-intel.")
    return "\n\n".join(parts)
