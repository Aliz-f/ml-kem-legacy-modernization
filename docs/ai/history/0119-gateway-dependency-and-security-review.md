# AI Task 0119 — Gateway dependency and security review

**Status:** Complete

**Created:** 2026-10-02T10:38:59+03:00

**Updated:** 2026-10-02T10:50:53+03:00

**Agent:** Claude Code

---

# Task

Member 3 task M3-76. Review the crypto dependencies for unnecessary packages, unmaintained packages, duplicate crypto libraries, and unsafe low-level usage. Keep one maintained crypto stack. Record the review from the current lock file and source. Do not change the protocol, add or swap crypto libraries, or start M3-77. Branch feat/gateway-dependency-review from feat/gateway-member2-review at ca69ea7; origin/develop is 146064f and is not ahead of the parent.

---

# Prompt

start the next task

---

# AI Implementation — Initial

## LLM Output

Recorded a dependency and security review of uv.lock and the Gateway and Cloud crypto source. cryptography 50.0.1 is the only crypto library, with cffi 2.1.1 and pycparser 3.0 below it. No other crypto package is locked or imported. No runtime package was unnecessary: httpx is test-only and Graphify is dev-only. OSV returned no advisories for the locked runtime and test versions. All library calls go through cryptography.hazmat.primitives. The nonce comes from secrets.token_bytes(12). The random module is used only by failure injectors and the Legacy sensor simulation. Recommended follow-up: a separate dependency task to move the lock to cryptography 50.0.2, which rebuilds wheels with OpenSSL 4.0.3.

## Files Created

- docs/ai/history/0119-gateway-dependency-and-security-review.md
- edge_gateway/docs/dependency-review.md
- edge_gateway/tests/test_dependency_review.py

## Files Modified

- docs/ai/.state.json
- edge_gateway/README.md
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv lock --check
- uv tree --frozen --package edge-gateway; uv tree --frozen --package cloud-service
- OSV querybatch and PyPI JSON for the locked runtime and test packages
- uv run pytest -q edge_gateway/tests/test_dependency_review.py
- uv run ruff check .
- uv run pytest -q --tb=line
- uv run python scripts/refresh_graphify.py (with the claude CLI removed from PATH)
- uv run ai-history check

### Results

- uv lock --check resolved 60 packages with no change.
- OSV returned no advisories for cryptography 50.0.1, cffi 2.1.1, pycparser 3.0, fastapi 0.141.1, starlette 1.7.0, uvicorn 0.54.0, h11 0.16.0, pydantic 2.13.5, pydantic-core 2.46.5, anyio 4.15.1, idna 3.20, click 8.5.0, httpx 0.28.1, httpcore 1.0.9, or certifi 2026.7.22. PyPI shows cryptography 50.0.2 released 2026-09-30.
- Dependency review tests: 3 passed in 0.03s.
- Ruff passed.
- 1197 passed, 2 skipped, 1 warning in 55.78s. The skips are the Docker image runs. The warning is the existing StarletteDeprecationWarning.
- With the claude CLI on PATH, Graphify auto-selected claude-cli community labeling, reported a nonzero token cost, and produced different artifacts on every run, including on the parent commit. With the claude CLI removed from PATH, the unchanged refresh script reproduced the committed parent artifacts byte-for-byte twice, then gave matching artifacts on two runs for this branch: graph.json 664eeb11af3ef12aa73de1fb1ccb89ac8353ac63, GRAPH_REPORT.md 1c3854baf0f1ed264379621b8889e5feca376518, 2170 nodes, 5353 edges, 143 communities, token cost 0.
- AI history validation passed.

## AI Notes

The note is edge_gateway/docs/dependency-review.md. No dependency, lock entry, protocol, or runtime code was changed. M3-77 was not started. Graphify issue: scripts/refresh_graphify.py does not pass a labeling option, so a local refresh where the claude CLI is logged in sends graph node names to an LLM for community names and is not reproducible. This conflicts with the policy that Graphify stays code-only and local. Several such runs happened during this task before the cause was found; their output was discarded. The script was not changed here. A separate shared-tooling task should decide how to disable LLM labeling while keeping the current hub-node names. Running uv run in a git worktree also re-pointed the shared .venv workspace packages; uv sync --frozen restored them. Branch feat/gateway-dependency-review from feat/gateway-member2-review at ca69ea7, no upstream. This work is not committed.

---

# Human Review — Round 1

## Problems Found

None stated. Reviewer response: accepted.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

confirmed

---

# Final Outcome

**Status:** Complete
