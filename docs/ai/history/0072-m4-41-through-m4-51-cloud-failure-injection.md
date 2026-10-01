# AI Task 0072 — M4-41 through M4-51 Cloud failure injection

**Status:** Complete

**Created:** 2026-10-01T00:01:14+03:00

**Updated:** 2026-10-01T00:33:01+03:00

**Agent:** Codex

---

# Task

Implement and test Cloud-local controlled failure injection modes through the failure-injection safety review, preserving protocol contracts and fail-closed behavior. Do not start M4-52.

---

# Prompt

Complete M4-41 through M4-51 as one AI-history task.

Follow AGENTS.md and the frozen protocol.
Ask before changing Gateway/shared files.
Run required checks and stop for human review.
Do not start M4-52.

---

# AI Implementation — Initial

## LLM Output

Completed M4-41 through M4-51 as Cloud-local controlled failure injection. Added an opt-in seeded injector and wired public-key unavailability, explicit simulated ML-KEM wrapper/decapsulation failure, session-not-found and forced-expiry responses, decryption and storage failures, bounded processing delay, service unavailability, and post-commit retryable lost-acknowledgement simulation. Preserved secure-envelope validation and lookup then ownership then expiry. Added configuration bounds, Cloud tests and Cloud-local documentation. Refreshed the two approved Graphify artifacts.

## Files Created

- cloud_service/docs/failure-injection.md
- cloud_service/src/cloud_service/failure/
- cloud_service/tests/test_cloud_failure_injection.py
- docs/ai/history/0072-m4-41-through-m4-51-cloud-failure-injection.md

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/src/cloud_service/config.py
- cloud_service/src/cloud_service/gateway/crypto.py
- cloud_service/src/cloud_service/gateway/routes.py
- cloud_service/src/cloud_service/gateway/secure.py
- cloud_service/src/cloud_service/gateway/sessions.py
- cloud_service/tests/test_cloud_config.py
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest cloud_service/tests/test_cloud_failure_injection.py cloud_service/tests/test_cloud_config.py cloud_service/tests/test_cloud_secure.py cloud_service/tests/test_cloud_session_api.py cloud_service/tests/test_cloud_public_key.py cloud_service/tests/test_cloud_baseline.py
- uv run pytest
- uv run ruff check .
- uv run ai-history check
- git diff --check
- uv run python scripts/refresh_graphify.py

### Results

- 177 targeted tests passed; one existing Starlette TestClient deprecation warning.
- 1007 passed; one existing Starlette TestClient deprecation warning; 31.98 seconds.
- All checks passed.
- AI history validation passed.
- No whitespace errors.
- Refresh produced 1569 nodes and 3891 edges. Hash scope guard confirmed only graphify-out/graph.json and graphify-out/GRAPH_REPORT.md changed.

## AI Notes

Read the required course PDFs and frozen Cloud/shared protocol, roadmap, Member 4 and Member 5 task documents. Existing failure configuration was extended with Cloud-local runtime behavior only. Defaults none/0 leave behavior unchanged; seeded selection is only for injected faults, never cryptographic randomness. drop_response models an unavailable acknowledgement as retryable 503 after commit in the local harness; real transport connection-loss verification remains Member 5 E2E scope. No Gateway, dependencies, lockfile, or other shared files changed. M4-52 and later were not started; broader Cloud metrics/logging/secret-leakage work remains assigned to M4-52 through M4-56.

---

# Human Review — Round 1

## Problems Found

Random failure mode does not correctly satisfy the failure-rate contract. It selects a new random scenario on every inject(mode) probe, so even with FAILURE_RATE=1.0 a request can pass all relevant boundaries without any injected failure. The current random-mode test only checks that inject() returns bool values and does not verify the required behavior.

## Decision

Modified

## Requested Modifications

Refactor RANDOM mode so the rate gate is applied correctly and, when injection is triggered, one allowed failure scenario is selected deterministically from the seeded RNG rather than re-selecting independently at every boundary probe. Add tests proving: rate 0 never injects; rate 1 injects when an applicable random failure is selected; seeded random behavior is reproducible; random mode selects only supported injectable scenarios. Preserve all existing protocol behavior and do not start M4-52.

---

# AI Revision — Round 1

## Revision Summary

Corrected RANDOM failure injection. Each Cloud API request now asks the injector for one selection from only its applicable failure modes. The injector applies the configured rate gate once, uses the seeded RNG once to choose an allowed mode when random injection applies, and passes that immutable selection through subsequent secure-processing stages. The revision preserves direct configured modes and all frozen protocol behavior. Added rate-zero, rate-one, seeded reproducibility, supported-mode, and selection-reuse tests; updated failure-injection documentation and refreshed approved Graphify artifacts.

## Files Created

- cloud_service/docs/failure-injection.md
- cloud_service/src/cloud_service/failure/
- cloud_service/tests/test_cloud_failure_injection.py
- docs/ai/history/0072-m4-41-through-m4-51-cloud-failure-injection.md

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/src/cloud_service/config.py
- cloud_service/src/cloud_service/gateway/crypto.py
- cloud_service/src/cloud_service/gateway/routes.py
- cloud_service/src/cloud_service/gateway/secure.py
- cloud_service/src/cloud_service/gateway/sessions.py
- cloud_service/tests/test_cloud_config.py
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest cloud_service/tests/test_cloud_failure_injection.py cloud_service/tests/test_cloud_config.py cloud_service/tests/test_cloud_secure.py cloud_service/tests/test_cloud_session_api.py cloud_service/tests/test_cloud_public_key.py cloud_service/tests/test_cloud_baseline.py
- uv run pytest
- uv run ruff check .
- uv run ai-history check
- git diff --check
- uv run python scripts/refresh_graphify.py

### Results

- 179 targeted tests passed; one existing Starlette TestClient deprecation warning.
- 1009 passed; one existing Starlette TestClient deprecation warning; 31.74 seconds.
- All checks passed.
- AI history validation passed.
- No whitespace errors.
- Refresh produced 1574 nodes and 3905 edges. Hash scope guard confirmed only graphify-out/graph.json and graphify-out/GRAPH_REPORT.md changed.

## AI Notes

The random failure rate now governs one request-level selection, not each later boundary probe. Random mode chooses only endpoint-applicable supported failure modes. FAILURE_RATE=0 leaves all selections empty; at rate 1 a non-empty applicable set always selects one fault. The seeded RNG remains only a fault-injection test control, never cryptographic randomness. No Gateway, dependency, lockfile, or other shared files changed. M4-52 and later remain unstarted.

---

# Human Review — Round 2

## Problems Found

1. SESSION_NOT_FOUND invalidates the session before normal session lookup/ownership validation. A request using another Gateway's valid session_id could invalidate that session and return SESSION_INVALID instead of preserving lookup -> ownership -> expiry behavior. 2. event=failure_injected is logged when a fault is selected, not when it is actually applied. A request may fail earlier while the log still claims that the selected failure was injected.

## Decision

Modified

## Requested Modifications

Preserve normal lookup -> ownership -> expiry validation before applying the simulated SESSION_NOT_FOUND failure. A wrong-owner request must remain SECURE_MESSAGE_REJECTED and must not invalidate the other Gateway's session. Log event=failure_injected only when the selected fault is actually applied. Add focused regression tests for both behaviors. Preserve the corrected request-level RANDOM selection and do not start M4-52.

---

# AI Revision — Round 2

## Revision Summary

Corrected SESSION_NOT_FOUND ordering and failure-applied logging. Secure ingestion now performs the normal SessionManager lookup, ownership, and expiry checks before simulating session removal; a wrong-owner request therefore remains SECURE_MESSAGE_REJECTED and cannot invalidate another Gateway session. Failure selection no longer logs at selection time. It exposes an apply operation that emits event=failure_injected once only when the selected processing boundary is actually reached. Added focused regression tests for both cases while retaining request-level seeded random selection.

## Files Created

- cloud_service/docs/failure-injection.md
- cloud_service/src/cloud_service/failure/
- cloud_service/tests/test_cloud_failure_injection.py
- docs/ai/history/0072-m4-41-through-m4-51-cloud-failure-injection.md

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/src/cloud_service/config.py
- cloud_service/src/cloud_service/gateway/crypto.py
- cloud_service/src/cloud_service/gateway/routes.py
- cloud_service/src/cloud_service/gateway/secure.py
- cloud_service/src/cloud_service/gateway/sessions.py
- cloud_service/tests/test_cloud_config.py
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest cloud_service/tests/test_cloud_failure_injection.py cloud_service/tests/test_cloud_secure.py cloud_service/tests/test_cloud_session_api.py cloud_service/tests/test_cloud_config.py
- uv run pytest
- uv run ruff check .
- uv run ai-history check
- git diff --check
- uv run python scripts/refresh_graphify.py

### Results

- 145 focused tests passed; one existing Starlette TestClient deprecation warning.
- 1011 passed; one existing Starlette TestClient deprecation warning; 31.68 seconds.
- All checks passed.
- AI history validation passed.
- No whitespace errors.
- Refresh produced 1578 nodes and 3917 edges. Hash scope guard confirmed only graphify-out/graph.json and graphify-out/GRAPH_REPORT.md changed.

## AI Notes

Session-not-found failure now occurs only after normal session lookup, ownership, and expiry validation. A selected fault produces no injected event when an earlier request check rejects the request; it logs exactly once when its actual boundary is reached. Request-level RANDOM selection remains rate-gated, seeded, deterministic and restricted to endpoint-applicable supported modes. No Gateway, dependency, lockfile, or other shared files changed. M4-52 and later remain unstarted.

---

# Human Review — Round 3

## Problems Found

No blocking problems identified.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- uv run pytest: 1011 passed, one existing Starlette TestClient deprecation warning.
- uv run ruff check .: All checks passed.
- uv run ai-history check: AI history validation passed.
- git diff --check: No whitespace errors.

## Human-Confirmed Verification

I inspected the final M4-41–M4-51 work and accept it.

---

# Final Outcome

**Status:** Complete
