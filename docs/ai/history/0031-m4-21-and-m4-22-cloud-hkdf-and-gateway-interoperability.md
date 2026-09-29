# AI Task 0031 — M4-21 and M4-22 Cloud HKDF and Gateway interoperability

**Status:** Complete

**Created:** 2026-09-29T21:00:10+03:00

**Updated:** 2026-09-29T21:08:08+03:00

**Agent:** Codex

---

# Task

Implement the frozen Cloud HKDF-SHA-256 wrapper and tests proving actual Gateway/Cloud ML-KEM secrets derive identical session keys. Cloud-local changes and required AI history only; no M4-23.

---

# Prompt

Complete M4-21 and M4-22 as one AI-history task.

Ask before changing edge_gateway or shared/project-wide files.

Stop for human review. Do not start M4-23.

---

# AI Implementation — Initial

## LLM Output

Implemented M4-21 Cloud HKDF-SHA-256 wrapper using the existing cryptography dependency with salt=None, exact frozen info bytes and one 32-byte output. Added M4-22 real Gateway encapsulation/Cloud decapsulation interoperability followed by independent Gateway/Cloud KDF calls. Tests verify matching secrets and keys without printing material, exact library parameters, deterministic derivation, invalid input/output rejection and sanitized vendor failures. Added Cloud-local documentation.

## Files Created

- cloud_service/src/cloud_service/crypto/kdf.py
- cloud_service/tests/test_cloud_kdf.py
- cloud_service/docs/kdf.md
- docs/ai/history/0031-m4-21-and-m4-22-cloud-hkdf-and-gateway-interoperability.md

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv run ruff check .
- uv run pytest
- uv run ai-history check
- git diff --check

### Results

- All checks passed.
- 380 passed, 1 existing Starlette TestClient deprecation warning in 15.94 seconds; includes 14 new Cloud KDF tests.
- Validation passed.
- Passed.

## AI Notes

No Gateway source, shared manifests, lockfile or dependencies changed. Uses Member 3 existing wrappers in Cloud-local tests only. This is primitive interoperability, not HTTP sessions or secure E2E. M4-23 and later work not started. M4-17 container verification remains explicitly deferred to M4-81/M4-83. No secret material recorded. Stop for actual human review.

---

# Human Review — Round 1

## Problems Found

No blocking problems identified.

The Cloud HKDF wrapper matches the frozen protocol contract, and the interoperability test verifies matching Gateway/Cloud shared secrets and derived session keys without exposing secret material.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I inspected the final M4-21/M4-22 work and accept it.

---

# Final Outcome

**Status:** Complete
