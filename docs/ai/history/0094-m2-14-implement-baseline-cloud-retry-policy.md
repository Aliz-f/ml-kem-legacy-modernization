# AI Task 0094 — M2-14 implement baseline Cloud retry policy

**Status:** Complete

**Created:** 2026-10-01T13:35:18+03:00

**Updated:** 2026-10-01T14:59:50+03:00

**Agent:** Codex

---

# Task

Implement the Member 2 M2-14 bounded ordinary retry policy for the classical BaselineCloudClient: retry only classified network, timeout, HTTP 500/502/503/504 failures for at most CLOUD_MAX_RETRIES additional attempts, use the frozen 1-second then 2-second backoff with injectable sleep, preserve one logical canonical JSON body and X-Request-ID across retries, and stop on permanent errors. Preserve separate secure session recovery and fail-closed ML-KEM behavior. Do not add M2-15 mappings, M2-16 real Cloud integration, failure injection, develop synchronization, commit, push, or PR.

---

# Prompt

im member 2 now do the task Task M2-14 — Implement Cloud retry policy in this branch

---

# AI Implementation — Initial

## LLM Output

Implemented M2-14 bounded ordinary retry policy for the baseline Gateway-to-Cloud client. BaselineCloudClient now takes CLOUD_MAX_RETRIES, serializes once, retries only retryable BaselineCloudError results for at most configured additional attempts, and uses frozen 1-second then 2-second backoff through injected sleep. Every attempt reuses the same canonical JSON bytes and X-Request-ID. Permanent responses stop immediately; exhausted transient errors remain classified retryable for safe Legacy 503 handling. Classical application composition passes the configured retry count. Added retry test coverage and updated documentation and test configurations to suppress retries where tests verify unrelated behavior. Refreshed Graphify artifacts.

## Files Created

- docs/ai/history/0094-m2-14-implement-baseline-cloud-retry-policy.md

## Files Modified

- edge_gateway/src/edge_gateway/cloud/baseline.py
- edge_gateway/src/edge_gateway/app.py
- edge_gateway/tests/test_baseline_client.py
- edge_gateway/tests/test_gateway_app.py
- edge_gateway/tests/test_gateway_validation.py
- edge_gateway/README.md
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest edge_gateway/tests/test_baseline_client.py edge_gateway/tests/test_gateway_app.py edge_gateway/tests/test_gateway_validation.py edge_gateway/tests/test_gateway_measurements.py edge_gateway/tests/test_dispatch.py -q
- uv run python scripts/refresh_graphify.py
- uv run ruff check .
- uv run pytest -q
- uv run ai-history check
- git diff --check

### Results

- Focused M2-14 Gateway suite: 196 passed, 1 existing Starlette/httpx deprecation warning. Full repository suite completed successfully under approved local-socket execution; console output was truncated after passing progress. Ruff, AI-history validation, Graphify refresh, and whitespace check passed. Commands used UV_CACHE_DIR=/private/tmp/mlkem-uv-cache.

## AI Notes

Read frozen shared protocol retry/backoff sections, roadmap Phase 3 G7, Member 2 M2-14, and existing baseline/secure transport implementation. Retries remain baseline ordinary transport only; Member 3 secure session recovery stays separate and ML-KEM fail-closed behavior is unchanged. M2-15 response-mapping refinements and M2-16 real baseline Cloud integration remain out of scope. Before work, required feature-branch synchronization merged origin/develop at b3adc4e; only generated Graphify artifacts conflicted and were regenerated. The merge exposed duplicate AI-history IDs 0086-0089. Preserved all histories by chronological renumbering, recorded in a9e2629 and 8a8ab9a, restoring valid sequential history. No protocol/dependency changes. No M2-14 commit, push, or PR. Human review and final verification remain required.

---

# Human Review — Round 1

## Problems Found

No problems found.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final implementation and accept it.

---

# Final Outcome

**Status:** Complete
