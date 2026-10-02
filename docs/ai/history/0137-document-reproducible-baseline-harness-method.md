# AI Task 0137 — Document reproducible baseline harness method

**Status:** Complete

**Created:** 2026-10-02T17:14:22+03:00

**Updated:** 2026-10-02T17:28:27+03:00

**Agent:** Codex

---

# Task

M5-32: document the exact workload, environment, security mode, failure configuration, and execution method for the M5-31 classical baseline measurement harness only.

---

# Prompt

Let's Implement M5-32

---

# AI Implementation — Initial

## LLM Output

Documented the reproducible M5-31 classical baseline method and added environment and configuration metadata to every harness report.

## Files Created

- docs/evaluation/baseline-measurement-method.md, tests/test_baseline_measurement_method_document.py

## Files Modified

- scripts/measure_baseline_e2e.py, docs/ai/.state.json, graphify-out/GRAPH_REPORT.md, graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/test_baseline_measurement_method_document.py tests/test_measure_baseline_e2e.py -q; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check; git diff --check

### Results

- Ruff passed; Graphify refresh completed; focused tests passed (6 passed); full suite passed (1296 tests); AI-history validation and diff check passed.

## AI Notes

This task fixes the classical harness workload and measurement boundaries. It does not run or compare Modernized Mode, add deployment benchmarking, or make performance claims.

---

# Human Review — Round 1

## Problems Found

I do not find any problems during manual review

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I verify it

---

# Final Outcome

**Status:** Complete
