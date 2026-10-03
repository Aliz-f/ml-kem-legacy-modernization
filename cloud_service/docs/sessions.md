# Cloud sessions (M4-23–M4-29)

`crypto/session.py` owns process-local sessions and their lifecycle. Each
`SecureSession` has `session_id`, `gateway_id`, `cloud_key_id`, UTC `created_at`
and `expires_at`, a 32-byte mutable key buffer, and a state (`active`, `expired`,
`invalidated`, `closed`, or `failed`). The key is excluded from representation
and comparisons. Only the explicit four-field response is serialized; never
serialize the session object itself. There are no SQLite session records,
counters, replay windows or cryptographic key-confirmation messages.

## Session establishment

In `SECURITY_MODE=mlkem`, `POST /api/v1/crypto/sessions` accepts exactly:

```json
{
  "protocol_version": "1",
  "gateway_id": "gateway-001",
  "key_id": "<current Cloud key ID>",
  "encapsulation_ciphertext": "<Base64URL ML-KEM ciphertext>"
}
```

Validation precedes cryptography: JSON object/field set, version, non-empty
trimmed Gateway identifier, current key ID, strict Base64URL alphabet and
padding, canonical encoding, then 1088-byte decoded length. Padded and unpadded
Base64URL forms are accepted. This endpoint-local decoder is only for the
handshake ciphertext; it does not implement later envelope/AEAD work.

Cloud runs its existing ML-KEM decapsulation and frozen HKDF wrappers in the
thread pool, constructs and publishes an active session, then returns `200`:

```json
{
  "protocol_version": "1",
  "session_id": "sess-<UUID>",
  "status": "established",
  "expires_at": "<UTC timestamp>"
}
```

The response has `Cache-Control: no-store`. Identifiers use fresh UUIDs; repeated
handshakes create independent sessions. There is no handshake deduplication or
silent extension. A collision is rejected without replacing an existing session.
Private keys, shared secrets and session keys never appear in the response or
logs. Gateway identity is the declared identifier under the course trust model;
ownership checking does not constitute independent Gateway authentication.

| Establishment condition | HTTP / code |
| --- | --- |
| Malformed JSON, wrong/missing/extra fields, invalid Gateway ID, unknown key ID, malformed encoding/length | `400 INVALID_SESSION_REQUEST` |
| Unsupported protocol version | `400 UNSUPPORTED_PROTOCOL_VERSION` |
| Classical mode, unavailable service, operational decapsulation/KDF/session-creation failure | `503 SERVICE_UNAVAILABLE` |
| Successful creation | `200`, `status: established` |

Operational failures produce generic messages without vendor diagnostics.
Construction validates and completes before publishing a session. If response
construction fails after publication, the session is removed and its buffer
cleared with state `failed`. No failed establishment leaves a usable session.
A valid-length altered ciphertext may use ML-KEM implicit rejection and still
establish a session with mismatched material; no test or behavior claims that
arbitrary such tampering must fail during setup. Authentication of later secure
messages is outside these tasks.

## Ownership, expiry and cleanup

`SessionManager.get(session_id, gateway_id)` enforces the authoritative Shared
Protocol order: **lookup → ownership → expiry**. This preserves the accepted
M4-00 conflict decision despite expiry-first wording in the component/member
documents. It returns an active session or raises `SessionAccessError`:

| Access condition | HTTP mapping / code |
| --- | --- |
| Unknown or removed session | `409 SESSION_INVALID` |
| Wrong Gateway owner (including an expired session still present) | `400 SECURE_MESSAGE_REJECTED` |
| Correct owner at or after `expires_at` | `409 SESSION_EXPIRED`, remove and clear key |

TTL is fixed at the configured **300 seconds**. Tests inject a UTC clock rather
than changing production TTL. Reads never change creation or expiry timestamps.
Once removed, subsequent access returns `SESSION_INVALID`; no tombstones are
kept. `remove_expired()` performs explicit cleanup and clears each removed key.
There is no background sweeper in this task. A fresh handshake creates a new
session with a new lifetime. Cloud does not implement Gateway retry policy.

An `RLock` serializes manager operations. `invalidate()` removes a session and
clears its buffer; `close()` clears all sessions and prevents new creation.
Cloud initializes the manager only in `mlkem` mode and closes it before keys
and storage on shutdown, including exceptional exits. Startup failure releases
already-created keys/storage. Buffers are overwritten in place, but Python
and cryptographic-library memory zeroization of all copies is not guaranteed.

The app registers the frozen session-error HTTP mapping. Session tests exercise
it with a **test-only probe route**; M4-34–M4-36 now also use it in the production
[secure ingestion route](secure-ingestion.md). `/ready` remains `503` and
plaintext ingestion remains rejected in `mlkem` mode. The original session
task alone did not claim secure ingestion or full readiness.

## Verification scope

Tests cover strict pre-crypto request validation, wire metadata, matching
Gateway/Cloud session keys, no secret-bearing response/log fields, atomic
creation, safe operational failures, invalidation, exact expiry boundaries,
ownership-before-expiry, cleanup, concurrency and normal/exceptional shutdown.
Controlled-time HTTP tests verify the error mapping and a replacement handshake.
A separate loopback Uvicorn test calls the **existing Gateway session manager
and its HTTP clients** unchanged and compares session association, key ID,
expiry and derived key. This verifies a real session handshake, not Legacy or
secure-measurement E2E integration.

```powershell
$env:UV_NO_SYNC='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
uv run pytest cloud_service/tests/test_cloud_sessions.py cloud_service/tests/test_cloud_session_api.py -q
uv run ruff check .
uv run pytest
uv run ai-history check
```

No dependency, Gateway or shared protocol changes were required for this
original session task. At that time M4-30 and later work had not started;
current secure-route and Docker verification is documented in
`final-integration-and-operations.md`.
