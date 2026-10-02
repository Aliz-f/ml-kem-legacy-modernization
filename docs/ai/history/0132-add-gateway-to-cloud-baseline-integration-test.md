# AI Task 0132 — Add Gateway-to-Cloud baseline integration test

**Status:** Complete

**Created:** 2026-10-02T16:37:02+03:00

**Updated:** 2026-10-02T16:39:51+03:00

**Agent:** Codex

---

# Task

Implement M5-27 only: replace the root Gateway-to-Cloud baseline integration placeholder with a live production Cloud test driven by the real Gateway BaselineCloudClient. Verify exact canonical JSON without request_id, X-Request-ID propagation to Cloud logs/tracing, idempotent storage, received_at to gateway_received_at mapping, Cloud-added cloud_received_at, and record_id creation. Do not implement M5-28 or later full Legacy E2E, Docker, failure orchestration, or protocol changes.

---

# Prompt

let's implement M5-27

---

# AI Implementation — Initial

## LLM Output

Replaced the root M5-27 placeholder with a live production Cloud integration test driven by the real Gateway BaselineCloudClient. It verifies canonical wire preservation, header-only request correlation, Cloud idempotency, received_at to gateway_received_at storage mapping, record ID creation, and Cloud-added receipt timestamp.

## Files Created

- docs/ai/history/0129-document-sqlite-persistence-strategy.md
- docs/ai/history/0130-add-ci-contract-test-stage.md
- docs/ai/history/0131-add-legacy-to-gateway-http-integration-tests.md
- docs/ai/history/0132-add-gateway-to-cloud-baseline-integration-test.md
- docs/deployment/
- tests/test_sqlite_persistence_strategy_document.py

## Files Modified

- .github/workflows/ai-history.yml
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_gateway_cloud_baseline.py
- tests/integration/test_legacy_gateway.py
- tests/test_ci_workflow.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/integration/test_gateway_cloud_baseline.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check tests/integration/test_gateway_cloud_baseline.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest && UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check && git diff --check

### Results

- Targeted live integration test passed (1 test); Ruff passed; Graphify refresh completed; full suite passed (1287 tests); AI-history validation and diff check passed.

## AI Notes

This test isolates the Gateway-to-Cloud baseline boundary by using the real Gateway client and production Cloud routes. It does not start the Legacy endpoint, Docker, M5-28 full E2E, or any protocol/runtime behavior change.

---

# Human Review — Round 1

## Problems Found

I do not find any problem during manual preview.

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
