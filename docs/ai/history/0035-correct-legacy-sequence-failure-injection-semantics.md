# AI Task 0035 — Correct Legacy sequence failure injection semantics

**Status:** Complete

**Created:** 2026-09-30T12:44:29+03:00

**Updated:** 2026-09-30T12:48:38+03:00

**Agent:** Codex

---

# Task

Correct PR #14 so duplicate_sequence and random never abort on first use, and out_of_order_sequence always remains schema-valid and can exercise the frozen Gateway 409 sequence path. Preserve the frozen Legacy protocol, valid Measurement state, ownership boundaries, and prior history evidence. Repair AI-history ordinal sequencing after synchronizing develop. Add focused deterministic tests and run required checks.

---

# Prompt

ok, fix all of the problems and check ai-history numbers for correct ordinal sequences. and then close the PR#14 and merge it into develop

---

# AI Implementation — Initial

## LLM Output

Corrected Legacy sequence failure injection after synchronizing PR #14 with develop. Initial duplicate-sequence requests no longer raise or abort the device path; random mode selects only currently feasible sequence faults; and out-of-order mutations now choose an observed lower, non-negative sequence value. Renumbered the later colliding M1-04 history record from 0027 to 0032, preserving its content and review evidence.

## Files Created

- docs/ai/history/0033-correct-legacy-sequence-failure-injection-semantics.md

## Files Modified

- docs/ai/.state.json
- docs/ai/history/0032-implement-legacy-device-failure-injection.md
- legacy_system/src/legacy_system/failure.py
- legacy_system/tests/test_failure.py
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md

## Files Deleted

- docs/ai/history/0027-implement-legacy-device-failure-injection.md

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest legacy_system/tests/test_failure.py
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest legacy_system/tests
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check
- git diff --check

### Results

- Focused failure-injection tests: 23 passed.
- Legacy suite: 63 passed.
- Repository Ruff: passed.
- Graphify shared artifacts refreshed successfully; PDF extraction was skipped because the optional pypdf extra is not installed.
- Full repository suite: 321 passed; one existing FastAPI/Starlette deprecation warning.
- AI-history validation: passed; IDs are unique and sequential from 0001 through 0033.
- Whitespace validation: passed.

## AI Notes

No endpoint, schema, status-code, cryptographic, retry, or ownership contract changed. Fixed-mode duplicate/out-of-order injection returns an unchanged payload only when the requested sequence mutation is impossible (for example, first sequence); it does not emit a false injected-failure event. Random mode always has non-sequence candidates and therefore still emits a supported fault at rate 1.0. The original ignored cloud.db was restored; prior ignored Graphify cache artifacts remain preserved under /tmp/mlkem-pr14-preserved-artifacts while the repository-owned graph outputs were regenerated.

---

# Human Review — Round 1

## Problems Found

I do not find any problems during manul review

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- Focused failure-injection tests: 23 passed.
- Legacy suite: 63 passed.
- Repository Ruff: passed.
- Full repository suite: 321 passed; one existing FastAPI/Starlette deprecation warning.
- AI-history validation and whitespace validation: passed.

## Human-Confirmed Verification

I inspected the final correction and confirm it is ready to merge.

---

# Final Outcome

**Status:** Complete
