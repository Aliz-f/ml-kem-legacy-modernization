# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1270 nodes · 3088 edges · 66 communities (41 shown, 25 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 401 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- decrypt
- cli.py
- load_config
- load_config
- FailureMode
- test_sensor.py
- derive_session_key
- test_session.py
- MeasurementRepository
- SecureTransport
- SessionManager
- test_gateway_models.py
- SecureSession
- test_dispatch.py
- validate_measurement
- CanonicalMeasurement
- test_public_key_client.py
- measure_baseline.py
- create_app
- PqcMetrics
- load_config
- test_cloud_session_api.py
- repository.py
- encapsulate
- secure_transport.py
- session_client.py
- test_cloud_baseline.py
- CryptoFailureInjector
- test_failure_injection.py
- test_secure_transport.py
- cloud_service/crypto/mlkem.py
- test_cloud_queries.py
- SessionManager
- encoding.py
- test_cloud_kdf.py
- cloud_service/config.py
- pytest
- parse_public_key_response
- _Clock
- test_cloud_public_key.py
- KeyService
- cloud_service/app.py
- sessions.py
- queries.py
- test_cloud_mlkem.py
- public_key_client.py
- SessionEstablishmentError
- .__init__
- _HandshakeHandler
- cloud_service/crypto/symmetric.py
- json
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- _Handler
- _Handler
- cloud_server
- _Handler
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 41 edges
2. `SecureTransport` - 34 edges
3. `create_app()` - 34 edges
4. `FailureMode` - 33 edges
5. `MeasurementRepository` - 32 edges
6. `PqcMetrics` - 31 edges
7. `FailureInjector` - 31 edges
8. `load_config()` - 31 edges
9. `SessionManager` - 30 edges
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

## Communities (66 total, 25 thin omitted)

### Community 0 - "decrypt"
Cohesion: 0.05
Nodes (55): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+47 more)

### Community 1 - "cli.py"
Cohesion: 0.12
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "load_config"
Cohesion: 0.08
Nodes (33): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+25 more)

### Community 3 - "load_config"
Cohesion: 0.09
Nodes (24): Config, ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration() (+16 more)

### Community 4 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 5 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 6 - "derive_session_key"
Cohesion: 0.07
Nodes (15): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+7 more)

### Community 7 - "test_session.py"
Cohesion: 0.08
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _Handler, _manager(), _stamp(), test_close_wipes_the_session_key() (+6 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.11
Nodes (23): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), test_closed_database_errors_are_safe() (+15 more)

### Community 9 - "SecureTransport"
Cohesion: 0.11
Nodes (13): _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+5 more)

### Community 10 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 11 - "test_gateway_models.py"
Cohesion: 0.15
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 12 - "SecureSession"
Cohesion: 0.09
Nodes (13): _Sessions, SecureSession, _session(), _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+5 more)

### Community 13 - "test_dispatch.py"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 14 - "validate_measurement"
Cohesion: 0.14
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 15 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (13): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+5 more)

### Community 16 - "test_public_key_client.py"
Cohesion: 0.13
Nodes (15): _endpoint(), fetch_public_key(), PublicKeyTransportError, _body(), _Handler, _public_key(), test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+7 more)

### Community 17 - "measure_baseline.py"
Cohesion: 0.11
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 18 - "create_app"
Cohesion: 0.11
Nodes (17): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+9 more)

### Community 19 - "PqcMetrics"
Cohesion: 0.09
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 20 - "load_config"
Cohesion: 0.18
Nodes (15): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_defaults_do_not_create_database() (+7 more)

### Community 21 - "test_cloud_session_api.py"
Cohesion: 0.13
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 22 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 23 - "encapsulate"
Cohesion: 0.15
Nodes (12): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+4 more)

### Community 25 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 26 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500() (+1 more)

### Community 28 - "test_failure_injection.py"
Cohesion: 0.18
Nodes (11): _aad(), _injector(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault() (+3 more)

### Community 29 - "test_secure_transport.py"
Cohesion: 0.33
Nodes (15): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+7 more)

### Community 30 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 31 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 32 - "SessionManager"
Cohesion: 0.17
Nodes (4): clock(), SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 33 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 34 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 35 - "cloud_service/config.py"
Cohesion: 0.21
Nodes (5): FailureMode, SecurityMode, public_key(), _unavailable(), test_custom_environment()

### Community 36 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 37 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 38 - "_Clock"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 39 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 42 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 43 - "queries.py"
Cohesion: 0.29
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 44 - "test_cloud_mlkem.py"
Cohesion: 0.22
Nodes (4): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 397 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `SessionManager`, `load_config`, `SecureTransport`, `SecureSession`, `test_dispatch.py`, `.__init__`, `secure_transport.py`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `parse_public_key_response`, `derive_session_key`, `test_session.py`, `SecureSession`, `SessionEstablishmentError`, `test_public_key_client.py`, `PqcMetrics`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `test_cloud_session_api.py`, `encapsulate`, `secure_transport.py`, `session_client.py`, `CryptoFailureInjector`, `test_failure_injection.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `decrypt`, `encoding.py`, `SecureSession`, `test_dispatch.py`, `SessionEstablishmentError`, `.__init__`, `PqcMetrics`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `secure_transport.py`, `CryptoFailureInjector`, `test_failure_injection.py`, `test_secure_transport.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._