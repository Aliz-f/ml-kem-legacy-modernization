# AI Task 0002 — Development Workflow Handbook

**Status:** Complete

**Created:** 2026-09-10T16:46:47+03:00

**Updated:** 2026-09-10T17:39:26+03:00

**Agent:** Codex

---

# Task

Create docs/DEVELOPMENT_WORKFLOW.md as the detailed end-to-end handbook for teammates developing one task in this repository.

---

# Prompt

Create a highly detailed practical Markdown guide for the university group project. It must explain task selection through merge, use the existing Python 3.12 uv monorepo and real AI-history CLI commands, cover human review/revision/final verification, include ASCII and Mermaid visual explanations, and avoid incompatible invented commands.

---

# AI Implementation — Initial

## LLM Output

Created the main teammate development handbook covering task selection, repository synchronization, branching, AI-history workflow, implementation and checks, human review, revisions, final verification, commits, pull requests, peer review, merging, common mistakes, and quick reference. It uses real current repository commands and includes Mermaid and ASCII flow illustrations.

## Files Created

- docs/DEVELOPMENT_WORKFLOW.md

## Files Modified

- docs/ai/history/0002-development-workflow-handbook.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ai-history status
- uv run ai-history check

### Results

- Confirmed no active task before starting Task 0002.
- AI-history validation passed before recording completed work.

## AI Notes

The repository currently has no service implementation commands or service-specific test suites, so the handbook identifies such checks as task-dependent and does not invent them.

---

# Human Review — Round 1

## Problems Found

The Git rules are incomplete. The handbook must clearly explain how to use AI-history commands and whether teammates should run them or give prompts to the agent.

## Decision

Modified

## Requested Modifications

Document the team Git flow: main is the primary branch; develop receives all feature branches and is merged into main together; every feature branch starts from develop and uses the feat/ prefix. Clarify the end-to-end process when giving a new prompt to an AI agent, including which AI-history commands the agent runs and which commands require human input.

---

# AI Revision — Round 1

## Revision Summary

Expanded the development handbook with the required Git branch model: stable main, develop as the integration branch, feat/* branches created from develop, feature PRs targeting develop, and planned develop-to-main integration. Added a detailed new-prompt handoff sequence that distinguishes agent-run status/start/output/revision actions from human review and final-verification responsibilities.

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

- docs/DEVELOPMENT_WORKFLOW.md
- docs/ai/history/0002-development-workflow-handbook.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ai-history check

### Results

- AI-history validation passed before recording the revision.

## AI Notes

This revision documents the requested process only; it does not create or alter Git branches, remotes, pull requests, or application functionality.

---

# Human Review — Round 2

## Problems Found

The handbook must state that a feature branch is merged with the current develop branch before any changes are made, and again before opening a merge request to develop. It must also address how to avoid the same AI-history task number on different branches.

## Decision

Modified

## Requested Modifications

Add the two required develop synchronization steps. Document a process for unique AI-history task IDs when teammates work on different feature branches concurrently.

---

# AI Revision — Round 2

## Revision Summary

Added two mandatory develop synchronization points: merge current develop into a feature branch before any edits, and merge current develop again before opening a feature PR to develop. Added a documented reservation process and safe conflict-resolution procedure for concurrent AI-history task ID collisions across feature branches.

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

- docs/DEVELOPMENT_WORKFLOW.md
- docs/ai/history/0002-development-workflow-handbook.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ai-history check

### Results

- AI-history validation passed before recording the revision.

## AI Notes

The ID-collision procedure is process-based because the local CLI allocates IDs from the checked-out history and has no shared remote locking service.

---

# Human Review — Round 3

## Problems Found

The task-ID collision explanation is unclear. The repository needs an implemented way to resolve duplicate AI-history task IDs during a merge, and history should be ordered by creation date and time.

## Decision

Modified

## Requested Modifications

Implement an AI-history command/workflow that resolves same-ID history merge conflicts while preserving both records and allocating a correct later ID. Order displayed history by Created timestamp.

---

# AI Revision — Round 3

## Revision Summary

Implemented same-ID history merge-conflict resolution and creation-time ordering. The new resolve-merge-conflict command splits a simple two-way Git conflict, preserves both Markdown histories, retains the earlier-created task ID, and assigns the later-created record the next sequential ID. Updated the handbook with this command and its active-task limitation.

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

- src/ai_history/cli.py
- src/ai_history/storage.py
- docs/DEVELOPMENT_WORKFLOW.md
- docs/ai/history/0002-development-workflow-handbook.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check src/ai_history
- uv run pytest tests/ai_history
- uv run ai-history --help
- uv run ai-history check

### Results

- Ruff passed.
- pytest: 5 passed.
- CLI help and AI-history validation passed.

## AI Notes

The resolver supports simple two-way same-ID conflict markers and deliberately refuses active-task conflicts, which require the task owner to decide the correct state-file mapping.

---

# Human Review — Round 4

## Problems Found

No problems identified during manual review.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

It is verified.

---

# Final Outcome

**Status:** Complete
