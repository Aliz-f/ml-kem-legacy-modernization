# AI Task 0164 — Build project-wide technical-debt and risk registers

**Status:** Complete

**Created:** 2026-10-03T23:32:23+03:00

**Updated:** 2026-10-03T23:34:13+03:00

**Agent:** Codex

---

# Task

Implement M5-81 and M5-82 only. Add a project-wide technical-debt register and a separate security/operational risk register derived from the frozen architecture and existing evidence. Record component ownership, risk or impact, why debt is accepted or current controls, and proportionate future improvement or treatment. Explicitly preserve that business idempotency is not cryptographic replay protection. Add focused document regression tests. Do not implement new features or change protocol, service, deployment, or cryptographic behavior.

---

# Prompt

now, implement M5-81 and M5-82

---

# AI Implementation — Initial

## LLM Output

Added separate project-wide M5-81 technical-debt and M5-82 risk registers. The debt register coordinates frozen course-system limitations, components, accepted rationale, and future improvements. The risk register records linked security/operational events, qualitative residual assessments, current controls, and treatment. Added focused regression checks that preserve the idempotency-versus-cryptographic-replay distinction.

## Files Created

- docs/ai/history/0162-create-project-wide-test-matrix.md
- docs/ai/history/0163-coordinate-security-regressions-and-verify-fail-closed-behavior.md
- docs/ai/history/0164-build-project-wide-technical-debt-and-risk-registers.md
- docs/risk-register.md
- docs/technical-debt.md
- docs/testing/M5_SECURITY_REGRESSION_SUITE.md
- docs/testing/PROJECT_TEST_MATRIX.md
- tests/test_m5_security_regression_suite_document.py
- tests/test_project_registers.py
- tests/test_project_test_matrix_document.py

## Files Modified

- docs/ai/.state.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_mlkem_handshake_failure_demo.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest tests/test_project_registers.py && uv run ruff check . && uv run pytest && uv run python scripts/refresh_graphify.py && uv run ai-history check && git diff --check

### Results

- Focused register checks passed (3 tests); Ruff passed; full pytest passed (1477 tests); Graphify refresh, AI-history validation, and diff check passed.

## AI Notes

Registers are documentation only and do not authorize protocol, service, deployment, or cryptographic changes. Likelihood and impact labels are explicitly qualitative course-project assessments, not measured production probabilities.

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
