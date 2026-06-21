import pytest

from council_of_intel.output.builder import build_export_markdown, build_stage_final_markdown
from council_of_intel.output.models import (
    DiscardedOption,
    FailedSeat,
    FinalAnswerSections,
    RoundExportAnnexes,
    SatAnnex,
    SeatMetadata,
    SessionMetadata,
)


def _sections(dissent: list[str] | None = None) -> FinalAnswerSections:
    return FinalAnswerSections(
        chairman_personality="mclaughlin",
        chosen_answer="La tesis principal es intrusión oportunista con tooling compartido.",
        intro=(
            "3 de 4 seats convergen: hay actividad real, pero la atribución fuerte no aguanta."
        ),
        discarded_options=[
            DiscardedOption(
                name="atribución estatal directa",
                problem="insuficiente",
                reasoning="La evidencia técnica no discrimina actor y la victimología es débil.",
            ),
            DiscardedOption(
                name="falso positivo operativo",
                problem="poco plausible",
                reasoning="Hay persistencia y selección de objetivos incompatible con ruido puro.",
            ),
        ],
        why_chosen=(
            "La explicación oportunista encaja con los TTPs observados "
            "y no exige suposiciones extra."
        ),
        recommended_formulation=(
            "Evaluamos con confianza moderada que la campaña es oportunista "
            "y de atribución abierta."
        ),
        conclusion_bullets=[
            "No atribuir a actor estatal sin nueva evidencia.",
            "Priorizar colección sobre infraestructura y victimología.",
        ],
        dissent=dissent or [],
    )


def _metadata(status: str = "completed") -> SessionMetadata:
    return SessionMetadata(
        mode="sats",
        status=status,
        seats=[
            SeatMetadata(0, "ach-analyst", "anthropic/claude-sonnet-4.6"),
            SeatMetadata(1, "quality-of-info-auditor", "google/gemini-3.1-pro-preview"),
            SeatMetadata(2, "red-team", "x-ai/grok-4.3"),
            SeatMetadata(3, "devils-advocate", "openai/gpt-chat-latest"),
        ],
        chairman_synthesis_model="anthropic/claude-opus-4.7",
        chairman_personality="mclaughlin",
        chairman_counterfactual_model="openai/gpt-5.5",
        counterfactual_triggered=True,
        cost_eur=1.234,
        duration_seconds=87,
        session_id="01HZTEST",
        failed_seats=[
            FailedSeat(4, "attribution-skeptic", "deepseek/deepseek-v3.2", "timeout")
        ],
    )


def test_build_stage_final_snapshot() -> None:
    markdown = build_stage_final_markdown(
        sections=_sections(dissent=["Red Team mantiene que deception sigue abierta."]),
        metadata=_metadata(),
        sat_annexes=[
            SatAnnex("ach-analyst", 0, "ACH: H1 gana por menor inconsistencia."),
            SatAnnex("quality-of-info-auditor", 1, "Admiralty: B2, circularidad parcial."),
            SatAnnex("red-team", 2, "Caso alternativo: deception viable pero no dominante."),
        ],
        attribution_query=False,
    )

    expected = "\n".join(
        [
            "# Stage Final: Council Answer",
            "**Chairman:** anthropic/claude-opus-4.7 · mclaughlin",
            "**Respuesta del Consejo:** "
            "La tesis principal es intrusión oportunista con tooling compartido.",
            "",
            "3 de 4 seats convergen: hay actividad real, "
            "pero la atribución fuerte no aguanta.",
            "",
            "## 1. Por qué atribución estatal directa es insuficiente",
            "La evidencia técnica no discrimina actor y la victimología es débil.",
            "",
            "## 2. Por qué falso positivo operativo es poco plausible",
            "Hay persistencia y selección de objetivos incompatible con ruido puro.",
            "",
            "## 3. Por qué La tesis principal es intrusión oportunista con "
            "tooling compartido. es la respuesta correcta",
            "La explicación oportunista encaja con los TTPs observados "
            "y no exige suposiciones extra.",
            "",
            "## 4. Formulación recomendada",
            "Evaluamos con confianza moderada que la campaña es oportunista "
            "y de atribución abierta.",
            "",
            "## Conclusión",
            "- No atribuir a actor estatal sin nueva evidencia.",
            "- Priorizar colección sobre infraestructura y victimología.",
            "",
            "## Dissent registrado",
            "- Red Team mantiene que deception sigue abierta.",
            "",
            "## Anexo SAT: Matriz ACH",
            "ACH: H1 gana por menor inconsistencia.",
            "",
            "## Anexo SAT: Auditoría de Calidad de Información",
            "Admiralty: B2, circularidad parcial.",
            "",
            "## Anexo SAT: Argumento del Red Team",
            "Caso alternativo: deception viable pero no dominante.",
            "",
            "## Metadatos de sesión",
            "- Modo: SATs",
            "- Estado: completed",
            "- Seats: anthropic/claude-sonnet-4.6 + ach-analyst; "
            "google/gemini-3.1-pro-preview + quality-of-info-auditor; "
            "x-ai/grok-4.3 + red-team; "
            "openai/gpt-chat-latest + devils-advocate",
            "- Chairman síntesis: anthropic/claude-opus-4.7 + mclaughlin",
            "- Chairman counterfactual: openai/gpt-5.5",
            "- Coste real: 1.23€",
            "- Duración: 87s",
            "- Sesión: 01HZTEST",
            "- Counterfactual disparado: sí",
            "- Seats caídos: Seat 4 attribution-skeptic "
            "deepseek/deepseek-v3.2 (caído: timeout)",
            "",
        ]
    )
    assert markdown == expected


def test_dissent_registrado_is_always_present_when_empty() -> None:
    markdown = build_stage_final_markdown(
        sections=_sections(dissent=[]),
        metadata=_metadata(),
        sat_annexes=[],
        attribution_query=False,
    )

    assert "## Dissent registrado" in markdown
    assert (
        "Sin disidencia significativa — los 4 seats convergieron en la misma postura."
        in markdown
    )


def test_sat_annexes_render_in_fixed_order_and_duplicate_suffixes() -> None:
    markdown = build_stage_final_markdown(
        sections=_sections(),
        metadata=_metadata(),
        sat_annexes=[
            SatAnnex("red-team", 6, "Red late."),
            SatAnnex("ach-analyst", 5, "ACH duplicate."),
            SatAnnex("devils-advocate", 3, "Devils."),
            SatAnnex("ach-analyst", 0, "ACH first."),
            SatAnnex("indicators-of-change", 2, "IoC."),
            SatAnnex("attribution-skeptic", 4, "Attribution red flags."),
        ],
        attribution_query=True,
    )

    headings = [line for line in markdown.splitlines() if line.startswith("## Anexo SAT:")]
    assert headings == [
        "## Anexo SAT: Matriz ACH (Seat 5)",
        "## Anexo SAT: Matriz ACH (Seat 0)",
        "## Anexo SAT: Indicadores de Cambio",
        "## Anexo SAT: Atribución — Bandera Roja",
        "## Anexo SAT: Caso del Devil's Advocate",
        "## Anexo SAT: Argumento del Red Team",
    ]


def test_export_markdown_includes_round_annexes() -> None:
    markdown = build_export_markdown(
        sections=_sections(),
        metadata=_metadata(),
        sat_annexes=[],
        attribution_query=False,
        round_annexes=RoundExportAnnexes(
            round1="Seat 0: respuesta individual.",
            round2="Response A ranking.",
            round3="Counterfactual externo.",
        ),
    )

    assert "## Anexo: Round 1 (respuestas individuales)" in markdown
    assert "Seat 0: respuesta individual." in markdown
    assert "## Anexo: Round 2 (cross-examination anonimizada)" in markdown
    assert "## Anexo: Round 3 (counterfactual)" in markdown


def test_cancelled_sessions_reflect_status_in_metadata() -> None:
    markdown = build_stage_final_markdown(
        sections=_sections(),
        metadata=_metadata(status="cancelled_by_user"),
        sat_annexes=[],
        attribution_query=False,
    )

    assert "- Estado: cancelled_by_user" in markdown


def test_stage_builder_rejects_counterfactual_self_reference() -> None:
    with pytest.raises(ValueError, match="counterfactual"):
        build_stage_final_markdown(
            sections=_sections(
                dissent=["Como dije antes en mi argumento adversarial, esto no cuadra."]
            ),
            metadata=_metadata(),
            sat_annexes=[],
            attribution_query=False,
        )
