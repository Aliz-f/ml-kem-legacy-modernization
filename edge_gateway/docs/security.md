# Gateway security documentation

Member 3 maintains the Gateway security record here. The canonical security sections are already in these files:

- `docs/architecture/02 - Edge Gateway.md`
- `docs/architecture/04 - Shared Cross-Component Protocol Specification.md`
- `docs/architecture/ml-kem-library-decision.md`

`docs/architecture/edge-gateway.md`, `docs/architecture/protocol-specification.md`, and `docs/architecture/security-design.md` are not separate specifications. A second copy would drift from the frozen design. This note points at the canonical sections and states the facts a reviewer has to keep. It does not change the protocol.

## ML-KEM library decision

The selected library is `cryptography` from `pyca/cryptography`, version 48 or newer. The decision record is `docs/architecture/ml-kem-library-decision.md`. Gateway code calls it through `edge_gateway.crypto`. This repository does not implement ML-KEM, HKDF, or AES-GCM.

## ML-KEM-768 parameter set

The parameter set is ML-KEM-768. The public key is 1184 bytes, the ciphertext is 1088 bytes, and the shared secret is 32 bytes. The Gateway encapsulates to a Cloud public key. The private key stays on the Cloud. Edge Gateway design section 16 states the public-key response and the encapsulation step.

## ML-KEM implicit-rejection caveat

A modified valid-length ML-KEM ciphertext is not required to raise. ML-KEM can use implicit rejection and return different pseudorandom keying material. Edge Gateway design section 64 and the shared protocol specification both record that caveat.

## Public-key response

The Cloud public-key response contains exactly:

- protocol_version
- algorithm
- key_id
- public_key

`protocol_version` is `"1"`, `algorithm` is `ML-KEM-768`, `key_id` is non-empty, and `public_key` is Base64URL. Edge Gateway design section 16 lists those fields.

## Public-key trust limitation

ML-KEM does not authenticate Cloud identity. The Gateway trusts the public key because it came from the configured Cloud URL. The course test environment, including Docker, may use HTTP. TLS, mTLS, PKI, pinning, and signed key distribution stay outside this implementation. Edge Gateway design section 24 and `edge_gateway/docs/transport-trust.md` record that limit.

## HKDF-SHA-256

Session-key derivation is HKDF-SHA-256 with:

- salt=None
- info="ml-kem-project:v1:gateway-cloud-session"
- a 32-byte session key

`salt=None` is the `cryptography` call, which follows RFC 5869 with a HashLen string of zero bytes. The info string has no gateway ID, Cloud identity, or key ID. Gateway and Cloud use that same call. The shared protocol specification and Edge Gateway design section 15 state the parameters.

## Session lifecycle

The Gateway holds at most one in-memory session. It reuses that session until expiry, then establishes a replacement. `SESSION_TTL_SECONDS` is 300. Edge Gateway design sections 17, 18, and 19 describe the session model, states, and lifetime.

## 409 session recovery

`409 SESSION_INVALID` and `409 SESSION_EXPIRED` are not ordinary transport retries. The Gateway invalidates the local session, establishes one new ML-KEM session, rebuilds the envelope under the new session key, keeps the same logical request ID, and retries that request once. A second 409 is not recovered. Edge Gateway design section 39 states this recovery.

## AES-256-GCM

Measurements are encrypted with AES-256-GCM under the 32-byte session key. Each new logical message uses a 12-byte nonce from `secrets.token_bytes`. Edge Gateway design section 22 states the nonce rule.

## AAD fields

The AAD object contains exactly:

- protocol_version
- gateway_id
- session_id
- request_id

Canonical AAD serialization is UTF-8 JSON with sorted keys and compact separators. Gateway and Cloud must produce the same bytes. Edge Gateway design section 21 states that encoding.

## SecureEnvelope format

A SecureEnvelope contains exactly `protocol_version`, `gateway_id`, `session_id`, `request_id`, `nonce`, and `ciphertext`. The nonce and ciphertext use Base64URL encoding. Edge Gateway design section 20 states the envelope.

## Ordinary ambiguous retry

An ordinary retry after a timeout, a lost response, or another ambiguous transport result resends the same already-built SecureEnvelope:

- same request_id
- same nonce
- same ciphertext
- same AAD

The Gateway does not re-encrypt that request under the same session key. `CLOUD_MAX_RETRIES=2` means one initial attempt plus at most two transport retries. Edge Gateway design section 22 states the same-envelope rule, and section 40 keeps the retry count bounded.

## Session-recovery encryption

Session recovery is separate from that ordinary retry. The replacement session produces a new nonce and a new ciphertext under the new session key. The logical request ID stays the same.

## Business idempotency

Cloud persistence is unique on `(device_id, sequence_number)`. That is business idempotency.

## Replay window

Protocol version 1 has no message counter and no dedicated cryptographic anti-replay counter or window. That limitation is documented as technical debt. Business idempotency is not cryptographic replay protection. Edge Gateway design section 84 states this debt. This note does not add a replay window.

## Fail-closed policy

`PQC_FAILURE_POLICY=fail_closed` is the only runtime policy. There is no runtime plaintext fallback. A cryptographic or session failure does not send the measurement to the baseline endpoint. Edge Gateway design section 27 states that policy.

## Failure injection

`FAILURE_MODE`, `FAILURE_RATE`, and `FAILURE_SEED` can simulate a handshake failure, a corrupted ciphertext, a missing session, or an expired session during tests. Injection mutates a copy or forces a session fault. It does not change the session key, and `FAILURE_MODE=none` leaves the secure path unchanged. Edge Gateway design sections 28 through 36 describe the injection modes.

## Secret handling

Logs, metrics, and AI-history records do not contain an ML-KEM private key, a shared secret, or a session key. Edge Gateway design section 46 lists the values that must not be logged.

## Python memory zeroization

The session key stays in process memory. Replacing or shutting down a session clears that buffer and drops the object. Python does not guarantee cryptographic memory zeroization. Edge Gateway design section 23 and `edge_gateway/docs/session-memory.md` record that limit.
