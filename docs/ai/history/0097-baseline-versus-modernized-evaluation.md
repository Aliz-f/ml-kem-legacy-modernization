# AI Task 0097 — Baseline versus modernized evaluation

**Status:** Complete

**Created:** 2026-10-01T14:09:06+03:00

**Updated:** 2026-10-01T15:08:35+03:00

**Agent:** Grok Build

---

# Task

Member 3 task M3-70. Measure an equivalent four-measurement workload in SECURITY_MODE=classical and SECURITY_MODE=mlkem. Report handshake duration, encapsulation duration, first secure-message latency separately from steady-state latency, SecureEnvelope size, session reuse count, and session re-establishment count. Also record handshake-failure and corrupted-ciphertext behavior. Do not rank the modes or invent a conclusion. Do not start M3-71 or later tasks. Do not add a production Legacy delivery route.

---

# Prompt

commit nad push and then start the next task

---

# AI Implementation — Initial

## LLM Output

Measured one equivalent four-measurement workload in classical mode and mlkem mode. The first secure request is 15.871 ms and includes a 13.542 ms handshake. The steady-state secure mean is 1.253 ms across three reused sessions. The SecureEnvelope is 455 bytes. One later invalidation caused one re-establishment. Injected handshake and ciphertext failures did not call the baseline endpoint. The sample does not rank the modes.

## Files Created

- docs/ai/history/0097-baseline-versus-modernized-evaluation.md
- edge_gateway/docs/mode-evaluation.md
- tests/integration/test_mode_evaluation.py

## Files Modified

- docs/ai/.state.json
- edge_gateway/README.md
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run python -c measure_modes
- uv run ruff check .
- uv run pytest -q --tb=line
- uv run python scripts/refresh_graphify.py

### Results

- One local sample: classical first 13.012 ms, classical steady mean 1.390 ms, canonical JSON 192 bytes, handshake 13.542 ms, encapsulation 0.259 ms, first secure message 15.871 ms, steady secure mean 1.253 ms, SecureEnvelope 455 bytes, reuse count 3, re-establishment count 1, fallback count 0, baseline calls during mlkem 0.
- Ruff passed.
- 1114 passed, 2 skipped, 1 warning in 32.40s. The skips are the Docker image runs. The warning is the existing StarletteDeprecationWarning about httpx and starlette.testclient.
- Ran twice. Both refreshes matched: graph.json 78ab515208fffc5603323c72e01fda5090a3782f, GRAPH_REPORT.md ed10b2bef334764b47b951a7902b3e3769e99502, 1958 nodes, 4799 edges, 116 communities. pypdf is not installed and claude community labeling is not logged in, so both runs used Community N placeholders.

## AI Notes

The sample is edge_gateway/docs/mode-evaluation.md and tests/integration/test_mode_evaluation.py. The production Legacy route still stops before delivery, so the measurement uses CloudDispatch. The classical post is the baseline transport used by that dispatch. M3-71 was not started. This branch is feat/gateway-mode-evaluation from c9c6f81 and has no upstream. This work is not committed.

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
