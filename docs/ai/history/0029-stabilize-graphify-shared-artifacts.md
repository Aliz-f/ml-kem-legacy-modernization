# AI Task 0029 — Stabilize Graphify shared artifacts

**Status:** Complete

**Created:** 2026-09-30T11:52:21+03:00

**Updated:** 2026-09-30T11:57:18+03:00

**Agent:** Codex

---

# Task

Correct Graphify CI nondeterminism by excluding machine-local manifest metadata and normalizing commit-specific output metadata, while preserving automated shared graph refresh and existing frozen rules.

---

# Prompt

ok then, fix this problem

---

# AI Implementation — Initial

## LLM Output

Removed Graphify's machine-specific manifest from version control and corrected the PR workflow so its bot refresh commits only portable graph/report artifacts without running a self-invalidating post-commit diff.

## Files Created

- docs/ai/history/0029-stabilize-graphify-shared-artifacts.md

## Files Modified

- .github/workflows/graphify.yml
- .gitignore
- AGENTS.md
- docs/ai/.state.json
- docs/development/graphify.md
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- graphify-out/manifest.json

## AI-Executed Verification

### Commands

- uv run graphify extract . --code-only --no-viz; uv run graphify cluster-only . --no-viz; uv run ruff check .; uv run pytest; uv run ai-history check

### Results

- Repeated local refresh left the staged graph/report unchanged; manifest.json is ignored; Ruff passed; 297 tests passed with one existing FastAPI deprecation warning; AI-history validation passed.

## AI Notes

Graphify embeds the current commit in graph/report output, so a bot refresh commit necessarily changes that metadata. The workflow's successful refresh and commit are the freshness guarantee; it no longer performs an impossible post-commit exact-diff check.

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

I inspected the final Graphify CI correction and accept it for merge.

---

# Final Outcome

**Status:** Complete
