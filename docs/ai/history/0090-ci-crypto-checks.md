# AI Task 0090 — CI crypto checks

**Status:** Complete

**Created:** 2026-10-01T11:30:56+03:00

**Updated:** 2026-10-01T11:41:57+03:00

**Agent:** Grok Build

---

# Task

Member 3 task M3-63. On a new branch from origin/develop at 719a760, make the repository quality workflow run the Gateway ML-KEM, KDF, AEAD, secure-envelope, key-confirmation, replay-limitation, secure-integration, and secret-leakage tests explicitly. Keep the existing full pytest run. Do not start M3-64 or later tasks. Do not add a production secure-ingest route or Member 2 delivery.

---

# Prompt

start the next task and tell me the status of tasks

---

# AI Implementation — Initial

## LLM Output

Added an explicit Gateway crypto step to the repository quality workflow. It runs the ML-KEM, KDF, AEAD, secure-envelope, key-confirmation, secret-leakage, tamper, and secure-integration suites after the full pytest command. The new branch feat/gateway-ci-crypto-checks starts from origin/develop at 719a760. The full pytest command remains.

## Files Created

- docs/ai/history/0090-ci-crypto-checks.md
- tests/test_gateway_crypto_ci.py

## Files Modified

- .github/workflows/ai-history.yml
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/test_refresh_graphify.py

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
- 1092 passed, 2 skipped, 1 warning in 32.42s. The skips are the Docker image runs. The warning is the existing StarletteDeprecationWarning about httpx and starlette.testclient.
- AI history validation passed.
- Ran twice. Both refreshes matched: graph.json 4dbae25bc3cfd7dfca7dedbcab75bb91b91716af, GRAPH_REPORT.md bc0fe1bc4a8003d6164d5d765ee8b5a34b4f40f7, 1903 nodes, 4702 edges, 106 communities. pypdf is not installed and claude community labeling is not logged in, so both runs used Community N placeholders.

## AI Notes

The key-confirmation suite is the transport-trust test, which records that protocol version 1 has no separate confirmation tag. The replay-limitation coverage is the secure integration and tamper suites, which keep business idempotency separate from a cryptographic replay window. A pre-existing graphify test used a title the normalizer does not strip. The fixture now uses the Graph Report title. Graphify warned that pypdf is missing and that claude is not logged in. The pytest warning is the existing StarletteDeprecationWarning. M3-64 was not started. This work is not committed.

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
