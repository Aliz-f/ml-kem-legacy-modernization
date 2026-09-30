# AI Task 0037 — Make Graphify refresh independent of incremental cache state

**Status:** Complete

**Created:** 2026-09-30T13:01:12+03:00

**Updated:** 2026-09-30T13:05:31+03:00

**Agent:** Codex

---

# Task

Repair the shared Graphify refresh command so local and CI regeneration produce the same committed graph when ignored Graphify incremental state exists. Clear only documented generated Graphify cache/manifest state before extraction, retain the committed graph/report contract, add focused regression coverage, and do not change application or frozen protocol behavior.

---

# Prompt

ok, now let's fix all of the problems, check for in inconsistency and if there wasn't anything, merge PR#13 into develop and close the PR

---

# AI Implementation — Initial

## LLM Output

Made the shared Graphify refresh deterministic across local and clean CI environments. It clears only ignored generated state before extraction and invokes both Graphify subprocesses with PYTHONHASHSEED=0, preventing cache- and hash-order-dependent graph communities. Added focused tests for preserving committed artifacts and passing the fixed seed.

## Files Created

- docs/ai/history/0037-make-graphify-refresh-independent-of-incremental-cache-state.md

## Files Modified

- docs/ai/.state.json
- scripts/refresh_graphify.py
- tests/test_refresh_graphify.py
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest tests/test_refresh_graphify.py
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py (twice; compared SHA-256 hashes)
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check
- git diff --check

### Results

- Focused Graphify tests: 3 passed.
- Two clean refreshes produced identical SHA-256 hashes for graph.json and GRAPH_REPORT.md after the fixed hash seed was applied.
- Repository Ruff: passed.
- Full repository suite: 386 passed; one existing FastAPI/Starlette deprecation warning.
- AI-history and whitespace validation: passed.

## AI Notes

No application, endpoint, schema, status-code, cryptographic, retry, session, storage, or ownership behavior changed. The reset deletes only ignored entries beneath the fixed graphify-out directory and preserves the two committed shared artifacts. The closed PR will be reopened only after this correction completes the required human-review and final-verification gates.

---

# Human Review — Round 1

## Problems Found

I do not find any problems during manual review

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- Focused Graphify tests: 3 passed.
- Two clean refreshes produced identical SHA-256 hashes for graph.json and GRAPH_REPORT.md.
- Repository Ruff: passed.
- Full repository suite: 386 passed; one existing FastAPI/Starlette deprecation warning.
- AI-history and whitespace validation: passed.

## Human-Confirmed Verification

I verify it

---

# Final Outcome

**Status:** Complete
