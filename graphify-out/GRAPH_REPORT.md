# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1609 nodes · 4001 edges · 76 communities (51 shown, 25 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 579 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- json
- FailureMode
- test_cloud_secure.py
- LegacyMeasurement
- test_session.py
- test_client.py
- GatewayErrorCode
- test_failure_injection.py
- measure_baseline.py
- test_sensor.py
- derive_session_key
- SecureTransport
- cloud_service/app.py
- MeasurementRepository
- load_config
- test_public_key_client.py
- create_app
- SecureSession
- secure_transport.py
- PqcMetrics
- test_dispatch.py
- test_secure_transport.py
- FailureMode
- CanonicalMeasurement
- SessionManager
- SecureEnvelope
- load_config
- repository.py
- test_cloud_failure_injection.py
- encapsulate
- validate_measurement
- test_cloud_session_api.py
- CryptoFailureInjector
- edge_gateway/app.py
- decode_binary
- test_cloud_baseline.py
- cloud_service/crypto/mlkem.py
- secure.py
- test_cloud_kdf.py
- test_cloud_queries.py
- parse_public_key_response
- test_gateway_validation.py
- _fixture
- edge_gateway/crypto/encoding.py
- test_cloud_mlkem.py
- test_cloud_config.py
- test_cloud_public_key.py
- envelope_validation.py
- sessions.py
- keys.py
- .__init__
- GatewayConfig
- pytest
- test_refresh_graphify.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- _Handler
- _unavailable
- _DroppedResponse
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

## Communities (76 total, 25 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (44): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), main(), parser(), record_work(), recorded_changes() (+36 more)

### Community 1 - "json"
Cohesion: 0.05
Nodes (50): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+42 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "test_cloud_secure.py"
Cohesion: 0.06
Nodes (36): SecureSession, SessionAccessError, SessionManager, SessionState, canonical(), envelope(), establish(), forbid() (+28 more)

### Community 4 - "LegacyMeasurement"
Cohesion: 0.08
Nodes (30): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+22 more)

### Community 5 - "test_session.py"
Cohesion: 0.06
Nodes (23): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+15 more)

### Community 6 - "test_client.py"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 7 - "GatewayErrorCode"
Cohesion: 0.08
Nodes (19): GatewayError, GatewayErrorCode, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized() (+11 more)

### Community 8 - "test_failure_injection.py"
Cohesion: 0.07
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 9 - "measure_baseline.py"
Cohesion: 0.08
Nodes (19): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+11 more)

### Community 10 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 11 - "derive_session_key"
Cohesion: 0.08
Nodes (15): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+7 more)

### Community 12 - "SecureTransport"
Cohesion: 0.11
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 13 - "cloud_service/app.py"
Cohesion: 0.11
Nodes (8): SecurityMode, public_key(), _unavailable(), _error(), get_measurement(), list_measurements(), baseline_measurement(), _error()

### Community 14 - "MeasurementRepository"
Cohesion: 0.12
Nodes (22): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+14 more)

### Community 15 - "load_config"
Cohesion: 0.13
Nodes (21): create_app(), main(), ConfigurationError, load_config(), integer(), number(), text(), value() (+13 more)

### Community 16 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (17): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, _body(), cloud_server(), _public_key(), _Response (+9 more)

### Community 17 - "create_app"
Cohesion: 0.11
Nodes (21): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+13 more)

### Community 18 - "SecureSession"
Cohesion: 0.10
Nodes (12): _Sessions, SecureSession, _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 20 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 21 - "test_dispatch.py"
Cohesion: 0.17
Nodes (13): CloudDispatch, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 22 - "test_secure_transport.py"
Cohesion: 0.20
Nodes (18): _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable() (+10 more)

### Community 23 - "FailureMode"
Cohesion: 0.13
Nodes (8): Config, FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes()

### Community 24 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 25 - "SessionManager"
Cohesion: 0.13
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 26 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 27 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 28 - "repository.py"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 29 - "test_cloud_failure_injection.py"
Cohesion: 0.20
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 30 - "encapsulate"
Cohesion: 0.16
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 31 - "validate_measurement"
Cohesion: 0.19
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 32 - "test_cloud_session_api.py"
Cohesion: 0.15
Nodes (11): lifespan(), StartupError, handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+3 more)

### Community 34 - "edge_gateway/app.py"
Cohesion: 0.17
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 35 - "decode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 36 - "test_cloud_baseline.py"
Cohesion: 0.14
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 37 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 38 - "secure.py"
Cohesion: 0.21
Nodes (6): AeadError, decrypt(), _error(), _ingest(), secure_measurement(), fail()

### Community 39 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 40 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 41 - "parse_public_key_response"
Cohesion: 0.21
Nodes (8): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 42 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), client(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 43 - "_fixture"
Cohesion: 0.14
Nodes (13): client(), payload(), payload(), client(), database(), measurement(), payload(), cloud() (+5 more)

### Community 44 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.24
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 45 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 46 - "test_cloud_config.py"
Cohesion: 0.24
Nodes (9): test_custom_environment(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries(), test_invalid_configuration(), test_invalid_database_url(), test_process_environment_and_explicit_mapping(), test_sqlite_paths() (+1 more)

### Community 47 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 48 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 49 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 52 - "GatewayConfig"
Cohesion: 0.25
Nodes (3): get_config(), GatewayConfig, test_from_config_uses_gateway_failure_settings()

### Community 54 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 58 - "_unavailable"
Cohesion: 0.50
Nodes (3): health(), ready(), _unavailable()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 498 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `CryptoFailureInjector`, `edge_gateway/app.py`, `SecureTransport`, `create_app`, `SecureSession`, `secure_transport.py`, `.__init__`, `test_dispatch.py`, `SessionManager`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `FailureMode` connect `FailureMode` to `secure.py`, `cloud_service/app.py`, `test_cloud_config.py`, `load_config`, `sessions.py`, `test_cloud_failure_injection.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `test_failure_injection.py`, `SecureTransport`, `SecureSession`, `secure_transport.py`, `GatewayConfig`, `SessionManager`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05570175438596491 - nodes in this community are weakly interconnected._