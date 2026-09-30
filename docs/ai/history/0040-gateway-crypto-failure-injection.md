# AI Task 0040 — Gateway crypto failure injection

**Status:** Complete

**Created:** 2026-09-30T13:05:20+03:00

**Updated:** 2026-09-30T13:26:16+03:00

**Agent:** Grok Build

---

# Task

Member 3 tasks M3-32 through M3-37. Add a crypto failure injector for mlkem_handshake_failure, corrupt_ciphertext, session_missing, and session_expired. FAILURE_MODE=none and FAILURE_RATE=0 leave the secure path unchanged. A seeded rate is deterministic. Handshake failure leaves no session, logs safely, counts a metric, and does not call the baseline endpoint. Ciphertext corruption mutates a copy of the ciphertext after encryption and does not change the session key. Missing and expired sessions force one new handshake. Do not implement crypto logging events beyond the injection warning, metrics export, or the Cloud service.

---

# Prompt

merge develop to the current branch and start the next task

---

# AI Implementation — Initial

## LLM Output

Added CryptoFailureInjector for mlkem_handshake_failure, corrupt_ciphertext, session_missing, and session_expired. FAILURE_MODE=none and FAILURE_RATE=0 leave handshakes, sessions, and ciphertext unchanged. A seeded generator decides only whether the configured fault happens. An injected handshake fails before a session is stored, logs a generic warning, increments mlkem_handshake_failures_total, and the secure dispatch does not call the baseline transport. Ciphertext injection mutates a copy after encryption and leaves the session key unchanged. Missing and expired sessions are cleared so the next request performs one new handshake. Enabling a crypto mode with a positive rate logs event=failure_injection_enabled and the mode name.

## Files Created

- docs/ai/history/0040-gateway-crypto-failure-injection.md
- edge_gateway/src/edge_gateway/crypto/failure.py
- edge_gateway/tests/test_failure_injection.py

## Files Modified

- docs/ai/.state.json
- edge_gateway/src/edge_gateway/crypto/secure_transport.py
- edge_gateway/src/edge_gateway/crypto/session.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .
- uv run pytest
- uv run ai-history check

### Results

- All checks passed!
- 351 passed, 1 warning in 19.63s
- AI history validation passed.

## AI Notes

Develop was merged into this branch again. Gateway secure transport is history 0038 and fail-closed dispatch is history 0039. This history id is 0040. encryption_failure, the crypto logging catalog, metrics export, and the Cloud service are outside this slice. The injector seed is not used as cryptographic randomness.

---

# Human Review — Round 1

## Problems Found

None stated. Reviewer response: accepted.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

confirmed

---

# Final Outcome

**Status:** Complete
