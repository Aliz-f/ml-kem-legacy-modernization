# AI Task 0139 — Harden secure transport error handling and message-phase metric

**Status:** Complete

**Created:** 2026-10-02T17:53:15+03:00

**Updated:** 2026-10-02T18:05:42+03:00

**Agent:** Claude Code (Opus 5.5)

---

# Task

M3-44/M3-46/M3-56/M3-43 review fixes

---

# Prompt

Review the codes of the member 3. ... yes, fix 1 to 3 (1: unhandled OSError/connection reset during Cloud response read; 2: in-flight request after shutdown raises AttributeError; 3: first/steady message-phase metric mislabels the first message after silent expiry).

---

# AI Implementation — Initial

## LLM Output

Fixed three Member 3 review findings in the Gateway secure path. (1) secure_transport._post now treats an OSError raised while reading the Cloud response (e.g. connection reset) as an ordinary retryable transport failure that resends the identical envelope; HTTPError body reads are guarded; session_client and public_key_client classify HTTPException/OSError during reads as retryable transport errors instead of 'unexpected'/non-retryable. (2) _post raises a non-retryable SecureTransportError (fail-closed, logged reason=closed) when shutdown() closed the HTTP client during an in-flight delivery, instead of an AttributeError. (3) The first/steady message-phase metric is now decided by whether opening the session completed a handshake, not by the active-session gauge, so the first message after local expiry is labelled first.

## Files Created

- docs/ai/history/0129-harden-secure-transport-error-handling-and-message-phase-metric.md

## Files Modified

- edge_gateway/src/edge_gateway/crypto/secure_transport.py
- edge_gateway/src/edge_gateway/crypto/session_client.py
- edge_gateway/src/edge_gateway/crypto/public_key_client.py
- edge_gateway/tests/test_secure_transport.py
- edge_gateway/tests/test_session.py
- edge_gateway/tests/test_public_key_client.py
- edge_gateway/tests/test_final_secure_transport_review.py
- edge_gateway/tests/test_member2_integration_review.py
- tests/integration/test_pqc_observability.py
- edge_gateway/docs/pqc-observability.md
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .
- uv run pytest
- uv run ai-history check
- uv run --frozen python scripts/refresh_graphify.py (x2, claude off PATH)

### Results

- Ruff: all checks passed. Pytest: 1279 passed, 2 skipped. ai-history check passed. Graphify refresh deterministic.

## AI Notes

No protocol, endpoint, status-code, crypto, AAD, nonce, or retry-policy change: ordinary retries still resend the same bytes and session recovery is unchanged. Fix 3 changes recorded observability output: tests/integration/test_pqc_observability.py and edge_gateway/docs/pqc-observability.md previously asserted/recorded the mislabel (first=1, steady=3 after expiry) and now expect first=2, steady=2. Two static review tests used the removed helper name _session_is_active as a split delimiter and now use _handshakes_completed. New regression tests were confirmed to fail on the previous source (6 failed) and pass after the fix. Graphify refreshed with the claude CLI off PATH; two runs produced identical hashes with token cost 0. Out of scope and not changed: local TTL cap/clock skew on expires_at and no ordinary retries after session recovery (review items 4 and 5).

---

# Human Review — Round 1

## Problems Found

None reported.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- uv run ruff check . passed; uv run pytest: 1279 passed, 2 skipped; uv run ai-history check passed; Graphify refresh deterministic (two identical runs, token cost 0).

## Human-Confirmed Verification

Verified: reviewed the diff and tests pass.

---

# Final Outcome

**Status:** Complete
