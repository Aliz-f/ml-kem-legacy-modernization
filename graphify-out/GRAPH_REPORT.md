# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2683 nodes · 6780 edges · 165 communities (109 shown, 56 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 935 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_device.py
- cli.py
- test_gateway_cloud_secure.py
- test_sensor.py
- test_baseline_client.py
- test_gateway_compose_e2e.py
- cloud_service/app.py
- test_crypto_failures.py
- MeasurementRepository
- derive_session_key
- edge_gateway/app.py
- test_session.py
- FailureMode
- SessionManager
- test_secure_transport.py
- create_app
- edge_gateway/crypto/symmetric.py
- SecureTransport
- PqcMetrics
- test_cloud_secure.py
- create_app
- test_dispatch.py
- GatewayError
- test_public_key_client.py
- FailureMode
- SessionManager
- CanonicalMeasurement
- LegacyMeasurement
- legacy_system/config.py
- test_legacy_compatibility.py
- encode_binary
- test_measure_modernized_e2e.py
- test_secure_message_tamper.py
- test_cloud_failure_injection.py
- test_session_recovery_is_counted
- GatewayClient
- SecureEnvelope
- CryptoFailureInjector
- test_baseline_gateway_measurements
- live_gateway
- load_config
- validate_measurement
- encapsulate
- log_application
- load_config
- session_client.py
- test_gateway_measurements.py
- CloudMetrics
- StoredMeasurement
- fields
- test_cloud_baseline.py
- GatewayConfig
- edge_gateway/crypto/envelope.py
- measurements.py
- CanonicalMeasurement
- test_secure_shutdown.py
- test_gateway_transport_interface.py
- public_key.py
- cloud_service/crypto/mlkem.py
- CloudDispatch
- test_mode_evaluation.py
- test_cloud_kdf.py
- edge_gateway/config.py
- Config
- Measurement
- edge_gateway/crypto/encoding.py
- validate_legacy_measurement
- test_gateway_validation.py
- run
- pytest
- test_cloud_queries.py
- run
- test_handshake_failure_stays_closed_without_a_session
- edge_gateway/crypto/mlkem.py
- edge_gateway/crypto/aad.py
- test_gateway_routes.py
- _Handler
- run
- test_session_expiry_system.py
- test_cloud_public_key.py
- edge_gateway/validation.py
- test_gateway_application_metrics.py
- test_gateway_errors.py
- test_gateway_response_mapping.py
- ErrorCategory
- envelope_validation.py
- handshake
- test_gateway_application_failures.py
- test_secure_envelope.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_protocol_version_999_is_rejected_before_secure_processing
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- _ingest
- _HandshakeHandler
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- test_gateway_cloud_secure_session.py
- _DroppedResponse
- test_gateway_correlation.py
- test_body_limit_before_sequence_and_delivery
- _Server
- test_handshake_counter_shows_reuse_then_expiry
- StartupError
- cloud_service/crypto/kdf.py
- main
- test_gateway_operations.py
- .send
- LiveCloud
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_session_reuse_system.py
- test_repository_hygiene.py
- get_measurement
- test_final_secure_transport_review.py
- _Handler
- .apply
- _Sizes
- test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row
- live_cloud
- test_legacy_mode_success_compatibility.py
- test_shared_integration_assets.py
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- test_sequence_state_timing_awareness_no_rollback_on_downstream_failure
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- edge_gateway/models.py
- test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression
- test_gateway_crypto_ci.py
- test_lifespan_closes_baseline_and_rejects_late_requests
- test_theoretical_retry_amplification_product_is_explicit_and_bounded
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 86 edges
2. `load_config()` - 82 edges
3. `SecureTransport` - 55 edges
4. `GatewayClient` - 51 edges
5. `load_config()` - 51 edges
6. `create_app()` - 49 edges
7. `FailureMode` - 47 edges
8. `SessionManager` - 46 edges
9. `PqcMetrics` - 46 edges
10. `FailureMode` - 42 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression()` --uses--> `DeviceController`  [INFERRED]
  tests/integration/test_legacy_gateway.py → legacy_system/src/legacy_system/device.py
- `test_valid_encapsulation_matches_shared_secret_and_hkdf()` --uses--> `SessionState`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/session.py

## Import Cycles
- None detected.

## Communities (165 total, 56 thin omitted)

### Community 0 - "test_device.py"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 1 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 3 - "test_sensor.py"
Cohesion: 0.06
Nodes (30): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+22 more)

### Community 4 - "test_baseline_client.py"
Cohesion: 0.07
Nodes (30): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+22 more)

### Community 5 - "test_gateway_compose_e2e.py"
Cohesion: 0.05
Nodes (24): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+16 more)

### Community 6 - "cloud_service/app.py"
Cohesion: 0.08
Nodes (12): _crypto_dependencies_ready(), SecurityMode, derive_session_key(), SessionAccessError, AeadError, decrypt(), public_key(), _unavailable() (+4 more)

### Community 8 - "test_crypto_failures.py"
Cohesion: 0.08
Nodes (20): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud (+12 more)

### Community 9 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 10 - "derive_session_key"
Cohesion: 0.07
Nodes (16): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+8 more)

### Community 12 - "test_session.py"
Cohesion: 0.09
Nodes (16): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+8 more)

### Community 13 - "FailureMode"
Cohesion: 0.17
Nodes (26): FailureMode, FailureInjector, make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+18 more)

### Community 14 - "SessionManager"
Cohesion: 0.10
Nodes (7): _Measurement, _RejectRedirect, log_security(), _token(), SecureSession, SessionEstablishmentError, SessionManager

### Community 15 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 16 - "create_app"
Cohesion: 0.08
Nodes (22): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+14 more)

### Community 17 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.18
Nodes (21): main(), AeadError, decrypt(), encrypt(), generate_nonce(), _require_bytes(), _require_key(), _require_nonce() (+13 more)

### Community 18 - "SecureTransport"
Cohesion: 0.09
Nodes (9): SecureEnvelope, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport (+1 more)

### Community 19 - "PqcMetrics"
Cohesion: 0.07
Nodes (7): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 20 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (27): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+19 more)

### Community 21 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), _logging_level(), main(), test_app_exports_real_baseline_attempt_metrics(), test_classical_app_constructs_and_uses_baseline_client(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup() (+10 more)

### Community 22 - "test_dispatch.py"
Cohesion: 0.12
Nodes (14): _Baseline, cloud(), _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 23 - "GatewayError"
Cohesion: 0.12
Nodes (13): GatewayError, GatewayErrorCode, UnavailableBaseline, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state() (+5 more)

### Community 24 - "test_public_key_client.py"
Cohesion: 0.13
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, _body(), _public_key(), test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+8 more)

### Community 25 - "FailureMode"
Cohesion: 0.11
Nodes (9): Config, FailureMode, FailureInjector, FailureSelection, test_custom_environment(), test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects() (+1 more)

### Community 26 - "SessionManager"
Cohesion: 0.13
Nodes (10): SecureSession, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed() (+2 more)

### Community 27 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 28 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 29 - "legacy_system/config.py"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 30 - "test_legacy_compatibility.py"
Cohesion: 0.14
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 31 - "encode_binary"
Cohesion: 0.13
Nodes (9): decode_binary(), encode_binary(), EncodingError, KeyService, _decode_ciphertext(), test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo() (+1 more)

### Community 32 - "test_measure_modernized_e2e.py"
Cohesion: 0.09
Nodes (8): _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 33 - "test_secure_message_tamper.py"
Cohesion: 0.16
Nodes (13): DecryptSpy, _different_nonce(), _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection (+5 more)

### Community 34 - "test_cloud_failure_injection.py"
Cohesion: 0.17
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 35 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (10): _Sessions, _Baseline, _measurement(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted() (+2 more)

### Community 36 - "GatewayClient"
Cohesion: 0.20
Nodes (14): GatewayClient, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff(), test_retry_logging_exposes_failed_attempts_and_retry_events() (+6 more)

### Community 37 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 38 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 39 - "test_baseline_gateway_measurements"
Cohesion: 0.10
Nodes (13): test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), sleep(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy() (+5 more)

### Community 40 - "live_gateway"
Cohesion: 0.16
Nodes (13): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry(), test_injected_out_of_order_sequence_is_rejected_without_retry() (+5 more)

### Community 42 - "load_config"
Cohesion: 0.18
Nodes (15): ConfigurationError, load_config(), integer(), number(), text(), value(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values() (+7 more)

### Community 43 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 44 - "encapsulate"
Cohesion: 0.14
Nodes (13): test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+5 more)

### Community 45 - "log_application"
Cohesion: 0.12
Nodes (13): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements(), ready() (+5 more)

### Community 46 - "load_config"
Cohesion: 0.18
Nodes (16): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+8 more)

### Community 47 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 48 - "test_gateway_measurements.py"
Cohesion: 0.16
Nodes (14): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline() (+6 more)

### Community 49 - "CloudMetrics"
Cohesion: 0.11
Nodes (6): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_injected_fault_is_counted_only_when_its_boundary_applies(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 50 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 51 - "fields"
Cohesion: 0.17
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 52 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 53 - "GatewayConfig"
Cohesion: 0.12
Nodes (5): _baseline_transport(), get_config(), _secure_transport(), GatewayConfig, ApplicationFailures

### Community 54 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.17
Nodes (11): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement() (+3 more)

### Community 55 - "measurements.py"
Cohesion: 0.14
Nodes (3): MeasurementProcessor, GatewayMetrics, SequenceTracker

### Community 56 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 57 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 58 - "test_gateway_transport_interface.py"
Cohesion: 0.13
Nodes (6): CloudDeliveryError, CloudTransport, _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 59 - "public_key.py"
Cohesion: 0.18
Nodes (9): validate_public_key(), CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected() (+1 more)

### Community 60 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 61 - "CloudDispatch"
Cohesion: 0.13
Nodes (3): BaselineTransport, CloudDispatch, DispatchMetrics

### Community 62 - "test_mode_evaluation.py"
Cohesion: 0.20
Nodes (8): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 63 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 65 - "Config"
Cohesion: 0.19
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 66 - "Measurement"
Cohesion: 0.18
Nodes (8): Measurement, _validate_number(), _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 67 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.23
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip()

### Community 68 - "validate_legacy_measurement"
Cohesion: 0.20
Nodes (6): normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 69 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 70 - "run"
Cohesion: 0.13
Nodes (7): distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve(), TimedRepository

### Community 71 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 72 - "test_cloud_queries.py"
Cohesion: 0.19
Nodes (8): test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503(), test_safe_query_errors()

### Community 73 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 74 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 75 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.19
Nodes (3): test_bad_vendor_secret_rejected(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 76 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 77 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 78 - "_Handler"
Cohesion: 0.21
Nodes (4): _Handler, _reset_mid_body(), _Handler, _reset_mid_body()

### Community 79 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 80 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 81 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 82 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 83 - "test_gateway_application_metrics.py"
Cohesion: 0.23
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 84 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 85 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 86 - "ErrorCategory"
Cohesion: 0.21
Nodes (6): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), opener(), test_transport_failures_are_stable_and_retryable()

### Community 87 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 88 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 89 - "test_gateway_application_failures.py"
Cohesion: 0.25
Nodes (6): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 90 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 91 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 92 - "test_protocol_version_999_is_rejected_before_secure_processing"
Cohesion: 0.22
Nodes (4): AadError, build_aad(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 93 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 94 - "_ingest"
Cohesion: 0.31
Nodes (4): _error(), _ingest(), _NoMetrics, secure_measurement()

### Community 96 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.28
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 97 - "test_gateway_cloud_secure_session.py"
Cohesion: 0.28
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 98 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 99 - "test_gateway_correlation.py"
Cohesion: 0.36
Nodes (5): create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 100 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 102 - "test_handshake_counter_shows_reuse_then_expiry"
Cohesion: 0.29
Nodes (5): _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 103 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 105 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 106 - "test_gateway_operations.py"
Cohesion: 0.38
Nodes (3): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 109 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 110 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 112 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 113 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 119 - "test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row"
Cohesion: 0.33
Nodes (3): query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row()

### Community 120 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 121 - "test_legacy_mode_success_compatibility.py"
Cohesion: 0.53
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 126 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 128 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 940 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **56 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `test_session_recovery_is_counted`, `CryptoFailureInjector`, `run`, `test_handshake_counter_shows_reuse_then_expiry`, `test_handshake_failure_stays_closed_without_a_session`, `edge_gateway/app.py`, `SessionManager`, `test_secure_transport.py`, `test_session_expiry_system.py`, `edge_gateway/crypto/symmetric.py`, `SecureTransport`, `GatewayConfig`, `create_app`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `CloudDispatch`, `test_mode_evaluation.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `edge_gateway/app.py`, `test_secure_transport.py`, `SecureTransport`, `PqcMetrics`, `GatewayError`, `test_lifespan_closes_baseline_and_rejects_late_requests`, `LegacyMeasurement`, `test_baseline_gateway_measurements`, `live_gateway`, `log_application`, `load_config`, `test_gateway_measurements.py`, `GatewayConfig`, `measurements.py`, `CloudDispatch`, `validate_legacy_measurement`, `pytest`, `test_gateway_routes.py`, `edge_gateway/validation.py`, `test_gateway_application_metrics.py`, `test_gateway_response_mapping.py`, `test_gateway_application_failures.py`, `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_operations.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `GatewayClient` connect `GatewayClient` to `test_device.py`, `test_sensor.py`, `test_baseline_client.py`, `test_gateway_compose_e2e.py`, `test_sequence_state_timing_awareness_no_rollback_on_downstream_failure`, `json`, `derive_session_key`, `.__init__`, `test_legacy_compatibility.py`, `test_theoretical_retry_amplification_product_is_explicit_and_bounded`, `test_baseline_gateway_measurements`, `live_gateway`, `run`, `run`, `test_session_expiry_system.py`, `ErrorCategory`, `test_legacy_gateway_cloud_http_path_persists_canonical_measurement`, `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `.send`, `test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path`, `test_session_reuse_system.py`, `test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row`, `test_legacy_mode_success_compatibility.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05258033106134372 - nodes in this community are weakly interconnected._