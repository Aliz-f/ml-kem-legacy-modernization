# AI Task 0031 — Automate Graphify refresh in agent workflow

**Status:** Complete

**Created:** 2026-09-30T12:15:56+03:00

**Updated:** 2026-09-30T12:22:40+03:00

**Agent:** Codex

---

# Task

Replace CI graph write-back with a repository-owned normalized refresh command that agents run before final checks and commits, and make CI verify rather than mutate shared Graphify artifacts.

---

# Prompt

ok, now implement this feature/fixation changes.

---

# AI Implementation — Initial

## LLM Output

Replaced Graphify CI write-back with an agent-run normalized refresh command and read-only CI verification, including tests for volatile metadata removal.

## Files Created

- docs/ai/history/0031-automate-graphify-refresh-in-agent-workflow.md
- scripts/refresh_graphify.py
- tests/test_refresh_graphify.py

## Files Modified

- .github/workflows/graphify.yml
- AGENTS.md
- docs/ai/.state.json
- docs/development/graphify.md
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run python scripts/refresh_graphify.py; sha256sum graphify-out/graph.json graphify-out/GRAPH_REPORT.md; uv run pytest tests/test_refresh_graphify.py; uv run ruff check .; uv run pytest; uv run ai-history check

### Results

- Two consecutive normalized refreshes produced identical graph/report checksums; focused refresh test passed; Ruff passed; 298 tests passed with one existing FastAPI deprecation warning; AI-history validation passed.

## AI Notes

CI now has read-only contents permission and fails on stale committed graph/report artifacts. Graphify extraction remains local and code-only.

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

I inspected the final agent-managed Graphify refresh redesign and accept it for merge.

---

# Final Outcome

**Status:** Complete
