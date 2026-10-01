# Gateway threat model

This note is Member 3's Gateway threat model. The Cloud design records the matching Cloud threats in section 102 of `docs/architecture/03 - Cloud Service.md`. This note does not change the protocol, and it does not add a replay window, TLS, or a plaintext downgrade path.

## Tampered ciphertext

Threat: an attacker changes the ciphertext, the nonce, the AAD, or the GCM tag after the Gateway encrypts a measurement.

Mitigation: AES-256-GCM authentication fails, Cloud rejects the envelope, and no measurement row is stored.

Remaining limitation: the Gateway does not repair the ciphertext and does not fall back to the baseline endpoint.

## Wrong or expired session

Threat: an envelope names a session that is missing, owned by another gateway, or past its expiry time.

Mitigation: Cloud checks lookup, ownership, and expiry, and a missing or expired session returns 409 SESSION_INVALID or 409 SESSION_EXPIRED. The Gateway invalidates the local session, establishes one replacement, rebuilds the envelope, and retries the same request ID once.

Remaining limitation: a second 409 is not recovered, and protocol version 1 adds no separate key-confirmation tag.

## Malformed or modified ML-KEM ciphertext

Threat: the encapsulation ciphertext is truncated, badly encoded, or modified before Cloud decapsulation.

Mitigation: a wrong length or a decapsulation exception creates no usable session. Tests can inject a handshake failure without using a failure-seed PRNG for real cryptographic randomness.

Remaining limitation: a valid-length change is not required to raise, because ML-KEM can use implicit rejection and return different keying material. The mismatch shows up when later AES-GCM authentication fails.

## Public-key substitution

Threat: an attacker on the path replaces the Cloud ML-KEM public key before the Gateway encapsulates.

Mitigation: the Gateway accepts the key only from the configured CLOUD_URL and checks protocol_version, algorithm, and key_id. `edge_gateway/docs/transport-trust.md` records the substitution risk.

Remaining limitation: the course test environment may use HTTP, ML-KEM does not authenticate Cloud identity, and TLS, pinning, and PKI are not implemented.

## Secret logging

Threat: a log or metric line contains an ML-KEM private key, a shared secret, or a session key.

Mitigation: `log_security` accepts only named correlation fields and drops bytes and values that are not single tokens. Tests require those secrets to stay out of the log text.

Remaining limitation: a hex encoding of a secret is still a token, so callers must not pass `shared_secret.hex()` or a session key to the logger.

## Replay of an authenticated secure envelope

Threat: an attacker resends a previously accepted authenticated SecureEnvelope.

Mitigation: Cloud business idempotency on `(device_id, sequence_number)` prevents duplicate rows.

Remaining limitation: business idempotency prevents duplicate rows, but protocol v1 has no dedicated cryptographic anti-replay counter/window.

## Downgrade

Threat: a cryptographic or session failure is sent as plaintext to the baseline endpoint.

Mitigation: `PQC_FAILURE_POLICY=fail_closed`. Dispatch counts the failure, logs `pqc_fail_closed`, and does not call the baseline endpoint.

Remaining limitation: `SECURITY_MODE=classical` still sends plaintext when that mode is configured explicitly. That is a separate mode, not an automatic downgrade.

## Cloud unavailability

Threat: Cloud does not answer, or it returns HTTP 500, 502, 503, or 504.

Mitigation: the Gateway resends the same already-built SecureEnvelope for the bounded `CLOUD_MAX_RETRIES` attempts and then fails closed.

Remaining limitation: there is no persistent message buffer, so a restart loses the unsent measurement, and an ordinary retry does not create a new session.

## Session race

Threat: two concurrent measurements could start two handshakes or replace the session while a send is using it.

Mitigation: `SessionManager.get_or_establish` holds one `asyncio.Lock` for the process, so one handshake is established and later sends reuse it.

Remaining limitation: the lock does not coordinate a second Gateway process. This course system runs one Gateway process.
