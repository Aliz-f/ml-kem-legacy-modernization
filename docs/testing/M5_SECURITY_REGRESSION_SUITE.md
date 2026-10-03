# M5-74 through M5-76 security-regression evidence

This coordination index maps the frozen M5-74 security suite and the M5-75
and M5-76 fail-closed checks to current automated tests. It adds no protocol
behavior or security mechanism. The repository-quality workflow runs
`uv run pytest` on every push and pull request, so every test named below is
in CI; its dedicated Gateway crypto stage also reruns the primary tamper and
secure Gateway-to-Cloud tests.

## M5-74 security regression suite

| Required regression | Automated evidence |
|---|---|
| Tampered AEAD ciphertext | `tests/integration/test_secure_message_tamper.py::test_tampered_field_is_rejected_and_stores_nothing` and `tests/integration/test_gateway_cloud_secure.py::test_tampered_secure_message_is_rejected` reject it without storage. |
| Tampered AAD: `protocol_version`, `gateway_id`, `session_id`, and `request_id` | `tests/integration/test_secure_message_tamper.py` exercises each field; `cloud_service/tests/test_cloud_aead.py::test_each_modified_aad_field_fails_authentication` confirms the four-field AAD binding. |
| Wrong session, expired session, and unknown session | `tests/integration/test_gateway_cloud_secure.py::test_wrong_session_is_rejected_without_storage`, `::test_expired_session_returns_409_and_recovers_once`, and `::test_invalid_session_returns_409_and_recovers_once`. |
| Malformed ML-KEM session input where detectable | `tests/integration/test_gateway_cloud_secure.py::test_malformed_mlkem_ciphertext_is_rejected`. |
| Simulated ML-KEM decapsulation/application failure | `tests/integration/test_gateway_cloud_secure.py::test_simulated_decapsulation_failure_leaves_no_session`. |
| ML-KEM implicit-rejection caveat | `tests/integration/test_gateway_cloud_secure.py::test_valid_length_mlkem_mutation_is_not_required_to_raise` does not require an exception for a valid-length mutation. |
| No secret logging | `edge_gateway/tests/test_secure_transport.py::test_keys_and_plaintext_are_not_logged`, `cloud_service/tests/test_cloud_session_api.py::test_synthetic_secret_markers_never_appear_in_cloud_logs`, and `edge_gateway/tests/test_static_checks.py::test_source_logs_do_not_receive_secret_material`. |
| No plaintext on the secure endpoint | `cloud_service/tests/test_cloud_secure.py::test_plaintext_never_falls_back` rejects plaintext and prevents session lookup and storage. |
| No automatic baseline fallback | `tests/integration/test_gateway_cloud_secure.py::test_secure_failure_does_not_call_baseline` and the M5-75 system test below assert zero baseline calls. |
| Ambiguous-response retry uses the same built envelope | `tests/integration/test_gateway_cloud_secure.py::test_ambiguous_transport_retries_the_same_envelope` compares the two serialized envelopes, including request ID, nonce, ciphertext, and AAD. |
| Retry remains business-idempotent | That same ambiguous-response test asserts one stored row; `docs/testing/M5_FAILURE_AUTOMATION.md` records the corresponding F18 evidence. |
| No dedicated cryptographic anti-replay counter/window | `tests/integration/test_secure_message_tamper.py` documents the protocol-v1 boundary, and `docs/testing/FAILURE_TEST_MATRIX.md` distinguishes business idempotency from cryptographic replay protection. |

## M5-75 — system-wide fail-closed verification

`tests/integration/test_mlkem_handshake_failure_demo.py::test_handshake_failure_stays_closed_without_a_session`
runs a live Gateway and Cloud in `SECURITY_MODE=mlkem` with the explicit
`PQC_FAILURE_POLICY=fail_closed` setting and deterministic
`mlkem_handshake_failure` injection. It asserts a visible Legacy-facing `503`,
no Gateway session, zero baseline calls, zero Cloud rows, and
`gateway_pqc_fallback_total 0`.

This is a fail-closed failure result, not a successful measurement delivery.

## M5-76 — no runtime plaintext fallback

The same live system test proves that the injected handshake failure makes
zero calls to `POST /api/v1/baseline/measurements`; no plaintext measurement
is sent to the Cloud. `tests/integration/test_mode_evaluation.py::test_injected_crypto_failure_does_not_call_baseline`
independently checks both handshake and ciphertext injection paths with zero
baseline calls and zero fallback metric.

`edge_gateway/tests/test_gateway_config.py::test_load_config_rejects_invalid_values`
rejects `PQC_FAILURE_POLICY=fallback` during configuration validation. Baseline
transport remains an explicit `SECURITY_MODE=classical` operator choice, never
a runtime recovery action in `SECURITY_MODE=mlkem`.

## Scope boundary

ML-KEM can use implicit rejection: a modified correctly sized encapsulation
ciphertext can yield different keying material rather than an explicit
decapsulation error. The suite therefore checks malformed input and a
simulated operational decapsulation failure, but does not assert that every
valid-length bit flip raises.
