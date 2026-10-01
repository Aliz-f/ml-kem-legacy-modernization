# Gateway crypto human review checklist

Generated Gateway crypto code is untrusted until a human completes this checklist. A passing test suite does not replace this checklist. Record the review through the workflow in [ai-history.md](ai-history.md). Decision records are a later task.

Review every generated security artifact for the items below. The file pointers are the current Gateway locations for those checks.

## ML-KEM correctness

- correct maintained library API
- ML-KEM-768 parameter set
- public/private key roles correct
- shared secret handled internally only
- no handmade lattice/KEM implementation
- no brittle assumption that every modified valid-length ciphertext throws

Look in `edge_gateway/src/edge_gateway/crypto/mlkem.py` and `docs/architecture/ml-kem-library-decision.md`. The Gateway calls `cryptography` `MLKEM768PublicKey`. The public key is 1184 bytes, the ciphertext is 1088 bytes, and the shared secret is 32 bytes. The Gateway encapsulates to a public key. The private key stays on the Cloud. The shared secret is not logged. A valid-length ciphertext change is not required to raise, because ML-KEM can use implicit rejection.

## Public-key trust

- protocol_version / algorithm / key_id validated
- unauthenticated HTTP substitution risk documented
- ML-KEM not misrepresented as Cloud identity authentication

Look in `edge_gateway/docs/transport-trust.md`. The Gateway trusts the public key because it came from the configured Cloud URL. ML-KEM does not authenticate Cloud identity. Protocol version 1 does not add a separate key-confirmation tag.

## KDF correctness

- HKDF-SHA-256
- salt=None
- info exactly:
- "ml-kem-project:v1:gateway-cloud-session"
- output length=32 bytes
- same fixed parameters as Cloud
- no extra transcript fields
- no extra confirmation key
- no ad hoc SHA256(shared_secret)

Look in `edge_gateway/src/edge_gateway/crypto/kdf.py`. `salt=None` is the `cryptography` HKDF call, which is RFC 5869 HashLen zero bytes. The info string and the 32-byte length are fixed. Cloud must use that same call. Do not add transcript fields or a confirmation key.

## Session correctness

- TTL enforced
- session reuse
- gateway/session ownership
- 409 SESSION_INVALID handling
- 409 SESSION_EXPIRED handling
- maximum one re-establishment per send

Look in `edge_gateway/src/edge_gateway/crypto/session.py` and `edge_gateway/src/edge_gateway/crypto/secure_transport.py`. `SESSION_TTL_SECONDS` must be 300. One handshake is reused until expiry. A 409 `SESSION_INVALID` or `SESSION_EXPIRED` invalidates the session, establishes one replacement, rebuilds the envelope for the same request ID, and retries that logical request once. A second 409 is not recovered.

## AEAD correctness

- AES-256-GCM
- 32-byte key
- 12-byte nonce
- cryptographically secure nonce generation
- AAD contains exactly:
- protocol_version
- gateway_id
- session_id
- request_id
- canonical AAD encoding matches Cloud
- authentication failure stops processing

Look in `edge_gateway/src/edge_gateway/crypto/symmetric.py` and `edge_gateway/src/edge_gateway/crypto/aad.py`. The key is 32 bytes. `generate_nonce()` uses `secrets.token_bytes` for 12 bytes. The AAD object is exactly those four fields, encoded as UTF-8 JSON with sorted keys and compact separators. An authentication failure raises and stops processing.

## Retry correctness

- transport retry bounded
- ordinary ambiguous retry reuses the same already-built SecureEnvelope
- same request_id / nonce / ciphertext / AAD for ordinary retransmission
- session recovery is separate from ordinary retry
- new-session recovery rebuilds encryption only because the session changed
- business idempotency handles already-stored measurement

Look in `edge_gateway/src/edge_gateway/crypto/secure_transport.py`. `CLOUD_MAX_RETRIES` bounds ordinary transport retries. Timeout, connection failure, and HTTP 500, 502, 503, or 504 resend the envelope already built. Session recovery is only the 409 path, and it rebuilds encryption because the session key changed. An already-stored measurement is business idempotency on `(device_id, sequence_number)`.

## Replay limitation

- no message counter in protocol v1
- no dedicated cryptographic anti-replay counter/window
- limitation is documented as technical debt
- do not claim replay protection that is not implemented

Protocol version 1 has no message counter and no dedicated cryptographic anti-replay counter or window. That limitation is documented as technical debt. Business idempotency is not cryptographic replay protection. See `docs/testing/FAILURE_TEST_MATRIX.md`.

## Fail-closed correctness

- PQC_FAILURE_POLICY=fail_closed only
- no runtime plaintext fallback
- no baseline endpoint call after crypto/session failure

Look in `edge_gateway/src/edge_gateway/config.py` and `edge_gateway/src/edge_gateway/dispatch.py`. The only allowed policy is `fail_closed`. A secure failure is logged, counted, and returned. It does not send the measurement to the baseline endpoint.

## Operational behavior

- timeouts
- logging safe
- metrics safe
- readiness does not require an active session
- shutdown clears session references

Look in `edge_gateway/src/edge_gateway/app.py`, `edge_gateway/src/edge_gateway/crypto/security_log.py`, and `edge_gateway/docs/secure-shutdown.md`. `CLOUD_TIMEOUT_SECONDS` bounds the Cloud call. Logs and metrics must not contain private keys, shared secrets, or session keys. `/ready` does not require an active session. Shutdown closes the HTTP client and then clears the in-memory session. Python does not guarantee secure memory zeroization.

## Architecture

- crypto isolated
- no crypto code in Legacy route handler
- CanonicalMeasurement not modified
- request_id remains separate request/transport context
- no direct Legacy coupling

Crypto stays in `edge_gateway.crypto`. The Legacy `POST /api/v1/measurements` handler parses and validates the Legacy JSON and does not encapsulate or encrypt. `CanonicalMeasurement` keeps the normalized measurement fields. `request_id` stays request and transport context. The Legacy Device does not learn ML-KEM, the session, the nonce, or AES-GCM.
