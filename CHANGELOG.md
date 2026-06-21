# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

---

## [0.1.0] - 2026-05-09

### Added

**Core protocol**
- One-shot deliberation protocol Round 0–4 with anti-convergence counterfactual (Round 3 conditional).
- Round 0 validation: mode, seat families, model whitelist, Chairman presence, duplicate seat/model checks, provider diversity warnings.
- Round 1 blind-first parallel seat completions.
- Round 2 cross-examination with `Winner: Response X` parsing and anti-recursion for socratic/KAC seats.
- Round 4 Chairman synthesis with `# Stage Final: Council Answer` normalization.
- Session cancellation during `status == running` with partial-data persistence and OpenRouter in-flight cleanup.

**Modes**
- SATs mode: up to 7 Family-A seats + Chairman; conditional SAT annexes (ACH, Key Assumptions, Indicators of Change, QoI, Attribution, Devil's Advocate, Red Team).
- Council mode: up to 9 Family-B/C seats + Chairman; methodological disagreement, warning intelligence, adversarial analysis.

**Personality catalog**
- 17 personalities across four families: A (7 SAT archetypes), B (5 IC doctrinarians), C (4 cognitive poles), D (McLaughlin, canonical Chairman).
- Data-driven loading from `personalities/<id>/agent.md` + `skill.md` + `knowledge.md`; schema-validated at startup via Pydantic.
- Reserved slots documented: `fer-style`, `santiago-style`.

**OpenRouter integration**
- Async client (`httpx`) with configurable retry, backoff and timeout.
- API key loaded from environment or local `.env`; never logged or exposed via API.
- Model whitelist validated against `GET /models` on `--dry-run`.
- `--dry-run --no-cache` to force model refresh.

**Anonymization and sanitization**
- Round 2 anonymization shuffles seat responses (Response A/B/C) to prevent Chairman bias.
- Sanitizer strips model self-references before cross-examination.

**Storage**
- JSON session records in `sessions/` + SQLite index in `sessions/index.sqlite3`.
- Rotating JSON logs in `logs/`.

**API (FastAPI)**
- `POST /sessions` — create and launch session.
- `GET /sessions/{id}/status` — polling endpoint (1.5s interval default).
- `POST /sessions/{id}/cancel` — cancel running session.
- `GET /sessions` — list sessions with date and preview.
- `GET /sessions/{id}` — full session record.
- `GET /personalities` — catalog with frontmatter.
- `GET /modes` — available modes.
- `GET /config` — active configuration (no secrets).
- `GET /health` — liveness check.
- `POST /sessions/dry-run` — validation without deliberation.
- `GET /logs` — recent log entries.
- `GET /` — SPA fallback (Web UI).

**Web UI (React + Vite + Tailwind)**
- Mode selector (SATs / Council).
- Drag-and-drop seat list with per-mode state (`seatsByMode`).
- Session launch with real-time status polling.
- Cancel button available during `status == running`.
- Log viewer.
- Markdown export (downloads `.md`).
- Session list with date and content preview.
- Blocks duplicate seat+model combos and duplicate models in Council mode.
- Seat defaults derived from personality catalog (`recommended_model`).

**TUI (Textual)**
- Full session flow: mode, seats, query, launch, poll, cancel, result display.
- Same backend as the Web UI.

**CLI launcher**
- `--tui`, `--web`, `--dry-run` flags.
- Interactive menu when launched without arguments: `[1] TUI · [2] Web · [3] Dry-run`.
- Port fallback range for `--web` (default 8000–8010).
- `.env` loaded at launch without overriding shell-exported variables.

**Distribution**
- Windows PyInstaller onedir package (`dist/council-of-intel/council-of-intel.exe`).
- `.bat` launcher (`council-of-intel.bat`).
- Embedded config, personalities, and static Web UI assets (`_MEIPASS` resource resolution).
- Release artifact: `dist/council-of-intel-v0.1.0-windows-onedir.zip` (SHA256: `9D7F85B330D2C90151E632BF8A9A1B5D9C2C9DD1A18AD5FC24AF773F5DB53C6D`).

**Testing**
- 87 backend tests passing, coverage 83.71%.
- ruff, compileall, tsc, eslint: all passing.

**Security and compliance docs**
- `docs/AUDIT.md`, `docs/SBOM.md`, `docs/THREAT_MODEL.md`, `docs/RGPD.md`.

### Known issues

- Vitest and Vite dev blocked by `spawn EPERM` in sandbox; run in a normal local environment.
- `npm audit` reports 5 moderate vulnerabilities in dev chain `vitest/vite-node/esbuild`; not present in production bundle.
- PyInstaller onefile not validated; only onedir is supported.
- Personality prompts are structurally valid but thin; analytical differentiation is addressed in Phase 12.

[Unreleased]: https://github.com/lacrimae0rerum/council-of-intel/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/lacrimae0rerum/council-of-intel/releases/tag/v0.1.0
