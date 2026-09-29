# AI Task 0032 — M4-23 through M4-29 Cloud sessions and expiry

**Status:** Complete

**Created:** 2026-09-29T21:15:04+03:00

**Updated:** 2026-09-29T21:26:20+03:00

**Agent:** Codex

---

# Task

Implement Cloud in-memory session model/manager, validated session establishment endpoint, ownership, controlled-time expiry and Gateway interoperability. Use shared lookup then ownership then expiry ordering. No M4-30 or secure measurement implementation. Cloud-local changes plus required history only.

---

# Prompt

Complete M4-23 through M4-29 as one AI-history task.

Ask before changing edge_gateway or shared/project-wide files.

Stop for human review. Do not start M4-30.

---

# AI Implementation — Initial

## LLM Output

Implemented M4-23 through M4-29 together: in-memory Cloud session model and synchronized manager, validated protocol-v1 session establishment endpoint using existing ML-KEM/HKDF wrappers, lookup then ownership then expiry checks, fixed 300-second lifetime, invalidation/expiry cleanup and shutdown key clearing. Added strict request/encoding validation, safe operational failures with cleanup, controlled-time tests, frozen session-error HTTP handler tests, and real HTTP interoperability with the unchanged Gateway session manager/clients. Added Cloud-local documentation and updated obsolete session-route assertions.

## Files Created

- cloud_service/src/cloud_service/crypto/session.py
- cloud_service/src/cloud_service/gateway/sessions.py
- cloud_service/tests/test_cloud_sessions.py
- cloud_service/tests/test_cloud_session_api.py
- cloud_service/docs/sessions.md
- docs/ai/history/0032-m4-23-through-m4-29-cloud-sessions-and-expiry.md

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/tests/test_cloud_app.py
- cloud_service/tests/test_cloud_public_key.py
- cloud_service/docs/application.md
- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest cloud_service/tests/test_cloud_sessions.py cloud_service/tests/test_cloud_session_api.py cloud_service/tests/test_cloud_public_key.py cloud_service/tests/test_cloud_app.py -q
- uv run ruff check .
- uv run pytest
- uv run ai-history check
- git diff --check

### Results

- Initial focused run: 58 passed, 1 existing Starlette warning. Four further validation/startup cases included in final full suite.
- All checks passed.
- 425 passed, 1 existing Starlette TestClient deprecation warning in 16.43 seconds. Includes 46 new session tests, live Gateway HTTP handshake, controlled-time expiry and replacement, failure cleanup and shutdown.
- Validation passed.
- Passed; Git line-ending conversion warnings only.

## AI Notes

No Gateway, shared protocol, dependency or lockfile modifications. Uses authoritative lookup/ownership/expiry ordering from Shared Protocol and accepted M4-00 boundary review. Unknown/removed session maps to 409 SESSION_INVALID, correct-owner expiry to 409 SESSION_EXPIRED, ownership mismatch to 400 SECURE_MESSAGE_REJECTED. HTTP access mapping exercised using a test-only route; production secure measurement endpoint remains 404, readiness remains 503 and classical fallback is absent. Real HTTP integration covers session handshake only, not secure-message or Legacy E2E. No counters, replay window or explicit key confirmation; valid-length tampering is not assumed to throw. Python cannot guarantee zeroization of all secret copies. M4-30 and later not started; M4-17 Docker verification remains deferred to M4-81/M4-83. No secrets or invented human review recorded. Stop for human review.

---

# Human Review — Round 1

## Problems Found

No blocking problems identified.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final M4-23–M4-29 work and accept it.

---

# Final Outcome

**Status:** Complete
