# AI Task 0076 — Legacy contract across security modes

**Status:** Complete

**Created:** 2026-10-01T00:46:04+03:00

**Updated:** 2026-10-01T00:53:06+03:00

**Agent:** Grok Build

---

# Task

Member 3 task M3-60. On a new branch from feat/gateway-crypto-unit-tests at c1b8d2c, not from origin/develop, verify the same Legacy client and JSON schema behave the same against SECURITY_MODE=classical and SECURITY_MODE=mlkem. The Legacy payload stays the five Legacy fields and must not learn ML-KEM, session_id, nonce, the Cloud public key, or AES-GCM. Do not implement Member 2 measurements-route delivery or a production Cloud secure-ingest route. Do not start M3-61 or later tasks. origin/develop is c8b7e26 and the parent branch is not behind it.

---

# Prompt

for the next task check if you need to create a new branch from the current branch and then start the next task

---

# AI Implementation — Initial

## LLM Output

Added an M3-60 check that the same Legacy client and five-field JSON behave the same against SECURITY_MODE=classical and SECURITY_MODE=mlkem. The new branch feat/gateway-legacy-compatibility starts from feat/gateway-crypto-unit-tests at c1b8d2c. origin/develop is still c8b7e26, so no merge was needed. The production measurements route was left unchanged.

## Files Created

- docs/ai/history/0076-legacy-contract-across-security-modes.md
- tests/integration/test_legacy_compatibility.py

## Files Modified

- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

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
- 915 passed, 1 warning in 29.09s. The warning is the existing StarletteDeprecationWarning about httpx and starlette.testclient.
- AI history validation passed.
- Ran twice. Both refreshes matched: graph.json b7e4bb12550abc8e7c8ceddd2c724b59334d947d, GRAPH_REPORT.md 759d5372c5f06ff06d3ffa1814358b7e2a8faf42, 1641 nodes, 3969 edges, 99 communities. pypdf is not installed and claude community labeling is not logged in, so both runs used Community N placeholders.

## AI Notes

The production Gateway measurements route still stops before delivery. Valid measurements are compared across modes without pinning today's unavailable status. Domain-invalid humidity stays 422 and is not retried. Malformed JSON stays 400. Metrics may show a different security_mode label while the measurement response stays identical. Legacy sources do not mention ML-KEM, session_id, nonce, public_key, or AES-GCM. Graphify warned that pypdf is missing and that claude is not logged in. The pytest warning is the existing StarletteDeprecationWarning. M3-61 was not started. This work is not committed.

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

confirmed

---

# Final Outcome

**Status:** Complete
