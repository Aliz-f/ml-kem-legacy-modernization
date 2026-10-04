# AI Task 0172 — Add live Gateway and Cloud metrics sanity tests

**Status:** Complete

**Created:** 2026-10-04T00:42:14+03:00

**Updated:** 2026-10-04T00:45:44+03:00

**Agent:** Codex

---

# Task

Implement M5-54 only. Add focused live metrics sanity tests for valid deliveries, corrupted secure ciphertext, and ambiguous same-envelope retry/idempotency. Preserve frozen metric names, protocol behavior, application ownership, and existing uncommitted work.

---

# Prompt

Implement m5-54

---

# AI Implementation — Initial

## LLM Output

Completed M5-54 by adding live Gateway/Cloud metrics sanity tests and selecting them explicitly in CI. The tests verify five valid classical deliveries increment Gateway receive/accept/send and Cloud baseline/store counters; corrupted ML-KEM ciphertext increments Cloud decryption rejection metrics without storage and leaves fallback at zero; and one ambiguous secure retry increments the Gateway retry counter while Cloud stores exactly one logical row and records one idempotent duplicate.

## Files Created

- docs/ai/history/0169-validate-gateway-and-cloud-container-health-and-readiness.md
- docs/ai/history/0170-add-explicit-integration-and-end-to-end-ci-stages.md
- docs/ai/history/0171-validate-ai-history-clean-environment-compatibility.md
- docs/ai/history/0172-add-live-gateway-and-cloud-metrics-sanity-tests.md
- tests/integration/test_metrics_sanity.py

## Files Modified

- .github/workflows/ai-history.yml
- docker-compose.yml
- docs/ai/.state.json
- docs/ai/README.md
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_gateway_compose_e2e.py
- tests/test_ci_workflow.py
- tests/test_gateway_docker_assets.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .; uv run pytest -q tests/test_ci_workflow.py tests/integration/test_metrics_sanity.py tests/integration/test_observability_integration.py tests/test_metrics_conventions_document.py; uv run python scripts/refresh_graphify.py; uv run ai-history check; git diff --check

### Results

- Passed: Ruff; focused CI/metrics/observability tests (15 passed); Graphify refresh; AI-history validation; diff check.

## AI Notes

Existing uncommitted M5-09 through M5-23 work was preserved. The tests use production Gateway and Cloud applications over loopback HTTP and do not change metrics contracts, protocol behavior, or component ownership.

---

# Human Review — Round 1

## Problems Found

No problems reported during manual review.

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
