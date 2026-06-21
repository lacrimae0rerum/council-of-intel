import pytest

from council_of_intel.openrouter.sanitizer import sanitize_model_self_references

TRAP_PHRASES = [
    "as an Anthropic model, I would assess this differently",
    "I'm GPT and my view is cautious",
    "I am GPT-5, so I cannot know that",
    "I'm Claude, but the evidence says no",
    "I am Claude from Anthropic",
    "I'm Gemini and this looks weak",
    "como Claude, diria que falta evidencia",
    "como modelo de OpenAI, no puedo atribuirlo",
    "soy un modelo de lenguaje grande entrenado por OpenAI",
    "as a large language model, I cannot browse",
    "as an AI language model, I have no beliefs",
    "como IA, no tengo preferencias",
    "as a language model, I would avoid certainty",
    "I am an AI developed by Anthropic",
    "I am an OpenAI model",
    "as ChatGPT, I would say",
    "como ChatGPT, no tengo acceso",
    "as Gemini, I cannot verify",
    "I'm an LLM, not an analyst",
    "como LLM, responderia",
    "as a machine learning model, I lack context",
]


@pytest.mark.parametrize("phrase", TRAP_PHRASES)
def test_sanitizer_removes_model_self_references(phrase: str) -> None:
    sanitized = sanitize_model_self_references(phrase)

    lowered = sanitized.lower()
    assert "anthropic" not in lowered
    assert "openai" not in lowered
    assert "claude" not in lowered
    assert "gpt" not in lowered
    assert "gemini" not in lowered
    assert "chatgpt" not in lowered
    assert "large language model" not in lowered
    assert "modelo de lenguaje" not in lowered
    assert "llm" not in lowered


def test_sanitizer_preserves_substantive_content() -> None:
    text = (
        "as an Anthropic model, "
        "I assess attribution as baja confianza por falta de victimologia."
    )

    assert sanitize_model_self_references(text) == (
        "I assess attribution as baja confianza por falta de victimologia."
    )
