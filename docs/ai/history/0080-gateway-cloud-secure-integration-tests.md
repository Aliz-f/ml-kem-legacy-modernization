# AI Task 0080 — Gateway Cloud secure integration tests

**Status:** Complete

**Created:** 2026-09-30T23:48:27+03:00

**Updated:** 2026-09-30T23:58:00+03:00

**Agent:** Grok Build

---

# Task

Member 3 task M3-58. Add the Gateway-to-Cloud secure integration tests: versioned public-key retrieval, ML-KEM-768 session establishment, matching shared secret, fixed HKDF interoperability, secure envelope round trip, byte-identical four-field AAD, Cloud decryption of the canonical measurement, session reuse, local expiry, 409 SESSION_EXPIRED and SESSION_INVALID recovery, one recovery attempt, corrupted ciphertext, nonce and AAD tampering, wrong session, wrong gateway ownership, unsupported protocol version, malformed ML-KEM input where detectable, simulated decapsulation failure, the implicit-rejection caveat, decryption failure, fail-closed behavior with no baseline call, same-envelope ordinary retry, and idempotent duplicate persistence. Do not require every valid-length ML-KEM ciphertext mutation to raise. Do not claim a cryptographic replay counter or window. Do not add a production Cloud secure-ingest route. Do not start M3-59 or later tasks.

---

# Prompt

start the next task

---

# AI Implementation — Initial

## LLM Output

Added the M3-58 Gateway-to-Cloud secure integration suite in tests/integration/test_gateway_cloud_secure.py. The tests call the real Cloud public-key and session HTTP routes through the Gateway clients. A test-only measurement receiver on that app instance uses Cloud session lookup, four-field AAD, and AES-GCM decrypt, then validates and stores the canonical measurement with the existing idempotent repository. The production Cloud app still has no secure measurement route.

## Files Created

- docs/ai/history/0074-gateway-cloud-secure-integration-tests.md

## Files Modified

- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_gateway_cloud_secure.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .
- uv run pytest -q --tb=line
- uv run ai-history check
- uv run python scripts/refresh_graphify.py

### Results

- All checks passed.
- 909 passed, 1 warning in 28.06s. The warning is the existing StarletteDeprecationWarning about httpx and starlette.testclient.
- AI history validation passed.
- Ran twice. Both refreshes matched: graph.json 5e76de938fdaa3e713ea16f953ce36cc19c9a725, GRAPH_REPORT.md a052cd5742d3997bf158a8bc5b0d3a801c3370df, 1592 nodes, 3890 edges, 85 communities. pypdf is not installed and claude community labeling is not logged in, so both runs used Community N placeholders.

## AI Notes

Shared secrets and session keys are compared with booleans and are not written to logs or history. A valid-length ML-KEM ciphertext mutation is not required to raise. Protocol version 1 is not treated as having a cryptographic replay window. An earlier local-expiry run rejected the replacement handshake because the moved Gateway clock was past the new Cloud expires_at; the recorded run sets that clock to the previous expiry instant. Graphify warned that pypdf is missing and that claude is not logged in. The pytest warning is the existing StarletteDeprecationWarning. M3-59 was not started. This work is not committed.

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
