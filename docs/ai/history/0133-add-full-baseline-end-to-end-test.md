# AI Task 0133 — Add full baseline end-to-end test

**Status:** Complete

**Created:** 2026-10-02T16:40:52+03:00

**Updated:** 2026-10-02T16:43:45+03:00

**Agent:** Codex

---

# Task

Implement M5-28 only: replace the root full-system test placeholder with one happy-path baseline test that starts production Cloud and Gateway instances, sends the deterministic Legacy measurement through the real Legacy serializer/client, queries Cloud, and compares original logical values with the stored row. Keep detailed metadata/correlation assertions for M5-29 and do not implement baseline freeze, benchmarks, secure mode, Docker, or protocol changes.

---

# Prompt

Let's implement these tasks: M5-28, M5-29, M5-30, M5-31

---

# AI Implementation — Initial

## LLM Output

Replaced the root full-system placeholder with a happy-path baseline E2E test. It starts production Cloud and Gateway instances, sends the frozen Legacy fixture through the real Measurement serializer and GatewayClient, queries Cloud, and verifies original logical measurement values in the persisted row.

## Files Created

- docs/ai/history/0129-document-sqlite-persistence-strategy.md
- docs/ai/history/0130-add-ci-contract-test-stage.md
- docs/ai/history/0131-add-legacy-to-gateway-http-integration-tests.md
- docs/ai/history/0132-add-gateway-to-cloud-baseline-integration-test.md
- docs/ai/history/0133-add-full-baseline-end-to-end-test.md
- docs/deployment/
- tests/test_sqlite_persistence_strategy_document.py

## Files Modified

- .github/workflows/ai-history.yml
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_end_to_end.py
- tests/integration/test_gateway_cloud_baseline.py
- tests/integration/test_legacy_gateway.py
- tests/test_ci_workflow.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/integration/test_end_to_end.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check tests/integration/test_end_to_end.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check && git diff --check

### Results

- Targeted full baseline E2E test passed (1 test); Ruff passed; Graphify refresh completed; full suite passed (1288 tests); AI-history validation and diff check passed.

## AI Notes

M5-28 covers the composed happy path only. Detailed Gateway/Cloud metadata, correlation, and canonical-field assertions remain M5-29; baseline freeze and measurements remain M5-30/M5-31. No protocol, Docker, dependency, or runtime behavior changed.

---

# Human Review — Round 1

## Problems Found

I do not find any problems during manual review.

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
