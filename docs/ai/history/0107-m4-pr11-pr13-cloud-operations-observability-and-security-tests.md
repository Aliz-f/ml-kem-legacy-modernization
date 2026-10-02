# AI Task 0107 — M4 PR11–PR13 Cloud operations, observability, and security tests

**Status:** Complete

**Created:** 2026-10-01T21:01:41+03:00

**Updated:** 2026-10-01T22:19:02+03:00

**Agent:** Codex

---

# Task

Implement only Member 4 PR11 through PR13: M4-52 through M4-56 and M4-57 through M4-68. Add safe Cloud logging, health/readiness and shutdown behavior, bounded-label metrics, and Cloud unit/negative security coverage. Preserve the frozen protocol, fail-closed behavior, and session lookup -> ownership -> expiry ordering. Do not start M4-69 or PR14 through PR16.

---

# Prompt

You misidentified the PR stream. We are Member 4. The authoritative Member 4 PR mapping is: PR11 = M4 Cloud logging + health/readiness; PR12 = M4 Metrics + PQC observability; PR13 = M4 Security/negative tests. PR10 is complete. Implement PR11–PR13 only on the current feat/pr11-13 branch. Re-read the Member 4 task file and identify the exact M4 task ranges, dependencies, and order before implementation. Do not implement any Member 2 tasks or PR14–PR16.

---

# AI Implementation — Initial

## LLM Output

Implemented M4 PR11–PR13 only: structured safe Cloud lifecycle, key/session, secure-ingest, storage, validation, and injected-failure logging; operational health and readiness checks; bounded Cloud and PQC metrics; and focused metrics, readiness, applied-fault, and negative security coverage. Preserved fail-closed secure ingestion and session lookup -> ownership -> expiry ordering.

## Files Created

- cloud_service/src/cloud_service/metrics.py
- cloud_service/tests/test_cloud_metrics.py
- docs/ai/history/0107-m4-pr11-pr13-cloud-operations-observability-and-security-tests.md

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/src/cloud_service/failure/injector.py
- cloud_service/src/cloud_service/gateway/crypto.py
- cloud_service/src/cloud_service/gateway/routes.py
- cloud_service/src/cloud_service/gateway/secure.py
- cloud_service/src/cloud_service/gateway/sessions.py
- cloud_service/tests/test_cloud_app.py
- cloud_service/tests/test_cloud_public_key.py
- cloud_service/tools/measure_baseline.py
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .; uv run pytest -q; uv run ai-history check; git diff --check; uv run python scripts/refresh_graphify.py

### Results

- Ruff passed. The full pytest suite passed. AI-history validation passed. Git whitespace validation passed. Graphify refresh completed and the change guard confirmed only graphify-out/graph.json and graphify-out/GRAPH_REPORT.md were generated.

## AI Notes

No Member 2 work or M4-69/PR14–PR16 work was started. No dependency changes were made. Graphify reported its optional PDF extraction was unavailable; code-graph generation still completed. Docker runtime verification is outside this PR scope.

---

# Human Review — Round 1

## Problems Found

Task 0104 is incomplete: PR13 includes M4-61 through M4-69, but M4-69 was excluded. Required synthetic secret-leakage coverage, consistent M4-52 storage/rejection events, readiness proof, shutdown proof, explicit M4-61 through M4-68 audit mapping, and the M4-69 shared-fixture Gateway-to-Cloud baseline contract test are incomplete.

## Decision

Modified

## Requested Modifications

Update task 0104 to cover M4-52 through M4-69. Implement M4-69; add the specified synthetic secret-leakage tests; align event=storage_failed and secure-envelope rejection logging; prove readiness and shutdown requirements; audit and map M4-61 through M4-68 requirements to existing or added tests; add the shared-fixture baseline Gateway-to-Cloud contract test. Do not start M4-70 or PR14+; do not commit or push.

---

# AI Revision — Round 1

## Revision Summary

Completed the requested task-0104 revision: scope now covers M4-52 through M4-69, including the baseline Gateway-to-Cloud contract test and focused Cloud security, readiness, shutdown, metrics, and observability coverage.

## Files Created

- cloud_service/src/cloud_service/metrics.py
- cloud_service/tests/test_cloud_metrics.py
- cloud_service/tests/test_gateway_cloud_baseline_contract.py
- docs/ai/history/0107-m4-pr11-pr13-cloud-operations-observability-and-security-tests.md
- review-0104.diff

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/src/cloud_service/failure/injector.py
- cloud_service/src/cloud_service/gateway/crypto.py
- cloud_service/src/cloud_service/gateway/routes.py
- cloud_service/src/cloud_service/gateway/secure.py
- cloud_service/src/cloud_service/gateway/sessions.py
- cloud_service/tests/test_cloud_app.py
- cloud_service/tests/test_cloud_public_key.py
- cloud_service/tests/test_cloud_secure.py
- cloud_service/tests/test_cloud_session_api.py
- cloud_service/tools/measure_baseline.py
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check cloud_service; uv run pytest cloud_service/tests/test_cloud_app.py cloud_service/tests/test_cloud_session_api.py cloud_service/tests/test_cloud_secure.py cloud_service/tests/test_gateway_cloud_baseline_contract.py -q; uv run ruff check .; uv run pytest -q; uv run ai-history check; git diff --check; uv run python scripts/refresh_graphify.py (guarded to graphify-out/graph.json and graphify-out/GRAPH_REPORT.md)

### Results

- Focused changed-area tests passed: 92 passed, 1 known Starlette TestClient deprecation warning. Full Ruff, full pytest, AI-history check, and Git whitespace check passed. Guarded Graphify refresh completed with only graphify-out/graph.json and graphify-out/GRAPH_REPORT.md eligible to change; Git whitespace check passed after refresh.

## AI Notes

Scope correction: the original task prompt is retained faithfully; this revision explicitly completes and maps M4-52 through M4-69. M4-52: cloud_service/tests/test_cloud_secure.py::test_secure_rejection_and_storage_failure_events_are_safe_and_consistent proves secure-envelope rejection and storage-failure events use the required vocabulary, including event=storage_failed, with no secret or payload content. Existing secure failure-injection and session-ordering tests cover the remaining rejection boundaries. M4-53: existing cloud_service/tests/test_cloud_baseline.py, test_cloud_secure.py, and test_cloud_session_api.py verify structured Cloud events at baseline, secure, and session boundaries. M4-54: cloud_service/tests/test_cloud_session_api.py::test_synthetic_secret_markers_never_appear_in_cloud_logs injects synthetic private-key and shared-secret markers, exercises Cloud key generation, ML-KEM decapsulation/session creation and KDF, authenticated decryption, and a decryption failure branch, then asserts actual captured Cloud logs omit private-key, shared-secret, session-key, and failure markers. Existing test_cloud_kdf.py and test_cloud_aead.py provide primitive and interoperability coverage. M4-55/M4-56: cloud_service/tests/test_cloud_metrics.py::test_metrics_endpoint_is_low_cardinality_and_starts_at_zero, ::test_metrics_reject_unknown_or_unbounded_labels, ::test_metrics_include_baseline_request_outcomes_and_storage_results, and ::test_injected_failure_metric_counts_only_applied_faults prove the frozen metric contract, safe labels, default zero values, and applied-fault observability. M4-57/M4-58/M4-59: test_cloud_app.py::test_lifecycle_endpoints_report_actual_health and ::test_mlkem_readiness_requires_initialized_dependencies_not_an_active_session, plus test_cloud_public_key.py::test_public_key_metadata_without_secret_material, prove health/readiness behavior for reachable storage, initialized ML-KEM keys and sessions, usable AES/KDF dependencies, no required active Gateway session, and response secrecy. M4-60: existing test_cloud_sessions.py::test_remove_expired_and_shutdown and expanded test_cloud_session_api.py::test_shutdown_and_classical_mode prove shutdown clears active sessions and closes storage safely. M4-61: the full Cloud suite exercises normal baseline, ML-KEM key, session, secure-ingestion, storage, failure, and lifecycle paths. M4-62: test_cloud_storage.py and test_cloud_baseline.py cover storage success, duplicate/idempotency, and storage failure. M4-63: test_cloud_baseline.py covers valid baseline acceptance, invalid body handling, response behavior, and idempotency. M4-64: test_cloud_public_key.py and failure-injection tests cover public-key metadata, malformed request handling, and unavailable/failure paths. M4-65: test_cloud_session_api.py covers session establishment, invalid/malformed requests, ownership, and expiry behavior. M4-66: test_cloud_sessions.py, test_cloud_session_api.py, and test_cloud_secure.py cover session lifecycle and strict lookup then ownership then expiry validation. M4-67: test_cloud_aead.py and test_cloud_secure.py cover authenticated decryption, tampering, invalid envelopes, and fail-closed behavior. M4-68: test_cloud_secure.py covers malformed, invalid, wrong-owner, expired, replay/idempotency, storage-failure, and injected secure-failure negative cases without plaintext fallback. M4-69: new cloud_service/tests/test_gateway_cloud_baseline_contract.py uses the shared tests/fixtures/canonical_measurement.json fixture and Cloud HTTP boundary only, with no Gateway application-model imports; it proves canonical field names, absent canonical request_id, X-Request-ID propagation into Cloud logging, compatible timestamps, gateway_id, received_at to gateway_received_at mapping, and idempotency. No real secret material is logged or persisted. M4-70 and later remain untouched.

---

# Human Review — Round 2

## Problems Found

None.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final task 0104 work and accept it

---

# Final Outcome

**Status:** Complete
