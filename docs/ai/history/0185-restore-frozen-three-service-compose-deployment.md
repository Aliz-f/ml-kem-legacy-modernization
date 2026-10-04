# AI Task 0185 — Restore frozen three-service Compose deployment

**Status:** Complete

**Created:** 2026-10-04T13:01:59+03:00

**Updated:** 2026-10-04T13:09:02+03:00

**Agent:** Codex

---

# Task

Fix the architecture-audit findings: Docker Compose must run legacy-device, edge-gateway, and cloud-service with service-scoped Legacy configuration; add a relevant Compose regression; correct stale deployment and project-status documentation. Preserve all frozen protocols and exclude unrelated Member 1 changes.

---

# Prompt

fix all three inconsistencies

---

# AI Implementation — Initial

## LLM Output

Restored the frozen three-service Docker Compose topology by adding legacy-device with its scoped runtime and failure configuration. Added a live Compose regression that verifies containerized Legacy delivery to SQLite, reconciled deployment/testing/project documentation, superseded the incompatible two-service decision entry, updated documentation tests, and refreshed Graphify artifacts.

## Files Created

- docs/ai/history/0185-restore-frozen-three-service-compose-deployment.md

## Files Modified

- README.md
- docker-compose.yml
- docs/AI_DECISION_REGISTER.md
- docs/ai/.state.json
- docs/deployment/sqlite-persistence.md
- docs/testing/DEVELOPER_TESTING_GUIDE.md
- docs/testing/M5_DEPLOYMENT_RECOVERY.md
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json
- tests/integration/test_gateway_compose_e2e.py
- tests/test_developer_testing_guide.py
- tests/test_sqlite_persistence_strategy_document.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- docker compose config --quiet; uv run pytest -q tests/integration/test_gateway_compose_e2e.py::test_compose_starts_legacy_device_and_persists_a_measurement; uv run pytest -q; uv run ruff check .; uv run python scripts/refresh_graphify.py; uv run ai-history check

### Results

- Compose configuration valid; new three-service Compose regression passed (1 passed); full pytest completed successfully; Ruff passed; Graphify refreshed; AI-history validation passed.

## AI Notes

No protocol, crypto, endpoint, schema, status-code, retry, session, or storage contract changed. The full suite output was progress-truncated by the execution interface, but the command exited successfully.

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
