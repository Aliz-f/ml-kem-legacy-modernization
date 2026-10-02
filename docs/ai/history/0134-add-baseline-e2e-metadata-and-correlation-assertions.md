# AI Task 0134 — Add baseline E2E metadata and correlation assertions

**Status:** Complete

**Created:** 2026-10-02T16:45:27+03:00

**Updated:** 2026-10-02T16:47:54+03:00

**Agent:** Codex

---

# Task

Implement M5-29 only: extend the root baseline E2E test with assertions for Gateway canonical received_at, received_at to gateway_received_at mapping, Cloud-added cloud_received_at, configured gateway_id, header-only X-Request-ID correlation in Cloud logs/tracing, and absence of request_id from canonical JSON. Preserve the existing happy path and do not implement baseline freeze, performance measurement, secure mode, Docker, or protocol changes.

---

# Prompt

let's implement M5-29

---

# AI Implementation — Initial

## LLM Output

Extended the root baseline E2E test with M5-29 metadata and trace assertions. It now captures the Gateway-to-Cloud baseline request, proves the exact canonical seven-field body excludes request_id, verifies X-Request-ID reaches Cloud logging, and checks Gateway/Cloud timestamps, gateway identity, and record ID in the persisted row.

## Files Created

- docs/ai/history/0129-document-sqlite-persistence-strategy.md
- docs/ai/history/0130-add-ci-contract-test-stage.md
- docs/ai/history/0131-add-legacy-to-gateway-http-integration-tests.md
- docs/ai/history/0132-add-gateway-to-cloud-baseline-integration-test.md
- docs/ai/history/0133-add-full-baseline-end-to-end-test.md
- docs/ai/history/0134-add-baseline-e2e-metadata-and-correlation-assertions.md
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

- Targeted baseline E2E test passed (1 test); Ruff passed; Graphify refresh completed; full suite passed (1288 tests); AI-history validation and diff check passed.

## AI Notes

M5-29 adds assertions only. M5-30 baseline freeze and M5-31 measurement harness remain untouched; no protocol, endpoint, storage, Docker, dependency, or runtime behavior changed.

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

I verify it.

---

# Final Outcome

**Status:** Complete
