# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1318 nodes · 3209 edges · 68 communities (48 shown, 20 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 428 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- json
- FailureMode
- cli.py
- test_cloud_session_api.py
- test_client.py
- pytest
- test_dispatch.py
- test_sensor.py
- MeasurementRepository
- SecureTransport
- test_gateway_models.py
- secure_transport.py
- edge_gateway/crypto/session.py
- CanonicalMeasurement
- PqcMetrics
- logging
- measure_baseline.py
- repository.py
- test_security_logging.py
- load_config
- validate_measurement
- test_secure_transport.py
- create_app
- encapsulate
- create_app
- session_client.py
- SessionManager
- test_cloud_baseline.py
- load_config
- SecureSession
- test_cloud_public_key.py
- test_cloud_queries.py
- plaintext.py
- SessionState
- encoding.py
- test_public_key_client.py
- cloud_service/crypto/mlkem.py
- edge_gateway/config.py
- CryptoFailureInjector
- test_session.py
- cloud_service/app.py
- test_failure_injection.py
- refresh_graphify.py
- KeyService
- sessions.py
- derive_session_key
- parse_public_key_response
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- edge_gateway/crypto/kdf.py
- _HandshakeHandler
- cloud_service/crypto/symmetric.py
- KdfError
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- _Handler
- _Handler
- test_session_missing_and_expired_force_a_new_handshake
- _Handler
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

## Communities (68 total, 20 thin omitted)

### Community 0 - "json"
Cohesion: 0.06
Nodes (45): AadError, build_aad(), fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers() (+37 more)

### Community 1 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 2 - "cli.py"
Cohesion: 0.12
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 3 - "test_cloud_session_api.py"
Cohesion: 0.06
Nodes (22): SecureSession, SessionAccessError, SessionManager, SessionState, client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement() (+14 more)

### Community 4 - "test_client.py"
Cohesion: 0.08
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "pytest"
Cohesion: 0.05
Nodes (14): test_harness_rejects_invalid_sample_count(), test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged() (+6 more)

### Community 6 - "test_dispatch.py"
Cohesion: 0.09
Nodes (17): BaselineTransport, CloudDispatch, DispatchMetrics, _Baseline, cloud(), _config(), _Handler, _measurement() (+9 more)

### Community 7 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.11
Nodes (22): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), test_closed_database_errors_are_safe() (+14 more)

### Community 9 - "SecureTransport"
Cohesion: 0.12
Nodes (9): _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport, SecureTransportError (+1 more)

### Community 10 - "test_gateway_models.py"
Cohesion: 0.15
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 11 - "secure_transport.py"
Cohesion: 0.11
Nodes (7): build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _RejectRedirect, log_security(), _token()

### Community 12 - "edge_gateway/crypto/session.py"
Cohesion: 0.12
Nodes (13): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+5 more)

### Community 13 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (13): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+5 more)

### Community 15 - "logging"
Cohesion: 0.13
Nodes (7): public_key(), _unavailable(), _error(), get_measurement(), list_measurements(), baseline_measurement(), _error()

### Community 16 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 17 - "repository.py"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 18 - "test_security_logging.py"
Cohesion: 0.12
Nodes (12): _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send() (+4 more)

### Community 19 - "load_config"
Cohesion: 0.18
Nodes (13): Config, FailureMode, load_config(), SecurityMode, test_custom_environment(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries() (+5 more)

### Community 20 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 21 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (16): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+8 more)

### Community 22 - "create_app"
Cohesion: 0.14
Nodes (14): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+6 more)

### Community 23 - "encapsulate"
Cohesion: 0.17
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 24 - "create_app"
Cohesion: 0.15
Nodes (10): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+2 more)

### Community 25 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 27 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 28 - "load_config"
Cohesion: 0.15
Nodes (11): load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration(), test_settings_dependency_can_be_overridden_and_isolated(), test_shutdown_runs_on_exception() (+3 more)

### Community 29 - "SecureSession"
Cohesion: 0.13
Nodes (6): _Sessions, SecureSession, test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 30 - "test_cloud_public_key.py"
Cohesion: 0.16
Nodes (9): secure_app(), test_classical_does_not_generate_keys(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized() (+1 more)

### Community 31 - "test_cloud_queries.py"
Cohesion: 0.14
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 32 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 33 - "SessionState"
Cohesion: 0.14
Nodes (8): SessionState, _manager(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active(), test_unavailable_cloud_is_retryable_and_leaves_no_session()

### Community 34 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 35 - "test_public_key_client.py"
Cohesion: 0.17
Nodes (7): _body(), cloud_server(), _Handler, _public_key(), _Response, test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key()

### Community 36 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 37 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 39 - "test_session.py"
Cohesion: 0.20
Nodes (5): _Clock, _Cloud, cloud_url(), _stamp(), test_session_response_must_be_in_the_future_and_explicitly_zoned()

### Community 40 - "cloud_service/app.py"
Cohesion: 0.21
Nodes (5): ConfigurationError, integer(), number(), text(), value()

### Community 41 - "test_failure_injection.py"
Cohesion: 0.22
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_enabled_warning_names_the_mode_and_not_the_seed(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode()

### Community 42 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 43 - "KeyService"
Cohesion: 0.17
Nodes (4): lifespan(), StartupError, KeyService, test_session_initialization_failure_releases_keys()

### Community 44 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 45 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 46 - "parse_public_key_response"
Cohesion: 0.33
Nodes (6): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 47 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 48 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 52 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 56 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 412 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `test_dispatch.py`, `SecureTransport`, `secure_transport.py`, `edge_gateway/crypto/session.py`, `test_security_logging.py`, `create_app`, `SessionManager`, `SecureSession`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `SessionState`, `test_cloud_session_api.py`, `CryptoFailureInjector`, `test_failure_injection.py`, `edge_gateway/crypto/session.py`, `PqcMetrics`, `test_security_logging.py`, `KdfError`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `encapsulate`, `test_session_missing_and_expired_force_a_new_handshake`, `session_client.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `Measurement` connect `test_sensor.py` to `FailureMode`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._