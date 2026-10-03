# AI Task 0141 — Add successful Legacy compatibility regression test

**Status:** Complete

**Created:** 2026-10-02T17:48:05+03:00

**Updated:** 2026-10-02T18:06:51+03:00

**Agent:** Codex

---

# Task

M5-36: add successful end-to-end evidence that the same Legacy client and five-field payload work against classical and ML-KEM modes, differing only in the Gateway address.

---

# Prompt

Let's implement M5-36

---

# AI Implementation — Initial

## LLM Output

Added successful M5-36 compatibility coverage proving the same Legacy client and five-field payload work against both classical and ML-KEM Gateway modes.

## Files Created

- tests/integration/test_legacy_mode_success_compatibility.py

## Files Modified

- docs/ai/.state.json, graphify-out/GRAPH_REPORT.md, graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/integration/test_legacy_mode_success_compatibility.py -q; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check; git diff --check

### Results

- Graphify refresh and Ruff passed; focused compatibility test passed (1 passed); AI-history validation and diff check passed.

## AI Notes

The prior full suite was green before this isolated integration-test addition. The test uses disposable live services and no Legacy protocol configuration or source change other than its supplied Gateway URL.

---

# Human Review — Round 1

## Problems Found

I do not find any problem during manual review

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
