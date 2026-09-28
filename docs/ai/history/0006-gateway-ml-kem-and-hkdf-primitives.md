# AI Task 0006 — Gateway ML-KEM and HKDF primitives

**Status:** Complete

**Created:** 2026-09-24T11:04:08+03:00

**Updated:** 2026-09-24T11:19:50+03:00

**Agent:** Grok Build

---

# Task

Start Member 3 at the current primitive phase: record the ML-KEM-768 library decision, add it to edge_gateway with uv, and implement the Gateway encapsulate wrapper plus the frozen HKDF-SHA-256 session-key wrapper with tests. Do not implement HTTP clients, sessions, AES-GCM, the Cloud service, or any protocol change.

---

# Prompt

start the member 3 tasks

---

# AI Implementation — Initial

## LLM Output

Started Member 3 primitives on the Gateway. Selected pyca/cryptography >= 48 (locked 50.0.1) for ML-KEM-768 and HKDF-SHA-256. Added it to edge_gateway with uv, and installed that workspace member in the root dev group so uv sync --frozen and pytest can import it. Implemented encapsulate() and derive_session_key() behind edge_gateway.crypto. Tests cover a key round trip, rejected keys, the frozen HKDF info string, and that key material is not logged. No HTTP client, session manager, AES-GCM, or Cloud service.

## Files Created

- docs/ai/history/0006-gateway-ml-kem-and-hkdf-primitives.md
- docs/architecture/ml-kem-library-decision.md
- edge_gateway/src/edge_gateway/crypto/
- edge_gateway/tests/test_kdf.py
- edge_gateway/tests/test_mlkem.py

## Files Modified

- docs/ai/.state.json
- edge_gateway/pyproject.toml
- pyproject.toml
- uv.lock

## Files Deleted

- None

## AI-Executed Verification

### Commands

- uv sync --frozen
- uv run pytest
- uv run ruff check .
- uv run ai-history check

### Results

- Installed cryptography 50.0.1 and edge-gateway 0.1.0. Frozen sync succeeded.
- 16 passed in 0.16s
- All checks passed!
- AI history validation passed.

## AI Notes

Library round trip was executed locally. A 1184-byte all-zero public key is accepted by cryptography; all-0xff is rejected. Tests do not require every valid-length ciphertext bit flip to raise. salt=None uses cryptography HKDF, which is RFC 5869 HashLen zero bytes. Member 4 still needs the matching Cloud decapsulation wrapper. Sessions, SecureEnvelope, AES-256-GCM, and the public-key HTTP client are not in this task.

---

# Human Review — Round 1

## Problems Found

Reviewed and it seemed correct.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- No additional AI checks recorded.

## Human-Confirmed Verification

I accept the final implementation

---

# Final Outcome

**Status:** Complete
