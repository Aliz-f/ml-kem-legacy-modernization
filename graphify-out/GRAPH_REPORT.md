# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1538 nodes · 3776 edges · 81 communities (59 shown, 22 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 519 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- decrypt
- FailureMode
- LegacyMeasurement
- test_client.py
- test_public_key_client.py
- test_sensor.py
- SessionManager
- MeasurementRepository
- SecureTransport
- secure_transport.py
- test_cloud_secure.py
- test_session.py
- SecureSession
- test_failure_injection.py
- load_config
- CryptoFailureInjector
- test_secure_transport.py
- measure_baseline.py
- cloud_service/app.py
- load_config
- PqcMetrics
- SessionManager
- create_app
- secure.py
- envelope_validation.py
- CanonicalMeasurement
- repository.py
- _fixture
- GatewayErrorCode
- session_client.py
- test_dispatch.py
- edge_gateway/app.py
- validate_measurement
- edge_gateway/crypto/encoding.py
- decode_binary
- test_cloud_baseline.py
- CloudDispatch
- encapsulate
- plaintext.py
- test_cloud_kdf.py
- keys.py
- test_cloud_mlkem.py
- edge_gateway/config.py
- test_cloud_public_key.py
- test_cloud_queries.py
- test_cloud_session_api.py
- edge_gateway/crypto/mlkem.py
- pytest
- test_gateway_validation.py
- refresh_graphify.py
- MlKemError
- test_cloud_envelope.py
- derive_session_key
- .__init__
- cloud_service/crypto/kdf.py
- _error_response
- _HandshakeHandler
- _Clock
- KdfError
- get_measurement
- establish_session
- test_gateway_config.py
- _Handler
- _Handler
- public_key
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 43 edges
2. `SecureTransport` - 36 edges
3. `create_app()` - 36 edges
4. `load_config()` - 35 edges
5. `create_app()` - 34 edges
6. `FailureMode` - 33 edges
7. `PqcMetrics` - 32 edges
8. `MeasurementRepository` - 32 edges
9. `FailureInjector` - 31 edges
10. `SessionManager` - 31 edges

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

## Communities (81 total, 22 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (42): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+34 more)

### Community 1 - "decrypt"
Cohesion: 0.06
Nodes (49): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+41 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "LegacyMeasurement"
Cohesion: 0.08
Nodes (30): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+22 more)

### Community 4 - "test_client.py"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "test_public_key_client.py"
Cohesion: 0.08
Nodes (22): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+14 more)

### Community 6 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 7 - "SessionManager"
Cohesion: 0.10
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.12
Nodes (22): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+14 more)

### Community 9 - "SecureTransport"
Cohesion: 0.13
Nodes (9): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport (+1 more)

### Community 11 - "test_cloud_secure.py"
Cohesion: 0.16
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 12 - "test_session.py"
Cohesion: 0.11
Nodes (12): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+4 more)

### Community 13 - "SecureSession"
Cohesion: 0.09
Nodes (13): SecureSession, _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+5 more)

### Community 14 - "test_failure_injection.py"
Cohesion: 0.11
Nodes (14): _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud, _plaintext() (+6 more)

### Community 15 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+9 more)

### Community 16 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (5): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), test_same_seed_makes_the_same_decisions()

### Community 17 - "test_secure_transport.py"
Cohesion: 0.20
Nodes (17): _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable() (+9 more)

### Community 18 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 19 - "cloud_service/app.py"
Cohesion: 0.18
Nodes (3): SecurityMode, baseline_measurement(), _error()

### Community 20 - "load_config"
Cohesion: 0.16
Nodes (14): create_app(), _logging_level(), main(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health() (+6 more)

### Community 22 - "SessionManager"
Cohesion: 0.13
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 23 - "create_app"
Cohesion: 0.12
Nodes (15): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+7 more)

### Community 24 - "secure.py"
Cohesion: 0.14
Nodes (8): AadError, build_aad(), AeadError, decrypt(), _error(), _ingest(), secure_measurement(), fail()

### Community 25 - "envelope_validation.py"
Cohesion: 0.13
Nodes (8): EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 26 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 27 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 28 - "_fixture"
Cohesion: 0.09
Nodes (18): payload(), payload(), client(), measurement(), client(), clock(), database(), measurement() (+10 more)

### Community 29 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 30 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 31 - "test_dispatch.py"
Cohesion: 0.21
Nodes (12): _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline(), test_failure_log_omits_the_measurement() (+4 more)

### Community 32 - "edge_gateway/app.py"
Cohesion: 0.14
Nodes (9): measurements(), get_config(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage() (+1 more)

### Community 33 - "validate_measurement"
Cohesion: 0.21
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 34 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.17
Nodes (7): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 35 - "decode_binary"
Cohesion: 0.20
Nodes (8): decode_binary(), encode_binary(), EncodingError, _decode_ciphertext(), test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 36 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (9): client(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500() (+1 more)

### Community 37 - "CloudDispatch"
Cohesion: 0.14
Nodes (4): GatewayConfig, BaselineTransport, CloudDispatch, DispatchMetrics

### Community 38 - "encapsulate"
Cohesion: 0.19
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 39 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 40 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 41 - "keys.py"
Cohesion: 0.13
Nodes (5): lifespan(), StartupError, KeyService, fail(), test_session_initialization_failure_releases_keys()

### Community 42 - "test_cloud_mlkem.py"
Cohesion: 0.15
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 43 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 44 - "test_cloud_public_key.py"
Cohesion: 0.22
Nodes (9): secure_app(), test_classical_does_not_generate_keys(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized() (+1 more)

### Community 45 - "test_cloud_queries.py"
Cohesion: 0.19
Nodes (8): test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503(), test_safe_query_errors()

### Community 46 - "test_cloud_session_api.py"
Cohesion: 0.25
Nodes (9): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), test_shutdown_and_classical_mode() (+1 more)

### Community 47 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.23
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 48 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 49 - "test_gateway_validation.py"
Cohesion: 0.33
Nodes (10): assert_rejection(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422(), test_parsed_non_measurements_are_422() (+2 more)

### Community 50 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 51 - "MlKemError"
Cohesion: 0.18
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 52 - "test_cloud_envelope.py"
Cohesion: 0.33
Nodes (8): payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation(), test_nonobjects_rejected(), test_wrong_types_rejected_for_parsing_and_direct_construction()

### Community 53 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 54 - ".__init__"
Cohesion: 0.18
Nodes (3): _endpoint(), _SessionRecovery, _Sessions

### Community 56 - "_error_response"
Cohesion: 0.25
Nodes (8): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response(), _unavailable()

### Community 58 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 59 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 60 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 61 - "establish_session"
Cohesion: 0.67
Nodes (4): _error(), _establish(), establish_session(), session_access_error_handler()

### Community 62 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 478 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `edge_gateway/app.py`, `CloudDispatch`, `SecureTransport`, `secure_transport.py`, `SecureSession`, `CryptoFailureInjector`, `load_config`, `.__init__`, `SessionManager`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `test_injected_handshake_failure_leaves_no_session_and_skips_baseline()` connect `CryptoFailureInjector` to `CloudDispatch`, `SecureTransport`, `test_failure_injection.py`, `load_config`, `SessionManager`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_public_key_client.py`, `encapsulate`, `secure_transport.py`, `test_session.py`, `SecureSession`, `test_failure_injection.py`, `CryptoFailureInjector`, `PqcMetrics`, `create_app`, `KdfError`, `_fixture`, `session_client.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.060424469413233456 - nodes in this community are weakly interconnected._