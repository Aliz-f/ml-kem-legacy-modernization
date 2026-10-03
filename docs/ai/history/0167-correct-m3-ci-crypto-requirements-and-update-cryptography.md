# AI Task 0167 — Correct M3 CI crypto requirements and update cryptography

**Status:** Complete

**Created:** 2026-10-04T00:05:42+03:00

**Updated:** 2026-10-04T00:11:46+03:00

**Agent:** Codex

---

# Task

Correct the M3-63 CI wording and CI selection so it validates the intentional absence of protocol-v1 key confirmation and the replay limitation; update the locked cryptography dependency from 50.0.1 to 50.0.2 and align current dependency/review documentation without altering historical records or frozen protocol contracts.

---

# Prompt

fix both of them, then again check for finding any inconsistency

---

# AI Implementation — Initial

## LLM Output

Corrected the M3-63 CI checklist to test protocol-v1 key-confirmation absence and replay limits, added that invariant checklist to the named CI crypto stage, updated the cryptography lock to 50.0.2, and aligned current dependency and container-review documentation.

## Files Created

- docs/ai/history/0166-correct-stale-member-2-ai-history-references.md
- docs/ai/history/0167-correct-m3-ci-crypto-requirements-and-update-cryptography.md
- tests/test_member2_history_references.py

## Files Modified

- uv.lock, .github/workflows/ai-history.yml, docs/architecture/08 - Member 3 Tasks.md, edge_gateway/docs/dependency-review.md, edge_gateway/docs/final-secure-transport-review.md, edge_gateway/docs/crypto-image.md, edge_gateway/docs/static-checks.md, cloud_service/docs/mlkem-key-service.md, tests/test_gateway_crypto_ci.py, graphify-out/graph.json, graphify-out/GRAPH_REPORT.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv sync --frozen; uv run pytest edge_gateway/tests/test_crypto_review_checklist.py edge_gateway/tests/test_dependency_review.py tests/test_gateway_crypto_ci.py; uv run ruff check .; uv run pytest -q; uv run pytest -q tests/integration/test_clean_container_crypto.py tests/integration/test_gateway_crypto_image.py; uv run python scripts/refresh_graphify.py; uv run ai-history check; git diff --check

### Results

- Passed: targeted tests 7, full suite 1482, Docker crypto-image tests 8, Ruff, Graphify refresh, AI-history validation, and diff check.

## AI Notes

Second consistency scan found and corrected stale current cryptography version references and stale Docker-test review markers; historical 50.0.1 evidence is explicitly marked historical. No remaining material M3 protocol, CI, dependency-lock, or current verification inconsistency was found.

---

# Human Review — Round 1

## Problems Found

No problems reported during manual review.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- Targeted tests, full pytest, Docker crypto-image tests, Ruff, Graphify refresh, AI-history validation, and diff check passed before human review.

## Human-Confirmed Verification

I verify it.

---

# Final Outcome

**Status:** Complete
