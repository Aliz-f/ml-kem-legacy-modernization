# M5-98 protocol-regression detection

This Member 5 coordination index identifies the existing tests that must fail
when a frozen cross-component contract changes accidentally. It does not make
the test suite a substitute for the shared protocol specification: an
intentional change must update that specification first, then component
designs, roadmap/member tasks, tests, and implementation.

The repository-quality workflow runs the complete suite on every push and pull
request. Its named `Run protocol contract tests` stage reruns the primary
schema, correlation, public-key, session, envelope, AAD, KDF, and baseline
contract files.

| Frozen contract category | Regression evidence |
|---|---|
| Legacy/Gateway endpoint, JSON fields, status boundary | `edge_gateway/tests/test_gateway_models.py`, `edge_gateway/tests/test_gateway_routes.py`, and `tests/integration/test_legacy_gateway.py` exercise the exact Legacy payload, endpoint, and `400`/`422` behavior. |
| Canonical JSON fields and Cloud storage mapping | `edge_gateway/tests/test_gateway_canonical_model.py`, `cloud_service/tests/test_gateway_cloud_baseline_contract.py`, and `tests/integration/test_gateway_cloud_baseline.py` verify canonical serialization, `X-Request-ID`, and `received_at` mapping. |
| Gateway/Cloud endpoint and protocol version | `cloud_service/tests/test_cloud_public_key.py`, `cloud_service/tests/test_cloud_session_api.py`, and `tests/integration/test_gateway_cloud_secure.py` verify versioned routes and reject unsupported protocol versions. |
| Public-key fields and `key_id` semantics | `edge_gateway/tests/test_public_key.py`, `edge_gateway/tests/test_public_key_client.py`, and `cloud_service/tests/test_cloud_public_key.py` verify the public-key response and restart key rotation. |
| Session request/response fields and errors | `cloud_service/tests/test_cloud_session_api.py` requires the exact session response fields and validates its request; `edge_gateway/tests/test_session.py` and `tests/integration/test_gateway_cloud_secure.py` cover `409 SESSION_INVALID` and `409 SESSION_EXPIRED`. |
| ML-KEM suite and HKDF salt/info/length | `edge_gateway/tests/test_mlkem.py`, `edge_gateway/tests/test_kdf.py`, and `cloud_service/tests/test_cloud_kdf.py` verify ML-KEM interoperation and the fixed 32-byte HKDF contract. |
| AES-GCM nonce size and four-field AAD serialization | `edge_gateway/tests/test_secure_envelope.py`, `edge_gateway/tests/test_aad.py`, and `cloud_service/tests/test_cloud_aead.py` verify the 12-byte nonce and byte-identical AAD for protocol version, gateway ID, session ID, and request ID. |
| Exact SecureEnvelope shape | `edge_gateway/tests/test_secure_envelope.py` and `cloud_service/tests/test_cloud_envelope.py` require exactly six wire fields and reject extra fields. |
| Ordinary retry and session recovery semantics | `edge_gateway/tests/test_secure_transport.py` and `tests/integration/test_gateway_cloud_secure.py` distinguish an identical-envelope ordinary retry from one bounded replacement-session recovery. |
| Health/readiness behavior, ports, and environment mapping | `edge_gateway/tests/test_gateway_operations.py`, `cloud_service/tests/test_cloud_app.py`, `tests/test_gateway_docker_assets.py`, and `tests/integration/test_gateway_compose_e2e.py` cover application health/readiness and Compose service wiring. |

## Explicit prohibited-addition guards

The following are not optional design preferences; the listed tests reject or
otherwise constrain them in protocol version 1.

| Prohibited accidental addition/change | Guard |
|---|---|
| `cloud_id` or another Cloud identity field in public/session protocol messages | `cloud_service/tests/test_cloud_session_api.py::test_extra_field_and_malformed_json` rejects `cloud_id`; public-key/session response contract tests require exact response fields. |
| `session_key` in a wire message | `cloud_service/tests/test_cloud_envelope.py::test_extra_fields_rejected_without_echo` rejects it, and `test_handshake_wire_contract_and_no_secret_leak` requires the exact session response. |
| Extra session-response field | `cloud_service/tests/test_cloud_session_api.py::test_handshake_wire_contract_and_no_secret_leak` requires exactly `protocol_version`, `session_id`, `status`, and `expires_at`. |
| `message_counter` or dedicated replay counter/window | `edge_gateway/tests/test_secure_envelope.py::test_envelope_has_exactly_the_protocol_fields` and `cloud_service/tests/test_cloud_envelope.py::test_extra_fields_rejected_without_echo` reject the envelope expansion. |
| Fresh encryption on ordinary transport retry | `tests/integration/test_gateway_cloud_secure.py::test_ambiguous_transport_retries_the_same_envelope` requires identical serialized envelopes, including request ID, nonce, ciphertext, and AAD. |

Business idempotency on `UNIQUE(device_id, sequence_number)` is not
cryptographic replay protection. The absence of a dedicated anti-replay
counter/window is a frozen protocol-v1 limitation, not a missing test feature.
