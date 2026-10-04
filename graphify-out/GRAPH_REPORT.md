# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2717 nodes · 6855 edges · 180 communities (113 shown, 67 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 940 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_device.py
- cli.py
- test_gateway_cloud_secure.py
- test_baseline_client.py
- test_sensor.py
- derive_session_key
- test_gateway_crypto_image.py
- secure_transport.py
- pathlib
- edge_gateway/app.py
- MeasurementRepository
- SecureSession
- cloud_service/app.py
- SecureTransport
- FailureMode
- SessionManager
- test_public_key_client.py
- test_secure_transport.py
- CloudDispatch
- PqcMetrics
- test_session.py
- SessionManager
- secure.py
- test_cloud_secure.py
- test_measure_modernized_e2e.py
- create_app
- edge_gateway/crypto/symmetric.py
- CanonicalMeasurement
- test_secure_message_tamper.py
- legacy_system/config.py
- encode_binary
- load_config
- FailureInjector
- encapsulate
- create_app
- LegacyMeasurement
- SecureEnvelope
- measurements.py
- test_gateway_measurements.py
- live_gateway
- validate_measurement
- load_config
- session_client.py
- GatewayError
- StoredMeasurement
- test_cloud_baseline.py
- test_cloud_failure_injection.py
- CanonicalMeasurement
- test_crypto_failures.py
- test_client.py
- FailureMode
- test_secure_shutdown.py
- edge_gateway/crypto/encoding.py
- edge_gateway/crypto/envelope.py
- CryptoFailureInjector
- build_aad
- test_gateway_app.py
- test_cloud_kdf.py
- CloudMetrics
- fields
- test_cloud_queries.py
- test_gateway_validation.py
- Config
- run
- test_gateway_correlation.py
- edge_gateway/validation.py
- test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback
- _dispatch
- cloud_service/crypto/mlkem.py
- test_handshake_failure_stays_closed_without_a_session
- GatewayClient
- test_cloud_mlkem.py
- parse_public_key_response
- _Clock
- test_gateway_routes.py
- ErrorCategory
- run
- test_session_expiry_system.py
- test_cloud_public_key.py
- live_cloud
- test_gateway_errors.py
- test_gateway_response_mapping.py
- envelope_validation.py
- handshake
- test_secure_envelope.py
- run
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- _baseline_transport
- normalize
- CloudDeliveryError
- test_gateway_application_failures.py
- _HandshakeHandler
- test_gateway_operations.py
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- LiveCloud
- _secure_transport
- GatewayErrorCode
- ApplicationFailures
- test_baseline_gateway_measurements
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- test_fixtures.py
- test_handshake_counter_shows_reuse_then_expiry
- StartupError
- establish_session
- main
- test_untrusted_values_do_not_create_metric_labels
- _Handler
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_session_reuse_system.py
- test_repository_hygiene.py
- _crypto_dependencies_ready
- get_measurement
- test_final_secure_transport_review.py
- _Handler
- _Handler
- .apply
- Measurement
- _Sizes
- test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row
- live_cloud
- _Gateway
- _Server
- test_shared_integration_assets.py
- baseline_measurement
- CloudTransport
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- test_sequence_state_timing_awareness_no_rollback_on_downstream_failure
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- edge_gateway/models.py
- TimedRepository
- test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression
- _deliver
- test_gateway_crypto_ci.py
- test_faults_preserve_real_cloud_storage_and_mode_boundaries
- test_lifespan_closes_baseline_and_rejects_late_requests
- payload
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 86 edges
2. `load_config()` - 82 edges
3. `SecureTransport` - 55 edges
4. `GatewayClient` - 55 edges
5. `load_config()` - 51 edges
6. `create_app()` - 49 edges
7. `FailureMode` - 48 edges
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
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression()` --uses--> `DeviceController`  [INFERRED]
  tests/integration/test_legacy_gateway.py → legacy_system/src/legacy_system/device.py

## Import Cycles
- None detected.

## Communities (180 total, 67 thin omitted)

### Community 0 - "test_device.py"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 1 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 3 - "test_baseline_client.py"
Cohesion: 0.08
Nodes (30): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+22 more)

### Community 4 - "test_sensor.py"
Cohesion: 0.06
Nodes (30): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values() (+22 more)

### Community 5 - "derive_session_key"
Cohesion: 0.06
Nodes (17): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+9 more)

### Community 6 - "test_gateway_crypto_image.py"
Cohesion: 0.06
Nodes (18): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+10 more)

### Community 9 - "edge_gateway/app.py"
Cohesion: 0.09
Nodes (3): get_config(), GatewayConfig, test_gateway_process_exits_cleanly_on_signal()

### Community 10 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 11 - "SecureSession"
Cohesion: 0.07
Nodes (14): _endpoint(), _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send() (+6 more)

### Community 12 - "cloud_service/app.py"
Cohesion: 0.11
Nodes (4): SecurityMode, derive_session_key(), public_key(), _unavailable()

### Community 13 - "SecureTransport"
Cohesion: 0.09
Nodes (9): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport (+1 more)

### Community 14 - "FailureMode"
Cohesion: 0.17
Nodes (26): FailureMode, FailureInjector, make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+18 more)

### Community 15 - "SessionManager"
Cohesion: 0.09
Nodes (10): clock(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run() (+2 more)

### Community 16 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+11 more)

### Community 17 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 18 - "CloudDispatch"
Cohesion: 0.12
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions (+7 more)

### Community 19 - "PqcMetrics"
Cohesion: 0.07
Nodes (7): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 20 - "test_session.py"
Cohesion: 0.10
Nodes (16): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+8 more)

### Community 21 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 22 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 23 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 24 - "test_measure_modernized_e2e.py"
Cohesion: 0.08
Nodes (9): test_harness_rejects_invalid_sample_count(), _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed() (+1 more)

### Community 25 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+10 more)

### Community 26 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 27 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 28 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 29 - "legacy_system/config.py"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 30 - "encode_binary"
Cohesion: 0.13
Nodes (9): decode_binary(), encode_binary(), EncodingError, KeyService, _decode_ciphertext(), test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo() (+1 more)

### Community 31 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 32 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 33 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 34 - "create_app"
Cohesion: 0.13
Nodes (17): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements() (+9 more)

### Community 35 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (14): LegacyMeasurement, LegacyMeasurementSchemaError, test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values(), test_extra_fields_are_rejected() (+6 more)

### Community 36 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 37 - "measurements.py"
Cohesion: 0.13
Nodes (4): MeasurementProcessor, GatewayMetrics, SequenceTracker, test_registry_updates_are_thread_safe_and_instances_are_isolated()

### Community 38 - "test_gateway_measurements.py"
Cohesion: 0.15
Nodes (15): test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario() (+7 more)

### Community 39 - "live_gateway"
Cohesion: 0.16
Nodes (13): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry(), test_injected_out_of_order_sequence_is_rejected_without_retry() (+5 more)

### Community 40 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 41 - "load_config"
Cohesion: 0.18
Nodes (16): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+8 more)

### Community 42 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 43 - "GatewayError"
Cohesion: 0.13
Nodes (11): GatewayError, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap(), test_gap_is_logged_and_advances_state() (+3 more)

### Community 44 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 45 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 46 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 47 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 48 - "test_crypto_failures.py"
Cohesion: 0.15
Nodes (11): _aad(), _injector(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault() (+3 more)

### Community 49 - "test_client.py"
Cohesion: 0.22
Nodes (11): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff(), test_retry_logging_exposes_failed_attempts_and_retry_events(), test_retry_stops_after_non_retryable_result() (+3 more)

### Community 50 - "FailureMode"
Cohesion: 0.16
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 51 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 52 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 53 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.19
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 55 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 56 - "test_gateway_app.py"
Cohesion: 0.12
Nodes (12): _logging_level(), main(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_mlkem_readiness_requires_initialized_transport_but_not_active_session() (+4 more)

### Community 57 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 58 - "CloudMetrics"
Cohesion: 0.14
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 59 - "fields"
Cohesion: 0.22
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 60 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 61 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 62 - "Config"
Cohesion: 0.19
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 63 - "run"
Cohesion: 0.16
Nodes (11): test_existing_gateway_session_client_over_real_http(), canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run() (+3 more)

### Community 65 - "test_gateway_correlation.py"
Cohesion: 0.19
Nodes (7): baseline_headers(), create_request_id(), build_secure_envelope(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 66 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 67 - "test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback"
Cohesion: 0.23
Nodes (11): _compose(), _measurement(), _metrics(), _port(), _send(), test_compose_cloud_restart_recovers_readiness_and_delivery(), test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback(), test_compose_gateway_restart_establishes_a_fresh_mlkem_session() (+3 more)

### Community 68 - "_dispatch"
Cohesion: 0.20
Nodes (8): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 69 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 71 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 72 - "GatewayClient"
Cohesion: 0.21
Nodes (3): GatewayClient, GatewayResult, test_theoretical_retry_amplification_product_is_explicit_and_bounded()

### Community 73 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 74 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 75 - "_Clock"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 76 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 77 - "ErrorCategory"
Cohesion: 0.18
Nodes (8): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable(), test_unserializable_payload_is_non_retryable()

### Community 78 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 79 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 80 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 81 - "live_cloud"
Cohesion: 0.20
Nodes (7): test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(), test_legacy_to_sqlite_preserves_gateway_transformations()

### Community 82 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 83 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 84 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 85 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 86 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 87 - "run"
Cohesion: 0.18
Nodes (6): distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve()

### Community 88 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 90 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 91 - "_baseline_transport"
Cohesion: 0.20
Nodes (3): _baseline_transport(), BaselineTransport, UnavailableBaseline

### Community 92 - "normalize"
Cohesion: 0.24
Nodes (4): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input()

### Community 93 - "CloudDeliveryError"
Cohesion: 0.22
Nodes (5): CloudDeliveryError, _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 94 - "test_gateway_application_failures.py"
Cohesion: 0.29
Nodes (5): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 96 - "test_gateway_operations.py"
Cohesion: 0.28
Nodes (4): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 97 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.28
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 98 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 100 - "_secure_transport"
Cohesion: 0.25
Nodes (3): _secure_transport(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 103 - "test_baseline_gateway_measurements"
Cohesion: 0.25
Nodes (4): cloud(), test_baseline_gateway_measurements(), _post(), send()

### Community 104 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 105 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 106 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 107 - "test_handshake_counter_shows_reuse_then_expiry"
Cohesion: 0.29
Nodes (5): _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 108 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 109 - "establish_session"
Cohesion: 0.52
Nodes (4): _error(), _establish(), establish_session(), session_access_error_handler()

### Community 110 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 111 - "test_untrusted_values_do_not_create_metric_labels"
Cohesion: 0.33
Nodes (4): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 113 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 114 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 115 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 117 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 118 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 119 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 127 - "test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row"
Cohesion: 0.33
Nodes (3): query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row()

### Community 128 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 137 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 139 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

### Community 156 - "_deliver"
Cohesion: 0.67
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 959 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **67 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app` to `_Gateway`, `test_baseline_client.py`, `edge_gateway/app.py`, `SecureSession`, `SecureTransport`, `test_secure_transport.py`, `CloudDispatch`, `PqcMetrics`, `LegacyMeasurement`, `measurements.py`, `test_faults_preserve_real_cloud_storage_and_mode_boundaries`, `test_gateway_measurements.py`, `test_lifespan_closes_baseline_and_rejects_late_requests`, `load_config`, `live_gateway`, `GatewayError`, `test_gateway_app.py`, `test_gateway_validation.py`, `edge_gateway/validation.py`, `test_gateway_routes.py`, `live_cloud`, `test_gateway_response_mapping.py`, `_baseline_transport`, `test_gateway_application_failures.py`, `test_gateway_operations.py`, `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `_secure_transport`, `GatewayErrorCode`, `ApplicationFailures`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_validation_bypass.py`, `test_untrusted_values_do_not_create_metric_labels`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `secure_transport.py`, `edge_gateway/app.py`, `SecureSession`, `SessionManager`, `test_secure_transport.py`, `CloudDispatch`, `PqcMetrics`, `edge_gateway/crypto/symmetric.py`, `create_app`, `measurements.py`, `live_gateway`, `test_crypto_failures.py`, `test_secure_shutdown.py`, `edge_gateway/crypto/encoding.py`, `edge_gateway/crypto/envelope.py`, `CryptoFailureInjector`, `build_aad`, `_dispatch`, `test_handshake_failure_stays_closed_without_a_session`, `test_session_expiry_system.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_gateway_application_failures.py`, `_secure_transport`, `test_handshake_counter_shows_reuse_then_expiry`, `main`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `create_app`, `_secure_transport`, `_dispatch`, `ApplicationFailures`, `secure_transport.py`, `test_handshake_failure_stays_closed_without_a_session`, `edge_gateway/app.py`, `SecureSession`, `test_handshake_counter_shows_reuse_then_expiry`, `SecureTransport`, `SessionManager`, `test_session_expiry_system.py`, `test_secure_transport.py`, `CloudDispatch`, `CryptoFailureInjector`, `run`, `test_corrupted_ciphertext_is_rejected_and_not_stored`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05258033106134372 - nodes in this community are weakly interconnected._