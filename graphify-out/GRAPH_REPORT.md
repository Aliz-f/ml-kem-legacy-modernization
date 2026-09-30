# Graph Report - ml-kem-legacy-modernization  (2026-10-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1578 nodes · 3917 edges · 69 communities (50 shown, 19 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 548 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- LegacyMeasurement
- FailureMode
- decrypt
- test_session.py
- test_cloud_secure.py
- test_client.py
- FailureMode
- test_failure_injection.py
- MeasurementRepository
- measure_baseline.py
- test_sensor.py
- SecureTransport
- derive_session_key
- json
- dataclasses
- SessionManager
- secure_transport.py
- test_cloud_mlkem.py
- cloud_service/app.py
- test_dispatch.py
- test_secure_transport.py
- load_config
- PqcMetrics
- test_public_key_client.py
- validate_measurement
- SessionManager
- GatewayErrorCode
- CanonicalMeasurement
- CryptoFailureInjector
- public_key.py
- StoredMeasurement
- encapsulate
- load_config
- SecureSession
- test_cloud_session_api.py
- test_gateway_validation.py
- test_cloud_baseline.py
- _fixture
- test_cloud_queries.py
- edge_gateway/app.py
- cloud_service/crypto/mlkem.py
- edge_gateway/config.py
- edge_gateway/crypto/encoding.py
- pytest
- refresh_graphify.py
- test_cloud_public_key.py
- sessions.py
- _error_response
- queries.py
- .__init__
- test_gateway_config.py
- _Handler
- _Handler
- _RejectRedirect
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 46 edges
2. `create_app()` - 39 edges
3. `FailureMode` - 38 edges
4. `SecureTransport` - 36 edges
5. `load_config()` - 35 edges
6. `create_app()` - 34 edges
7. `FailureMode` - 33 edges
8. `PqcMetrics` - 32 edges
9. `MeasurementRepository` - 32 edges
10. `FailureInjector` - 31 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_exact_protocol_fields_and_json_serialization()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_canonical_model.py → cloud_service/tests/test_cloud_aead.py

## Import Cycles
- None detected.

## Communities (69 total, 19 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (42): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+34 more)

### Community 1 - "LegacyMeasurement"
Cohesion: 0.06
Nodes (36): baseline_headers(), create_request_id(), CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize() (+28 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "decrypt"
Cohesion: 0.07
Nodes (43): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+35 more)

### Community 4 - "test_session.py"
Cohesion: 0.06
Nodes (23): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+15 more)

### Community 5 - "test_cloud_secure.py"
Cohesion: 0.08
Nodes (33): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet() (+25 more)

### Community 6 - "test_client.py"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 7 - "FailureMode"
Cohesion: 0.10
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 8 - "test_failure_injection.py"
Cohesion: 0.07
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 9 - "MeasurementRepository"
Cohesion: 0.10
Nodes (23): Database, StorageConflictError, StorageError, MeasurementRepository, test_acceptance_is_committed_and_correlated(), test_concurrent_duplicates_across_connections(), save(), test_unrelated_record_id_collision_is_not_idempotent_success() (+15 more)

### Community 10 - "measure_baseline.py"
Cohesion: 0.08
Nodes (19): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+11 more)

### Community 11 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 12 - "SecureTransport"
Cohesion: 0.09
Nodes (12): build_secure_envelope(), SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport (+4 more)

### Community 13 - "derive_session_key"
Cohesion: 0.08
Nodes (15): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+7 more)

### Community 14 - "json"
Cohesion: 0.09
Nodes (11): SecurityMode, AadError, build_aad(), AeadError, decrypt(), public_key(), _unavailable(), _error() (+3 more)

### Community 15 - "dataclasses"
Cohesion: 0.11
Nodes (16): EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+8 more)

### Community 16 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 17 - "secure_transport.py"
Cohesion: 0.11
Nodes (10): get_config(), GatewayConfig, corrupt_ciphertext_copy(), _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+2 more)

### Community 18 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (10): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent() (+2 more)

### Community 19 - "cloud_service/app.py"
Cohesion: 0.10
Nodes (17): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+9 more)

### Community 20 - "test_dispatch.py"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 21 - "test_secure_transport.py"
Cohesion: 0.17
Nodes (18): _Cloud, _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried() (+10 more)

### Community 22 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 24 - "test_public_key_client.py"
Cohesion: 0.14
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _body(), cloud_server(), _public_key(), _Response, test_cloud_url_and_timeout_are_validated() (+8 more)

### Community 25 - "validate_measurement"
Cohesion: 0.16
Nodes (13): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema() (+5 more)

### Community 26 - "SessionManager"
Cohesion: 0.13
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 27 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 28 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 29 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 30 - "public_key.py"
Cohesion: 0.15
Nodes (8): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 31 - "StoredMeasurement"
Cohesion: 0.14
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 32 - "encapsulate"
Cohesion: 0.17
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 33 - "load_config"
Cohesion: 0.18
Nodes (13): create_app(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration() (+5 more)

### Community 34 - "SecureSession"
Cohesion: 0.13
Nodes (6): _Sessions, SecureSession, test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 35 - "test_cloud_session_api.py"
Cohesion: 0.17
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 36 - "test_gateway_validation.py"
Cohesion: 0.24
Nodes (13): parse_legacy_measurement(), assert_rejection(), test_domain_bounds_remain_a_separate_stage(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+5 more)

### Community 37 - "test_cloud_baseline.py"
Cohesion: 0.15
Nodes (7): client(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 38 - "_fixture"
Cohesion: 0.13
Nodes (12): payload(), payload(), client(), database(), measurement(), payload(), cloud(), values() (+4 more)

### Community 39 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 40 - "edge_gateway/app.py"
Cohesion: 0.17
Nodes (6): _logging_level(), main(), LegacyJSONError, LegacyMeasurementDomainError, _reject_constant(), validate_legacy_measurement()

### Community 41 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 42 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 43 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.24
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 44 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 45 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 46 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 47 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 48 - "_error_response"
Cohesion: 0.22
Nodes (9): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready(), _error_response() (+1 more)

### Community 49 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 51 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 486 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `load_config`, `SecureSession`, `edge_gateway/app.py`, `SecureTransport`, `secure_transport.py`, `.__init__`, `test_dispatch.py`, `SessionManager`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `test_failure_injection.py`, `secure_transport.py`, `SessionManager`, `SecureTransport`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `load_config`, `SecureSession`, `decrypt`, `test_failure_injection.py`, `measure_baseline.py`, `edge_gateway/crypto/encoding.py`, `secure_transport.py`, `.__init__`, `test_dispatch.py`, `test_secure_transport.py`, `PqcMetrics`, `SessionManager`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.060424469413233456 - nodes in this community are weakly interconnected._