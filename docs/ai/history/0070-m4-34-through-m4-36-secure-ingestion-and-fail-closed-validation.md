# AI Task 0070 — M4-34 through M4-36 secure ingestion and fail-closed validation

**Status:** Complete

**Created:** 2026-09-30T17:57:36+03:00

**Updated:** 2026-09-30T22:37:58+03:00

**Agent:** Codex

---

# Task

Implement strict 64 KiB envelope validation and authenticated secure ingestion with existing sessions/AAD/AEAD/canonical validation/idempotent storage. Preserve lookup ownership expiry ordering and no plaintext fallback. Cloud-only implementation plus required history and explicitly approved two generated Graphify artifacts. No M4-37 task.

---

# Prompt

Complete M4-34 through M4-36 as one AI-history task.

Follow AGENTS.md and the authoritative frozen protocol.
Implement strict envelope validation, secure measurement ingestion, and fail-closed behavior without plaintext fallback.
Preserve session lookup → ownership → expiry ordering.

Ask before changing Gateway or shared project files.
You may refresh only the two standard generated Graphify artifacts.
Stop if unexpected files change.

Run all required checks.
Stop for human review. Do not start M4-37.

---

# AI Implementation — Initial

## LLM Output

Completed M4-34 through M4-36: strict UTF-8/JSON six-field envelope validation, canonical Base64URL decoding and nonce checks, frozen 64 KiB body limit including streaming enforcement; secure HTTP ingestion using lookup then ownership then expiry, existing AAD/AES-GCM wrappers, strict authenticated plaintext/canonical/Gateway validation and idempotent SQLite persistence. Both mode guards remain fail-closed without plaintext fallback. Added Cloud-local integration/negative tests and updated documentation and obsolete route assertions. Resumed task 0063 without duplication and preserved prior work.

## Files Created

- cloud_service/src/cloud_service/crypto/envelope_validation.py
- cloud_service/src/cloud_service/gateway/secure.py
- cloud_service/tests/test_cloud_secure.py
- cloud_service/docs/secure-ingestion.md
- docs/ai/history/0063-m4-34-through-m4-36-secure-ingestion-and-fail-closed-validation.md

## Files Modified

- cloud_service/src/cloud_service/app.py
- cloud_service/tests/test_cloud_app.py
- cloud_service/tests/test_cloud_baseline.py
- cloud_service/tests/test_cloud_public_key.py
- cloud_service/docs/application.md
- cloud_service/docs/envelope.md
- cloud_service/docs/sessions.md
- docs/ai/.state.json
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run pytest cloud_service/tests/test_cloud_secure.py cloud_service/tests/test_cloud_app.py cloud_service/tests/test_cloud_public_key.py -q
- uv run python scripts/refresh_graphify.py
- uv run ruff check .
- uv run pytest
- uv run ai-history check
- git diff --check

### Results

- Initial focused run: 54 passed with 1 existing Starlette warning; additional streaming/padding cases included in final suite.
- Regenerated after final code/test correction: 116 code files, 1417 nodes, 3466 edges, 74 communities. Snapshot comparison verified only approved standard Graphify artifacts changed; no unexpected changes. Local code-only extraction, no document/LLM extraction.
- All checks passed.
- Final: 746 passed, 1 existing Starlette TestClient deprecation warning in 30.98 seconds. Previous run had 745 passed and one obsolete baseline test expecting 404; corrected to the required classical-mode 503 SERVICE_UNAVAILABLE and reran all checks.
- Validation passed.
- Passed; Git line-ending conversion warnings only.

## AI Notes

User resumed existing task and requested preservation, checks and human-review stop; status was checked first and confirmed 0063 In Progress. No Gateway, dependency, lockfile, shared protocol or unrelated files modified. Graphify limited to the two explicitly approved artifacts. Frozen 202 acknowledgement reuses existing idempotent repository behavior as required by M4-35; no separate M4-37 work started. Tests cover actual Cloud HTTP handshake plus unchanged Gateway envelope builder through SQLite/query, exact size limit and streaming overrun, validation-before-lookup, auth-before-storage, ownership-before-expiry, invalid authenticated plaintext and Gateway mismatch, actual SQLite write failure, safe internal errors and no plaintext fallback. This is Cloud HTTP application integration, not full deployment E2E. Readiness remains placeholder; Docker verification remains deferred under M4-17 to M4-81/M4-83. No runtime failure injection added. No secrets or fabricated human fields recorded. Stop for human review.

---

# Human Review — Round 1

## Problems Found

No blocking problems identified.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final M4-34–M4-36 work and accept it.

---

# Final Outcome

**Status:** Complete
