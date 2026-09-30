# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1521 nodes · 3697 edges · 89 communities (56 shown, 33 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 500 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- LegacyMeasurement
- decrypt
- FailureMode
- test_client.py
- test_public_key_client.py
- MeasurementRepository
- test_sensor.py
- SessionManager
- SecureSession
- SessionManager
- cloud_service/app.py
- test_secure_message_tamper.py
- measure_baseline.py
- secure_transport.py
- create_app
- PqcMetrics
- envelope.py
- test_dispatch.py
- SecureTransportError
- test_secure_transport.py
- CanonicalMeasurement
- session_client.py
- GatewayErrorCode
- encapsulate
- test_secure_shutdown.py
- load_config
- StoredMeasurement
- validate_measurement
- create_app
- load_config
- test_session.py
- test_cloud_mlkem.py
- test_cloud_session_api.py
- test_cloud_baseline.py
- _fixture
- test_cloud_queries.py
- decode_binary
- CryptoFailureInjector
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- edge_gateway/app.py
- SecureTransport
- edge_gateway/config.py
- test_failure_injection.py
- json
- refresh_graphify.py
- KeyService
- test_cloud_public_key.py
- test_security_logging.py
- sessions.py
- derive_session_key
- _Clock
- edge_gateway/crypto/kdf.py
- queries.py
- _Clock
- _HandshakeHandler
- cloud_service/crypto/symmetric.py
- test_public_key.py
- KdfError
- test_refresh_graphify.py
- test_repository_hygiene.py
- AadError
- pytest
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- _Handler
- _Handler
- BaselineTransport
- _Handler
- _Sessions
- _Handler
- _Handler
- test_session_missing_and_expired_force_a_new_handshake
- measurement_url
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 41 edges
2. `SecureTransport` - 38 edges
3. `load_config()` - 37 edges
4. `create_app()` - 35 edges
5. `create_app()` - 34 edges
6. `SessionManager` - 33 edges
7. `FailureMode` - 33 edges
8. `PqcMetrics` - 32 edges
9. `MeasurementRepository` - 32 edges
10. `SecureTransportError` - 31 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `SessionEstablishmentError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py

## Import Cycles
- None detected.

## Communities (89 total, 33 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 1 - "LegacyMeasurement"
Cohesion: 0.06
Nodes (45): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), parse_legacy_measurement(), _reject_constant() (+37 more)

### Community 2 - "decrypt"
Cohesion: 0.07
Nodes (41): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+33 more)

### Community 3 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 4 - "test_client.py"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (21): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+13 more)

### Community 6 - "MeasurementRepository"
Cohesion: 0.12
Nodes (22): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+14 more)

### Community 7 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 8 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 9 - "SecureSession"
Cohesion: 0.09
Nodes (12): _Sessions, SecureSession, _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 10 - "SessionManager"
Cohesion: 0.11
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 11 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (8): Config, FailureMode, SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error(), test_custom_environment()

### Community 12 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 13 - "measure_baseline.py"
Cohesion: 0.11
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 15 - "create_app"
Cohesion: 0.11
Nodes (18): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+10 more)

### Community 17 - "envelope.py"
Cohesion: 0.14
Nodes (12): build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement() (+4 more)

### Community 18 - "test_dispatch.py"
Cohesion: 0.20
Nodes (13): CloudDispatch, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 19 - "SecureTransportError"
Cohesion: 0.14
Nodes (8): _dump(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransportError, _SessionRecovery

### Community 20 - "test_secure_transport.py"
Cohesion: 0.23
Nodes (17): _Cloud, _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable() (+9 more)

### Community 21 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 22 - "session_client.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 23 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 24 - "encapsulate"
Cohesion: 0.15
Nodes (13): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh() (+5 more)

### Community 25 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 26 - "load_config"
Cohesion: 0.21
Nodes (14): ConfigurationError, load_config(), integer(), number(), text(), value(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values() (+6 more)

### Community 27 - "StoredMeasurement"
Cohesion: 0.15
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 28 - "validate_measurement"
Cohesion: 0.21
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 29 - "create_app"
Cohesion: 0.14
Nodes (14): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+6 more)

### Community 30 - "load_config"
Cohesion: 0.15
Nodes (12): load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration(), test_settings_dependency_can_be_overridden_and_isolated() (+4 more)

### Community 31 - "test_session.py"
Cohesion: 0.16
Nodes (10): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active() (+2 more)

### Community 32 - "test_cloud_mlkem.py"
Cohesion: 0.14
Nodes (3): test_bad_vendor_secret_rejected(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 33 - "test_cloud_session_api.py"
Cohesion: 0.18
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 34 - "test_cloud_baseline.py"
Cohesion: 0.14
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 35 - "_fixture"
Cohesion: 0.13
Nodes (12): client(), payload(), payload(), database(), measurement(), payload(), cloud(), values() (+4 more)

### Community 36 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 37 - "decode_binary"
Cohesion: 0.23
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _different_nonce(), _tamper()

### Community 39 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 40 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 41 - "edge_gateway/app.py"
Cohesion: 0.17
Nodes (6): get_config(), _logging_level(), main(), GatewayConfig, LegacyJSONError, LegacyMeasurementDomainError

### Community 42 - "SecureTransport"
Cohesion: 0.16
Nodes (4): lifespan(), _endpoint(), SecureTransport, DispatchMetrics

### Community 43 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 44 - "test_failure_injection.py"
Cohesion: 0.23
Nodes (10): _aad(), _injector(), _plaintext(), test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected() (+2 more)

### Community 45 - "json"
Cohesion: 0.25
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 46 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 47 - "KeyService"
Cohesion: 0.17
Nodes (4): lifespan(), StartupError, KeyService, test_session_initialization_failure_releases_keys()

### Community 48 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 49 - "test_security_logging.py"
Cohesion: 0.23
Nodes (4): _Clock, _Cloud, cloud_url(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 50 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 51 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 52 - "_Clock"
Cohesion: 0.24
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 54 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 55 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 58 - "test_public_key.py"
Cohesion: 0.39
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 59 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 60 - "test_refresh_graphify.py"
Cohesion: 0.38
Nodes (3): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 72 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.67
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 494 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `edge_gateway/app.py`, `SecureTransport`, `SessionManager`, `SecureSession`, `secure_transport.py`, `test_security_logging.py`, `test_dispatch.py`, `create_app`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `_Handler` connect `_Handler` to `test_security_logging.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `encode_binary()` connect `decode_binary` to `test_cloud_session_api.py`, `test_public_key_client.py`, `secure_transport.py`, `envelope.py`, `test_security_logging.py`, `SecureTransportError`, `_Clock`, `session_client.py`, `_Clock`, `test_public_key.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05509518477043673 - nodes in this community are weakly interconnected._