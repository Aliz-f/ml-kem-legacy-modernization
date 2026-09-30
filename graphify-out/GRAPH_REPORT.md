# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1579 nodes · 3920 edges · 79 communities (54 shown, 25 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 548 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- LegacyMeasurement
- FailureMode
- decrypt
- test_cloud_secure.py
- test_client.py
- test_failure_injection.py
- FailureMode
- SecureTransport
- measure_baseline.py
- test_sensor.py
- MeasurementRepository
- dataclasses
- SessionManager
- cloud_service/app.py
- SecureSession
- validate_measurement
- load_config
- test_dispatch.py
- load_config
- PqcMetrics
- test_public_key_client.py
- GatewayErrorCode
- cloud_service/config.py
- CanonicalMeasurement
- secure.py
- test_cloud_session_api.py
- edge_gateway/app.py
- CryptoFailureInjector
- encapsulate
- session_client.py
- test_security_logging.py
- StoredMeasurement
- secure_transport.py
- test_session.py
- _fixture
- test_secure_transport.py
- test_cloud_kdf.py
- test_cloud_baseline.py
- SessionManager
- cloud_service/crypto/mlkem.py
- test_cloud_queries.py
- edge_gateway/crypto/encoding.py
- edge_gateway/config.py
- test_gateway_validation.py
- test_cloud_mlkem.py
- test_cloud_public_key.py
- json
- parse_public_key_response
- derive_session_key
- _Clock
- queries.py
- edge_gateway/crypto/kdf.py
- _error_response
- .__init__
- KdfError
- test_refresh_graphify.py
- test_repository_hygiene.py
- pytest
- test_gateway_config.py
- _Handler
- _Handler
- _Handler
- _Handler
- _Handler
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
8. `MeasurementRepository` - 32 edges
9. `PqcMetrics` - 32 edges
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

## Communities (79 total, 25 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (44): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), main(), parser(), record_work(), recorded_changes() (+36 more)

### Community 1 - "LegacyMeasurement"
Cohesion: 0.06
Nodes (35): baseline_headers(), create_request_id(), CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize() (+27 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "decrypt"
Cohesion: 0.07
Nodes (43): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+35 more)

### Community 4 - "test_cloud_secure.py"
Cohesion: 0.08
Nodes (33): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet() (+25 more)

### Community 5 - "test_client.py"
Cohesion: 0.08
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 6 - "test_failure_injection.py"
Cohesion: 0.07
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 7 - "FailureMode"
Cohesion: 0.11
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 8 - "SecureTransport"
Cohesion: 0.09
Nodes (12): build_secure_envelope(), SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport (+4 more)

### Community 9 - "measure_baseline.py"
Cohesion: 0.08
Nodes (19): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+11 more)

### Community 10 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 11 - "MeasurementRepository"
Cohesion: 0.11
Nodes (22): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+14 more)

### Community 12 - "dataclasses"
Cohesion: 0.11
Nodes (16): EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+8 more)

### Community 13 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 14 - "cloud_service/app.py"
Cohesion: 0.10
Nodes (17): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+9 more)

### Community 15 - "SecureSession"
Cohesion: 0.09
Nodes (8): _Sessions, SecureSession, SessionEstablishmentError, _session(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 16 - "validate_measurement"
Cohesion: 0.15
Nodes (13): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema() (+5 more)

### Community 17 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 18 - "test_dispatch.py"
Cohesion: 0.20
Nodes (13): CloudDispatch, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 19 - "load_config"
Cohesion: 0.16
Nodes (15): create_app(), _logging_level(), main(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health() (+7 more)

### Community 21 - "test_public_key_client.py"
Cohesion: 0.14
Nodes (15): fetch_public_key(), PublicKeyRejected, _body(), cloud_server(), _public_key(), _Response, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+7 more)

### Community 22 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 23 - "cloud_service/config.py"
Cohesion: 0.15
Nodes (9): SecurityMode, derive_session_key(), public_key(), _unavailable(), _decode_ciphertext(), _error(), _establish(), establish_session() (+1 more)

### Community 24 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 25 - "secure.py"
Cohesion: 0.15
Nodes (8): AadError, build_aad(), AeadError, decrypt(), _error(), _ingest(), secure_measurement(), fail()

### Community 26 - "test_cloud_session_api.py"
Cohesion: 0.14
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 27 - "edge_gateway/app.py"
Cohesion: 0.13
Nodes (10): measurements(), get_config(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_normalization_preserves_values_and_input() (+2 more)

### Community 28 - "CryptoFailureInjector"
Cohesion: 0.13
Nodes (4): GatewayConfig, CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 29 - "encapsulate"
Cohesion: 0.17
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 30 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 31 - "test_security_logging.py"
Cohesion: 0.14
Nodes (10): _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+2 more)

### Community 32 - "StoredMeasurement"
Cohesion: 0.15
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 33 - "secure_transport.py"
Cohesion: 0.17
Nodes (4): corrupt_ciphertext_copy(), _RejectRedirect, log_security(), _token()

### Community 34 - "test_session.py"
Cohesion: 0.15
Nodes (8): SessionState, _manager(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active(), test_unavailable_cloud_is_retryable_and_leaves_no_session()

### Community 35 - "_fixture"
Cohesion: 0.11
Nodes (14): client(), payload(), payload(), client(), database(), measurement(), payload(), cloud() (+6 more)

### Community 36 - "test_secure_transport.py"
Cohesion: 0.33
Nodes (15): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+7 more)

### Community 37 - "test_cloud_kdf.py"
Cohesion: 0.12
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 38 - "test_cloud_baseline.py"
Cohesion: 0.14
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 40 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 41 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 42 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 43 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 44 - "test_gateway_validation.py"
Cohesion: 0.33
Nodes (10): assert_rejection(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422(), test_parsed_non_measurements_are_422() (+2 more)

### Community 45 - "test_cloud_mlkem.py"
Cohesion: 0.20
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 46 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 47 - "json"
Cohesion: 0.20
Nodes (3): _endpoint(), PublicKeyTransportError, _RejectRedirect

### Community 48 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 49 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 50 - "_Clock"
Cohesion: 0.22
Nodes (5): _Clock, _Cloud, cloud_url(), _stamp(), test_session_response_must_be_in_the_future_and_explicitly_zoned()

### Community 51 - "queries.py"
Cohesion: 0.33
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 53 - "_error_response"
Cohesion: 0.25
Nodes (8): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response(), _unavailable()

### Community 55 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 56 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 59 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 486 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `secure_transport.py`, `SessionManager`, `SecureTransport`, `SecureSession`, `test_dispatch.py`, `load_config`, `.__init__`, `edge_gateway/app.py`, `test_security_logging.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `create_app()` connect `cloud_service/app.py` to `_fixture`, `test_cloud_secure.py`, `FailureMode`, `test_cloud_queries.py`, `measure_baseline.py`, `MeasurementRepository`, `SessionManager`, `test_cloud_public_key.py`, `load_config`, `cloud_service/config.py`, `test_cloud_session_api.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `_fixture`, `test_cloud_secure.py`, `test_cloud_baseline.py`, `FailureMode`, `test_cloud_queries.py`, `measure_baseline.py`, `MeasurementRepository`, `cloud_service/app.py`, `test_cloud_public_key.py`, `cloud_service/config.py`, `test_cloud_session_api.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05570175438596491 - nodes in this community are weakly interconnected._