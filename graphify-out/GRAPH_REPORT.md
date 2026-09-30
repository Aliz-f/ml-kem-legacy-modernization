# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1063 nodes · 2495 edges · 54 communities (39 shown, 15 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 325 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- decrypt
- cli.py
- test_cloud_session_api.py
- load_config
- test_client.py
- FailureMode
- MeasurementRepository
- test_sensor.py
- test_gateway_models.py
- load_config
- test_session.py
- CanonicalMeasurement
- load_config
- create_app
- edge_gateway/crypto/session.py
- measure_baseline.py
- cloud_service/app.py
- repository.py
- SessionManager
- derive_session_key
- validate_measurement
- test_cloud_baseline.py
- test_public_key_client.py
- test_cloud_public_key.py
- test_cloud_queries.py
- fetch_public_key
- test_cloud_kdf.py
- encapsulate
- cloud_service/crypto/mlkem.py
- encoding.py
- test_crypto_failure_is_classified_and_recorded
- test_cloud_mlkem.py
- refresh_graphify.py
- KeyService
- public_key.py
- edge_gateway/crypto/mlkem.py
- cloud_service/crypto/symmetric.py
- test_public_key.py
- json
- establish_session
- pytest
- get_measurement
- _Handler
- test_refresh_graphify.py
- public_key
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 41 edges
2. `create_app()` - 34 edges
3. `FailureMode` - 33 edges
4. `MeasurementRepository` - 32 edges
5. `FailureInjector` - 31 edges
6. `StorageError` - 25 edges
7. `load_config()` - 25 edges
8. `CanonicalMeasurement` - 23 edges
9. `validate_measurement()` - 23 edges
10. `load_config()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_protocol_example_and_independent_round_trip()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_models.py → cloud_service/tests/test_cloud_aead.py
- `test_unrelated_record_id_collision_is_not_idempotent_success()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_baseline.py → edge_gateway/tests/test_session.py

## Import Cycles
- None detected.

## Communities (54 total, 15 thin omitted)

### Community 0 - "decrypt"
Cohesion: 0.05
Nodes (55): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+47 more)

### Community 1 - "cli.py"
Cohesion: 0.12
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "test_cloud_session_api.py"
Cohesion: 0.06
Nodes (21): SecureSession, SessionAccessError, SessionManager, SessionState, handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json() (+13 more)

### Community 3 - "load_config"
Cohesion: 0.08
Nodes (32): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+24 more)

### Community 4 - "test_client.py"
Cohesion: 0.08
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 6 - "MeasurementRepository"
Cohesion: 0.11
Nodes (25): Database, StorageConflictError, StorageError, MeasurementRepository, test_acceptance_is_committed_and_correlated(), test_concurrent_duplicates_across_connections(), save(), test_device_filter_and_limit_preserve_insertion_order() (+17 more)

### Community 7 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 8 - "test_gateway_models.py"
Cohesion: 0.15
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 9 - "load_config"
Cohesion: 0.14
Nodes (20): Config, ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration() (+12 more)

### Community 10 - "test_session.py"
Cohesion: 0.11
Nodes (12): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+4 more)

### Community 11 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (13): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+5 more)

### Community 12 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+9 more)

### Community 13 - "create_app"
Cohesion: 0.11
Nodes (16): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+8 more)

### Community 14 - "edge_gateway/crypto/session.py"
Cohesion: 0.15
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 15 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 16 - "cloud_service/app.py"
Cohesion: 0.18
Nodes (3): SecurityMode, baseline_measurement(), _error()

### Community 17 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 18 - "SessionManager"
Cohesion: 0.12
Nodes (3): SecureSession, SessionEstablishmentError, SessionManager

### Community 19 - "derive_session_key"
Cohesion: 0.14
Nodes (9): derive_session_key(), KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+1 more)

### Community 20 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 21 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (9): client(), payload(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500() (+1 more)

### Community 22 - "test_public_key_client.py"
Cohesion: 0.14
Nodes (9): _body(), cloud_server(), _Handler, _public_key(), _Response, test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key(), test_invalid_json_is_not_a_transport_retry() (+1 more)

### Community 23 - "test_cloud_public_key.py"
Cohesion: 0.18
Nodes (9): secure_app(), test_classical_does_not_generate_keys(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized() (+1 more)

### Community 24 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (9): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 25 - "fetch_public_key"
Cohesion: 0.17
Nodes (9): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable(), test_http_status_is_classified(), test_redirect_is_not_followed() (+1 more)

### Community 26 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 27 - "encapsulate"
Cohesion: 0.21
Nodes (10): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), encapsulate(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 28 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 29 - "encoding.py"
Cohesion: 0.24
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 30 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.15
Nodes (5): KdfError, SessionMetrics, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 31 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (4): test_bad_vendor_secret_rejected(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 32 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 33 - "KeyService"
Cohesion: 0.17
Nodes (4): lifespan(), StartupError, KeyService, test_session_initialization_failure_releases_keys()

### Community 34 - "public_key.py"
Cohesion: 0.26
Nodes (4): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, test_missing_fields_and_non_object_are_rejected()

### Community 37 - "test_public_key.py"
Cohesion: 0.39
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 39 - "establish_session"
Cohesion: 0.52
Nodes (5): _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 41 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 43 - "test_refresh_graphify.py"
Cohesion: 0.47
Nodes (3): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 322 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `StorageError` connect `MeasurementRepository` to `cloud_service/app.py`, `get_measurement`, `create_app`, `repository.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `KeyService`, `test_cloud_session_api.py`, `MeasurementRepository`, `create_app`, `measure_baseline.py`, `cloud_service/app.py`, `test_cloud_baseline.py`, `test_cloud_public_key.py`, `test_cloud_queries.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `test_cloud_session_api.py` to `cloud_service/app.py`, `KeyService`, `create_app`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `MeasurementRepository` (e.g. with `CanonicalMeasurement` and `Database`) actually correct?**
  _`MeasurementRepository` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `FailureInjector` (e.g. with `FailureMode` and `test_duplicate_sequence_selection_varies_by_seed()`) actually correct?**
  _`FailureInjector` has 22 INFERRED edges - model-reasoned connections that need verification._