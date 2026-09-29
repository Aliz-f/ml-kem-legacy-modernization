# AI Task 0011 — Implement Legacy measurement model

**Status:** Complete

**Created:** 2026-09-28T22:14:57+03:00

**Updated:** 2026-09-28T23:59:04+03:00

**Agent:** GitHub Copilot

---

# Task

Implement task M1-02: add a valid Legacy Device Measurement model and explicit serializer for the frozen Legacy-to-Gateway payload, with focused tests. Keep it independent from HTTP, retries, Gateway, Cloud, ML-KEM, sensor generation, and failure injection; do not implement later M1 tasks.

---

# Prompt

Implement task M1-02: Legacy Device measurement data model and serialization. Read and follow AGENTS.md and the repository documents required by it. Inspect the existing Legacy Device code and tests before editing. Implement only M1-02. Add the smallest suitable measurement model and an explicit serializer for the frozen Legacy-to-Gateway payload. Keep the model independent from HTTP, retry, Gateway, Cloud, ML-KEM, sensor generation, and failure injection. Pay particular attention to the M1-02 invariant: Measurement must represent valid internal state only. Malformed payload cases belong to a later serialization/failure-injection step. Add focused tests for model validation, exact field names, numeric and timestamp serialization, sequence serialization, and independence of the returned payload. Run: uv run pytest legacy_system/tests; uv run ruff check legacy_system; uv run ai-history check. Use the AI-history workflow, record the actual prompt and factual results, and stop at human review. Do not implement later M1 tasks, modify unrelated files, commit changes, or run human review/final verification commands yourself.

---

# AI Implementation — Initial

## LLM Output

Added a validated Measurement dataclass in legacy_system.sensor with explicit to_payload serialization and focused M1-02 tests for validation, frozen field names, numeric/timestamp/sequence serialization, and payload independence.

## Files Created

- docs/ai/history/0010-implement-legacy-measurement-model.md
- legacy_system/src/legacy_system/sensor.py
- legacy_system/tests/test_sensor.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest legacy_system/tests; uv run ruff check legacy_system; get_errors on touched files; uv run ai-history check

### Results

- pytest: 34 passed. ruff: All checks passed. Editor diagnostics: no errors in sensor.py or test_sensor.py. AI-history check: pending final command.

## AI Notes

Measurement is frozen internal state only; malformed payload mutation and later M1 tasks were not implemented. Timestamp values require timezone awareness and are normalized to UTC during construction. Awaiting human review.

---

# Human Review — Round 1

## Problems Found

Pylance reports a type warning in _validate_number when comparing float bounds with Real; the test suite lacks explicit coverage for converting a timezone-aware non-UTC timestamp to UTC Z serialization.

## Decision

Modified

## Requested Modifications

Convert the validated numeric value to a local float before math.isfinite() and range checks without changing Measurement field or payload numeric types. Add a focused test for correct UTC Z serialization from a non-UTC timestamp offset. Run relevant tests and Ruff, confirm the Pylance warning is resolved, record the revision, and stop for human review.

---

# AI Revision — Round 1

## Revision Summary

Resolved the Pylance numeric comparison warning by converting the validated Real value to a local float before finiteness and range checks. Added a focused test proving a +02:00 timestamp serializes to the correct UTC Z timestamp without changing Measurement field or payload numeric types.

## Files Created

- docs/ai/history/0010-implement-legacy-measurement-model.md
- legacy_system/src/legacy_system/sensor.py
- legacy_system/tests/test_sensor.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest legacy_system/tests; uv run ruff check legacy_system; editor diagnostics for sensor.py and test_sensor.py

### Results

- pytest: 35 passed. ruff: All checks passed. Editor diagnostics: no errors in sensor.py or test_sensor.py; the reported Pylance warning is resolved.

## AI Notes

Only the two requested review modifications were made. Task is returned to human review.

---

# Human Review — Round 2

## Problems Found

No problems identified during manual review.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final M1-02 implementation and tests, confirmed the requested modifications are complete, and accept the result.

---

# Final Outcome

**Status:** Complete
