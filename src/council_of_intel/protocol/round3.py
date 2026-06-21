"""Round 3 anti-convergence and Chairman counterfactual."""

from __future__ import annotations

from collections import Counter
from typing import Protocol

from council_of_intel.config import AppConfig
from council_of_intel.openrouter.client import (
    ChatCompletionRequest,
    ChatCompletionResult,
    ChatMessage,
)
from council_of_intel.protocol.models import Round2Result, Round3Result

COUNTERFACTUAL_SYSTEM_PROMPT = (
    "Eres una voz adversarial neutra. Tu única tarea es construir el mejor argumento posible "
    "contra la siguiente respuesta consenso, sin valorarla; solo presentando el caso contrario "
    "con fuerza. Máximo 200 palabras."
)


class CompletionClient(Protocol):
    """Protocol for anything that can complete a chat request."""

    async def complete_chat(self, request: ChatCompletionRequest) -> ChatCompletionResult: ...


async def run_round3(
    round2: Round2Result,
    config: AppConfig,
    client: CompletionClient,
) -> Round3Result:
    """Trigger counterfactual if aggregated winner agreement is above threshold."""
    winner_labels = [
        evaluation.winner_label for evaluation in round2.evaluations if evaluation.winner_label
    ]
    if not winner_labels:
        return Round3Result(triggered=False)

    consensus_label, count = Counter(winner_labels).most_common(1)[0]
    agreement_ratio = count / len(round2.evaluations)
    if agreement_ratio <= config.anticonvergence.agreement_threshold:
        return Round3Result(
            triggered=False,
            consensus_label=consensus_label,
            agreement_ratio=agreement_ratio,
        )

    consensus_content = _content_for_label(round2, consensus_label)
    request = ChatCompletionRequest(
        seat_idx=0,
        model=config.chairman_model_counterfactual,
        messages=[
            ChatMessage(role="system", content=COUNTERFACTUAL_SYSTEM_PROMPT),
            ChatMessage(
                role="user",
                content=f"Respuesta consenso ({consensus_label}):\n{consensus_content}",
            ),
        ],
        max_tokens=config.anticonvergence.counterfactual_max_words * 4,
    )
    response = await client.complete_chat(request)
    return Round3Result(
        triggered=True,
        consensus_label=consensus_label,
        agreement_ratio=agreement_ratio,
        counterfactual=response.content,
        usage_cost=response.usage_cost,
    )


def _content_for_label(round2: Round2Result, label: str) -> str:
    for item in round2.anonymized.items:
        if item.label == label:
            return item.content
    return ""
