# AI Task 0136 — Add full classical baseline measurement harness

**Status:** Complete

**Created:** 2026-10-02T17:07:22+03:00

**Updated:** 2026-10-02T17:13:24+03:00

**Agent:** Unknown

---

# Task

M5-31: build a small reproducible root-level harness measuring the real Legacy-to-Gateway-to-Cloud classical path.

---

# Prompt

ok, now let's implement M5-31

---

# AI Implementation — Initial

## LLM Output

Added an executable M5-31 harness for the real classical Legacy-to-Gateway-to-Cloud-to-SQLite path and focused regression coverage.

## Files Created

- scripts/measure_baseline_e2e.py, tests/test_measure_baseline_e2e.py

## Files Modified

- docs/ai/.state.json, graphify-out/GRAPH_REPORT.md, graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/test_measure_baseline_e2e.py -q; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check; git diff --check

### Results

- Ruff passed; Graphify refresh completed; focused harness tests passed (4 passed); full suite passed (1294 tests); AI-history validation and diff check passed.

## AI Notes

The harness uses disposable loopback Uvicorn services, a temporary SQLite database, and the production Legacy client and application composition. It records observational timings only; M5-32 reproducibility documentation and later mode comparisons remain out of scope.

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
