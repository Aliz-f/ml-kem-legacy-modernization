# AI Task 0127 — Scope session invalidation to rejected recovery session

**Status:** Complete

**Created:** 2026-10-02T12:44:00+03:00

**Updated:** 2026-10-02T15:38:42+03:00

**Agent:** Codex

---

# Task

Align Gateway concurrent 409 session recovery with the frozen requirement to invalidate the rejected old session only, and add coverage. Preserve one bounded recovery per send, same logical request ID, fail-closed behavior, and all frozen protocol contracts.

---

# Prompt

fix the inconsistency and ai-history IDs

---

# AI Implementation — Initial

## LLM Output

Merged current develop into PR #33, renumbered its colliding AI-history records to 0124–0126, and scoped Gateway 409 recovery invalidation to the rejected envelope session ID.

## Files Created

- docs/ai/history/0120-align-legacy-timing-configuration-and-log-component-field.md
- docs/ai/history/0121-align-edge-gateway-logging-with-project-convention.md
- docs/ai/history/0122-align-cloud-logging-and-implementation-documentation.md
- docs/ai/history/0123-align-gateway-correlation-test-with-structured-logging.md
- docs/ai/history/0127-scope-session-invalidation-to-rejected-recovery-session.md

## Files Modified

- cloud_service/docs/application.md
- cloud_service/docs/baseline.md
- cloud_service/docs/canonical-validation.md
- cloud_service/docs/mlkem-key-service.md
- cloud_service/src/cloud_service/app.py
- cloud_service/src/cloud_service/failure/injector.py
- cloud_service/src/cloud_service/gateway/crypto.py
- cloud_service/src/cloud_service/gateway/queries.py
- cloud_service/src/cloud_service/gateway/routes.py
- cloud_service/src/cloud_service/gateway/sessions.py
- cloud_service/tests/test_cloud_app.py
- cloud_service/tests/test_cloud_baseline.py
- cloud_service/tests/test_cloud_failure_injection.py
- cloud_service/tests/test_cloud_queries.py
- docs/ai/.state.json
- docs/ai/history/0120-gateway-dependency-and-security-review.md -> docs/ai/history/0124-gateway-dependency-and-security-review.md
- docs/ai/history/0121-gateway-static-and-code-quality-verification.md -> docs/ai/history/0125-gateway-static-and-code-quality-verification.md
- docs/ai/history/0122-final-secure-transport-review.md -> docs/ai/history/0126-final-secure-transport-review.md
- edge_gateway/docs/final-secure-transport-review.md
- edge_gateway/src/edge_gateway/app.py
- edge_gateway/src/edge_gateway/correlation.py
- edge_gateway/src/edge_gateway/crypto/failure.py
- edge_gateway/src/edge_gateway/crypto/secure_transport.py
- edge_gateway/src/edge_gateway/crypto/security_log.py
- edge_gateway/src/edge_gateway/crypto/session.py
- edge_gateway/src/edge_gateway/failure/injector.py
- edge_gateway/src/edge_gateway/sequence.py
- edge_gateway/tests/test_crypto_failures.py
- edge_gateway/tests/test_dispatch.py
- edge_gateway/tests/test_final_secure_transport_review.py
- edge_gateway/tests/test_gateway_app.py
- edge_gateway/tests/test_gateway_correlation.py
- edge_gateway/tests/test_gateway_errors.py
- edge_gateway/tests/test_gateway_failure_injector.py
- edge_gateway/tests/test_gateway_sequence.py
- edge_gateway/tests/test_member2_integration_review.py
- edge_gateway/tests/test_secure_shutdown.py
- edge_gateway/tests/test_secure_transport.py
- edge_gateway/tests/test_security_logging.py
- edge_gateway/tests/test_session.py
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- legacy_system/src/legacy_system/client.py
- legacy_system/src/legacy_system/config.py
- legacy_system/src/legacy_system/device.py
- legacy_system/src/legacy_system/failure.py
- legacy_system/src/legacy_system/main.py
- legacy_system/tests/test_client.py
- legacy_system/tests/test_config.py
- legacy_system/tests/test_device.py
- legacy_system/tests/test_failure.py
- legacy_system/tests/test_main.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .
- uv run pytest
- uv run ai-history check
- uv run python scripts/refresh_graphify.py

### Results

- passed
- 1275 passed; one existing Starlette TestClient deprecation warning
- passed
- completed; code-only graph refresh

## AI Notes

The repair preserves one bounded recovery per send, a replacement envelope with the same logical request ID, and fail-closed behavior. A focused regression test confirms a delayed mismatched invalidation preserves a replacement session.

---

# Human Review — Round 1

## Problems Found

I do not find any problem during manual review

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- uv run ruff check .; uv run pytest; uv run ai-history check

## Human-Confirmed Verification

I verify it

---

# Final Outcome

**Status:** Complete
