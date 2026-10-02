# AI Task 0131 — Add Legacy-to-Gateway HTTP integration tests

**Status:** Complete

**Created:** 2026-10-02T16:25:59+03:00

**Updated:** 2026-10-02T16:36:10+03:00

**Agent:** Codex

---

# Task

Implement M5-26 only: replace the root Legacy-to-Gateway integration placeholder with tests that exercise the real Legacy JSON HTTP boundary against a live Gateway in classical mode. Verify valid acceptance plus malformed JSON (400), parsed validation failures (422), and duplicate/out-of-order sequence rejections (409). Keep Cloud delivery stubbed only to isolate this boundary. Do not implement M5-27 or later E2E, failure-matrix, Docker, CI, or protocol changes.

---

# Prompt

now, let's implement M5-26–M5-38

---

# AI Implementation — Initial

## LLM Output

Replaced the root M5-26 placeholder with live Legacy-to-Gateway HTTP integration tests. The suite uses the real Legacy Measurement serializer and GatewayClient for valid delivery, raw HTTP for malformed bytes, and a boundary-only accepted baseline transport to isolate Legacy/Gateway behavior.

## Files Created

- docs/ai/history/0129-document-sqlite-persistence-strategy.md
- docs/ai/history/0130-add-ci-contract-test-stage.md
- docs/ai/history/0131-add-legacy-to-gateway-http-integration-tests.md
- docs/deployment/
- tests/test_sqlite_persistence_strategy_document.py

## Files Modified

- .github/workflows/ai-history.yml
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_legacy_gateway.py
- tests/test_ci_workflow.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/integration/test_legacy_gateway.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check tests/integration/test_legacy_gateway.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check && git diff --check

### Results

- Targeted live integration suite passed (8 tests); Ruff passed; Graphify refresh completed; full suite passed (1286 tests); AI-history validation and diff check passed.

## AI Notes

The accepted baseline transport is deliberately a local boundary stub so M5-26 does not implement M5-27 Gateway-to-Cloud integration. No protocol, endpoint, status code, retry, session, crypto, Docker, or CI behavior changed.

---

# Human Review — Round 1

## Problems Found

I do not find any problem during manual review.

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
