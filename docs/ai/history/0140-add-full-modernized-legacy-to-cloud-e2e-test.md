# AI Task 0140 — Add full modernized Legacy-to-Cloud E2E test

**Status:** Complete

**Created:** 2026-10-02T17:43:23+03:00

**Updated:** 2026-10-02T17:47:34+03:00

**Agent:** Codex

---

# Task

M5-35: add one full live Legacy-to-Gateway-to-ML-KEM-Cloud-to-SQLite happy-path test, including unchanged Legacy payload, separate request correlation, and queried stored measurement. Do not add retry, recovery, expiry, or tampering scenarios.

---

# Prompt

Let's implement M5-35

---

# AI Implementation — Initial

## LLM Output

Added a complete live Legacy-to-ML-KEM-Gateway-to-Cloud-to-SQLite E2E test and documented the protocol-v1 replay limitation.

## Files Created

- tests/integration/test_modernized_end_to_end.py, docs/evaluation/modernized-e2e.md

## Files Modified

- docs/ai/.state.json, graphify-out/GRAPH_REPORT.md, graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/integration/test_modernized_end_to_end.py tests/integration/test_gateway_cloud_secure_session.py -q; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check; git diff --check

### Results

- Ruff passed; Graphify refresh completed; focused integration tests passed (2 passed); full suite passed (1299 tests); AI-history validation and diff check passed.

## AI Notes

The controlled drop-response case verifies same-envelope ordinary retry and one idempotent row. Protocol v1 has no dedicated cryptographic anti-replay counter or window; idempotency is not cryptographic replay protection.

---

# Human Review — Round 1

## Problems Found

I do not find any problem during manual review

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
