# AI Task 0058 — Design project-wide failure test matrix

**Status:** Complete

**Created:** 2026-09-30T17:09:45+03:00

**Updated:** 2026-09-30T17:12:21+03:00

**Agent:** Codex

---

# Task

Implement M5-39 only. Add a project-wide failure-test matrix document derived from the frozen protocol, roadmap, and Member 5 task list. Cover F1 through F18 with fault owner, injection scenario, expected externally observable result, and later automation task. Explicitly retain the ML-KEM implicit-rejection caveat and state that protocol v1 has no dedicated cryptographic replay-rejection test. Add focused regression coverage for the matrix structure and frozen session/retry semantics. Do not implement any fault injection or live failure tests.

---

# Prompt

let\x27s implement M5-39

---

# AI Implementation — Initial

## LLM Output

Completed M5-39 by adding the project-wide F1–F18 failure-test matrix. Each scenario identifies its fault owner, injected condition, frozen observable result, and later automation task. The matrix explicitly distinguishes one-time session recovery from ordinary identical-envelope retransmission, preserves fail-closed behavior, records the ML-KEM implicit-rejection caveat, and excludes a nonexistent protocol-v1 crypto replay test. Added focused matrix regression checks and refreshed Graphify artifacts.

## Files Created

- docs/ai/history/0055-complete-member-5-hygiene-and-environment-example.md
- docs/ai/history/0056-add-foundational-repository-quality-ci.md
- docs/ai/history/0057-add-shared-integration-test-scaffold-and-fixtures.md
- docs/ai/history/0058-design-project-wide-failure-test-matrix.md
- docs/testing/
- tests/fixtures/
- tests/integration/test_end_to_end.py
- tests/integration/test_failure_paths.py
- tests/integration/test_gateway_cloud_baseline.py
- tests/integration/test_gateway_cloud_secure.py
- tests/integration/test_legacy_gateway.py
- tests/test_ci_workflow.py
- tests/test_failure_matrix_document.py
- tests/test_repository_hygiene.py
- tests/test_shared_integration_assets.py

## Files Modified

- .env.example
- .github/workflows/ai-history.yml
- .gitignore
- docs/DEVELOPMENT_WORKFLOW.md
- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest tests/test_failure_matrix_document.py && uv run ruff check . && uv run pytest && uv run python scripts/refresh_graphify.py && uv run ai-history check && git diff --check

### Results

- Targeted matrix tests passed; Ruff passed; pytest passed (642 tests, one existing FastAPI/httpx deprecation warning); Graphify refresh completed with its optional PDF-extraction warning; AI-history validation and diff check passed.

## AI Notes

M5-39 is planning/documentation only. No failure injection, live failure scenario, protocol behavior, or service implementation was changed. Existing approved but uncommitted Member 5 task changes were preserved.

---

# Human Review — Round 1

## Problems Found

I do not find any problem during manual review.

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
