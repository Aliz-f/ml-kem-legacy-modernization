# AI Task 0130 — Add CI contract-test stage

**Status:** Complete

**Created:** 2026-10-02T16:04:52+03:00

**Updated:** 2026-10-02T16:25:26+03:00

**Agent:** Codex

---

# Task

Implement M5-19 only: add an explicit GitHub Actions contract-test stage after the existing unit-test stage. Run a focused existing suite that verifies the frozen Legacy payload, canonical baseline mapping and X-Request-ID, public-key/session wire contracts, SecureEnvelope/AAD, HKDF parameters, nonce length, and session error codes. Add focused CI workflow regression coverage. Do not change application protocol code, introduce new protocol fields, add Docker/integration/E2E stages, or modify component ownership.

---

# Prompt

let's implement task M5-19

---

# AI Implementation — Initial

## LLM Output

Added an explicit GitHub Actions protocol contract-test stage after the unit-test stage. It runs the existing focused tests for Legacy/canonical schemas, baseline X-Request-ID mapping, public-key and session wire contracts, HKDF, SecureEnvelope, four-field AAD, nonce validation, and session errors. Extended CI workflow regression coverage to lock the stage, selected suite, and ordering.

## Files Created

- docs/ai/history/0129-document-sqlite-persistence-strategy.md
- docs/ai/history/0130-add-ci-contract-test-stage.md
- docs/deployment/
- tests/test_sqlite_persistence_strategy_document.py

## Files Modified

- .github/workflows/ai-history.yml
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/test_ci_workflow.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/test_ci_workflow.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check . && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest [247-test contract suite] && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check && git diff --check

### Results

- CI workflow regression tests passed (2 tests); Ruff passed; selected contract suite passed (247 tests, one existing Starlette/httpx deprecation warning); Graphify refresh completed; full suite passed (1278 tests); AI-history validation and diff check passed.

## AI Notes

No endpoint, schema, crypto, retry, session, storage, dependency, Docker, integration-stage, or E2E-stage behavior changed. The CI stage reuses component-owned boundary tests rather than importing application models to create a new shared contract layer.

---

# Human Review — Round 1

## Problems Found

I do not find any problems durin manual review.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I verify it

---

# Final Outcome

**Status:** Complete
