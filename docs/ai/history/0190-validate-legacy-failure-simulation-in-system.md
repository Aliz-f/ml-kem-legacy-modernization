# AI Task 0190 — Validate Legacy failure simulation in system

**Status:** Complete

**Created:** 2026-10-04T17:06:58+03:00

**Updated:** 2026-10-04T17:16:57+03:00

**Agent:** Antigravity

---

# Task

Validate Legacy Device failure simulation and non-retryable rejection behaviors (M1-17), demonstrating the full fault injector matrix against Gateway error semantics.

---

# Prompt

proceed

---

# AI Implementation — Initial

## LLM Output

Validated Legacy Device failure simulation and protocol rejection behavior (M1-17). Implemented 10 automated tests covering the complete failure injector matrix (none -> 202, domain/schema faults -> 422, sequence duplicate/out-of-order -> 409, malformed syntax -> 400, and deterministic random mode). Verified that all 4xx rejection codes produce exactly 1 attempt with 0 client retries and structured failure logs without process termination. Documented the demonstration matrix and findings in legacy_system/docs/failure-simulation.md.

## Files Created

- docs/ai/history/0190-validate-legacy-failure-simulation-in-system.md
- legacy_system/docs/failure-simulation.md
- legacy_system/tests/test_failure_simulation.py

## Files Modified

- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- rtk uv run pytest legacy_system/tests && rtk uv run ruff check legacy_system && rtk uv run python scripts/refresh_graphify.py && rtk uv run ai-history check

### Results

- 169 passed in legacy_system/tests; ruff passed; Graphify refreshed (2811 nodes, 7064 edges); ai-history validation passed.

## AI Notes

Fault injection targets outgoing serialized payloads only, preserving internal Measurement model integrity. No production protocol or runtime changes were introduced.

---

# Human Review — Round 1

## Problems Found

No problems identified during manual review.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final implementation and tests and accept the result.

---

# Final Outcome

**Status:** Complete
