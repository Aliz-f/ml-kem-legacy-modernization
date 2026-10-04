# AI Task 0180 — Repair gateway restart ML-KEM session regression

**Status:** Complete

**Created:** 2026-10-04T12:17:43+03:00

**Updated:** 2026-10-04T12:23:17+03:00

**Agent:** Codex

---

# Task

Fix the Compose gateway-restart integration regression so a restarted Gateway establishes a fresh in-memory ML-KEM session under the frozen session and metrics contracts.

---

# Prompt

fix it: test_compose_gateway_restart_establishes_a_fresh_mlkem_session fails because cloud_mlkem_sessions_created_total remains 1 after restarting the Gateway and sending the second measurement.

---

# AI Implementation — Initial

## LLM Output

Made the M5-78 Compose Gateway restart test force a fresh edge-gateway container before its second measurement, guaranteeing Gateway-local in-memory ML-KEM session loss and a new handshake.

## Files Created

- docs/ai/history/0180-repair-gateway-restart-ml-kem-session-regression.md

## Files Modified

- docs/ai/.state.json
- graphify-out/graph.json
- tests/integration/test_gateway_compose_e2e.py

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run python scripts/refresh_graphify.py; uv run ruff check .; uv run pytest tests/integration/test_gateway_compose_e2e.py; uv run ai-history check

### Results

- Graphify refresh completed; Ruff passed; the 5-test Compose integration module passed; AI history validation passed.

## AI Notes

The focused regression was initially non-reproducible locally. The change makes the Docker lifecycle explicit without changing frozen protocol, session, or metrics contracts.

---

# Human Review — Round 1

## Problems Found

No problems reported; reviewer decision supplied as Accepted.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- uv run ruff check .
- uv run pytest tests/integration/test_gateway_compose_e2e.py
- uv run ai-history check

## Human-Confirmed Verification

I verify it.

---

# Final Outcome

**Status:** Complete
