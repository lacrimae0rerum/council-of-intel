# Release Notes - v0.1.0

Date: 2026-05-09

## Summary

First local Windows onedir release candidate for `council-of-intel`.

The app supports one-shot intelligence council sessions through a packaged Web UI, TUI, local FastAPI backend, OpenRouter model calls, cancellation, local persistence, logs, and Markdown export.

## Included

- Closed personality catalog with 17 personalities and canonical Chairman.
- SATs and Council modes.
- Round 0 validation for mode, seats, model whitelist, chairman, duplicates, and provider diversity warnings.
- OpenRouter async client with retries, timeout handling, and key from environment or local `.env`.
- Deliberation protocol Round 1-4 with anti-convergence counterfactual call.
- Stage Final normalization to enforce `# Stage Final: Council Answer`.
- Local JSON session records plus SQLite index.
- Rotating JSON logs.
- Web UI with session launch, cancel, polling, logs, Markdown export, and compact session list.
- TUI client flow.
- Dry-run model validation.
- Windows PyInstaller onedir package.
- Phase 10 docs: audit, SBOM, threat model, RGPD notes.

## Artifact

- `dist/council-of-intel/council-of-intel.exe`
- `dist/council-of-intel/council-of-intel.bat`
- embedded config, personalities, and static Web UI assets
- `dist/council-of-intel-v0.1.0-windows-onedir.zip`

SHA256:

```text
9D7F85B330D2C90151E632BF8A9A1B5D9C2C9DD1A18AD5FC24AF773F5DB53C6D
```

## Final Gates

- `uv run pytest -q`: 87 passed, coverage 83.71%.
- `uv run ruff check src tests`: passed.
- `uv run python -m compileall -q src`: passed.
- `node node_modules/typescript/bin/tsc -b`: passed.
- `node node_modules/eslint/bin/eslint.js .`: passed.
- Packaged exe `--dry-run`: valid.
- Packaged Web/API TestClient smoke: passed.
- Manual real Web matrix: passed.

## Accepted Risks

- Vitest and Vite dev are blocked in this sandbox by `spawn EPERM`; run them in a normal local dev environment before further frontend work.
- `npm audit` reports five moderate vulnerabilities in the dev chain `vitest/vite-node/esbuild`; fixing requires a Vitest major upgrade.
- PyInstaller onefile is not validated in this sandbox; v0.1.0 ships/supports onedir.

## Operator Notes

Create `.env` next to the executable or export the variable before launch:

```powershell
OPENROUTER_API_KEY=sk-or-v1-...
```

Recommended smoke:

```powershell
.\council-of-intel.exe --dry-run
.\council-of-intel.exe --web
```
