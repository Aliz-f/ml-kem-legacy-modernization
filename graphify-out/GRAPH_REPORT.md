# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2184 nodes · 5405 edges · 118 communities (79 shown, 39 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 758 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- test_gateway_cloud_secure.py
- cli.py
- GatewayClient
- edge_gateway/app.py
- pytest
- test_crypto_failures.py
- test_baseline_client.py
- cloud_service/app.py
- PqcMetrics
- secure_transport.py
- GatewayErrorCode
- MeasurementRepository
- test_sensor.py
- create_app
- SecureTransportError
- pathlib
- load_config
- test_cloud_secure.py
- edge_gateway/crypto/symmetric.py
- FailureMode
- CanonicalMeasurement
- test_legacy_compatibility.py
- SessionManager
- LegacyMeasurement
- test_mode_evaluation.py
- test_public_key_client.py
- test_session.py
- measure_baseline.py
- test_dispatch.py
- SecureEnvelope
- test_cloud_failure_injection.py
- StoredMeasurement
- load_config
- SessionManager
- validate_measurement
- CloudMetrics
- test_cloud_baseline.py
- session_client.py
- CanonicalMeasurement
- encode_binary
- derive_session_key
- test_gateway_measurements.py
- test_secure_transport.py
- ConfigurationError
- edge_gateway/crypto/envelope.py
- build_aad
- _Sessions
- fields
- test_cloud_queries.py
- edge_gateway/crypto/encoding.py
- edge_gateway/models.py
- test_gateway_validation.py
- test_secure_message_tamper.py
- test_cloud_mlkem.py
- test_cloud_kdf.py
- edge_gateway/validation.py
- SecureSession
- test_pqc_observability.py
- cloud_service/crypto/mlkem.py
- test_cloud_session_api.py
- test_gateway_correlation.py
- public_key.py
- test_handshake_failure_stays_closed_without_a_session
- encapsulate
- KeyService
- test_cloud_public_key.py
- test_gateway_errors.py
- envelope_validation.py
- clean_container_crypto.py
- MlKemError
- CloudDispatch
- test_secure_envelope.py
- _receive
- _Clock
- _ingest
- edge_gateway/crypto/mlkem.py
- test_dependency_review.py
- _DroppedResponse
- SessionState
- _Cloud
- SessionAccessError
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- get_measurement
- test_fetch_does_not_encapsulate
- _Handler
- _Handler
- test_shared_integration_assets.py
- public_key
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- _Handler
- _Handler
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 53 edges
2. `load_config()` - 50 edges
3. `SecureTransport` - 49 edges
4. `create_app()` - 48 edges
5. `load_config()` - 48 edges
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
- `test_corrupted_ciphertext_is_rejected_and_not_stored()` --uses--> `PqcMetrics`  [INFERRED]
  tests/integration/test_corrupt_ciphertext_demo.py → edge_gateway/src/edge_gateway/crypto/metrics.py

## Import Cycles
- None detected.

## Communities (118 total, 39 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 3 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 4 - "GatewayClient"
Cohesion: 0.07
Nodes (24): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener (+16 more)

### Community 5 - "edge_gateway/app.py"
Cohesion: 0.06
Nodes (14): _baseline_transport(), get_config(), _logging_level(), main(), _secure_transport(), GatewayConfig, CryptoFailureInjector, _endpoint() (+6 more)

### Community 6 - "pytest"
Cohesion: 0.06
Nodes (16): test_harness_rejects_invalid_sample_count(), clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install() (+8 more)

### Community 7 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 8 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (24): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+16 more)

### Community 9 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (13): health(), ready(), _crypto_dependencies_ready(), _unavailable(), SecurityMode, derive_session_key(), AeadError, decrypt() (+5 more)

### Community 10 - "PqcMetrics"
Cohesion: 0.06
Nodes (14): _Duration, PqcMetrics, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+6 more)

### Community 12 - "GatewayErrorCode"
Cohesion: 0.10
Nodes (15): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once() (+7 more)

### Community 13 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 14 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 15 - "create_app"
Cohesion: 0.08
Nodes (22): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), ready() (+14 more)

### Community 16 - "SecureTransportError"
Cohesion: 0.11
Nodes (12): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+4 more)

### Community 18 - "load_config"
Cohesion: 0.12
Nodes (19): create_app(), main(), load_config(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage() (+11 more)

### Community 19 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (26): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+18 more)

### Community 20 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 21 - "FailureMode"
Cohesion: 0.12
Nodes (8): Config, FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes()

### Community 22 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 23 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 24 - "SessionManager"
Cohesion: 0.14
Nodes (10): SecureSession, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed() (+2 more)

### Community 25 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 26 - "test_mode_evaluation.py"
Cohesion: 0.13
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 27 - "test_public_key_client.py"
Cohesion: 0.14
Nodes (12): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, PublicKeyRejected, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable(), test_http_status_is_classified() (+4 more)

### Community 28 - "test_session.py"
Cohesion: 0.13
Nodes (13): _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+5 more)

### Community 29 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 30 - "test_dispatch.py"
Cohesion: 0.18
Nodes (13): _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 31 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 32 - "test_cloud_failure_injection.py"
Cohesion: 0.19
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 33 - "StoredMeasurement"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 34 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 36 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 37 - "CloudMetrics"
Cohesion: 0.11
Nodes (6): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_injected_fault_is_counted_only_when_its_boundary_applies(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 38 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 39 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 40 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 41 - "encode_binary"
Cohesion: 0.18
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet(), test_published_public_key_round_trip_and_handshake()

### Community 42 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 43 - "test_gateway_measurements.py"
Cohesion: 0.17
Nodes (12): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook() (+4 more)

### Community 44 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 45 - "ConfigurationError"
Cohesion: 0.16
Nodes (14): ConfigurationError, integer(), number(), text(), value(), test_custom_environment(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values() (+6 more)

### Community 46 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.19
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 47 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 48 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 49 - "fields"
Cohesion: 0.22
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 50 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 51 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 52 - "edge_gateway/models.py"
Cohesion: 0.17
Nodes (5): _timestamp(), normalize(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 53 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 54 - "test_secure_message_tamper.py"
Cohesion: 0.24
Nodes (9): _envelope(), _establish(), _reject(), test_authentic_envelope_is_stored_once(), test_gateway_002_cannot_use_the_session_owned_by_gateway_001(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key(), test_session_a_ciphertext_is_rejected_when_the_envelope_claims_session_b() (+1 more)

### Community 55 - "test_cloud_mlkem.py"
Cohesion: 0.15
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 56 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 57 - "edge_gateway/validation.py"
Cohesion: 0.16
Nodes (8): measurements(), LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), canonical(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 58 - "SecureSession"
Cohesion: 0.15
Nodes (4): _Sessions, SecureSession, _session(), get_or_establish()

### Community 59 - "test_pqc_observability.py"
Cohesion: 0.19
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 60 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 61 - "test_cloud_session_api.py"
Cohesion: 0.23
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 62 - "test_gateway_correlation.py"
Cohesion: 0.21
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 63 - "public_key.py"
Cohesion: 0.23
Nodes (7): CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 64 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 65 - "encapsulate"
Cohesion: 0.26
Nodes (8): encapsulate(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged(), test_valid_public_key_round_trip_matches_decapsulation(), test_wrong_type_is_rejected()

### Community 66 - "KeyService"
Cohesion: 0.17
Nodes (4): lifespan(), StartupError, KeyService, test_session_initialization_failure_releases_keys()

### Community 67 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 68 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 69 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 70 - "clean_container_crypto.py"
Cohesion: 0.25
Nodes (3): _install(), main(), _serve()

### Community 71 - "MlKemError"
Cohesion: 0.22
Nodes (5): KdfError, MlKemError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 73 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 74 - "_receive"
Cohesion: 0.22
Nodes (4): DecryptSpy, _receive(), _require_envelope(), SecureRejection

### Community 75 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 76 - "_ingest"
Cohesion: 0.31
Nodes (4): _error(), _ingest(), _NoMetrics, secure_measurement()

### Community 78 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 79 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 85 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 86 - "test_fetch_does_not_encapsulate"
Cohesion: 0.40
Nodes (4): _body(), _public_key(), test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key()

### Community 95 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 97 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 748 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `edge_gateway/app.py` to `test_gateway_cloud_secure.py`, `test_crypto_failures.py`, `PqcMetrics`, `secure_transport.py`, `create_app`, `SecureTransportError`, `edge_gateway/crypto/symmetric.py`, `test_mode_evaluation.py`, `test_dispatch.py`, `SessionManager`, `test_secure_transport.py`, `edge_gateway/crypto/envelope.py`, `build_aad`, `_Sessions`, `edge_gateway/crypto/encoding.py`, `SecureSession`, `test_pqc_observability.py`, `test_handshake_failure_stays_closed_without_a_session`, `clean_container_crypto.py`, `CloudDispatch`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_handshake_failure_stays_closed_without_a_session`, `test_gateway_cloud_secure.py`, `test_mode_evaluation.py`, `edge_gateway/app.py`, `clean_container_crypto.py`, `MlKemError`, `session_client.py`, `test_crypto_failures.py`, `PqcMetrics`, `secure_transport.py`, `test_pqc_observability.py`, `load_config`, `test_secure_message_tamper.py`, `SecureSession`, `test_public_key_client.py`, `test_session.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `load_config`, `edge_gateway/app.py`, `CloudDispatch`, `PqcMetrics`, `test_gateway_measurements.py`, `GatewayErrorCode`, `test_gateway_validation.py`, `test_legacy_compatibility.py`, `edge_gateway/validation.py`, `LegacyMeasurement`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `SecureTransport` (e.g. with `main()` and `create_app()`) actually correct?**
  _`SecureTransport` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.05720122574055159 - nodes in this community are weakly interconnected._