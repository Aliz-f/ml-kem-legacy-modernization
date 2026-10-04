# AI Task 0178 — Repair M5 CI documentation contract regressions

**Status:** Complete

**Created:** 2026-10-04T12:05:02+03:00

**Updated:** 2026-10-04T12:07:33+03:00

**Agent:** Codex

---

# Task

Repair the three CI-contract failures caused by the M5 CI separation and restart-recovery documentation changes. Align stale test expectations with the current split workflow, retain required workflow-guide wording, and preserve the original Compose recovery test name in the matrix evidence. Do not change CI execution behavior or protocol/service behavior.

---

# Prompt

after commiting, we have this in CI: [three failing documentation and CI-contract tests] fix it

---

# AI Implementation — Initial

## LLM Output

Repaired the CI-contract regressions from the split M5 workflow: restored required CI-stage wording in the development workflow, retained the original Cloud-restart test as matrix evidence, and updated the stale crypto-CI test to validate the current unit-test job layout. No CI execution, protocol, service, Docker, or crypto behavior changed.

## Files Created

- docs/ai/history/0178-repair-m5-ci-documentation-contract-regressions.md

## Files Modified

- docs/DEVELOPMENT_WORKFLOW.md
- docs/ai/.state.json
- docs/testing/PROJECT_TEST_MATRIX.md
- graphify-out/graph.json
- tests/test_gateway_crypto_ci.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check . && uv run pytest && uv run ai-history check && git diff --check

### Results

- Passed: Ruff reported no issues; pytest collected 1501 tests and completed successfully; AI-history validation and whitespace validation passed. The three reported regressions plus related CI-contract tests passed (15 tests).

## AI Notes

The failure was a textual/contract mismatch after CI job separation, not a runtime CI behavior defect. Graphify was refreshed after the test change.

---

# Human Review — Round 1

## Problems Found

I do not find any problem durin manual review

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
