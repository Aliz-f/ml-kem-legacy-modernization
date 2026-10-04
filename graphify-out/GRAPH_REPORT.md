# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2875 nodes · 7197 edges · 181 communities (120 shown, 61 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1029 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- baseline.py
- DeviceController
- cli.py
- test_gateway_compose_e2e.py
- test_gateway_cloud_secure.py
- logging
- load_config
- FailureMode
- SecureTransport
- edge_gateway/app.py
- FailureMode
- MeasurementRepository
- Sensor
- test_public_key_client.py
- test_secure_transport.py
- SessionManager
- CloudDispatch
- PqcMetrics
- secure.py
- measure_modernized_e2e.py
- SecureSession
- test_cloud_session_api.py
- test_cloud_secure.py
- edge_gateway/crypto/symmetric.py
- GatewayErrorCode
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- create_app
- load_config
- encapsulate
- CryptoFailureInjector
- LegacyMeasurement
- CanonicalMeasurement
- FailureInjector
- _dispatch
- encode_binary
- SessionManager
- test_sensor.py
- SecureEnvelope
- repository.py
- validate_measurement
- session_client.py
- test_gateway_measurements.py
- fields
- create_app
- edge_gateway/crypto/envelope.py
- CanonicalMeasurement
- test_secure_shutdown.py
- test_client.py
- test_measure_modernized_e2e.py
- test_crypto_failures.py
- edge_gateway/crypto/encoding.py
- Measurement
- test_legacy_gateway.py
- sessions.py
- test_cloud_baseline.py
- test_static_quality.py
- test_cloud_public_key.py
- derive_session_key
- test_cloud_queries.py
- load_config
- test_gateway_validation.py
- test_session.py
- _start_scripted_server
- CloudMetrics
- edge_gateway/config.py
- test_cloud_kdf.py
- validate_legacy_measurement
- cloud_service/crypto/mlkem.py
- run
- _start_loopback_gateway
- test_handshake_failure_stays_closed_without_a_session
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- test_cloud_mlkem.py
- edge_gateway/crypto/aad.py
- parse_public_key_response
- measurements.py
- test_gateway_routes.py
- ErrorCategory
- GatewayClient
- test_pqc_observability.py
- edge_gateway/validation.py
- test_gateway_application_failures.py
- pytest
- test_gateway_errors.py
- test_gateway_response_mapping.py
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- envelope_validation.py
- _baseline_transport
- test_gateway_correlation.py
- GatewayMetrics
- test_gateway_application_metrics.py
- test_gateway_request_size.py
- _Handler
- test_secure_envelope.py
- _Clock
- run
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_failure_paths.py
- test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- ApplicationFailures
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- test_gateway_transport_interface.py
- _Clock
- queries.py
- GatewayError
- _HandshakeHandler
- test_gateway_operations.py
- fastapi_testclient
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- KdfError
- SessionState
- test_gateway_application_failures_integration.py
- test_fixtures.py
- main
- test_gateway_shutdown.py
- _Handler
- _GatewayValidationHandler
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_repository_hygiene.py
- test_final_secure_transport_review.py
- _Handler
- _BaselineGatewayHandler
- _ScriptedNetworkHandler
- live_cloud
- test_shared_integration_assets.py
- public_key
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- measure_mode_comparison.py
- test_sequence_state_timing_awareness_no_rollback_on_downstream_failure
- test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries
- test_cloud_metrics.py
- edge_gateway/models.py
- TimedRepository
- _deliver
- test_gateway_crypto_ci.py
- KdfError
- AcceptedBaseline
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
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()` --uses--> `BaselineCloudClient`  [INFERRED]
  tests/integration/test_gateway_cloud_baseline.py → edge_gateway/src/edge_gateway/cloud/baseline.py

## Import Cycles
- None detected.

## Communities (181 total, 61 thin omitted)

### Community 0 - "baseline.py"
Cohesion: 0.05
Nodes (42): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+34 more)

### Community 1 - "DeviceController"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 2 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 3 - "test_gateway_compose_e2e.py"
Cohesion: 0.05
Nodes (31): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+23 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 6 - "logging"
Cohesion: 0.08
Nodes (11): Config, main(), test_default_configuration_failure_injection_disabled(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller() (+3 more)

### Community 7 - "load_config"
Cohesion: 0.06
Nodes (25): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+17 more)

### Community 8 - "FailureMode"
Cohesion: 0.11
Nodes (30): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), test_duplicate_sequence_selection_varies_by_seed() (+22 more)

### Community 9 - "SecureTransport"
Cohesion: 0.07
Nodes (13): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport (+5 more)

### Community 10 - "edge_gateway/app.py"
Cohesion: 0.10
Nodes (6): _logging_level(), main(), log_application(), _token(), corrupt_ciphertext_copy(), CloudDeliveryError

### Community 11 - "FailureMode"
Cohesion: 0.11
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 12 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 13 - "Sensor"
Cohesion: 0.06
Nodes (13): Sensor, test_domain_measurement_immutability_under_failure_injection(), test_strict_absence_of_simulation_metadata_on_wire(), _GatewayValidationServer, _start_gateway_server(), test_data_failure_modes_rejected_or_accepted_without_retry(), test_device_controller_runs_through_fault_injections_without_crashing(), test_failure_rejections_logged_with_structured_attributes() (+5 more)

### Community 14 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+11 more)

### Community 15 - "test_secure_transport.py"
Cohesion: 0.19
Nodes (26): SecureTransportError, _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics(), test_application_rejection_is_not_retried() (+18 more)

### Community 16 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 17 - "CloudDispatch"
Cohesion: 0.13
Nodes (14): CloudDispatch, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 18 - "PqcMetrics"
Cohesion: 0.07
Nodes (6): _Duration, PqcMetrics, _Cloud, __init__(), test_metrics_endpoint_exposes_the_same_registry(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 19 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 20 - "measure_modernized_e2e.py"
Cohesion: 0.11
Nodes (7): test_baseline_device_controller_graceful_continuity_on_failure(), distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve()

### Community 21 - "SecureSession"
Cohesion: 0.09
Nodes (13): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+5 more)

### Community 22 - "test_cloud_session_api.py"
Cohesion: 0.10
Nodes (15): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+7 more)

### Community 23 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 24 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 25 - "GatewayErrorCode"
Cohesion: 0.14
Nodes (12): GatewayErrorCode, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap() (+4 more)

### Community 26 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 27 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 28 - "create_app"
Cohesion: 0.10
Nodes (16): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+8 more)

### Community 29 - "load_config"
Cohesion: 0.16
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), SecurityMode (+9 more)

### Community 30 - "encapsulate"
Cohesion: 0.13
Nodes (11): test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+3 more)

### Community 31 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (6): get_config(), _secure_transport(), GatewayConfig, CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 32 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 33 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 34 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 35 - "_dispatch"
Cohesion: 0.10
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 36 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 38 - "test_sensor.py"
Cohesion: 0.13
Nodes (17): FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp() (+9 more)

### Community 39 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 40 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 41 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 42 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 43 - "test_gateway_measurements.py"
Cohesion: 0.16
Nodes (14): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline() (+6 more)

### Community 44 - "fields"
Cohesion: 0.18
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 45 - "create_app"
Cohesion: 0.13
Nodes (13): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements() (+5 more)

### Community 46 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.17
Nodes (11): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement() (+3 more)

### Community 47 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 48 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 49 - "test_client.py"
Cohesion: 0.22
Nodes (11): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff(), test_retry_logging_exposes_failed_attempts_and_retry_events(), test_retry_stops_after_non_retryable_result() (+3 more)

### Community 50 - "test_measure_modernized_e2e.py"
Cohesion: 0.12
Nodes (6): test_harness_rejects_invalid_sample_count(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 51 - "test_crypto_failures.py"
Cohesion: 0.14
Nodes (12): clock(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_enabled_warning_names_the_mode_and_not_the_seed(), test_invalid_failure_rate_is_rejected() (+4 more)

### Community 52 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 53 - "Measurement"
Cohesion: 0.13
Nodes (7): Measurement, _validate_number(), query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(), test_legacy_controller_continues_after_bounded_cloud_delivery_failure(), read()

### Community 54 - "test_legacy_gateway.py"
Cohesion: 0.27
Nodes (11): fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry(), test_injected_out_of_order_sequence_is_rejected_without_retry(), test_injected_payload_faults_are_rejected_without_retry_or_cloud_delivery() (+3 more)

### Community 55 - "sessions.py"
Cohesion: 0.18
Nodes (10): health(), ready(), _crypto_dependencies_ready(), _unavailable(), derive_session_key(), _decode_ciphertext(), _error(), _establish() (+2 more)

### Community 56 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 57 - "test_static_quality.py"
Cohesion: 0.12
Nodes (7): test_legacy_ai_decisions_register_exists(), test_legacy_architecture_operations_documentation_exists(), test_legacy_technical_debt_register_exists(), test_no_cloud_or_crypto_imports_in_legacy_src(), test_no_debug_prints_or_breakpoints_in_legacy_src(), test_no_keys_or_env_files_in_legacy_system(), test_no_private_key_blocks_in_legacy_files()

### Community 58 - "test_cloud_public_key.py"
Cohesion: 0.17
Nodes (10): StartupError, secure_app(), test_classical_does_not_generate_keys(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary() (+2 more)

### Community 59 - "derive_session_key"
Cohesion: 0.19
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 60 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 61 - "load_config"
Cohesion: 0.18
Nodes (11): load_config(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_mlkem_readiness_requires_initialized_transport_but_not_active_session(), test_readiness_is_local_and_delivery_still_requires_cloud() (+3 more)

### Community 62 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 63 - "test_session.py"
Cohesion: 0.18
Nodes (10): _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_connection_reset_during_session_post_is_retryable(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_replacement_clears_a_held_session_before_the_new_handshake() (+2 more)

### Community 64 - "_start_scripted_server"
Cohesion: 0.15
Nodes (8): _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout(), test_gateway_stopped_or_connection_refused(), test_transient_failure_eventual_recovery_succeeds()

### Community 65 - "CloudMetrics"
Cohesion: 0.15
Nodes (3): CloudMetrics, _labels(), _render_labels()

### Community 66 - "edge_gateway/config.py"
Cohesion: 0.28
Nodes (12): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float() (+4 more)

### Community 67 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 68 - "validate_legacy_measurement"
Cohesion: 0.20
Nodes (6): normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 69 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 70 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 71 - "_start_loopback_gateway"
Cohesion: 0.14
Nodes (7): _BaselineServer, _calculate_distribution(), _start_loopback_gateway(), test_baseline_gateway_http_503_controlled_failure(), test_baseline_gateway_unavailable_bounded_retries(), test_baseline_healthy_workload_100_measurements(), test_baseline_validation_failure_no_retries()

### Community 72 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 73 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.14
Nodes (3): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 74 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (4): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 75 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 76 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 78 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 79 - "ErrorCategory"
Cohesion: 0.18
Nodes (8): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable(), test_unserializable_payload_is_non_retryable()

### Community 80 - "GatewayClient"
Cohesion: 0.21
Nodes (3): GatewayClient, GatewayResult, test_theoretical_retry_amplification_product_is_explicit_and_bounded()

### Community 81 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 82 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 83 - "test_gateway_application_failures.py"
Cohesion: 0.23
Nodes (7): test_cloud_fault_uses_existing_retries(), session(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 84 - "pytest"
Cohesion: 0.17
Nodes (4): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults(), test_harness_rejects_invalid_sample_counts()

### Community 85 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 86 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 87 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 88 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 89 - "_baseline_transport"
Cohesion: 0.20
Nodes (3): _baseline_transport(), BaselineTransport, DispatchMetrics

### Community 90 - "test_gateway_correlation.py"
Cohesion: 0.27
Nodes (5): create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 92 - "test_gateway_application_metrics.py"
Cohesion: 0.25
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 93 - "test_gateway_request_size.py"
Cohesion: 0.24
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 94 - "_Handler"
Cohesion: 0.22
Nodes (4): _Handler, _reset_mid_body(), _Handler, _reset_mid_body()

### Community 95 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 96 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 97 - "run"
Cohesion: 0.18
Nodes (4): distribution(), _persisted_rows(), run(), TimedRepository

### Community 98 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 99 - "test_failure_paths.py"
Cohesion: 0.31
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 100 - "test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively"
Cohesion: 0.18
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 102 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 103 - "ApplicationFailures"
Cohesion: 0.27
Nodes (3): ApplicationFailures, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario()

### Community 104 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 105 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 106 - "test_gateway_transport_interface.py"
Cohesion: 0.29
Nodes (4): _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 107 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 108 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 111 - "test_gateway_operations.py"
Cohesion: 0.28
Nodes (4): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 112 - "fastapi_testclient"
Cohesion: 0.31
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 113 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 114 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 116 - "test_gateway_application_failures_integration.py"
Cohesion: 0.32
Nodes (3): test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_service()

### Community 117 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 118 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 122 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 123 - "test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression"
Cohesion: 0.29
Nodes (3): test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression(), read(), test_sequence_gap_is_accepted_and_logged()

### Community 124 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 126 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 132 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 139 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 141 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

### Community 147 - "test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries"
Cohesion: 0.40
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 158 - "_deliver"
Cohesion: 0.67
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1042 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **61 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `edge_gateway/app.py`, `test_secure_transport.py`, `CloudDispatch`, `PqcMetrics`, `SecureSession`, `edge_gateway/crypto/symmetric.py`, `CryptoFailureInjector`, `_dispatch`, `SessionManager`, `create_app`, `edge_gateway/crypto/envelope.py`, `test_secure_shutdown.py`, `edge_gateway/crypto/encoding.py`, `test_legacy_gateway.py`, `test_handshake_failure_stays_closed_without_a_session`, `edge_gateway/crypto/aad.py`, `test_pqc_observability.py`, `test_gateway_application_failures.py`, `_baseline_transport`, `GatewayMetrics`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `main`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `baseline.py`, `SecureTransport`, `edge_gateway/app.py`, `test_secure_transport.py`, `CloudDispatch`, `PqcMetrics`, `SecureSession`, `GatewayErrorCode`, `test_legacy_compatibility.py`, `CryptoFailureInjector`, `LegacyMeasurement`, `test_gateway_measurements.py`, `test_legacy_gateway.py`, `load_config`, `test_gateway_validation.py`, `validate_legacy_measurement`, `measurements.py`, `test_gateway_routes.py`, `edge_gateway/validation.py`, `test_gateway_application_failures.py`, `test_gateway_response_mapping.py`, `_baseline_transport`, `GatewayMetrics`, `test_gateway_application_metrics.py`, `test_gateway_request_size.py`, `test_failure_paths.py`, `ApplicationFailures`, `GatewayError`, `test_gateway_operations.py`, `fastapi_testclient`, `test_gateway_application_failures_integration.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `FailureMode` connect `FailureMode` to `test_gateway_cloud_secure.py`, `pathlib`, `logging`, `public_key`, `baseline_measurement`, `test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row`, `secure.py`, `Measurement`, `sessions.py`, `test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path`, `load_config`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 61 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._