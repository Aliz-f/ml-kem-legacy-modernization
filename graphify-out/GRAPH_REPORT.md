# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2725 nodes · 6880 edges · 168 communities (108 shown, 60 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 947 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- GatewayClient
- cli.py
- test_session.py
- test_gateway_cloud_secure.py
- test_baseline_client.py
- CryptoFailureInjector
- test_security_logging.py
- secure_transport.py
- test_public_key_client.py
- load_config
- MeasurementRepository
- SecureTransport
- FailureMode
- test_crypto_failures.py
- test_secure_transport.py
- measure_modernized_e2e.py
- SessionManager
- create_app
- secure.py
- PqcMetrics
- validate_measurement
- test_dispatch.py
- test_sensor.py
- test_legacy_gateway.py
- test_cloud_secure.py
- edge_gateway/crypto/symmetric.py
- SessionManager
- test_device.py
- FailureMode
- CanonicalMeasurement
- create_app
- LegacyMeasurement
- legacy_system/config.py
- load_config
- test_cloud_session_api.py
- FailureInjector
- test_baseline_gateway_measurements
- encapsulate
- SecureEnvelope
- test_cloud_mlkem.py
- test_secure_message_tamper.py
- test_cloud_failure_injection.py
- session_client.py
- test_gateway_measurements.py
- StoredMeasurement
- edge_gateway/crypto/envelope.py
- CloudDispatch
- GatewayErrorCode
- measurements.py
- CanonicalMeasurement
- make_config
- test_legacy_compatibility.py
- sessions.py
- fields
- test_gateway_compose_e2e.py
- pytest
- Measurement
- test_cloud_baseline.py
- validate_legacy_measurement
- encode_binary
- test_cloud_queries.py
- edge_gateway/crypto/encoding.py
- DeviceController
- Config
- CloudMetrics
- derive_session_key
- test_gateway_validation.py
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- run
- parse_public_key_response
- errors.py
- test_gateway_routes.py
- test_gateway_correlation.py
- edge_gateway/crypto/aad.py
- GatewayError
- run
- test_pqc_observability.py
- test_session_expiry_system.py
- test_cloud_public_key.py
- edge_gateway/validation.py
- test_gateway_response_mapping.py
- test_static_checks.py
- test_gateway_crypto_image.py
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- envelope_validation.py
- test_clean_container_crypto.py
- test_gateway_application_failures.py
- test_gateway_application_metrics.py
- test_secure_envelope.py
- test_shutdown_after_gateway_unavailable_delivery
- refresh_graphify.py
- measure_modes
- test_gateway_transport_interface.py
- CloudDeliveryError
- queries.py
- _HandshakeHandler
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- test_gateway_cloud_secure_session.py
- test_gateway_operations.py
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- legacy_system/failure.py
- test_fixtures.py
- _Cloud
- cloud_service/crypto/kdf.py
- main
- FakeResponse
- test_session_reuse_system.py
- test_refresh_graphify.py
- test_repository_hygiene.py
- test_final_secure_transport_review.py
- _Handler
- _Handler
- _Sizes
- _Cloud
- live_cloud
- _Gateway
- test_legacy_mode_success_compatibility.py
- _Server
- test_shared_integration_assets.py
- public_key
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- test_crypto_failure_is_classified_and_recorded
- test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression
- edge_gateway/models.py
- TimedRepository
- test_gateway_crypto_ci.py
- test_lifespan_closes_baseline_and_rejects_late_requests
- _Baseline
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 86 edges
2. `load_config()` - 82 edges
3. `GatewayClient` - 56 edges
4. `SecureTransport` - 55 edges
5. `load_config()` - 51 edges
6. `FailureMode` - 49 edges
7. `create_app()` - 49 edges
8. `PqcMetrics` - 46 edges
9. `SessionManager` - 46 edges
10. `FailureMode` - 43 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `live_baseline_gateway()` --uses--> `GatewayClient`  [INFERRED]
  edge_gateway/tests/test_gateway_baseline_integration.py → legacy_system/src/legacy_system/client.py
- `test_baseline_gateway_measurements()` --uses--> `GatewayClient`  [INFERRED]
  edge_gateway/tests/test_gateway_baseline_integration.py → legacy_system/src/legacy_system/client.py

## Import Cycles
- None detected.

## Communities (168 total, 60 thin omitted)

### Community 0 - "GatewayClient"
Cohesion: 0.05
Nodes (34): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener (+26 more)

### Community 1 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 2 - "test_session.py"
Cohesion: 0.05
Nodes (26): SessionState, _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+18 more)

### Community 3 - "test_gateway_cloud_secure.py"
Cohesion: 0.06
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 4 - "test_baseline_client.py"
Cohesion: 0.08
Nodes (29): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+21 more)

### Community 5 - "CryptoFailureInjector"
Cohesion: 0.05
Nodes (14): _baseline_transport(), get_config(), _secure_transport(), GatewayConfig, CryptoFailureInjector, ApplicationFailures, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline() (+6 more)

### Community 6 - "test_security_logging.py"
Cohesion: 0.06
Nodes (18): _Sessions, SecureSession, _Sessions, _Baseline, _Clock, _Cloud, cloud_url(), _measurement() (+10 more)

### Community 8 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (20): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+12 more)

### Community 9 - "load_config"
Cohesion: 0.10
Nodes (27): _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer() (+19 more)

### Community 10 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 11 - "SecureTransport"
Cohesion: 0.10
Nodes (10): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+2 more)

### Community 12 - "FailureMode"
Cohesion: 0.17
Nodes (26): FailureMode, FailureInjector, make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+18 more)

### Community 13 - "test_crypto_failures.py"
Cohesion: 0.09
Nodes (19): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud (+11 more)

### Community 14 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 15 - "measure_modernized_e2e.py"
Cohesion: 0.10
Nodes (8): _load(), run(), distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve()

### Community 16 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 18 - "create_app"
Cohesion: 0.08
Nodes (19): create_app(), lifespan(), main(), StartupError, test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start() (+11 more)

### Community 19 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 20 - "PqcMetrics"
Cohesion: 0.07
Nodes (6): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__()

### Community 22 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 23 - "test_dispatch.py"
Cohesion: 0.14
Nodes (13): _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 24 - "test_sensor.py"
Cohesion: 0.11
Nodes (18): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 25 - "test_legacy_gateway.py"
Cohesion: 0.15
Nodes (15): AcceptedBaseline, FailingBaseline, fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry() (+7 more)

### Community 26 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 27 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 28 - "SessionManager"
Cohesion: 0.11
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 29 - "test_device.py"
Cohesion: 0.10
Nodes (11): FakeMeasurement, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, RecordingClient, RecordingFailureInjector, test_delivery_failure_does_not_stop_loop_or_roll_back_sequence() (+3 more)

### Community 30 - "FailureMode"
Cohesion: 0.12
Nodes (10): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates() (+2 more)

### Community 31 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 32 - "create_app"
Cohesion: 0.11
Nodes (19): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements() (+11 more)

### Community 33 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 34 - "legacy_system/config.py"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 35 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 36 - "test_cloud_session_api.py"
Cohesion: 0.12
Nodes (13): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+5 more)

### Community 37 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 38 - "test_baseline_gateway_measurements"
Cohesion: 0.09
Nodes (14): cloud(), test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), sleep(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_preserves_fields_correlation_and_persistence() (+6 more)

### Community 39 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 40 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 41 - "test_cloud_mlkem.py"
Cohesion: 0.10
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 42 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 43 - "test_cloud_failure_injection.py"
Cohesion: 0.20
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 44 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 45 - "test_gateway_measurements.py"
Cohesion: 0.16
Nodes (14): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline() (+6 more)

### Community 46 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 47 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.17
Nodes (11): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement() (+3 more)

### Community 48 - "CloudDispatch"
Cohesion: 0.12
Nodes (4): BaselineTransport, CloudDispatch, DispatchMetrics, _dispatch()

### Community 49 - "GatewayErrorCode"
Cohesion: 0.14
Nodes (11): GatewayErrorCode, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap(), test_gap_is_logged_and_advances_state() (+3 more)

### Community 50 - "measurements.py"
Cohesion: 0.14
Nodes (3): MeasurementProcessor, GatewayMetrics, SequenceTracker

### Community 51 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 52 - "make_config"
Cohesion: 0.16
Nodes (13): FakeSensor, make_config(), RaisingClient, test_client_exception_is_logged_then_loop_continues_and_closes(), test_controller_run_in_background_thread_skips_signal_handling(), test_default_device_controller_initialization(), test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible() (+5 more)

### Community 53 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 54 - "sessions.py"
Cohesion: 0.16
Nodes (11): health(), ready(), _crypto_dependencies_ready(), _unavailable(), SecurityMode, derive_session_key(), _decode_ciphertext(), _error() (+3 more)

### Community 55 - "fields"
Cohesion: 0.19
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 56 - "test_gateway_compose_e2e.py"
Cohesion: 0.23
Nodes (13): _compose(), _measurement(), _metrics(), _port(), _send(), test_compose_cloud_restart_recovers_readiness_and_delivery(), test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback(), test_compose_gateway_restart_establishes_a_fresh_mlkem_session() (+5 more)

### Community 57 - "pytest"
Cohesion: 0.12
Nodes (3): test_harness_rejects_invalid_sample_count(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads()

### Community 58 - "Measurement"
Cohesion: 0.13
Nodes (7): Measurement, _validate_number(), query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(), test_legacy_controller_continues_after_bounded_cloud_delivery_failure(), read()

### Community 59 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 60 - "validate_legacy_measurement"
Cohesion: 0.16
Nodes (7): normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_legacy_values_survive_secure_delivery()

### Community 61 - "encode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 62 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 63 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 65 - "Config"
Cohesion: 0.19
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 66 - "CloudMetrics"
Cohesion: 0.15
Nodes (3): CloudMetrics, _labels(), _render_labels()

### Community 67 - "derive_session_key"
Cohesion: 0.20
Nodes (8): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 68 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 69 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 70 - "test_cloud_kdf.py"
Cohesion: 0.16
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 71 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 72 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 73 - "errors.py"
Cohesion: 0.18
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 74 - "test_gateway_routes.py"
Cohesion: 0.24
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 75 - "test_gateway_correlation.py"
Cohesion: 0.23
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 76 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 78 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 79 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 80 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 81 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 82 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 83 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 84 - "test_static_checks.py"
Cohesion: 0.26
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 85 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 86 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.17
Nodes (3): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 87 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 88 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 89 - "test_clean_container_crypto.py"
Cohesion: 0.18
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 90 - "test_gateway_application_failures.py"
Cohesion: 0.25
Nodes (6): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 91 - "test_gateway_application_metrics.py"
Cohesion: 0.25
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 92 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 93 - "test_shutdown_after_gateway_unavailable_delivery"
Cohesion: 0.22
Nodes (4): test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown(), fake_signal()

### Community 94 - "refresh_graphify.py"
Cohesion: 0.27
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 95 - "measure_modes"
Cohesion: 0.25
Nodes (6): _Calls, measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 97 - "test_gateway_transport_interface.py"
Cohesion: 0.29
Nodes (4): _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 99 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 101 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.28
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 102 - "test_gateway_cloud_secure_session.py"
Cohesion: 0.28
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 103 - "test_gateway_operations.py"
Cohesion: 0.32
Nodes (3): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 104 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 105 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 107 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 111 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 113 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 114 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 116 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 123 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 125 - "test_legacy_mode_success_compatibility.py"
Cohesion: 0.53
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 132 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 134 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

### Community 138 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.40
Nodes (3): test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 962 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **60 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FailureMode` connect `FailureMode` to `GatewayClient`, `public_key`, `load_config`, `test_gateway_cloud_secure.py`, `test_cloud_failure_injection.py`, `secure.py`, `pathlib`, `sessions.py`, `validate_measurement`, `Measurement`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_session.py`, `test_gateway_cloud_secure.py`, `CryptoFailureInjector`, `test_security_logging.py`, `secure_transport.py`, `test_crypto_failures.py`, `test_secure_transport.py`, `edge_gateway/app.py`, `PqcMetrics`, `test_dispatch.py`, `test_legacy_gateway.py`, `edge_gateway/crypto/symmetric.py`, `SessionManager`, `create_app`, `edge_gateway/crypto/envelope.py`, `CloudDispatch`, `measurements.py`, `edge_gateway/crypto/encoding.py`, `edge_gateway/crypto/aad.py`, `test_pqc_observability.py`, `test_session_expiry_system.py`, `test_gateway_application_failures.py`, `main`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `BaselineCloudClient` connect `test_baseline_client.py` to `CryptoFailureInjector`, `test_baseline_gateway_measurements`, `edge_gateway/app.py`, `measurements.py`, `test_gateway_application_failures.py`, `live_cloud`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GatewayClient` be split into smaller, more focused modules?**
  _Cohesion score 0.05046948356807512 - nodes in this community are weakly interconnected._