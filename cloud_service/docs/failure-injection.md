# Cloud failure injection (M4-41–M4-51)

Cloud supports controlled local failure scenarios through `FAILURE_MODE`,
`FAILURE_RATE`, `FAILURE_SEED`, and `FAILURE_DELAY_SECONDS`. Defaults are
`none`, `0.0`, empty seed, and two seconds. A configured delay is limited to
30 seconds. The seeded generator is used only to decide test faults; it is
never used for keys, shared secrets, session keys, or AEAD nonces.

| Mode | Injection point and public result |
| --- | --- |
| `public_key_unavailable` | Public-key endpoint returns `503 SERVICE_UNAVAILABLE`. |
| `mlkem_decapsulation_failure` | A valid session request fails before decapsulation; no session is created and `503` is returned. This is an explicit wrapper/application test fault, not a claim about every altered valid-length ML-KEM ciphertext. |
| `session_not_found` | The current session is removed, then lookup returns `409 SESSION_INVALID`. |
| `session_expired` | Ownership has succeeded; the session is removed as expired and returns `409 SESSION_EXPIRED`. |
| `decryption_failure` | After session validation, secure processing returns `400 SECURE_MESSAGE_REJECTED` without parsing or storing plaintext. |
| `storage_failure` | After validation, secure and baseline paths return `503 STORAGE_UNAVAILABLE` without a false `202`. |
| `processing_delay` | Secure and baseline processing await the configured bounded delay. |
| `service_unavailable` | Secure, session-establishment, baseline, or public-key API boundaries return `503`. |
| `drop_response` | The measurement commits, then Cloud returns a retryable non-acceptance `503`. Retrying the same already-built envelope reaches idempotency and returns `202 already_accepted` with the original record ID. |
| `random` | Applies the rate gate once per request, then chooses one applicable injectable mode using the configured seed. |

`drop_response` deliberately models the Cloud-side lost acknowledgement in the
in-process HTTP harness. It does not claim to close a real TCP connection; the
Member 5 network/E2E suite owns that transport-level verification. The tested
retry is an identical envelope: same request ID, session ID, nonce, ciphertext,
and AAD. It is business idempotency, not a cryptographic replay counter/window.

When a non-default mode has a positive rate, Cloud logs the safe warning
`event=failure_injection_enabled`; every selected fault logs
`event=failure_injected` with only its bounded failure type when its actual
processing boundary is reached. Normal mode and a
zero rate do not alter requests. Random selection is made once at the request
boundary and reused by later processing stages, so it cannot select a new fault
at every probe or allow a rate-one request to miss its selected applicable fault.
M4-52 through M4-56 own the broader logging,
secret-leakage, and metrics work and are not implemented here.
