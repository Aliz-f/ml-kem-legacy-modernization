# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2782 nodes · 6993 edges · 173 communities (108 shown, 65 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 973 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- fields
- FailureMode
- cli.py
- test_gateway_compose_e2e.py
- test_gateway_cloud_secure.py
- test_baseline_client.py
- test_device.py
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- edge_gateway/app.py
- MeasurementRepository
- create_app
- load_config
- SecureTransport
- test_secure_transport.py
- CloudDispatch
- PqcMetrics
- SessionManager
- test_public_key_client.py
- GatewayError
- secure.py
- CanonicalMeasurement
- SecureSession
- test_gateway_measurements.py
- FailureMode
- test_cloud_session_api.py
- test_cloud_secure.py
- validate_measurement
- test_secure_message_tamper.py
- load_config
- load_config
- test_sensor.py
- create_app
- test_session.py
- FailureInjector
- measurements.py
- LegacyMeasurement
- SecureEnvelope
- test_cloud_mlkem.py
- test_measure_modernized_e2e.py
- log_application
- test_baseline_gateway_measurements
- test_client.py
- edge_gateway/crypto/mlkem.py
- session_client.py
- SessionManager
- FailureInjector
- test_cloud_baseline.py
- GatewayConfig
- CanonicalMeasurement
- test_legacy_compatibility.py
- derive_session_key
- test_crypto_failures.py
- test_secure_shutdown.py
- test_multi_device.py
- Config
- Measurement
- StoredMeasurement
- CryptoFailureInjector
- encode_binary
- test_cloud_queries.py
- edge_gateway/crypto/encoding.py
- CloudMetrics
- encapsulate
- test_docker_assets.py
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- test_gateway_validation.py
- run
- validate_legacy_measurement
- test_handshake_failure_stays_closed_without_a_session
- sessions.py
- test_gateway_routes.py
- GatewayClient
- test_session_expiry_system.py
- test_cloud_public_key.py
- edge_gateway/validation.py
- test_gateway_application_metrics.py
- test_gateway_errors.py
- test_gateway_response_mapping.py
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- test_gateway_transport_interface.py
- envelope_validation.py
- .__init__
- _Clock
- ErrorCategory
- run
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_pqc_observability.py
- _start_loopback_gateway
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- _Clock
- _HandshakeHandler
- run
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- KdfError
- test_body_limit_before_sequence_and_delivery
- test_fixtures.py
- test_gateway_operations.py
- _Handler
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_session_reuse_system.py
- test_refresh_graphify.py
- test_repository_hygiene.py
- _crypto_dependencies_ready
- get_measurement
- test_final_secure_transport_review.py
- test_gateway_shutdown.py
- test_configured_failure_never_bypasses_domain_validation
- _Handler
- _Handler
- _BaselineGatewayHandler
- FakeResponse
- live_cloud
- _Gateway
- test_legacy_mode_success_compatibility.py
- test_shared_integration_assets.py
- public_key
- BaselineTransport
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- test_baseline_gateway_unavailable_bounded_retries
- edge_gateway/models.py
- _Handler
- TimedRepository
- TimedRepository
- test_gateway_crypto_ci.py
- _RejectRedirect
- FakeMeasurement
- payload
- .send
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 86 edges
2. `load_config()` - 82 edges
3. `GatewayClient` - 60 edges
4. `SecureTransport` - 55 edges
5. `load_config()` - 51 edges
6. `FailureMode` - 49 edges
7. `create_app()` - 49 edges
8. `FailureMode` - 48 edges
9. `PqcMetrics` - 46 edges
10. `SessionManager` - 46 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/aad.py
- `test_legacy_controller_continues_after_bounded_cloud_delivery_failure()` --uses--> `FailureMode`  [INFERRED]
  tests/integration/test_end_to_end.py → legacy_system/src/legacy_system/config.py

## Import Cycles
- None detected.

## Communities (173 total, 65 thin omitted)

### Community 0 - "fields"
Cohesion: 0.05
Nodes (54): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+46 more)

### Community 1 - "FailureMode"
Cohesion: 0.06
Nodes (49): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+41 more)

### Community 2 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 3 - "test_gateway_compose_e2e.py"
Cohesion: 0.05
Nodes (31): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+23 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 5 - "test_baseline_client.py"
Cohesion: 0.08
Nodes (29): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+21 more)

### Community 6 - "test_device.py"
Cohesion: 0.09
Nodes (28): DeviceController, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, make_config(), RaisingClient (+20 more)

### Community 8 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.05
Nodes (17): _install(), main(), _serve(), cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract(), _Baseline, _Calls (+9 more)

### Community 10 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 11 - "create_app"
Cohesion: 0.07
Nodes (26): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+18 more)

### Community 12 - "load_config"
Cohesion: 0.11
Nodes (22): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), main(), test_default_configuration() (+14 more)

### Community 13 - "SecureTransport"
Cohesion: 0.10
Nodes (10): build_secure_envelope(), SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), SecureAcceptance, SecureTransport (+2 more)

### Community 14 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 15 - "CloudDispatch"
Cohesion: 0.12
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions (+7 more)

### Community 16 - "PqcMetrics"
Cohesion: 0.07
Nodes (7): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 17 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 18 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, _body(), cloud_server(), _public_key(), _Response (+10 more)

### Community 19 - "GatewayError"
Cohesion: 0.11
Nodes (13): GatewayError, GatewayErrorCode, UnavailableBaseline, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state() (+5 more)

### Community 20 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 21 - "CanonicalMeasurement"
Cohesion: 0.13
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 22 - "SecureSession"
Cohesion: 0.09
Nodes (12): _Sessions, SecureSession, _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 23 - "test_gateway_measurements.py"
Cohesion: 0.12
Nodes (18): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_processing_fault_is_visible_and_preserves_sequence() (+10 more)

### Community 24 - "FailureMode"
Cohesion: 0.17
Nodes (22): FailureMode, canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently() (+14 more)

### Community 25 - "test_cloud_session_api.py"
Cohesion: 0.10
Nodes (14): StartupError, client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject() (+6 more)

### Community 26 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 27 - "validate_measurement"
Cohesion: 0.14
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 28 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 29 - "load_config"
Cohesion: 0.16
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), SecurityMode (+9 more)

### Community 30 - "load_config"
Cohesion: 0.15
Nodes (19): _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer() (+11 more)

### Community 31 - "test_sensor.py"
Cohesion: 0.13
Nodes (18): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 32 - "create_app"
Cohesion: 0.11
Nodes (15): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+7 more)

### Community 33 - "test_session.py"
Cohesion: 0.13
Nodes (12): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_connection_reset_during_session_post_is_retryable(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced() (+4 more)

### Community 34 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 35 - "measurements.py"
Cohesion: 0.12
Nodes (4): MeasurementProcessor, GatewayMetrics, SequenceTracker, CloudTransport

### Community 36 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (14): LegacyMeasurement, LegacyMeasurementSchemaError, test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values(), test_extra_fields_are_rejected() (+6 more)

### Community 37 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 38 - "test_cloud_mlkem.py"
Cohesion: 0.10
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 39 - "test_measure_modernized_e2e.py"
Cohesion: 0.09
Nodes (5): test_harness_rejects_invalid_sample_count(), _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads()

### Community 40 - "log_application"
Cohesion: 0.12
Nodes (10): lifespan(), log_application(), _token(), baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data() (+2 more)

### Community 41 - "test_baseline_gateway_measurements"
Cohesion: 0.10
Nodes (13): test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), sleep(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy() (+5 more)

### Community 42 - "test_client.py"
Cohesion: 0.19
Nodes (13): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_statuses_are_classified_by_retryability(), opener(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff() (+5 more)

### Community 43 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.16
Nodes (9): validate_public_key(), CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected() (+1 more)

### Community 44 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 46 - "FailureInjector"
Cohesion: 0.11
Nodes (5): FailureInjector, FailureSelection, test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_injected_fault_is_counted_only_when_its_boundary_applies(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 47 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 48 - "GatewayConfig"
Cohesion: 0.12
Nodes (5): _baseline_transport(), get_config(), _secure_transport(), GatewayConfig, ApplicationFailures

### Community 49 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 50 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 52 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 53 - "test_crypto_failures.py"
Cohesion: 0.13
Nodes (12): clock(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_enabled_warning_names_the_mode_and_not_the_seed(), test_invalid_failure_rate_is_rejected() (+4 more)

### Community 54 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 55 - "test_multi_device.py"
Cohesion: 0.11
Nodes (4): test_multiple_device_controllers_deliver_independently_to_gateway_interface(), test_multiple_device_controllers_have_independent_lifecycle_state(), test_multiple_devices_configured_via_environment_without_code_changes(), test_multiple_sensor_instances_maintain_independent_monotonic_sequences()

### Community 56 - "Config"
Cohesion: 0.12
Nodes (8): Config, test_baseline_device_controller_graceful_continuity_on_failure(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression(), read()

### Community 57 - "Measurement"
Cohesion: 0.13
Nodes (7): Measurement, _validate_number(), query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(), test_legacy_controller_continues_after_bounded_cloud_delivery_failure(), read()

### Community 58 - "StoredMeasurement"
Cohesion: 0.16
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 59 - "CryptoFailureInjector"
Cohesion: 0.15
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 60 - "encode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 61 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 62 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 63 - "CloudMetrics"
Cohesion: 0.15
Nodes (3): CloudMetrics, _labels(), _render_labels()

### Community 64 - "encapsulate"
Cohesion: 0.22
Nodes (9): encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged(), test_valid_public_key_round_trip_matches_decapsulation() (+1 more)

### Community 67 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 68 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 69 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 70 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 71 - "validate_legacy_measurement"
Cohesion: 0.19
Nodes (7): measurements(), normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 72 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 73 - "sessions.py"
Cohesion: 0.28
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 74 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 75 - "GatewayClient"
Cohesion: 0.21
Nodes (3): GatewayClient, GatewayResult, test_theoretical_retry_amplification_product_is_explicit_and_bounded()

### Community 76 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 77 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 78 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 79 - "test_gateway_application_metrics.py"
Cohesion: 0.23
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 80 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 81 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 82 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 83 - "test_gateway_transport_interface.py"
Cohesion: 0.25
Nodes (4): _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 84 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 85 - ".__init__"
Cohesion: 0.18
Nodes (3): _endpoint(), _RetryableTransport, _SessionRecovery

### Community 86 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 87 - "ErrorCategory"
Cohesion: 0.20
Nodes (6): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable(), test_unserializable_payload_is_non_retryable()

### Community 88 - "run"
Cohesion: 0.18
Nodes (6): distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve()

### Community 89 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 90 - "test_pqc_observability.py"
Cohesion: 0.27
Nodes (5): _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 92 - "_start_loopback_gateway"
Cohesion: 0.20
Nodes (5): _calculate_distribution(), _start_loopback_gateway(), test_baseline_gateway_http_503_controlled_failure(), test_baseline_healthy_workload_100_measurements(), test_baseline_validation_failure_no_retries()

### Community 93 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 94 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 95 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 96 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 99 - "run"
Cohesion: 0.22
Nodes (4): distribution(), _persisted_rows(), run(), serve()

### Community 100 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 101 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 102 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 103 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 104 - "test_gateway_operations.py"
Cohesion: 0.38
Nodes (3): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 106 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 107 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 108 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 109 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 111 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 112 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 113 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 115 - "test_configured_failure_never_bypasses_domain_validation"
Cohesion: 0.40
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 122 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 124 - "test_legacy_mode_success_compatibility.py"
Cohesion: 0.53
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 131 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 133 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 997 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **65 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app` to `BaselineTransport`, `FailureMode`, `edge_gateway/app.py`, `SecureTransport`, `test_secure_transport.py`, `CloudDispatch`, `PqcMetrics`, `GatewayError`, `test_gateway_measurements.py`, `load_config`, `measurements.py`, `LegacyMeasurement`, `log_application`, `test_baseline_gateway_measurements`, `GatewayConfig`, `validate_legacy_measurement`, `test_gateway_routes.py`, `edge_gateway/validation.py`, `test_gateway_application_metrics.py`, `test_gateway_response_mapping.py`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_operations.py`, `test_configured_failure_never_bypasses_domain_validation`, `_Gateway`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `FailureMode`, `test_gateway_cloud_secure.py`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`, `edge_gateway/app.py`, `create_app`, `SecureTransport`, `PqcMetrics`, `test_public_key_client.py`, `SecureSession`, `test_gateway_measurements.py`, `test_cloud_session_api.py`, `test_secure_message_tamper.py`, `test_session.py`, `edge_gateway/crypto/mlkem.py`, `session_client.py`, `GatewayConfig`, `test_crypto_failures.py`, `CryptoFailureInjector`, `encapsulate`, `test_handshake_failure_stays_closed_without_a_session`, `test_session_expiry_system.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_pqc_observability.py`, `KdfError`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `GatewayClient` connect `GatewayClient` to `FailureMode`, `test_gateway_compose_e2e.py`, `test_baseline_client.py`, `test_device.py`, `pytest`, `test_baseline_gateway_unavailable_bounded_retries`, `load_config`, `test_baseline_gateway_measurements`, `test_client.py`, `test_legacy_compatibility.py`, `Config`, `Measurement`, `test_session_expiry_system.py`, `test_live_end_to_end_trace_is_correlated_safe_and_observable`, `ErrorCategory`, `run`, `_start_loopback_gateway`, `test_legacy_gateway_cloud_http_path_persists_canonical_measurement`, `run`, `test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row`, `test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path`, `test_session_reuse_system.py`, `test_legacy_mode_success_compatibility.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `fields` be split into smaller, more focused modules?**
  _Cohesion score 0.05087719298245614 - nodes in this community are weakly interconnected._