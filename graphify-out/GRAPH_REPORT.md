# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2860 nodes · 7181 edges · 178 communities (119 shown, 59 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1029 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DeviceController
- cli.py
- test_gateway_cloud_secure.py
- edge_gateway/app.py
- test_baseline_client.py
- _dispatch
- SessionManager
- CloudDispatch
- FailureMode
- SecureTransport
- MeasurementRepository
- create_app
- test_session.py
- PqcMetrics
- test_public_key_client.py
- legacy_system/config.py
- SessionManager
- encapsulate
- test_secure_transport.py
- measure_modernized_e2e.py
- test_measure_modernized_e2e.py
- test_cloud_secure.py
- secure.py
- validate_measurement
- test_gateway_correlation.py
- create_app
- load_config
- CanonicalMeasurement
- test_secure_message_tamper.py
- load_config
- test_cloud_session_api.py
- test_session_recovery_is_counted
- FailureInjector
- encode_binary
- LegacyMeasurement
- Sensor
- test_sensor.py
- FailureMode
- SecureEnvelope
- GatewayError
- test_baseline_gateway_measurements
- test_client.py
- test_cloud_failure_injection.py
- session_client.py
- test_gateway_measurements.py
- device.py
- test_failure_simulation.py
- derive_session_key
- StoredMeasurement
- measurements.py
- edge_gateway/crypto/envelope.py
- CanonicalMeasurement
- test_legacy_compatibility.py
- CloudMetrics
- fields
- CryptoFailureInjector
- test_crypto_failures.py
- test_gateway_compose_e2e.py
- ErrorCategory
- edge_gateway/crypto/encoding.py
- Config
- Measurement
- test_network_failures.py
- test_legacy_gateway.py
- test_cloud_baseline.py
- _Handler
- _Sessions
- sessions.py
- test_cloud_kdf.py
- edge_gateway/crypto/symmetric.py
- test_cloud_queries.py
- GatewayMetrics
- encrypt
- CloudDeliveryError
- test_docker_assets.py
- cloud_service/crypto/mlkem.py
- build_aad
- edge_gateway/validation.py
- test_gateway_validation.py
- client.py
- test_gateway_crypto_image.py
- run
- parse_public_key_response
- test_handshake_failure_stays_closed_without_a_session
- GatewayErrorCode
- GatewayConfig
- _Clock
- test_gateway_routes.py
- GatewayClient
- run
- test_session_expiry_system.py
- test_cloud_public_key.py
- normalize
- test_gateway_application_metrics.py
- test_gateway_response_mapping.py
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- envelope_validation.py
- test_gateway_application_failures.py
- test_secure_envelope.py
- test_static_checks.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- _error_response
- _Clock
- queries.py
- _HandshakeHandler
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- test_fixtures.py
- main
- _baseline_transport
- ApplicationFailures
- test_application_errors_have_stable_http_contract
- test_gateway_operations.py
- test_transport_failures_are_stable_and_retryable
- _GatewayValidationHandler
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_session_reuse_system.py
- test_repository_hygiene.py
- test_final_secure_transport_review.py
- _Handler
- _BaselineGatewayHandler
- _ScriptedNetworkHandler
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- live_cloud
- _Gateway
- test_shared_integration_assets.py
- public_key
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- test_sequence_state_timing_awareness_no_rollback_on_downstream_failure
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- TimedRepository
- test_gateway_crypto_ci.py
- test_lifespan_closes_baseline_and_rejects_late_requests
- AcceptedBaseline
- payload
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 86 edges
2. `load_config()` - 82 edges
3. `GatewayClient` - 69 edges
4. `FailureMode` - 63 edges
5. `SecureTransport` - 55 edges
6. `load_config()` - 51 edges
7. `FailureMode` - 49 edges
8. `FailureInjector` - 49 edges
9. `create_app()` - 49 edges
10. `PqcMetrics` - 46 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_legacy_controller_continues_after_bounded_cloud_delivery_failure()` --uses--> `DeviceController`  [INFERRED]
  tests/integration/test_end_to_end.py → legacy_system/src/legacy_system/device.py
- `test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression()` --uses--> `DeviceController`  [INFERRED]
  tests/integration/test_legacy_gateway.py → legacy_system/src/legacy_system/device.py

## Import Cycles
- None detected.

## Communities (178 total, 59 thin omitted)

### Community 0 - "DeviceController"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 1 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 4 - "test_baseline_client.py"
Cohesion: 0.08
Nodes (29): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+21 more)

### Community 6 - "_dispatch"
Cohesion: 0.05
Nodes (18): cloud(), LiveCloud, _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server (+10 more)

### Community 7 - "SessionManager"
Cohesion: 0.07
Nodes (11): clock(), _RejectRedirect, log_security(), _token(), SecureSession, SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake() (+3 more)

### Community 8 - "CloudDispatch"
Cohesion: 0.10
Nodes (16): CloudDispatch, DispatchMetrics, _Baseline, cloud(), _config(), _Handler, _measurement(), _Secure (+8 more)

### Community 9 - "FailureMode"
Cohesion: 0.15
Nodes (26): FailureMode, FailureInjector, make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+18 more)

### Community 10 - "SecureTransport"
Cohesion: 0.10
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 11 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 12 - "create_app"
Cohesion: 0.07
Nodes (22): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+14 more)

### Community 13 - "test_session.py"
Cohesion: 0.09
Nodes (16): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+8 more)

### Community 14 - "PqcMetrics"
Cohesion: 0.06
Nodes (7): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 15 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+11 more)

### Community 16 - "legacy_system/config.py"
Cohesion: 0.13
Nodes (23): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), main(), test_default_configuration() (+15 more)

### Community 17 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 18 - "encapsulate"
Cohesion: 0.10
Nodes (15): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe(), encapsulate(), MlKemError, validate_public_key() (+7 more)

### Community 19 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (26): session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics(), test_application_rejection_is_not_retried() (+18 more)

### Community 20 - "measure_modernized_e2e.py"
Cohesion: 0.11
Nodes (6): distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve()

### Community 21 - "test_measure_modernized_e2e.py"
Cohesion: 0.08
Nodes (9): test_harness_rejects_invalid_sample_count(), _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed() (+1 more)

### Community 22 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (26): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+18 more)

### Community 23 - "secure.py"
Cohesion: 0.11
Nodes (9): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+1 more)

### Community 24 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 25 - "test_gateway_correlation.py"
Cohesion: 0.09
Nodes (6): test_gateway_process_exits_cleanly_on_signal(), clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_script_stores_one_secure_measurement()

### Community 26 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), _logging_level(), main(), test_app_exports_real_baseline_attempt_metrics(), test_classical_app_constructs_and_uses_baseline_client(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup() (+9 more)

### Community 27 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), SecurityMode (+9 more)

### Community 28 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 29 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 30 - "load_config"
Cohesion: 0.14
Nodes (18): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+10 more)

### Community 31 - "test_cloud_session_api.py"
Cohesion: 0.12
Nodes (13): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+5 more)

### Community 32 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (11): _Sessions, _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 33 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 34 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 35 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 36 - "Sensor"
Cohesion: 0.10
Nodes (7): Sensor, test_default_configuration_failure_injection_disabled(), test_domain_measurement_immutability_under_failure_injection(), test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), test_strict_absence_of_simulation_metadata_on_wire(), test_device_controller_discards_failed_measurement_and_advances_sequence()

### Community 37 - "test_sensor.py"
Cohesion: 0.13
Nodes (17): FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp() (+9 more)

### Community 38 - "FailureMode"
Cohesion: 0.14
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 39 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 40 - "GatewayError"
Cohesion: 0.13
Nodes (12): GatewayError, UnavailableBaseline, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap() (+4 more)

### Community 41 - "test_baseline_gateway_measurements"
Cohesion: 0.10
Nodes (13): test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), sleep(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy() (+5 more)

### Community 42 - "test_client.py"
Cohesion: 0.19
Nodes (13): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_statuses_are_classified_by_retryability(), opener(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff() (+5 more)

### Community 43 - "test_cloud_failure_injection.py"
Cohesion: 0.20
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 44 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 45 - "test_gateway_measurements.py"
Cohesion: 0.16
Nodes (14): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline() (+6 more)

### Community 46 - "device.py"
Cohesion: 0.10
Nodes (6): _sequence_number(), test_multiple_device_controllers_deliver_independently_to_gateway_interface(), test_multiple_device_controllers_have_independent_lifecycle_state(), test_multiple_devices_configured_via_environment_without_code_changes(), test_multiple_failure_injectors_operate_independently(), test_multiple_sensor_instances_maintain_independent_monotonic_sequences()

### Community 47 - "test_failure_simulation.py"
Cohesion: 0.12
Nodes (8): _GatewayValidationServer, _start_gateway_server(), test_data_failure_modes_rejected_or_accepted_without_retry(), test_device_controller_runs_through_fault_injections_without_crashing(), test_failure_rejections_logged_with_structured_attributes(), test_malformed_wire_body_is_400_without_retry(), test_random_failure_mode_generates_mixed_controlled_outcomes(), test_sequence_failure_modes_trigger_409_without_retry()

### Community 48 - "derive_session_key"
Cohesion: 0.15
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 49 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 50 - "measurements.py"
Cohesion: 0.14
Nodes (9): lifespan(), log_application(), _token(), baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids() (+1 more)

### Community 51 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.17
Nodes (11): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement() (+3 more)

### Community 52 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 53 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 54 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 55 - "fields"
Cohesion: 0.17
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 56 - "CryptoFailureInjector"
Cohesion: 0.13
Nodes (3): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_same_seed_makes_the_same_decisions()

### Community 57 - "test_crypto_failures.py"
Cohesion: 0.16
Nodes (10): _aad(), _injector(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault() (+2 more)

### Community 58 - "test_gateway_compose_e2e.py"
Cohesion: 0.23
Nodes (13): _compose(), _measurement(), _metrics(), _port(), _send(), test_compose_cloud_restart_recovers_readiness_and_delivery(), test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback(), test_compose_gateway_restart_establishes_a_fresh_mlkem_session() (+5 more)

### Community 59 - "ErrorCategory"
Cohesion: 0.12
Nodes (9): ErrorCategory, _BaselineServer, _calculate_distribution(), _start_loopback_gateway(), test_baseline_gateway_http_503_controlled_failure(), test_baseline_gateway_unavailable_bounded_retries(), test_baseline_healthy_workload_100_measurements(), test_baseline_validation_failure_no_retries() (+1 more)

### Community 60 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 61 - "Config"
Cohesion: 0.13
Nodes (8): Config, test_baseline_device_controller_graceful_continuity_on_failure(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory()

### Community 62 - "Measurement"
Cohesion: 0.13
Nodes (7): Measurement, _validate_number(), query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(), test_legacy_controller_continues_after_bounded_cloud_delivery_failure(), read()

### Community 63 - "test_network_failures.py"
Cohesion: 0.18
Nodes (8): _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout(), test_gateway_stopped_or_connection_refused(), test_transient_failure_eventual_recovery_succeeds()

### Community 64 - "test_legacy_gateway.py"
Cohesion: 0.27
Nodes (11): fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry(), test_injected_out_of_order_sequence_is_rejected_without_retry(), test_injected_payload_faults_are_rejected_without_retry_or_cloud_delivery() (+3 more)

### Community 65 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 66 - "_Handler"
Cohesion: 0.14
Nodes (6): _Handler, _reset_mid_body(), _Handler, _reset_mid_body(), _Handler, _reset_mid_body()

### Community 67 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 68 - "sessions.py"
Cohesion: 0.19
Nodes (8): _crypto_dependencies_ready(), derive_session_key(), KdfError, _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 69 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 70 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.18
Nodes (8): test_vendor_error_diagnostics_are_suppressed(), main(), AeadError, decrypt(), _require_bytes(), _require_key(), _require_nonce(), test_existing_secure_envelope_authenticates_same_request_context()

### Community 71 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 72 - "GatewayMetrics"
Cohesion: 0.15
Nodes (3): MeasurementProcessor, GatewayMetrics, SequenceTracker

### Community 73 - "encrypt"
Cohesion: 0.37
Nodes (12): encrypt(), _aad(), _key(), _plaintext(), test_authentication_failure_does_not_return_plaintext(), test_independent_cloud_aad_authenticates_and_each_field_change_fails(), test_invalid_key_and_nonce_lengths_are_rejected(), test_keys_and_plaintext_are_not_logged() (+4 more)

### Community 74 - "CloudDeliveryError"
Cohesion: 0.14
Nodes (6): CloudDeliveryError, CloudTransport, _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 76 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 77 - "build_aad"
Cohesion: 0.22
Nodes (7): AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 78 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 79 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 80 - "client.py"
Cohesion: 0.22
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 81 - "test_gateway_crypto_image.py"
Cohesion: 0.18
Nodes (6): test_clean_container_image_runs_when_docker_is_available(), _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 82 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 83 - "parse_public_key_response"
Cohesion: 0.23
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 84 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 86 - "GatewayConfig"
Cohesion: 0.17
Nodes (5): get_config(), _secure_transport(), GatewayConfig, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 87 - "_Clock"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 88 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 89 - "GatewayClient"
Cohesion: 0.21
Nodes (3): GatewayClient, GatewayResult, test_theoretical_retry_amplification_product_is_explicit_and_bounded()

### Community 90 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 91 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 92 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 93 - "normalize"
Cohesion: 0.20
Nodes (4): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input()

### Community 94 - "test_gateway_application_metrics.py"
Cohesion: 0.23
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 95 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 96 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 97 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 98 - "test_gateway_application_failures.py"
Cohesion: 0.25
Nodes (6): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 99 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 100 - "test_static_checks.py"
Cohesion: 0.29
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 101 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 103 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 104 - "_error_response"
Cohesion: 0.22
Nodes (9): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready(), _error_response() (+1 more)

### Community 105 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 106 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 108 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 109 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 110 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 111 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 112 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 115 - "test_application_errors_have_stable_http_contract"
Cohesion: 0.33
Nodes (4): test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized()

### Community 116 - "test_gateway_operations.py"
Cohesion: 0.38
Nodes (3): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 117 - "test_transport_failures_are_stable_and_retryable"
Cohesion: 0.29
Nodes (4): test_http_error_is_classified_without_leaking_exception(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable()

### Community 119 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 120 - "test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression"
Cohesion: 0.29
Nodes (3): test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression(), read(), test_sequence_gap_is_accepted_and_logged()

### Community 121 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 122 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 124 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 130 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.47
Nodes (5): _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 131 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 138 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 140 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1035 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **59 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app` to `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `edge_gateway/app.py`, `_Gateway`, `CloudDispatch`, `SecureTransport`, `PqcMetrics`, `test_secure_transport.py`, `load_config`, `test_lifespan_closes_baseline_and_rejects_late_requests`, `LegacyMeasurement`, `GatewayError`, `test_baseline_gateway_measurements`, `test_gateway_measurements.py`, `measurements.py`, `test_legacy_gateway.py`, `GatewayMetrics`, `edge_gateway/validation.py`, `GatewayErrorCode`, `GatewayConfig`, `test_gateway_routes.py`, `test_gateway_application_metrics.py`, `test_gateway_response_mapping.py`, `test_gateway_application_failures.py`, `_error_response`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_validation_bypass.py`, `_baseline_transport`, `ApplicationFailures`, `test_gateway_operations.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `GatewayClient` connect `GatewayClient` to `DeviceController`, `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `test_baseline_client.py`, `test_sequence_state_timing_awareness_no_rollback_on_downstream_failure`, `measure_modernized_e2e.py`, `Sensor`, `test_baseline_gateway_measurements`, `test_client.py`, `device.py`, `test_failure_simulation.py`, `test_legacy_compatibility.py`, `test_gateway_compose_e2e.py`, `ErrorCategory`, `Measurement`, `test_network_failures.py`, `test_legacy_gateway.py`, `client.py`, `run`, `test_session_expiry_system.py`, `test_live_end_to_end_trace_is_correlated_safe_and_observable`, `test_legacy_gateway_cloud_http_path_persists_canonical_measurement`, `test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row`, `test_transport_failures_are_stable_and_retryable`, `test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression`, `test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path`, `test_session_reuse_system.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `SecureSession` connect `SessionManager` to `test_session_recovery_is_counted`, `edge_gateway/app.py`, `_Sessions`, `CloudDispatch`, `SecureTransport`, `test_session.py`, `test_secure_transport.py`, `test_crypto_failures.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 61 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._