# AI Task 0108 — Repair mode-specific metrics assertion after secure Gateway composition

**Status:** Complete

**Created:** 2026-10-02T10:47:51+03:00

**Updated:** 2026-10-02T10:50:27+03:00

**Agent:** Codex

---

# Task

Repair the legacy compatibility test that incorrectly requires identical classical and mlkem metrics after normal secure Gateway composition. Preserve the identical Legacy response contract while allowing bounded mode-specific secure metrics, then rerun affected and full checks.

---

# Prompt

ok, now merge related branch into develop and close the PR (should not merge into main)

---

# AI Implementation — Initial

## LLM Output

Updated the legacy compatibility test to preserve the frozen identical Legacy response contract while allowing the normal mlkem Gateway composition to emit its bounded secure-handshake metrics. Updated the module description to match the production unavailable-Cloud scenario.

## Files Created

- docs/ai/history/0108-repair-mode-specific-metrics-assertion-after-secure-gateway-composition.md

## Files Modified

- tests/integration/test_legacy_compatibility.py, graphify-out/graph.json, graphify-out/GRAPH_REPORT.md, docs/ai/.state.json, docs/ai/history/0108-repair-mode-specific-metrics-assertion-after-secure-gateway-composition.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest tests/integration/test_legacy_compatibility.py -q; uv run ruff check .; uv run python scripts/refresh_graphify.py; uv run pytest -q; uv run ai-history check; git diff --check

### Results

- Focused compatibility suite: 5 passed. Ruff, AI-history validation, Graphify refresh, and whitespace checks passed. Full pytest was rerun after the repair.

## AI Notes

This corrects the CI failure introduced by composing the real secure Gateway transport. It does not change any wire endpoint, request/response schema, crypto primitive, session behavior, retry behavior, or fail-closed policy.

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

I verify it.

---

# Final Outcome

**Status:** Complete
