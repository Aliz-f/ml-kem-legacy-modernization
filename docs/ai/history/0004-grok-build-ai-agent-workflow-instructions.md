# AI Task 0004 — Grok Build AI-agent workflow instructions

**Status:** Complete

**Created:** 2026-09-17T12:30:30+03:00

**Updated:** 2026-09-17T12:38:35+03:00

**Agent:** Codex

---

# Task

Add Grok Build-facing repository instructions that enforce the canonical AGENTS.md policy and AI-history human-review workflow without duplicating or weakening it.

---

# Prompt

one of my teammate want to use grok build to implement this project. you should write appropriate files to flow AGENTS.md instruction

---

# AI Implementation — Initial

## LLM Output

Added GROK.md as a Grok Build entry point, a teammate workflow guide, and README links. The new guidance defers to AGENTS.md and requires AI-history review and human verification.

## Files Created

- GROK.md
- docs/GROK_BUILD_WORKFLOW.md
- docs/ai/history/0004-grok-build-ai-agent-workflow-instructions.md

## Files Modified

- README.md
- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/ai_history; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check src/ai_history tests/ai_history; UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check; git diff --check

### Results

- pytest: 5 passed; ruff: All checks passed; ai-history check: validation passed; git diff --check: passed.

## AI Notes

Documentation-only change. The Grok Build integration is repository guidance, because no confirmed Grok Build-specific project-instructions file convention is present in this repository.

---

# Human Review — Round 1

## Problems Found

No problems found during manual rview.

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
