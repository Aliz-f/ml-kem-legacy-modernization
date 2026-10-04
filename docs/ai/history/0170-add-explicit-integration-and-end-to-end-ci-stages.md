# AI Task 0170 — Add explicit integration and end-to-end CI stages

**Status:** Complete

**Created:** 2026-10-04T00:35:17+03:00

**Updated:** 2026-10-04T00:38:20+03:00

**Agent:** Codex

---

# Task

Implement M5-20 and M5-21 only. Add explicit required CI stages for existing real cross-component integration tests and full Legacy-to-Gateway-to-Cloud SQLite E2E tests in classical and ML-KEM fail-closed modes. Preserve frozen protocols, ownership, and existing uncommitted M5-09 through M5-14 work; do not add a Legacy container.

---

# Prompt

now, let's implement M5-20 and M5-21

---

# AI Implementation — Initial

## LLM Output

Completed M5-20 and M5-21 by adding explicit required CI stages for existing real cross-component integration tests and full Legacy-to-Gateway-to-Cloud SQLite E2E tests. The integration stage covers Legacy/Gateway, baseline Cloud delivery, ML-KEM session establishment, fixed HKDF, AES-GCM SecureEnvelope/AAD, 409 recovery, same-envelope retry, idempotency, and fail-closed behavior. The E2E stage covers classical, ML-KEM fail-closed, and unchanged Legacy-client compatibility.

## Files Created

- docs/ai/history/0169-validate-gateway-and-cloud-container-health-and-readiness.md
- docs/ai/history/0170-add-explicit-integration-and-end-to-end-ci-stages.md

## Files Modified

- .github/workflows/ai-history.yml
- docker-compose.yml
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_gateway_compose_e2e.py
- tests/test_ci_workflow.py
- tests/test_gateway_docker_assets.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .; uv run pytest -q tests/test_ci_workflow.py tests/integration/test_legacy_gateway.py tests/integration/test_gateway_cloud_baseline.py tests/integration/test_mlkem_session_orchestration.py tests/integration/test_gateway_cloud_secure_session.py tests/integration/test_gateway_cloud_secure.py tests/integration/test_end_to_end.py tests/integration/test_modernized_end_to_end.py tests/integration/test_legacy_mode_success_compatibility.py; uv run python scripts/refresh_graphify.py; uv run ai-history check; git diff --check

### Results

- Passed: Ruff; the exact added CI selection (46 passed, one existing Starlette/httpx deprecation warning); Graphify refresh; AI-history validation; diff check.

## AI Notes

The pre-existing full pytest command was launched, but this environment ended its streamed output before a final summary; the exact new CI selection was run to completion. Existing uncommitted M5-09 through M5-14 work was preserved. No protocol, application, Docker topology, or ownership behavior changed.

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
