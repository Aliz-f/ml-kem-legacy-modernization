# AI Task 0154 — Repair failed CI test assertions

**Status:** Complete

**Created:** 2026-10-03T19:06:19+03:00

**Updated:** 2026-10-03T19:16:29+03:00

**Agent:** Codex

---

# Task

Repair the two CI test failures without changing frozen protocol behavior.

---

# Prompt

fix them

---

# AI Implementation — Initial

## LLM Output

Updated the static-output allowlist for the legitimate baseline E2E JSON-report CLI and corrected the crypto-workflow assertion to locate duplicate suite paths after the crypto step.

## Files Created

- docs/ai/history/0154-repair-failed-ci-test-assertions.md

## Files Modified

- edge_gateway/tests/test_static_checks.py
- tests/test_gateway_crypto_ci.py
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest edge_gateway/tests/test_static_checks.py tests/test_gateway_crypto_ci.py; uv run ruff check .; uv run ai-history check; uv run python scripts/refresh_graphify.py

### Results

- Focused regression tests: 4 passed. Ruff and AI-history validation passed. Graphify refresh completed.

## AI Notes

The reported pre-fix full CI suite had 2 failed and 1446 passed; no frozen protocol behavior, endpoints, crypto, retry, or storage behavior changed.

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
