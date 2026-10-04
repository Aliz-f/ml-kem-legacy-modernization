# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2906 nodes · 7276 edges · 189 communities (120 shown, 69 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1041 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- test_gateway_cloud_secure.py
- test_baseline_client.py
- edge_gateway/app.py
- derive_session_key
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- SecureTransport
- create_app
- FailureMode
- MeasurementRepository
- test_public_key_client.py
- SecureSession
- pytest
- sessions.py
- client.py
- PqcMetrics
- test_secure_transport.py
- test_session.py
- CloudDispatch
- SessionManager
- secure.py
- load_config
- test_cloud_mlkem.py
- test_measure_modernized_e2e.py
- create_app
- test_cloud_secure.py
- edge_gateway/crypto/symmetric.py
- load_config
- CanonicalMeasurement
- session_client.py
- FailureInjector
- test_baseline_gateway_measurements
- encode_binary
- repository.py
- LegacyMeasurement
- _start_contract_receiver
- test_sensor.py
- SecureEnvelope
- encapsulate
- test_secure_message_tamper.py
- validate_measurement
- load_config
- GatewayErrorCode
- test_gateway_measurements.py
- Sensor
- test_cloud_failure_injection.py
- measurements.py
- CanonicalMeasurement
- Config
- test_client.py
- test_cloud_session_api.py
- fields
- test_crypto_failures.py
- FailureMode
- Measurement
- test_legacy_gateway.py
- plaintext.py
- _Handler
- test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback
- CloudMetrics
- edge_gateway/crypto/encoding.py
- test_gateway_validation.py
- _Sessions
- _start_loopback_receiver
- _start_scripted_server
- test_security_mode_preserves_the_legacy_measurement_contract
- test_cloud_baseline.py
- test_cloud_queries.py
- test_docker_assets.py
- test_static_quality.py
- cloud_service/crypto/mlkem.py
- build_aad
- DeviceController
- edge_gateway/validation.py
- test_cloud_response_failures.py
- make_config
- test_gateway_crypto_image.py
- run
- CryptoFailureInjector
- errors.py
- test_handshake_failure_stays_closed_without_a_session
- SessionManager
- test_gateway_correlation.py
- _Clock
- test_gateway_routes.py
- ErrorCategory
- GatewayClient
- run
- run
- test_session_expiry_system.py
- test_cloud_public_key.py
- test_gateway_application_failures.py
- test_gateway_response_mapping.py
- RecordingClient
- envelope_validation.py
- parse_public_key_response
- test_gateway_application_metrics.py
- test_secure_envelope.py
- test_static_checks.py
- test_shutdown_after_gateway_unavailable_delivery
- test_corrupted_ciphertext_is_rejected_and_not_stored
- routes.py
- normalize
- CloudDeliveryError
- _HandshakeHandler
- test_gateway_operations.py
- test_falsey_injected_dependencies_are_preserved
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- queries.py
- _secure_transport
- GatewayError
- ApplicationFailures
- test_body_limit_before_sequence_and_delivery
- test_fixtures.py
- normalize_artifacts
- StartupError
- main
- _baseline_transport
- FakeResponse
- _LegacyContractReceiver
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression
- test_legacy_mode_success_compatibility.py
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_session_reuse_system.py
- test_repository_hygiene.py
- _crypto_dependencies_ready
- test_final_secure_transport_review.py
- test_configured_failure_never_bypasses_domain_validation
- _Handler
- _BaselineLoopbackReceiver
- test_client_exception_is_logged_then_loop_continues_and_closes
- _ScriptedNetworkHandler
- live_cloud
- _Gateway
- test_shared_integration_assets.py
- public_key
- CloudTransport
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- test_sequence_state_timing_awareness_no_rollback_on_downstream_failure
- edge_gateway/models.py
- Handler
- _Handler
- test_multiple_device_controllers_deliver_independently_to_gateway_interface
- test_gateway_crypto_ci.py
- client
- test_lifespan_closes_baseline_and_rejects_late_requests
- FakeMeasurement
- AcceptedBaseline
- payload
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 87 edges
2. `load_config()` - 83 edges
3. `GatewayClient` - 71 edges
4. `FailureMode` - 63 edges
5. `SecureTransport` - 56 edges
6. `load_config()` - 51 edges
7. `FailureMode` - 49 edges
8. `FailureInjector` - 49 edges
9. `create_app()` - 49 edges
10. `PqcMetrics` - 46 edges

## Surprising Connections (you probably didn't know these)
- `open_response()` --indirect_call--> `status()`  [INFERRED]
  edge_gateway/tests/test_cloud_response_failures.py → src/ai_history/cli.py
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py

## Import Cycles
- None detected.

## Communities (189 total, 69 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 1 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 2 - "test_baseline_client.py"
Cohesion: 0.06
Nodes (32): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint() (+24 more)

### Community 5 - "derive_session_key"
Cohesion: 0.05
Nodes (19): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+11 more)

### Community 6 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.05
Nodes (19): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract(), _Baseline, _Calls, _dispatch(), measure_modes(), _serve() (+11 more)

### Community 7 - "SecureTransport"
Cohesion: 0.07
Nodes (12): build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance() (+4 more)

### Community 8 - "create_app"
Cohesion: 0.07
Nodes (30): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements() (+22 more)

### Community 9 - "FailureMode"
Cohesion: 0.13
Nodes (28): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+20 more)

### Community 10 - "MeasurementRepository"
Cohesion: 0.10
Nodes (26): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_acceptance_is_committed_and_correlated(), test_concurrent_duplicates_across_connections(), save() (+18 more)

### Community 11 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (20): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+12 more)

### Community 12 - "SecureSession"
Cohesion: 0.06
Nodes (14): _Sessions, SecureSession, Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send() (+6 more)

### Community 14 - "sessions.py"
Cohesion: 0.10
Nodes (18): derive_session_key(), SecureSession, SessionAccessError, SessionState, _decode_ciphertext(), _error(), _establish(), establish_session() (+10 more)

### Community 16 - "PqcMetrics"
Cohesion: 0.07
Nodes (7): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 17 - "test_secure_transport.py"
Cohesion: 0.19
Nodes (26): SecureTransportError, _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics(), test_application_rejection_is_not_retried() (+18 more)

### Community 18 - "test_session.py"
Cohesion: 0.10
Nodes (16): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+8 more)

### Community 19 - "CloudDispatch"
Cohesion: 0.13
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions (+7 more)

### Community 20 - "SessionManager"
Cohesion: 0.10
Nodes (7): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 21 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 22 - "load_config"
Cohesion: 0.13
Nodes (23): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+15 more)

### Community 23 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (10): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent() (+2 more)

### Community 24 - "test_measure_modernized_e2e.py"
Cohesion: 0.08
Nodes (9): test_harness_rejects_invalid_sample_count(), _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed() (+1 more)

### Community 25 - "create_app"
Cohesion: 0.10
Nodes (18): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+10 more)

### Community 26 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 27 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 28 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 29 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 30 - "session_client.py"
Cohesion: 0.14
Nodes (11): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+3 more)

### Community 31 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 32 - "test_baseline_gateway_measurements"
Cohesion: 0.10
Nodes (14): test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), sleep(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence() (+6 more)

### Community 33 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 34 - "repository.py"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 35 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (14): LegacyMeasurement, LegacyMeasurementSchemaError, test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values(), test_extra_fields_are_rejected() (+6 more)

### Community 36 - "_start_contract_receiver"
Cohesion: 0.09
Nodes (10): _LegacyContractServer, _start_contract_receiver(), test_contract_receiver_rejects_extra_fields_without_retry(), test_contract_receiver_rejects_wrong_types_and_domains_without_retry(), test_data_failure_modes_rejected_or_accepted_without_retry(), test_device_controller_runs_through_fault_injections_without_crashing(), test_failure_rejections_logged_with_structured_attributes(), test_malformed_wire_body_is_400_without_retry() (+2 more)

### Community 37 - "test_sensor.py"
Cohesion: 0.13
Nodes (17): FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp() (+9 more)

### Community 38 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 39 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 40 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 41 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 42 - "load_config"
Cohesion: 0.18
Nodes (16): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+8 more)

### Community 43 - "GatewayErrorCode"
Cohesion: 0.13
Nodes (11): GatewayErrorCode, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap(), test_gap_is_logged_and_advances_state() (+3 more)

### Community 44 - "test_gateway_measurements.py"
Cohesion: 0.16
Nodes (14): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline() (+6 more)

### Community 45 - "Sensor"
Cohesion: 0.10
Nodes (7): Sensor, test_domain_measurement_immutability_under_failure_injection(), test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), test_strict_absence_of_simulation_metadata_on_wire(), test_multiple_sensor_instances_maintain_independent_monotonic_sequences(), test_device_controller_discards_failed_measurement_and_advances_sequence()

### Community 46 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 47 - "measurements.py"
Cohesion: 0.14
Nodes (3): MeasurementProcessor, GatewayMetrics, SequenceTracker

### Community 48 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 49 - "Config"
Cohesion: 0.14
Nodes (10): Config, main(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory() (+2 more)

### Community 50 - "test_client.py"
Cohesion: 0.22
Nodes (11): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff(), test_retry_logging_exposes_failed_attempts_and_retry_events(), test_retry_stops_after_non_retryable_result() (+3 more)

### Community 51 - "test_cloud_session_api.py"
Cohesion: 0.16
Nodes (10): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), test_shutdown_and_classical_mode() (+2 more)

### Community 52 - "fields"
Cohesion: 0.17
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 53 - "test_crypto_failures.py"
Cohesion: 0.16
Nodes (11): _aad(), _injector(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault() (+3 more)

### Community 54 - "FailureMode"
Cohesion: 0.17
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 55 - "Measurement"
Cohesion: 0.13
Nodes (7): Measurement, _validate_number(), query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(), test_legacy_controller_continues_after_bounded_cloud_delivery_failure(), read()

### Community 56 - "test_legacy_gateway.py"
Cohesion: 0.27
Nodes (11): fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry(), test_injected_out_of_order_sequence_is_rejected_without_retry(), test_injected_payload_faults_are_rejected_without_retry_or_cloud_delivery() (+3 more)

### Community 57 - "plaintext.py"
Cohesion: 0.21
Nodes (11): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_device_id_whitespace_is_preserved_like_baseline_delivery() (+3 more)

### Community 58 - "_Handler"
Cohesion: 0.14
Nodes (6): _Handler, _reset_mid_body(), _Handler, _reset_mid_body(), _Handler, _reset_mid_body()

### Community 59 - "test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback"
Cohesion: 0.19
Nodes (13): _compose(), _measurement(), _metrics(), _port(), _send(), test_compose_cloud_restart_recovers_readiness_and_delivery(), test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback(), test_compose_gateway_restart_establishes_a_fresh_mlkem_session() (+5 more)

### Community 60 - "CloudMetrics"
Cohesion: 0.14
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 61 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 62 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 63 - "_Sessions"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 64 - "_start_loopback_receiver"
Cohesion: 0.12
Nodes (8): _BaselineLoopbackServer, _calculate_distribution(), _start_loopback_receiver(), test_baseline_device_controller_graceful_continuity_on_failure(), test_baseline_receiver_422_no_retries(), test_baseline_receiver_http_503_controlled_failure(), test_baseline_receiver_unavailable_bounded_retries(), test_client_loopback_workload_100_measurements()

### Community 65 - "_start_scripted_server"
Cohesion: 0.15
Nodes (8): _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout(), test_gateway_stopped_or_connection_refused(), test_transient_failure_eventual_recovery_succeeds()

### Community 66 - "test_security_mode_preserves_the_legacy_measurement_contract"
Cohesion: 0.18
Nodes (12): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+4 more)

### Community 67 - "test_cloud_baseline.py"
Cohesion: 0.16
Nodes (7): test_distinct_logical_identity_creates_second_row(), test_duplicate_and_lost_response_retry_preserve_original(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 68 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 70 - "test_static_quality.py"
Cohesion: 0.12
Nodes (7): test_legacy_ai_decisions_register_exists(), test_legacy_architecture_operations_documentation_exists(), test_legacy_technical_debt_register_exists(), test_no_cloud_or_crypto_imports_in_legacy_src(), test_no_debug_prints_or_breakpoints_in_legacy_src(), test_no_keys_or_env_files_in_legacy_system(), test_no_private_key_blocks_in_legacy_files()

### Community 71 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 72 - "build_aad"
Cohesion: 0.22
Nodes (7): AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 74 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 75 - "test_cloud_response_failures.py"
Cohesion: 0.25
Nodes (9): assert_unavailable(), Cloud, Reply, test_complete_malformed_acceptance_maps_to_503_without_retry(), test_connection_reset_while_reading_preserves_retry_policy(), open_response(), test_malformed_error_body_preserves_http_retry_classification(), test_truncated_acceptance_exhausts_the_existing_retry_bound() (+1 more)

### Community 76 - "make_config"
Cohesion: 0.23
Nodes (9): FakeSensor, make_config(), test_default_device_controller_initialization(), test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure(), test_runtime_logs_lifecycle_and_delivery_events(), stop_after_first_measurement() (+1 more)

### Community 77 - "test_gateway_crypto_image.py"
Cohesion: 0.18
Nodes (6): test_clean_container_image_runs_when_docker_is_available(), _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 78 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 80 - "errors.py"
Cohesion: 0.18
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 81 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 83 - "test_gateway_correlation.py"
Cohesion: 0.23
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 84 - "_Clock"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 85 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 86 - "ErrorCategory"
Cohesion: 0.18
Nodes (8): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable(), test_unserializable_payload_is_non_retryable()

### Community 87 - "GatewayClient"
Cohesion: 0.21
Nodes (3): GatewayClient, GatewayResult, test_theoretical_retry_amplification_product_is_explicit_and_bounded()

### Community 88 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 89 - "run"
Cohesion: 0.15
Nodes (6): distribution(), _metrics(), _persisted_rows(), run(), _sample(), TimedRepository

### Community 90 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 91 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 92 - "test_gateway_application_failures.py"
Cohesion: 0.23
Nodes (7): test_cloud_fault_uses_existing_retries(), session(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 93 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 94 - "RecordingClient"
Cohesion: 0.18
Nodes (5): RecordingClient, RecordingFailureInjector, test_controller_run_in_background_thread_skips_signal_handling(), test_delivery_failure_does_not_stop_loop_or_roll_back_sequence(), test_runtime_pipeline_serializes_before_failure_injection_and_sends()

### Community 95 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 96 - "parse_public_key_response"
Cohesion: 0.29
Nodes (7): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), reject_public_key()

### Community 97 - "test_gateway_application_metrics.py"
Cohesion: 0.25
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 98 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 99 - "test_static_checks.py"
Cohesion: 0.29
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 100 - "test_shutdown_after_gateway_unavailable_delivery"
Cohesion: 0.22
Nodes (4): test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown(), fake_signal()

### Community 101 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 103 - "routes.py"
Cohesion: 0.27
Nodes (3): SecurityMode, baseline_measurement(), _error()

### Community 104 - "normalize"
Cohesion: 0.24
Nodes (4): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input()

### Community 105 - "CloudDeliveryError"
Cohesion: 0.25
Nodes (5): CloudDeliveryError, _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 107 - "test_gateway_operations.py"
Cohesion: 0.28
Nodes (4): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 108 - "test_falsey_injected_dependencies_are_preserved"
Cohesion: 0.22
Nodes (5): FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, test_falsey_injected_dependencies_are_preserved()

### Community 109 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.28
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 110 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 111 - "queries.py"
Cohesion: 0.46
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 112 - "_secure_transport"
Cohesion: 0.25
Nodes (3): _secure_transport(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 115 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 116 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 117 - "normalize_artifacts"
Cohesion: 0.32
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 118 - "StartupError"
Cohesion: 0.29
Nodes (3): StartupError, fail(), test_session_initialization_failure_releases_keys()

### Community 119 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 123 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 124 - "test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression"
Cohesion: 0.29
Nodes (3): test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression(), read(), test_sequence_gap_is_accepted_and_logged()

### Community 125 - "test_legacy_mode_success_compatibility.py"
Cohesion: 0.43
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 126 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 127 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 129 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 130 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 131 - "test_configured_failure_never_bypasses_domain_validation"
Cohesion: 0.40
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 136 - "test_client_exception_is_logged_then_loop_continues_and_closes"
Cohesion: 0.33
Nodes (4): RaisingClient, test_client_exception_is_logged_then_loop_continues_and_closes(), test_stop_during_delivery_skips_interval_wait(), send()

### Community 138 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 146 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 148 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1051 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **69 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_gateway_cloud_secure.py`, `edge_gateway/app.py`, `derive_session_key`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`, `test_public_key_client.py`, `SecureSession`, `PqcMetrics`, `test_session.py`, `create_app`, `session_client.py`, `encapsulate`, `test_crypto_failures.py`, `test_legacy_gateway.py`, `CryptoFailureInjector`, `test_handshake_failure_stays_closed_without_a_session`, `test_session_expiry_system.py`, `test_gateway_application_failures.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `_secure_transport`, `main`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `edge_gateway/app.py`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`, `create_app`, `SecureSession`, `PqcMetrics`, `test_secure_transport.py`, `CloudDispatch`, `SessionManager`, `edge_gateway/crypto/symmetric.py`, `measurements.py`, `test_crypto_failures.py`, `test_legacy_gateway.py`, `plaintext.py`, `edge_gateway/crypto/encoding.py`, `_Sessions`, `build_aad`, `CryptoFailureInjector`, `test_handshake_failure_stays_closed_without_a_session`, `test_session_expiry_system.py`, `test_gateway_application_failures.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `_secure_transport`, `main`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `test_baseline_client.py`, `edge_gateway/app.py`, `test_configured_failure_never_bypasses_domain_validation`, `SecureTransport`, `_Gateway`, `SecureSession`, `PqcMetrics`, `test_secure_transport.py`, `CloudDispatch`, `test_baseline_gateway_measurements`, `LegacyMeasurement`, `load_config`, `GatewayErrorCode`, `test_gateway_measurements.py`, `test_lifespan_closes_baseline_and_rejects_late_requests`, `measurements.py`, `test_legacy_gateway.py`, `test_gateway_validation.py`, `edge_gateway/validation.py`, `test_gateway_routes.py`, `test_gateway_application_failures.py`, `test_gateway_response_mapping.py`, `test_gateway_application_metrics.py`, `test_gateway_operations.py`, `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `_secure_transport`, `GatewayError`, `ApplicationFailures`, `test_body_limit_before_sequence_and_delivery`, `_baseline_transport`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 63 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._