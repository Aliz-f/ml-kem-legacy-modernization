# Final secure-transport review

This note records Member 3's final review before project freeze. It checks each item of the frozen M3-78 checklist against the current Gateway and Cloud code, tests, documentation, and AI history. It does not change runtime code or the protocol.

Checked on 2026-10-02 on `feat/gateway-final-review`, after merging `origin/develop` at `022e7f9`.

## Checklist

| Item | Result | Evidence |
|---|---|---|
| ML-KEM library choice | Pass | `docs/architecture/ml-kem-library-decision.md` selects `cryptography`. `dependency-review.md` finds it is the only crypto library. |
| ML-KEM-768 wrapper | Pass | `crypto/mlkem.py` calls `MLKEM768PublicKey.encapsulate` and checks the 1184-byte key, 1088-byte ciphertext, and 32-byte secret. `test_mlkem.py`. |
| Public-key response | Pass | `crypto/public_key.py` requires `protocol_version` `"1"`, `algorithm` `ML-KEM-768`, a non-empty `key_id`, and a Base64URL `public_key` that the wrapper accepts. `test_public_key.py`. |
| Public-key trust limitation | Pass | `transport-trust.md` and the `public_key.py` docstring state that the key is trusted only because it came from the configured Cloud URL. |
| HKDF-SHA-256 | Pass | `crypto/kdf.py` uses `salt=None`, `info=b"ml-kem-project:v1:gateway-cloud-session"`, and length 32. Cloud `crypto/kdf.py` uses the same call. `test_kdf.py`, `test_cloud_kdf.py`. |
| Session manager | Pass | `crypto/session.py` holds at most one session and establishes it under one `asyncio.Lock`. `test_concurrent_callers_share_one_handshake`. |
| Session reuse | Pass | `get_or_establish` returns the active session. `test_send_posts_one_envelope_and_reuses_the_session`, `test_handshake_counter_shows_reuse_then_expiry`. |
| Session expiry | Pass | `_usable_session` clears a session at `expires_at` and a new handshake follows. `test_expired_session_is_replaced`, `test_local_session_expiry_reestablishes_before_the_next_send`. |
| 409 `SESSION_INVALID` recovery | Pass | `_raise_http` maps it to one recovery. `test_session_conflict_rebuilds_once_with_the_same_request_id`, `test_invalid_session_returns_409_and_recovers_once`. |
| 409 `SESSION_EXPIRED` recovery | Pass | Same path. `test_expired_session_returns_409_and_recovers_once`. |
| One-recovery-attempt bound | Pass | `send` calls `_recover` once. A 409 inside `_recover` raises `SecureTransportError`. `test_a_second_session_conflict_is_not_recovered_again`, `test_a_second_session_rejection_is_not_recovered`. |
| AES-256-GCM | Pass | `crypto/symmetric.py` uses `AESGCM` with a 32-byte key. Cloud decrypts with the same library. `test_symmetric.py`, `test_cloud_aead.py`. |
| 12-byte nonce handling | Pass | `generate_nonce` returns `secrets.token_bytes(12)`. `build_secure_envelope` makes one new nonce per call. Both sides reject any other length. |
| Canonical AAD | Pass | `crypto/aad.py` encodes exactly `protocol_version`, `gateway_id`, `session_id`, and `request_id` with sorted keys and compact separators. Cloud `crypto/aad.py` matches. `test_aad.py`. |
| SecureEnvelope | Pass | `crypto/envelope.py` has exactly six fields, including `request_id`, `nonce`, and `ciphertext`, and no `message_counter`. Cloud rejects an envelope with a seventh field. `test_secure_envelope.py`, `test_cloud_envelope.py`. |
| Ambiguous ordinary transport retry | Pass | `_deliver` serializes the envelope once and resends the same bytes, so `request_id`, nonce, ciphertext, and AAD stay the same. `test_transport_retry_resends_the_same_envelope`, `test_lost_response_retries_the_same_envelope`, `test_ambiguous_transport_retries_the_same_envelope`. |
| Session recovery | Pass | `_recover` invalidates the session, establishes a new one, and calls `_seal` again under the new key with the same `request_id`. The tests check a new `session_id`, a new nonce, and the same `request_id`. |
| Replay limitation | Pass | No counter or replay window exists. `technical-debt.md` records it as debt. Cloud storage is `UNIQUE(device_id, sequence_number)`, and a repeated measurement returns `already_accepted`. |
| Secure Cloud transport | Pass | `secure_transport.py` posts only to `POST /api/v1/secure/measurements` and rejects redirects. `app.py` composes it when `SECURITY_MODE=mlkem`. |
| Fail closed | Pass | `CloudDispatch` accepts only `PQC_FAILURE_POLICY=fail_closed`. A `SecureTransportError` is counted, logged as `pqc_fail_closed`, and raised. |
| No runtime plaintext fallback | Pass | The secure failure path in `dispatch.py` never calls the baseline transport. `test_secure_transport_has_no_baseline_fallback`. The fallback metric stays 0. |
| Failure injection | Pass | `crypto/failure.py` covers `mlkem_handshake_failure`, `corrupt_ciphertext`, `session_missing`, and `session_expired`. `test_crypto_failures.py`, `corrupt-ciphertext.md`, `mlkem-handshake-failure.md`. |
| Logging | Pass | `security_log.py` writes fixed event names and IDs only. `test_security_logging.py` and `test_static_checks.py` check that no secret reaches a log call. |
| Metrics | Pass | `crypto/metrics.py` exports handshake, reuse, re-establishment, failure, and fallback counters with bounded labels. `pqc-observability.md`. |
| Tests | Pass | On this branch: 564 Gateway tests passed. The 59 secure integration tests passed, and 2 Docker image tests were skipped because Docker is not installed. |
| Docs | Pass | `security.md`, `threat-model.md`, `technical-debt.md`, `transport-trust.md`, `session-memory.md`, `secure-shutdown.md`, and the four review notes. |
| AI history | Pass | Every Member 3 task has a completed history file. `uv run ai-history check` passes. |

## Observations

These are not checklist failures. They are recorded for the team before freeze.

- `SessionManager.invalidate()` drops whatever session is current, not only the session the Cloud rejected. If two requests get a 409 for the same old session, the second invalidation can discard the replacement that the first request just established. Each request still recovers once with its own `request_id`. The cost is an extra handshake. No test covers concurrent recovery.
- The single post after session recovery goes through `_post`, not `_deliver`, so a timeout on that post is not retried. The request fails closed. This keeps the one-recovery-attempt bound.
- The Docker image tests (`test_clean_container_crypto.py` and `test_gateway_crypto_image.py`) have not run on this machine. CI or a machine with Docker must run them before freeze.
- `GET /ready` on the Gateway is still the Member 2 placeholder and always returns unavailable.
- The M3-76 follow-ups remain open: moving the lock to `cryptography` 50.0.2, and the Graphify refresh script choosing an LLM labeling backend when a `claude` CLI is on `PATH`.

## Review result

Every item of the M3-78 checklist passes on the current branch. The secure path uses ML-KEM-768, HKDF-SHA-256, and AES-256-GCM through one maintained library and matches the frozen protocol. It fails closed with no plaintext fallback. The open items above are recorded and do not change the protocol.
