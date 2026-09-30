# AI Task 0034 — Implement Legacy Device failure injection

**Status:** Complete

**Created:** 2026-09-29T21:20:16+03:00

**Updated:** 2026-09-30T01:59:59+03:00

**Agent:** GitHub Copilot

---

# Task

Implement M1-04 failure injection after serialization with deterministic focused tests, preserving the frozen protocol and valid Measurement state.

---

# Prompt

Implement task M1-04: Legacy Device failure-injection subsystem. Read and follow the repository policy, workflow, roadmap, Legacy Device design, shared protocol, Member 1 task document, relevant AI instructions, and both required Group-Explanation PDFs before implementation. Inspect existing code and tests, implement only M1-04, add focused deterministic tests, run relevant tests and Ruff plus ai-history check, record factual results, and stop for human review.

---

# AI Implementation — Initial

## LLM Output

Implemented M1-04 failure injection after serialization with deterministic tests.

## Files Created

- docs/ai/history/0027-implement-legacy-device-failure-injection.md
- legacy_system/src/legacy_system/failure.py
- legacy_system/tests/test_failure.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest legacy_system/tests; uv run ruff check legacy_system; uv run ruff check .; uv run ai-history check; uv run pytest

### Results

- Legacy tests: 49 passed. Legacy Ruff: passed. Repository Ruff: passed. AI-history validation: passed. Full repository tests: 304 passed, 2 failed in existing tests/ai_history/test_cli.py due encoding/revision assertions unrelated to M1-04.

## AI Notes

Added failure.py and test_failure.py only. Full-suite test execution generated cloud.db, which was removed. No secrets, protocol fields, or simulation markers were added.

---

# Human Review — Round 1

## Problems Found

Mutation values are static, so a selected failure mode always produces the same invalid payload. Tests do not verify seed-dependent mutation variation, valid Measurement preservation, or sensor/sequence-state preservation.

## Decision

Modified

## Requested Modifications

Generate mutation values from the seeded fault-simulation PRNG, retain valid Measurement and sequence state, and expand tests to cover the missing behaviors.

---

# AI Revision — Round 1

## Revision Summary

Revised M1-04 to generate seed-dependent mutation values and expanded coverage for mutation variation, sequence history, valid Measurement preservation, and skipped logging.

## Files Created

- docs/ai/history/0027-implement-legacy-device-failure-injection.md
- legacy_system/src/legacy_system/failure.py
- legacy_system/tests/test_failure.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest legacy_system/tests; uv run ruff check legacy_system; uv run ruff check .; uv run ai-history check

### Results

- Legacy tests: 57 passed. Legacy Ruff: passed. Repository Ruff: passed. AI-history validation: passed. Focused M1-04 tests: 22 passed. Diagnostics: no errors in revised files.

## AI Notes

Invalid temperature and humidity values are generated outside protocol ranges from the seeded fault PRNG. Invalid timestamps vary by seed, duplicate faults select from previously observed sequences, and valid input state remains unchanged. No protocol fields or simulation metadata were added.

---

# Human Review — Round 2

## Problems Found

The test helpers still duplicate Measurement construction. The first duplicate_sequence call can return the current sequence and log an injected duplicate even though no previous sequence exists. One test name claims to verify monotonic Sensor state although it only checks input immutability. Seed-variation tests rely on single outputs from seeds 1 and 2.

## Decision

Modified

## Requested Modifications

Refactor the helpers, make first-call duplicate injection a no-op without a failure log, rename the misleading test, and compare short output sequences for seeded variation.

---

# AI Revision — Round 2

## Revision Summary

Applied the second M1-04 review revision: deduplicated test helpers, skipped first duplicate injection without history, corrected test naming, and strengthened seeded variation checks.

## Files Created

- docs/ai/history/0027-implement-legacy-device-failure-injection.md
- legacy_system/src/legacy_system/failure.py
- legacy_system/tests/test_failure.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest legacy_system/tests/test_failure.py; uv run pytest legacy_system/tests; uv run ruff check legacy_system; uv run ruff check .; uv run ai-history check

### Results

- Focused M1-04 tests: 23 passed. Legacy tests: 58 passed. Legacy Ruff: passed. Repository Ruff: passed. AI-history validation: passed. Diagnostics: no errors in revised files. Git diff check: passed.

## AI Notes

The first duplicate_sequence request now returns an unchanged payload without an injection log when no previous sequence exists. Later duplicate requests select from observed sequence history. No M1-05 or later work was added.

---

# Human Review — Round 3

## Problems Found

The first-call duplicate_sequence path still returns a clean payload after injection is selected. The unreachable current-sequence fallback remains, and tests cover a no-op rather than the required error. The behavior also needs to be recorded as a documentation clarification opportunity without changing documentation in this feature branch.

## Decision

Modified

## Requested Modifications

Raise a clear ValueError when duplicate_sequence has no previous sequence history, remove the fallback, add focused error and later-duplicate tests, and record the documentation clarification opportunity in the AI-history revision notes only.

---

# AI Revision — Round 3

## Revision Summary

Replaced silent first-call duplicate injection with an explicit error and added focused history/error tests.

## Files Created

- docs/ai/history/0027-implement-legacy-device-failure-injection.md
- legacy_system/src/legacy_system/failure.py
- legacy_system/tests/test_failure.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest legacy_system/tests/test_failure.py; uv run pytest legacy_system/tests; uv run ruff check legacy_system; uv run ruff check .; uv run ai-history check

### Results

- Focused M1-04 tests: 23 passed. Legacy tests: 58 passed. Legacy Ruff: passed. Repository Ruff: passed. AI-history validation: passed. Diagnostics: no errors in revised files. Git diff check: passed.

## AI Notes

duplicate_sequence now raises ValueError when no previously observed sequence history exists; later calls select from recorded prior sequences and preserve input payloads. This exposed a documentation clarification opportunity for M1-04: explicitly define first-use duplicate_sequence behavior. Documentation was intentionally not changed in this feature branch; the clarification can be proposed after team agreement.

---

# Human Review — Round 4

## Problems Found

No problems found in the latest revision.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final implementation and tests, confirmed the requested modifications are complete, and accept the result.

---

# Final Outcome

**Status:** Complete
