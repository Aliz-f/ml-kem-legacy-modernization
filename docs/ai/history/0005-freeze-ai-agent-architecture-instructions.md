# AI Task 0005 — Freeze AI-agent architecture instructions

**Status:** Complete

**Created:** 2026-09-22T14:10:00+03:00

**Updated:** 2026-09-22T14:17:24+03:00

**Agent:** Codex

---

# Task

Update repository AI-agent and development-workflow instruction files to require the frozen architecture, protocol, roadmap, ownership, scope, testing, and review constraints; do not modify application code.

---

# Prompt

Update the repository’s AI-agent instruction files so Codex, Claude, Grok, and other coding agents follow the frozen architecture and implementation baseline before making changes. Update AGENTS.md, CLAUDE.md, GROK.md, docs/DEVELOPMENT_WORKFLOW.md, docs/GROK_BUILD_WORKFLOW.md, and clearly necessary synchronized guidance. Do not modify application code.

---

# AI Implementation — Initial

## LLM Output

Expanded the canonical AI-agent contract and synchronized Claude, Grok, team workflow, and README guidance with mandatory architecture/roadmap reading, frozen-protocol drift controls, ownership/scope gates, and verification rules. No application code was modified.

## Files Created

- docs/ai/history/0005-freeze-ai-agent-architecture-instructions.md
- docs/architecture/

## Files Modified

- AGENTS.md
- CLAUDE.md
- GROK.md
- README.md
- docs/DEVELOPMENT_WORKFLOW.md
- docs/GROK_BUILD_WORKFLOW.md
- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check; git diff --check

### Results

- ruff: All checks passed; pytest: 5 passed; ai-history check: validation passed; git diff --check: passed.

## AI Notes

Documentation-only change. Existing untracked docs/architecture/ content was not modified by this task.

---

# Human Review — Round 1

## Problems Found

No problems found during human review.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final implementation and accept it.

---

# Final Outcome

**Status:** Complete
