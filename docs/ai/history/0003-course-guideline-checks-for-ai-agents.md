# AI Task 0003 — Course Guideline Checks for AI Agents

**Status:** Complete

**Created:** 2026-09-10T17:41:24+03:00

**Updated:** 2026-09-10T17:43:57+03:00

**Agent:** Codex

---

# Task

Update the canonical AI-agent policy and agent-specific adapters so agents must review the two course guideline PDFs before developing a new feature.

---

# Prompt

Based on Group-Explanation 01.pdf and Group-Explanation 02.pdf, update AGENTS.md and related agent instruction files to require checking the course guidelines before new feature development, without implementing application functionality.

---

# AI Implementation — Initial

## LLM Output

Updated the canonical AI-agent policy and Claude/Copilot adapters to require reading both supplied course-guideline PDFs before planning, designing, or implementing any new feature. The policy also captures the course constraints on scope, AI evaluation and documentation, maintained ML-KEM libraries, and personal reflections.

## Files Created

- .env.example
- .github/
- .gitignore
- .python-version
- AGENTS.md
- CLAUDE.md
- "Group-Explanation 01.pdf"
- "Group-Explanation 02.pdf"
- README.md
- cloud_service/
- docker-compose.yml
- docs/
- edge_gateway/
- legacy_system/
- pyproject.toml
- src/
- tests/
- uv.lock

## Files Modified

- AGENTS.md
- CLAUDE.md
- .github/copilot-instructions.md
- docs/ai/history/0003-course-guideline-checks-for-ai-agents.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- pdftotext 'Group-Explanation 01.pdf' -
- pdftotext 'Group-Explanation 02.pdf' -
- uv run ai-history check

### Results

- Both supplied PDF course-guideline documents were read successfully.
- AI-history validation passed.

## AI Notes

Instruction files guide compatible agents but cannot technically force every external AI product to read local documents.

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

I verify it.

---

# Final Outcome

**Status:** Complete
