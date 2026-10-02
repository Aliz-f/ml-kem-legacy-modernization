# Graph Report - mlkem-pr33-fix

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2260 nodes · 5591 edges · 118 communities (80 shown, 38 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 783 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_device.py
- FailureMode
- test_gateway_cloud_secure.py
- SecureTransport
- LegacyMeasurement
- cli.py
- GatewayErrorCode
- pathlib
- test_gateway_crypto_image.py
- GatewayClient
- secure_transport.py
- MeasurementRepository
- load_config
- SessionManager
- test_public_key_client.py
- create_app
- derive_session_key
- measure_baseline.py
- create_app
- SecureTransportError
- SessionManager
- test_gateway_validation.py
- test_cloud_mlkem.py
- test_session.py
- test_cloud_secure.py
- cloud_service/app.py
- validate_measurement
- test_sensor.py
- CanonicalMeasurement
- edge_gateway/crypto/symmetric.py
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- edge_gateway/app.py
- test_mode_evaluation.py
- load_config
- test_crypto_failures.py
- encapsulate
- SecureEnvelope
- FailureInjector
- FailureMode
- CloudMetrics
- session_client.py
- test_dispatch.py
- test_cloud_baseline.py
- test_secure_shutdown.py
- test_secure_transport.py
- encode_binary
- StoredMeasurement
- build_aad
- test_cloud_failure_injection.py
- edge_gateway/crypto/encoding.py
- CryptoFailureInjector
- test_cloud_queries.py
- plaintext.py
- device.py
- test_baseline_client.py
- test_pqc_observability.py
- cloud_service/crypto/mlkem.py
- pytest
- BaselineCloudClient
- test_handshake_failure_stays_closed_without_a_session
- test_full_path_integration.py
- test_cloud_session_api.py
- edge_gateway/crypto/aad.py
- _Clock
- sessions.py
- test_cloud_public_key.py
- live_cloud
- test_gateway_response_mapping.py
- envelope_validation.py
- clean_container_crypto.py
- test_gateway_correlation.py
- test_secure_envelope.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- BaselineCloudError
- parse_public_key_response
- queries.py
- _HandshakeHandler
- test_dependency_review.py
- edge_gateway/crypto/envelope.py
- test_baseline_gateway_measurements
- Measurement
- json
- test_repository_hygiene.py
- StartupError
- cloud_service/crypto/aad.py
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- test_final_secure_transport_review.py
- _Handler
- _Handler
- KeyService
- public_key
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _DroppedResponse
- _Handler
- _Handler
- _Handler
- _Handler
- _Cloud
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 59 edges
2. `load_config()` - 56 edges
3. `load_config()` - 50 edges
4. `SecureTransport` - 49 edges
5. `create_app()` - 48 edges
6. `FailureMode` - 46 edges
7. `SessionManager` - 43 edges
8. `SecureTransportError` - 38 edges
9. `PqcMetrics` - 37 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `SessionEstablishmentError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/session.py

## Import Cycles
- None detected.

## Communities (118 total, 38 thin omitted)

### Community 0 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 1 - "FailureMode"
Cohesion: 0.07
Nodes (46): ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value(), FailureInjector (+38 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 3 - "SecureTransport"
Cohesion: 0.05
Nodes (20): lifespan(), _secure_transport(), _Duration, PqcMetrics, _endpoint(), SecureTransport, _Sessions, _Baseline (+12 more)

### Community 4 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (32): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+24 more)

### Community 5 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 6 - "GatewayErrorCode"
Cohesion: 0.07
Nodes (20): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed() (+12 more)

### Community 8 - "test_gateway_crypto_image.py"
Cohesion: 0.06
Nodes (18): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+10 more)

### Community 9 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 11 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 12 - "load_config"
Cohesion: 0.11
Nodes (27): _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config() (+19 more)

### Community 13 - "SessionManager"
Cohesion: 0.07
Nodes (6): SecureSession, SessionEstablishmentError, SessionManager, _session(), test_crypto_failure_is_classified_and_recorded(), fail_encapsulation()

### Community 14 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+11 more)

### Community 15 - "create_app"
Cohesion: 0.10
Nodes (23): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+15 more)

### Community 16 - "derive_session_key"
Cohesion: 0.08
Nodes (13): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+5 more)

### Community 17 - "measure_baseline.py"
Cohesion: 0.10
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 18 - "create_app"
Cohesion: 0.08
Nodes (21): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+13 more)

### Community 19 - "SecureTransportError"
Cohesion: 0.11
Nodes (12): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+4 more)

### Community 20 - "SessionManager"
Cohesion: 0.12
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 21 - "test_gateway_validation.py"
Cohesion: 0.12
Nodes (20): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client() (+12 more)

### Community 22 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (10): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent() (+2 more)

### Community 23 - "test_session.py"
Cohesion: 0.11
Nodes (15): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+7 more)

### Community 24 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (26): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+18 more)

### Community 25 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (9): _crypto_dependencies_ready(), SecurityMode, AeadError, decrypt(), _error(), _ingest(), _NoMetrics, secure_measurement() (+1 more)

### Community 26 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 27 - "test_sensor.py"
Cohesion: 0.11
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 28 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 29 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 30 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 31 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 32 - "edge_gateway/app.py"
Cohesion: 0.12
Nodes (6): _baseline_transport(), get_config(), GatewayConfig, BaselineTransport, CloudDispatch, DispatchMetrics

### Community 33 - "test_mode_evaluation.py"
Cohesion: 0.13
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 34 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 35 - "test_crypto_failures.py"
Cohesion: 0.12
Nodes (14): clock(), _aad(), _injector(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake() (+6 more)

### Community 36 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 37 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 38 - "FailureInjector"
Cohesion: 0.15
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 39 - "FailureMode"
Cohesion: 0.14
Nodes (9): FailureMode, FailureInjector, FailureSelection, test_drop_response_commits_then_same_envelope_retries_idempotently(), test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes() (+1 more)

### Community 40 - "CloudMetrics"
Cohesion: 0.11
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 41 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 42 - "test_dispatch.py"
Cohesion: 0.21
Nodes (12): _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline(), test_failure_log_omits_the_measurement() (+4 more)

### Community 43 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 44 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 45 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 46 - "encode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 47 - "StoredMeasurement"
Cohesion: 0.15
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 48 - "build_aad"
Cohesion: 0.20
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 49 - "test_cloud_failure_injection.py"
Cohesion: 0.24
Nodes (15): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_injected_session_failures_are_frozen_409s(), test_none_and_zero_rate_leave_secure_flow_unchanged() (+7 more)

### Community 50 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 52 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 53 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 54 - "device.py"
Cohesion: 0.20
Nodes (7): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero()

### Community 55 - "test_baseline_client.py"
Cohesion: 0.31
Nodes (13): _client(), _send(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request(), test_redirect_is_rejected_and_constructor_validates_inputs(), test_retry_count_must_be_a_non_negative_integer() (+5 more)

### Community 56 - "test_pqc_observability.py"
Cohesion: 0.19
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 57 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 58 - "pytest"
Cohesion: 0.18
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 59 - "BaselineCloudClient"
Cohesion: 0.19
Nodes (6): BaselineAcceptance, BaselineCloudClient, _dump(), _error_code(), _parse_acceptance(), baseline_headers()

### Community 60 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 61 - "test_full_path_integration.py"
Cohesion: 0.21
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 62 - "test_cloud_session_api.py"
Cohesion: 0.26
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 63 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 64 - "_Clock"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 65 - "sessions.py"
Cohesion: 0.32
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 66 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 67 - "live_cloud"
Cohesion: 0.21
Nodes (7): live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(), test_legacy_to_sqlite_preserves_gateway_transformations()

### Community 68 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 69 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 70 - "clean_container_crypto.py"
Cohesion: 0.25
Nodes (3): _install(), main(), _serve()

### Community 71 - "test_gateway_correlation.py"
Cohesion: 0.27
Nodes (5): create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 72 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 73 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 74 - "BaselineCloudError"
Cohesion: 0.20
Nodes (4): BaselineCloudError, _endpoint(), _RejectRedirect, post()

### Community 75 - "parse_public_key_response"
Cohesion: 0.33
Nodes (6): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 76 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 78 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 79 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.29
Nodes (4): main(), build_secure_envelope(), generate_nonce(), test_generate_nonce_returns_distinct_12_byte_values()

### Community 80 - "test_baseline_gateway_measurements"
Cohesion: 0.25
Nodes (4): cloud(), test_baseline_gateway_measurements(), _post(), send()

### Community 87 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 94 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 95 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 772 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app` to `edge_gateway/app.py`, `SecureTransport`, `LegacyMeasurement`, `live_cloud`, `GatewayErrorCode`, `test_gateway_response_mapping.py`, `load_config`, `test_gateway_validation.py`, `test_legacy_compatibility.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_gateway_cloud_secure.py`, `SecureTransport`, `secure_transport.py`, `test_public_key_client.py`, `derive_session_key`, `create_app`, `test_session.py`, `test_secure_message_tamper.py`, `edge_gateway/app.py`, `test_mode_evaluation.py`, `test_crypto_failures.py`, `encapsulate`, `session_client.py`, `CryptoFailureInjector`, `test_pqc_observability.py`, `test_handshake_failure_stays_closed_without_a_session`, `clean_container_crypto.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `secure_transport.py`, `SessionManager`, `create_app`, `SecureTransportError`, `edge_gateway/crypto/symmetric.py`, `edge_gateway/app.py`, `test_mode_evaluation.py`, `test_crypto_failures.py`, `test_dispatch.py`, `test_secure_shutdown.py`, `test_secure_transport.py`, `edge_gateway/crypto/encoding.py`, `CryptoFailureInjector`, `plaintext.py`, `test_pqc_observability.py`, `test_handshake_failure_stays_closed_without_a_session`, `edge_gateway/crypto/aad.py`, `clean_container_crypto.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.07237871674491393 - nodes in this community are weakly interconnected._