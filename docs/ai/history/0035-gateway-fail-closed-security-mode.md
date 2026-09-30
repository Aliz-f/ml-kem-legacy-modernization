# AI Task 0035 — Gateway fail-closed security mode

**Status:** Complete

**Created:** 2026-09-30T10:53:31+03:00

**Updated:** 2026-09-30T10:56:35+03:00

**Agent:** Grok Build

---

# Task

Member 3 tasks M3-28 through M3-31. Add a security-mode dispatch that sends through the injected baseline transport when SECURITY_MODE=classical and through SecureTransport when SECURITY_MODE=mlkem. On any secure failure, log a generic warning, count the failure, and return the classified error. Do not call the baseline endpoint after a secure failure. Do not implement the baseline HTTP client, the Legacy HTTP route, or the Cloud service.

---

# Prompt

start the next task

---

# AI Implementation — Initial

## LLM Output

Added CloudDispatch. SECURITY_MODE=classical forwards a measurement to the injected baseline transport. SECURITY_MODE=mlkem uses only SecureTransport. A secure failure increments secure_failures_total, logs a generic warning, and raises SecureTransportError. The baseline transport is not called. Tests cover classical forwarding, secure forwarding, an ML-KEM handshake failure, an encryption failure, and a rejected secure response. The baseline HTTP client and the Legacy route are not implemented.

## Files Created

- docs/ai/history/0035-gateway-fail-closed-security-mode.md
- edge_gateway/src/edge_gateway/dispatch.py
- edge_gateway/tests/test_dispatch.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .
- uv run pytest
- uv run ai-history check

### Results

- All checks passed!
- 311 passed, 1 warning in 17.75s
- AI history validation passed.

## AI Notes

The branch starts from feat/gateway-secure-transport because that commit is not on develop yet. This history id is 0035. PQC_FAILURE_POLICY other than fail_closed is rejected. SecureTransport does not construct or call a baseline client. Member 2 still owns POST /api/v1/baseline/measurements and the Legacy HTTP route.

---

# Human Review — Round 1

## Problems Found

None stated. Reviewer response: Accepted.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

Inspected and confirmed

---

# Final Outcome

**Status:** Complete
