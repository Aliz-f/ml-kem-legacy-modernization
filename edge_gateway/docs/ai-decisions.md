# Gateway crypto AI decisions

This note records accepted, modified, and rejected outcomes for generated Gateway crypto proposals. The proposals below are the decision examples Member 3 keeps for the course record. Each one names the proposal, the decision, and the reason. The accepted behavior is what the Gateway implements. This note does not change the protocol, and it does not replace the human review of an individual task. The review checklist is [crypto-review-checklist.md](crypto-review-checklist.md).

## Accepted behavior

The Gateway uses the maintained `cryptography` library for ML-KEM-768, HKDF-SHA-256, and AES-256-GCM. That library decision is `docs/architecture/ml-kem-library-decision.md`.

HKDF uses `salt=None`, the info string `ml-kem-project:v1:gateway-cloud-session`, and a 32-byte output. AI task 0007 corrected the salt documentation and left that call unchanged.

A session is reused until its 300-second TTL expires. An ordinary transport retry resends the SecureEnvelope already built. `PQC_FAILURE_POLICY=fail_closed`, and a crypto failure does not fall back to plaintext or to the baseline endpoint.

## Encrypting sensor JSON directly with ML-KEM

Proposal: AI proposed encrypting sensor JSON directly with ML-KEM.

Decision: Rejected.

Reason: ML-KEM is a KEM for shared-secret establishment, not bulk message encryption.

The Gateway encapsulates with ML-KEM-768 in `edge_gateway/src/edge_gateway/crypto/mlkem.py` and encrypts the measurement with AES-256-GCM in `edge_gateway/src/edge_gateway/crypto/symmetric.py`.

## SHA-256 of the shared secret

Proposal: AI proposed SHA-256(shared_secret) as session-key derivation.

Decision: Rejected/Modified.

Reason: use the frozen HKDF-SHA-256 contract.

The derivation is `edge_gateway/src/edge_gateway/crypto/kdf.py`. It does not use an ad hoc SHA-256 of the shared secret.

## HKDF info bound to identities

Proposal: AI proposed HKDF with gateway_id/Cloud identity/key_id.

Decision: Rejected/Modified.

Reason: protocol v1 deliberately uses the simpler fixed info string: "ml-kem-project:v1:gateway-cloud-session".

The info string has no gateway ID, Cloud identity, or key ID. Both sides use that same fixed value.

## Separate key confirmation

Proposal: AI proposed a separate key-confirmation key and session response.

Decision: Rejected.

Reason: protocol v1 does not include a key-confirmation exchange.

`edge_gateway/docs/transport-trust.md` records that protocol version 1 adds no separate key-confirmation tag. A confirmation tag would also not remove unauthenticated public-key substitution.

## Message counter and replay window

Proposal: AI proposed adding message counter and a replay window.

Decision: Rejected for protocol v1.

Reason: dedicated cryptographic anti-replay remains documented technical debt.

The SecureEnvelope has no `message_counter`. Business idempotency on `(device_id, sequence_number)` is not cryptographic replay protection. See `docs/testing/FAILURE_TEST_MATRIX.md`.

## Logging the shared secret

Proposal: AI proposed logging shared_secret.hex() for debugging.

Decision: Rejected.

Reason: secret leakage.

Private keys, ML-KEM shared secrets, and session keys are not logged or written into history. Tests compare those values with a boolean so the assertion output does not print them.

## Plaintext fallback

Proposal: AI proposed automatic plaintext fallback after ML-KEM failure.

Decision: Rejected.

Reason: silent downgrade violates our fail-closed migration design.

`edge_gateway/src/edge_gateway/dispatch.py` logs and counts a secure failure, then returns it. It does not send that measurement to the baseline endpoint.

## Handshake on every measurement

Proposal: AI proposed creating a new ML-KEM handshake for every measurement.

Decision: Modified.

Reason: reuse bounded sessions to reduce overhead.

`edge_gateway/src/edge_gateway/crypto/session.py` reuses the in-memory session until `SESSION_TTL_SECONDS` (300) expires. A new handshake replaces an expired or invalidated session.

## Fresh nonce after an ambiguous timeout

Proposal: AI proposed re-encrypting the same request with a fresh nonce after an ambiguous HTTP timeout.

Decision: Rejected/Modified.

Reason: ordinary protocol-v1 transport retry retransmits the same already-built SecureEnvelope. Re-encryption happens only after a new session is established.

`edge_gateway/src/edge_gateway/crypto/secure_transport.py` resends the same request ID, nonce, ciphertext, and AAD on an ordinary retry. A 409 `SESSION_INVALID` or `SESSION_EXPIRED` is the separate recovery path: one new session, one rebuilt envelope, and the same logical request ID.
