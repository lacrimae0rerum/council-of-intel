import pytest

from council_of_intel.config import load_config
from council_of_intel.errors import CouncilValidationError
from council_of_intel.openrouter.client import (
    ChatCompletionRequest,
    ChatCompletionResult,
    OpenRouterRequestError,
)
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.protocol.engine import DeliberationProtocol
from council_of_intel.validation import SeatConfig


class FailingProtocolClient:
    """Client that always raises OpenRouterRequestError to simulate network failures."""

    async def complete_chat(self, request: ChatCompletionRequest) -> ChatCompletionResult:
        raise OpenRouterRequestError(request.seat_idx, request.model, "simulated network failure")


class FakeProtocolClient:
    def __init__(self, outputs: list[str]) -> None:
        self.outputs = list(outputs)
        self.requests: list[ChatCompletionRequest] = []

    async def complete_chat(self, request: ChatCompletionRequest) -> ChatCompletionResult:
        self.requests.append(request)
        content = self.outputs.pop(0)
        return ChatCompletionResult(
            seat_idx=request.seat_idx,
            model=request.model,
            content=content,
            usage_cost=0.1,
            raw_response={"choices": [{"message": {"content": content}}], "usage": {"cost": 0.1}},
        )


@pytest.fixture
def config_and_catalog():
    return load_config(), load_personalities()


def _council_seats() -> list[SeatConfig]:
    return [
        SeatConfig(personality_id="kent", model="openai/gpt-5.5"),
        SeatConfig(personality_id="heuer", model="anthropic/claude-sonnet-4.6"),
        SeatConfig(personality_id="feynman", model="google/gemini-3.1-pro-preview"),
    ]


@pytest.mark.asyncio
async def test_round3_triggers_counterfactual_when_agreement_above_threshold(
    config_and_catalog,
) -> None:
    config, catalog = config_and_catalog
    client = FakeProtocolClient(
        [
            "R1 Kent",
            "R1 Heuer",
            "R1 Feynman",
            "Winner: Response A\nEngage: B and C are weaker.",
            "Winner: Response A\nEngage: B and C are weaker.",
            "Winner: Response A\nEngage: B and C are weaker.",
            "Argumento contrario fuerte.",
            "# Stage Final: Council Answer\nSin auto-referencia.",
        ]
    )

    result = await DeliberationProtocol(config, catalog, client, anonymizer_seed=1).run(
        query="Que esta pasando?",
        mode="council",
        seats=_council_seats(),
        chairman_personality_id="mclaughlin",
    )

    assert result.status == "completed"
    assert result.counterfactual_triggered is True
    assert result.counterfactual == "Argumento contrario fuerte."
    assert client.requests[-2].model == config.chairman_model_counterfactual
    assert "voz adversarial neutra" in client.requests[-2].messages[0].content
    assert "Chairman" not in client.requests[-2].messages[0].content
    assert "argumento contrario externo" in client.requests[-1].messages[-1].content


@pytest.mark.asyncio
async def test_round3_skips_counterfactual_when_agreement_below_threshold(
    config_and_catalog,
) -> None:
    config, catalog = config_and_catalog
    client = FakeProtocolClient(
        [
            "R1 Kent",
            "R1 Heuer",
            "R1 Feynman",
            "Winner: Response A\nEngage: B and C.",
            "Winner: Response B\nEngage: A and C.",
            "Winner: Response C\nEngage: A and B.",
            "# Stage Final: Council Answer\nSin counterfactual.",
        ]
    )

    result = await DeliberationProtocol(config, catalog, client, anonymizer_seed=2).run(
        query="Que esta pasando?",
        mode="council",
        seats=_council_seats(),
        chairman_personality_id="mclaughlin",
    )

    assert result.status == "completed"
    assert result.counterfactual_triggered is False
    assert result.counterfactual is None
    assert len(client.requests) == 7
    assert client.requests[-1].model == config.chairman_model_synthesis


@pytest.mark.asyncio
async def test_round4_wraps_noncanonical_chairman_heading(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    client = FakeProtocolClient(
        [
            "R1 Kent",
            "R1 Heuer",
            "R1 Feynman",
            "Winner: Response A\nEngage: B and C.",
            "Winner: Response B\nEngage: A and C.",
            "Winner: Response C\nEngage: A and B.",
            "# ESTIMACIÓN FINAL DEL CHAIRMAN\n\nFinal con formato libre.",
        ]
    )

    result = await DeliberationProtocol(config, catalog, client, anonymizer_seed=2).run(
        query="Que esta pasando?",
        mode="council",
        seats=_council_seats(),
        chairman_personality_id="mclaughlin",
    )

    assert result.final_answer is not None
    assert result.final_answer.startswith("# Stage Final: Council Answer\n\n# ESTIMACIÓN")


@pytest.mark.asyncio
async def test_round2_retries_socrates_when_response_is_only_questions(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    seats = [
        SeatConfig(personality_id="socrates", model="openai/gpt-5.5"),
        SeatConfig(personality_id="heuer", model="anthropic/claude-sonnet-4.6"),
        SeatConfig(personality_id="feynman", model="google/gemini-3.1-pro-preview"),
    ]
    client = FakeProtocolClient(
        [
            "R1 Socrates",
            "R1 Heuer",
            "R1 Feynman",
            "¿Que suponemos? ¿Que falta? ¿Y si no?",
            "Winner: Response A\nPostura: A gana. Engage: B y C flojean.",
            "Winner: Response A\nEngage: B and C.",
            "Winner: Response A\nEngage: B and C.",
            "Argumento contrario.",
            "# Stage Final: Council Answer\nSocrates tomo postura.",
        ]
    )

    result = await DeliberationProtocol(config, catalog, client, anonymizer_seed=3).run(
        query="Que esta pasando?",
        mode="council",
        seats=seats,
        chairman_personality_id="mclaughlin",
    )

    retry_requests = [
        request
        for request in client.requests
        if request.seat_idx == 0
        and "toma postura, no solo preguntes" in request.messages[-1].content
    ]
    assert result.status == "completed"
    assert len(retry_requests) == 1


@pytest.mark.asyncio
async def test_round4_rejects_chairman_self_reference_to_counterfactual(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    client = FakeProtocolClient(
        [
            "R1 Kent",
            "R1 Heuer",
            "R1 Feynman",
            "Winner: Response A\nEngage: B and C.",
            "Winner: Response A\nEngage: B and C.",
            "Winner: Response A\nEngage: B and C.",
            "Argumento contrario fuerte.",
            "Como dije antes en mi argumento adversarial, la tesis falla.",
        ]
    )

    with pytest.raises(CouncilValidationError) as exc_info:
        await DeliberationProtocol(config, catalog, client, anonymizer_seed=4).run(
            query="Que esta pasando?",
            mode="council",
            seats=_council_seats(),
            chairman_personality_id="mclaughlin",
        )

    assert exc_info.value.error_code == "CHAIRMAN_COUNTERFACTUAL_SELF_REFERENCE"


@pytest.mark.asyncio
async def test_protocol_aborts_when_all_round1_seats_fail(config_and_catalog) -> None:
    config, catalog = config_and_catalog
    client = FailingProtocolClient()

    result = await DeliberationProtocol(config, catalog, client).run(
        query="Que esta pasando?",
        mode="council",
        seats=_council_seats(),
        chairman_personality_id="mclaughlin",
    )

    assert result.status == "aborted_insufficient_seats"
    assert result.round2 is None
    assert result.final_answer is None
    assert len(result.round1.failed) == len(_council_seats())
