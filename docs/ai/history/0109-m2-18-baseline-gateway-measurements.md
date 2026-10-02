# AI Task 0109 — M2-18 baseline Gateway measurements

**Status:** Complete

**Created:** 2026-10-01T23:59:01+03:00

**Updated:** 2026-10-02T00:26:31+03:00

**Agent:** Codex

---

# Task

Collect reproducible Gateway baseline request counts, durations, retries and canonical payload sizes using existing live integration coverage; preserve frozen contracts and Member 5 ownership.

---

# Prompt

im member 2 in the same branch do task Task M2-18 — Baseline Gateway measurements

---

# AI Implementation — Initial

## LLM Output

Added a small M2-18 baseline evidence collector to the existing live Gateway integration module. It measures 100 successful Legacy requests, four rejection controls, and a separate real SQLite write-failure case with two real retries. Reports request counts, Gateway route duration, Cloud delivery and per-attempt latency, canonical body bytes, and verified persisted rows. Documented reproducible workload, measurement boundaries, limitations, and an actual local sample. Updated prior M2-16/17 readiness and log assertions for current Cloud behavior. Regenerated Graphify artifacts and reconciled incoming duplicate history IDs.

## Files Created

- edge_gateway/docs/baseline-measurements.md

## Files Modified

- edge_gateway/tests/test_gateway_baseline_integration.py
- edge_gateway/README.md
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md
- docs/ai/history: incoming Cloud records renamed from duplicate 0104/0105 to 0107/0108; only headings and self-paths updated

## Files Deleted

- docs/ai/history/0104-m4-pr11-pr13-cloud-operations-observability-and-security-tests.md
- docs/ai/history/0105-complete-baseline-cloud-logging-correlation-fields.md

## AI-Executed Verification

### Commands

- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest edge_gateway/tests/test_gateway_baseline_integration.py -q -s
- PATH=/Applications/Docker.app/Contents/Resources/bin:$PATH UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run pytest
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ruff check .
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run ai-history check
- UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python scripts/refresh_graphify.py
- git diff --check

### Results

- Focused integration: 9 passed in 6.67 seconds. Full suite: 1208 passed in 71.76 seconds, including Docker build/run tests; one existing Starlette/httpx deprecation warning. Ruff, history validation, whitespace checks, and graph refresh passed. Healthy sample: 104 requests, 100 accepted, 4 rejected, 100 persisted, 0 retries; accepted Gateway mean 2.212 ms, Cloud delivery mean 1.905 ms, body 201-203 bytes. Failure sample: 1 failed request, 3 Cloud attempts, 2 retries, 0 persisted rows.

## AI Notes

Read course PDFs, AI policy/workflow, applicable frozen contracts and baseline roadmap; queried committed graph. Continued on feat/gateway-response-mapping. Required develop synchronization created merge fc87e2e; only generated graph conflicts were resolved using the refresh command. Incoming Cloud readiness/logging changes required updating prior test expectations; initial integration check exposed these stale assertions. Incoming histories had duplicate IDs; preserved all human review text and verified only headings/self-paths changed during renumbering. M2-18 code and documentation remain uncommitted. No production runtime, protocol, dependency, or ownership changes. Samples use sequential loopback HTTP and temporary SQLite, not deployment performance. Compose has no services; Docker tests ran through the full suite. Used a writable uv cache and approved local socket/Docker access. Human review and final verification remain pending.

---

# Human Review — Round 1

## Problems Found

No problems found during final implementation review.

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
