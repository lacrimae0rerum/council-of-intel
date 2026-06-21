"""Sanitize model/provider self-identification before cross-examination."""

from __future__ import annotations

import re

SELF_REFERENCE_PATTERNS = [
    r"\bas an Anthropic model,?\s*",
    r"\bas an OpenAI model,?\s*",
    r"\bas ChatGPT,?\s*",
    r"\bas Gemini,?\s*",
    r"\bas an AI language model,?\s*",
    r"\bas a large language model,?\s*",
    r"\bas a language model,?\s*",
    r"\bas a machine learning model,?\s*",
    r"\bI'm GPT[-\w.]*,?\s*",
    r"\bI am GPT[-\w.]*,?\s*",
    r"\bI'm Claude,?\s*",
    r"\bI am Claude from Anthropic,?\s*",
    r"\bI'm Gemini,?\s*",
    r"\bI'm an LLM,?\s*",
    r"\bI am an AI developed by Anthropic,?\s*",
    r"\bI am an OpenAI model,?\s*",
    r"\bcomo Claude,?\s*",
    r"\bcomo modelo de OpenAI,?\s*",
    r"\bsoy un modelo de lenguaje grande entrenado por OpenAI,?\s*",
    r"\bcomo ChatGPT,?\s*",
    r"\bcomo IA,?\s*",
    r"\bcomo LLM,?\s*",
]


def sanitize_model_self_references(text: str) -> str:
    """Remove provider/model self-identification while preserving analysis content."""
    sanitized = text
    for pattern in SELF_REFERENCE_PATTERNS:
        sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    sanitized = re.sub(r"^[,;:\-\s]+", "", sanitized).strip()
    return sanitized
