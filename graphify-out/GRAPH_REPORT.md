# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1341 nodes · 3262 edges · 77 communities (52 shown, 25 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 443 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- decrypt
- cli.py
- test_client.py
- test_sensor.py
- MeasurementRepository
- load_config
- SessionManager
- json
- load_config
- test_gateway_models.py
- secure_transport.py
- test_session.py
- cloud_service/app.py
- test_dispatch.py
- CanonicalMeasurement
- logging
- PqcMetrics
- SecureSession
- measure_baseline.py
- edge_gateway/crypto/session.py
- test_cloud_envelope.py
- repository.py
- encapsulate
- validate_measurement
- test_cloud_session_api.py
- SessionManager
- derive_session_key
- test_security_logging.py
- test_secure_transport.py
- test_cloud_config.py
- test_cloud_queries.py
- SecureTransportError
- plaintext.py
- cloud_service/crypto/mlkem.py
- test_cloud_baseline.py
- test_cloud_kdf.py
- edge_gateway/config.py
- CryptoFailureInjector
- pytest
- SecureTransport
- test_failure_injection.py
- refresh_graphify.py
- test_cloud_public_key.py
- KeyService
- sessions.py
- test_cloud_mlkem.py
- test_envelope.py
- parse_public_key_response
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- _HandshakeHandler
- KdfError
- cloud_service/crypto/aad.py
- get_measurement
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- test_gateway_config.py
- _Handler
- _Handler
- StartupError
- test_session_missing_and_expired_force_a_new_handshake
- _Handler
- cloud_server
- _Handler
- _Handler
- _RejectRedirect
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 41 edges
2. `SecureTransport` - 36 edges
3. `create_app()` - 34 edges
4. `FailureMode` - 33 edges
5. `PqcMetrics` - 32 edges
6. `MeasurementRepository` - 32 edges
7. `load_config()` - 32 edges
8. `FailureInjector` - 31 edges
9. `SessionManager` - 31 edges
10. `SecureTransportError` - 28 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_protocol_example_and_independent_round_trip()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_models.py → cloud_service/tests/test_cloud_aead.py

## Import Cycles
- None detected.

## Communities (77 total, 25 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 1 - "decrypt"
Cohesion: 0.07
Nodes (39): AeadError, decrypt(), fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers() (+31 more)

### Community 2 - "cli.py"
Cohesion: 0.12
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 3 - "test_client.py"
Cohesion: 0.08
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 4 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 5 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_unrelated_record_id_collision_is_not_idempotent_success(), database() (+16 more)

### Community 6 - "load_config"
Cohesion: 0.10
Nodes (24): create_app(), health(), ready(), main(), _unavailable(), ConfigurationError, load_config(), integer() (+16 more)

### Community 7 - "SessionManager"
Cohesion: 0.10
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 8 - "json"
Cohesion: 0.11
Nodes (17): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), _public_key() (+9 more)

### Community 9 - "load_config"
Cohesion: 0.12
Nodes (18): create_app(), health(), measurements(), ready(), _logging_level(), main(), _unavailable(), load_config() (+10 more)

### Community 10 - "test_gateway_models.py"
Cohesion: 0.15
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 11 - "secure_transport.py"
Cohesion: 0.12
Nodes (10): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), test_invalid_alphabet_whitespace_and_empty_are_rejected() (+2 more)

### Community 12 - "test_session.py"
Cohesion: 0.11
Nodes (12): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+4 more)

### Community 13 - "cloud_service/app.py"
Cohesion: 0.13
Nodes (5): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 14 - "test_dispatch.py"
Cohesion: 0.17
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 15 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (13): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+5 more)

### Community 16 - "logging"
Cohesion: 0.10
Nodes (4): get_config(), GatewayConfig, BaselineTransport, DispatchMetrics

### Community 18 - "SecureSession"
Cohesion: 0.10
Nodes (8): _Sessions, SecureSession, _session(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish(), test_unsafe_log_values_are_dropped()

### Community 19 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 20 - "edge_gateway/crypto/session.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 21 - "test_cloud_envelope.py"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 22 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 23 - "encapsulate"
Cohesion: 0.15
Nodes (12): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+4 more)

### Community 24 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 25 - "test_cloud_session_api.py"
Cohesion: 0.15
Nodes (11): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail() (+3 more)

### Community 26 - "SessionManager"
Cohesion: 0.16
Nodes (4): log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 27 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 28 - "test_security_logging.py"
Cohesion: 0.14
Nodes (7): _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_injected_handshake_failure_stays_fail_closed(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 29 - "test_secure_transport.py"
Cohesion: 0.33
Nodes (15): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+7 more)

### Community 30 - "test_cloud_config.py"
Cohesion: 0.16
Nodes (11): Config, FailureMode, test_custom_environment(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries(), test_invalid_configuration(), test_invalid_database_url() (+3 more)

### Community 31 - "test_cloud_queries.py"
Cohesion: 0.14
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 32 - "SecureTransportError"
Cohesion: 0.17
Nodes (6): _error_code(), _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransportError, _SessionRecovery

### Community 33 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 34 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 35 - "test_cloud_baseline.py"
Cohesion: 0.15
Nodes (7): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 36 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 37 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 39 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 40 - "SecureTransport"
Cohesion: 0.23
Nodes (3): _endpoint(), _Measurement, SecureTransport

### Community 41 - "test_failure_injection.py"
Cohesion: 0.22
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 42 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 43 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 45 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 46 - "test_cloud_mlkem.py"
Cohesion: 0.22
Nodes (4): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 47 - "test_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 48 - "parse_public_key_response"
Cohesion: 0.33
Nodes (6): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 49 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 50 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 52 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 54 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 56 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 61 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 419 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `decrypt`, `SecureTransport`, `load_config`, `secure_transport.py`, `test_dispatch.py`, `logging`, `SecureSession`, `edge_gateway/crypto/session.py`, `SessionManager`, `.__init__`, `test_security_logging.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `SecureTransport`, `test_failure_injection.py`, `secure_transport.py`, `logging`, `edge_gateway/crypto/session.py`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `SessionManager`, `.__init__`, `test_security_logging.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_cloud_session_api.py`, `StartupError`, `cloud_service/app.py`, `load_config`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._