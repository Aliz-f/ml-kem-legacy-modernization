# AI Task 0014 — M4-02 Cloud application skeleton

**Status:** Complete

**Created:** 2026-09-28T23:10:38+03:00

**Updated:** 2026-09-28T23:20:52+03:00

**Agent:** Codex

---

# Task

Implement the next Member 4 PR 1 task, M4-02: runnable Cloud application skeleton with validated configuration, logging, lifecycle, safe liveness/readiness and Cloud-local tests/documentation. M4-00 and M4-01 complete. Defer storage, measurement endpoints, crypto, sessions and metrics to their designated tasks. Shared changes limited to required history and separately approved dependency lock updates.

---

# Prompt

Complete the next required Member 4 task for PR 1.

Do not modify shared/project-wide files other than required AI-history files without my approval.

---

# AI Implementation — Initial

## LLM Output

Implemented M4-02 Cloud application skeleton: FastAPI app factory, validated configuration, lifecycle logging and running state, Uvicorn CLI/module entry point, graceful lifespan cleanup, liveness endpoint, and honest unavailable readiness until storage exists. Modernized Mode fails startup rather than downgrading; future measurement/query/crypto/metrics endpoints remain unregistered. Added 14 application tests and Cloud-local usage documentation. Added Cloud runtime FastAPI/Uvicorn dependencies and optional HTTPX test extra; updated only the approved shared lockfile and required AI history.

## Files Created

- cloud_service/src/cloud_service/app.py
- cloud_service/tests/test_cloud_app.py
- cloud_service/docs/application.md
- docs/ai/history/0012-m4-02-cloud-application-skeleton.md

## Files Modified

- cloud_service/pyproject.toml
- uv.lock
- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv lock; uv sync --frozen --all-packages --all-extras
- uv run ruff check . (UV_NO_SYNC=1 after frozen all-package sync)
- uv run pytest (UV_NO_SYNC=1, PYTHONUTF8=1, PYTHONIOENCODING=utf-8)
- Live localhost HTTP smoke using Uvicorn.Server, an ephemeral loopback socket, urllib requests and server.should_exit
- git diff --check; git diff --stat; lockfile package-version comparison against HEAD

### Results

- Passed: 30 packages resolved, Cloud installed with runtime and optional test dependencies. No pre-existing package versions changed.
- Passed: all checks passed.
- Passed: 101 tests, including 14 new application tests. One upstream Starlette warning: HTTPX TestClient support is deprecated in favor of httpx2.
- Passed: health 200 with expected JSON, readiness 503 SERVICE_UNAVAILABLE, server thread exited and lifespan running state cleared.
- No whitespace errors; existing dependency versions unchanged; shared changes confined to approved uv.lock and required AI history.

## AI Notes

M4-00 and M4-01 prerequisites complete. Relevant architecture/workflow and accepted boundary review were inspected; course PDFs were read earlier in the same task sequence. M4-02 describes eventual endpoints; storage, canonical validation, baseline acceptance, crypto, sessions and metrics remain later tasks. Readiness cannot succeed before storage exists, and no measurement route returns false acceptance. FastAPI lifespan documentation was consulted at https://fastapi.tiangolo.com/advanced/events/. No Docker/E2E persistence claims or production signal tests were made; actual graceful server shutdown and lifespan cleanup were checked. On Windows tests use UTF-8 mode. Runtime dependencies are Cloud-local; full tests select all workspace packages/extras, leaving the root manifest unchanged. Previous untracked M4-00/M4-01 artifacts were preserved. Task ID was locally unused after origin fetch; no external reservation or teammate communication occurred. Dependency approval supplied by user: Yes, you may update the shared uv.lock only as required for the M4-02 Cloud dependencies. Do not modify any other shared/project-wide files without my approval. Work paused before dependency updates until this approval arrived; no new task was started on resumption. Only required AI history and the explicitly approved lockfile were changed outside Cloud. Human review and final verification remain pending.

---

# Human Review — Round 1

## Problems Found

No problems identified in the M4-02 implementation.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final M4-02 work and accept it.

---

# Final Outcome

**Status:** Complete
