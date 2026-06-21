"""Build Stage Final Markdown and export annexes."""

from __future__ import annotations

import re
from collections import Counter

from council_of_intel.output.models import (
    FinalAnswerSections,
    RoundExportAnnexes,
    SatAnnex,
    SessionMetadata,
)

SAT_ANNEX_ORDER = [
    ("ach-analyst", "Matriz ACH"),
    ("key-assumptions-checker", "Supuestos Clave Identificados"),
    ("quality-of-info-auditor", "Auditoría de Calidad de Información"),
    ("indicators-of-change", "Indicadores de Cambio"),
    ("attribution-skeptic", "Atribución — Bandera Roja"),
    ("devils-advocate", "Caso del Devil's Advocate"),
    ("red-team", "Argumento del Red Team"),
]

SELF_REFERENCE_PATTERNS = [
    r"como dije antes en mi argumento adversarial",
    r"como mencion[eé] antes en mi argumento adversarial",
    r"as I said earlier in my adversarial argument",
    r"as I mentioned in my counterfactual",
    r"mi counterfactual anterior",
]


def build_stage_final_markdown(
    sections: FinalAnswerSections,
    metadata: SessionMetadata,
    sat_annexes: list[SatAnnex],
    attribution_query: bool,
) -> str:
    """Build UI-visible Stage Final Markdown."""
    _validate_no_counterfactual_self_reference(sections)
    blocks = [
        _render_core(sections, metadata),
        *_render_sat_annexes(metadata, sat_annexes, attribution_query),
        _render_metadata(metadata),
    ]
    return "\n\n".join(block for block in blocks if block).rstrip() + "\n"


def build_export_markdown(
    sections: FinalAnswerSections,
    metadata: SessionMetadata,
    sat_annexes: list[SatAnnex],
    attribution_query: bool,
    round_annexes: RoundExportAnnexes,
) -> str:
    """Build full Markdown export including round annexes."""
    stage_final = build_stage_final_markdown(
        sections=sections,
        metadata=metadata,
        sat_annexes=sat_annexes,
        attribution_query=attribution_query,
    ).rstrip()
    annex_blocks = [
        f"## Anexo: Round 1 (respuestas individuales)\n{round_annexes.round1}",
        f"## Anexo: Round 2 (cross-examination anonimizada)\n{round_annexes.round2}",
    ]
    if round_annexes.round3:
        annex_blocks.append(f"## Anexo: Round 3 (counterfactual)\n{round_annexes.round3}")
    return stage_final + "\n\n" + "\n\n".join(annex_blocks).rstrip() + "\n"


def _render_core(sections: FinalAnswerSections, metadata: SessionMetadata) -> str:
    discarded = sections.discarded_options
    if len(discarded) < 2:
        raise ValueError("Stage Final needs at least two discarded options")

    return "\n\n".join(
        [
            "# Stage Final: Council Answer\n"
            f"**Chairman:** {metadata.chairman_synthesis_model} · "
            f"{metadata.chairman_personality}\n"
            f"**Respuesta del Consejo:** {sections.chosen_answer}",
            sections.intro,
            _render_discarded_section(1, discarded[0]),
            _render_discarded_section(2, discarded[1]),
            "## 3. Por qué "
            f"{sections.chosen_answer} es la respuesta correcta\n{sections.why_chosen}",
            f"## 4. Formulación recomendada\n{sections.recommended_formulation}",
            _render_conclusion(sections),
            _render_dissent(sections, metadata),
        ]
    )


def _render_discarded_section(index: int, option) -> str:
    return f"## {index}. Por qué {option.name} es {option.problem}\n{option.reasoning}"


def _render_conclusion(sections: FinalAnswerSections) -> str:
    bullets = "\n".join(f"- {bullet}" for bullet in sections.conclusion_bullets)
    return f"## Conclusión\n{bullets}"


def _render_dissent(sections: FinalAnswerSections, metadata: SessionMetadata) -> str:
    if not sections.dissent:
        return (
            "## Dissent registrado\n"
            f"Sin disidencia significativa — los {len(metadata.seats)} seats convergieron "
            "en la misma postura."
        )
    bullets = "\n".join(f"- {item}" for item in sections.dissent)
    return f"## Dissent registrado\n{bullets}"


def _render_sat_annexes(
    metadata: SessionMetadata,
    sat_annexes: list[SatAnnex],
    attribution_query: bool,
) -> list[str]:
    if metadata.mode != "sats":
        return []

    annexes_by_personality: dict[str, list[SatAnnex]] = {}
    for annex in sat_annexes:
        annexes_by_personality.setdefault(annex.personality_id, []).append(annex)

    duplicate_counts = Counter(annex.personality_id for annex in sat_annexes)
    blocks: list[str] = []
    for personality_id, title in SAT_ANNEX_ORDER:
        if personality_id == "attribution-skeptic" and not attribution_query:
            continue
        for annex in annexes_by_personality.get(personality_id, []):
            heading = title
            if duplicate_counts[personality_id] > 1:
                heading = f"{heading} (Seat {annex.seat_idx})"
            blocks.append(f"## Anexo SAT: {heading}\n{annex.content}")
    return blocks


def _render_metadata(metadata: SessionMetadata) -> str:
    mode = "SATs" if metadata.mode == "sats" else "Council"
    seats = "; ".join(f"{seat.model} + {seat.personality_id}" for seat in metadata.seats)
    counterfactual_model = (
        metadata.chairman_counterfactual_model if metadata.counterfactual_triggered else "no aplicó"
    )
    failed = (
        "; ".join(
            f"Seat {seat.seat_idx} {seat.personality_id} {seat.model} (caído: {seat.reason})"
            for seat in metadata.failed_seats
        )
        if metadata.failed_seats
        else "ninguno"
    )
    triggered = "sí" if metadata.counterfactual_triggered else "no"

    return "\n".join(
        [
            "## Metadatos de sesión",
            f"- Modo: {mode}",
            f"- Estado: {metadata.status}",
            f"- Seats: {seats}",
            f"- Chairman síntesis: {metadata.chairman_synthesis_model} + "
            f"{metadata.chairman_personality}",
            f"- Chairman counterfactual: {counterfactual_model}",
            f"- Coste real: {metadata.cost_eur:.2f}€",
            f"- Duración: {metadata.duration_seconds}s",
            f"- Sesión: {metadata.session_id}",
            f"- Counterfactual disparado: {triggered}",
            f"- Seats caídos: {failed}",
        ]
    )


def _validate_no_counterfactual_self_reference(sections: FinalAnswerSections) -> None:
    content = "\n".join(
        [
            sections.intro,
            sections.why_chosen,
            sections.recommended_formulation,
            "\n".join(sections.conclusion_bullets),
            "\n".join(sections.dissent),
        ]
    )
    for pattern in SELF_REFERENCE_PATTERNS:
        if re.search(pattern, content, flags=re.IGNORECASE):
            raise ValueError("Stage Final contains counterfactual self-reference")
