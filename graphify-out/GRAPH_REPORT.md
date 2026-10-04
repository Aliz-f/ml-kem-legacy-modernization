# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2915 nodes · 7290 edges · 158 communities (105 shown, 53 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1040 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_cloud_secure.py
- DeviceController
- measurements.py
- test_legacy_gateway.py
- create_app
- edge_gateway/app.py
- test_gateway_cloud_secure.py
- LegacyMeasurement
- cli.py
- load_config
- secure_transport.py
- pytest
- load_config
- FailureMode
- FailureMode
- MeasurementRepository
- cloud_service/app.py
- test_public_key_client.py
- log_security
- encapsulate
- SessionManager
- SessionManager
- test_gateway_measurements.py
- Sensor
- test_secure_transport.py
- test_gateway_validation.py
- CryptoFailureInjector
- SecureTransport
- run
- edge_gateway/crypto/symmetric.py
- test_cloud_session_api.py
- CanonicalMeasurement
- FailureInjector
- test_dispatch.py
- test_baseline_gateway_measurements
- test_sensor.py
- test_mode_evaluation.py
- test_static_quality.py
- SecureSession
- test_network_failures.py
- test_secure_message_tamper.py
- validate_measurement
- log_application
- edge_gateway/crypto/encoding.py
- session_client.py
- test_session.py
- StoredMeasurement
- test_legacy_compatibility.py
- test_client.py
- fields
- test_measure_modernized_e2e.py
- test_cloud_baseline.py
- edge_gateway/crypto/envelope.py
- test_baseline_client.py
- test_gateway_compose_e2e.py
- measure_modernized_e2e.py
- CloudMetrics
- test_cloud_response_failures.py
- test_failure_safety.py
- sessions.py
- _Sessions
- test_docker_assets.py
- test_cloud_kdf.py
- _start_loopback_receiver
- test_cloud_queries.py
- BaselineCloudError
- test_crypto_failures.py
- build_aad
- cloud_service/crypto/mlkem.py
- parse_public_key_response
- test_gateway_correlation.py
- test_gateway_routes.py
- ErrorCategory
- GatewayClient
- test_session_expiry_system.py
- test_cloud_public_key.py
- test_gateway_application_metrics.py
- BaselineCloudClient
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- test_handshake_counter_shows_reuse_then_expiry
- derive_session_key
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- test_secure_envelope.py
- _Clock
- test_static_checks.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- _Server
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- clean_container_crypto.py
- _Clock
- KeyService
- _HandshakeHandler
- test_dependency_review.py
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- queries.py
- KdfError
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- _Cloud
- cloud_service/crypto/kdf.py
- _Handler
- _LegacyContractReceiver
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- test_final_secure_transport_review.py
- _Handler
- _BaselineLoopbackReceiver
- _ScriptedNetworkHandler
- live_cloud
- _Gateway
- test_shared_integration_assets.py
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- _deliver
- test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries
- _Handler
- _Cloud
- test_multiple_device_controllers_deliver_independently_to_gateway_interface
- TimedRepository
- test_gateway_crypto_ci.py
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 87 edges
2. `load_config()` - 83 edges
3. `GatewayClient` - 71 edges
4. `FailureMode` - 62 edges
5. `SecureTransport` - 56 edges
6. `load_config()` - 52 edges
7. `create_app()` - 50 edges
8. `FailureMode` - 49 edges
9. `FailureInjector` - 48 edges
10. `SessionManager` - 46 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `open_response()` --indirect_call--> `status()`  [INFERRED]
  edge_gateway/tests/test_cloud_response_failures.py → src/ai_history/cli.py

## Import Cycles
- None detected.

## Communities (158 total, 53 thin omitted)

### Community 0 - "test_cloud_secure.py"
Cohesion: 0.05
Nodes (48): decode_binary(), encode_binary(), EncodingError, EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object() (+40 more)

### Community 1 - "DeviceController"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 2 - "measurements.py"
Cohesion: 0.05
Nodes (27): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, GatewayMetrics, SequenceTracker, CloudTransport, client() (+19 more)

### Community 3 - "test_legacy_gateway.py"
Cohesion: 0.05
Nodes (33): Measurement, _validate_number(), _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model() (+25 more)

### Community 4 - "create_app"
Cohesion: 0.06
Nodes (41): create_app(), _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl() (+33 more)

### Community 5 - "edge_gateway/app.py"
Cohesion: 0.04
Nodes (12): _baseline_transport(), get_config(), _secure_transport(), GatewayConfig, _Duration, PqcMetrics, BaselineTransport, CloudDispatch (+4 more)

### Community 6 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 7 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (32): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+24 more)

### Community 8 - "cli.py"
Cohesion: 0.13
Nodes (41): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+33 more)

### Community 9 - "load_config"
Cohesion: 0.07
Nodes (36): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+28 more)

### Community 10 - "secure_transport.py"
Cohesion: 0.08
Nodes (5): _token(), corrupt_ciphertext_copy(), _endpoint(), CloudDeliveryError, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 11 - "pytest"
Cohesion: 0.05
Nodes (13): test_gateway_process_exits_cleanly_on_signal(), clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install() (+5 more)

### Community 13 - "load_config"
Cohesion: 0.09
Nodes (30): Config, ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), main() (+22 more)

### Community 14 - "FailureMode"
Cohesion: 0.10
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 15 - "FailureMode"
Cohesion: 0.13
Nodes (27): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+19 more)

### Community 16 - "MeasurementRepository"
Cohesion: 0.10
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 17 - "cloud_service/app.py"
Cohesion: 0.08
Nodes (11): SecurityMode, AeadError, decrypt(), public_key(), _unavailable(), _DroppedResponse, _error(), _ingest() (+3 more)

### Community 18 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (20): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+12 more)

### Community 19 - "log_security"
Cohesion: 0.08
Nodes (13): build_secure_envelope(), SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport (+5 more)

### Community 20 - "encapsulate"
Cohesion: 0.09
Nodes (15): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe(), encapsulate(), MlKemError, validate_public_key() (+7 more)

### Community 21 - "SessionManager"
Cohesion: 0.07
Nodes (7): clock(), SessionEstablishmentError, SessionManager, test_invalid_failure_rate_is_rejected(), test_session_missing_and_expired_force_a_new_handshake(), _run(), test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 22 - "SessionManager"
Cohesion: 0.10
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 23 - "test_gateway_measurements.py"
Cohesion: 0.11
Nodes (20): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_processing_fault_is_visible_and_preserves_sequence() (+12 more)

### Community 24 - "Sensor"
Cohesion: 0.07
Nodes (12): Sensor, _LegacyContractServer, _start_contract_receiver(), test_contract_receiver_rejects_extra_fields_without_retry(), test_contract_receiver_rejects_wrong_types_and_domains_without_retry(), test_data_failure_modes_rejected_or_accepted_without_retry(), test_device_controller_runs_through_fault_injections_without_crashing(), test_failure_rejections_logged_with_structured_attributes() (+4 more)

### Community 25 - "test_secure_transport.py"
Cohesion: 0.22
Nodes (24): SecureTransportError, _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics(), test_application_rejection_is_not_retried(), test_connection_reset_while_reading_retries_the_same_envelope() (+16 more)

### Community 26 - "test_gateway_validation.py"
Cohesion: 0.12
Nodes (19): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client(), payload() (+11 more)

### Community 27 - "CryptoFailureInjector"
Cohesion: 0.09
Nodes (7): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _Baseline, _count(), test_handshake_failure_stays_closed_without_a_session()

### Community 28 - "SecureTransport"
Cohesion: 0.09
Nodes (11): SecureTransport, _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+3 more)

### Community 30 - "run"
Cohesion: 0.08
Nodes (15): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+7 more)

### Community 31 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 32 - "test_cloud_session_api.py"
Cohesion: 0.12
Nodes (13): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_metrics_excludes_expired_sessions_after_replacement(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+5 more)

### Community 33 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 34 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 35 - "test_dispatch.py"
Cohesion: 0.18
Nodes (13): _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 36 - "test_baseline_gateway_measurements"
Cohesion: 0.10
Nodes (13): cloud(), test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence() (+5 more)

### Community 37 - "test_sensor.py"
Cohesion: 0.13
Nodes (17): FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp() (+9 more)

### Community 38 - "test_mode_evaluation.py"
Cohesion: 0.14
Nodes (9): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Sizes, test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline() (+1 more)

### Community 39 - "test_static_quality.py"
Cohesion: 0.09
Nodes (8): _Handler, test_legacy_ai_decisions_register_exists(), test_legacy_architecture_operations_documentation_exists(), test_legacy_technical_debt_register_exists(), test_no_cloud_or_crypto_imports_in_legacy_src(), test_no_debug_prints_or_breakpoints_in_legacy_src(), test_no_keys_or_env_files_in_legacy_system(), test_no_private_key_blocks_in_legacy_files()

### Community 40 - "SecureSession"
Cohesion: 0.10
Nodes (7): SecureSession, Sessions, _Sessions, session(), _session(), get_or_establish(), get_or_establish()

### Community 41 - "test_network_failures.py"
Cohesion: 0.14
Nodes (9): _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_device_controller_discards_failed_measurement_and_advances_sequence(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout(), test_gateway_stopped_or_connection_refused() (+1 more)

### Community 42 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 43 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 44 - "log_application"
Cohesion: 0.12
Nodes (15): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements(), ready() (+7 more)

### Community 45 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.16
Nodes (10): decode_binary(), encode_binary(), EncodingError, _HandshakeCloud, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip() (+2 more)

### Community 46 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 47 - "test_session.py"
Cohesion: 0.16
Nodes (12): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_connection_reset_during_session_post_is_retryable(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced() (+4 more)

### Community 48 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 49 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 50 - "test_client.py"
Cohesion: 0.22
Nodes (11): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff(), test_retry_logging_exposes_failed_attempts_and_retry_events(), test_retry_stops_after_non_retryable_result() (+3 more)

### Community 51 - "fields"
Cohesion: 0.17
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 52 - "test_measure_modernized_e2e.py"
Cohesion: 0.12
Nodes (6): test_harness_rejects_invalid_sample_count(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 53 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_duplicate_and_lost_response_retry_preserve_original(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 55 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.18
Nodes (11): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_device_id_whitespace_is_preserved_like_baseline_delivery() (+3 more)

### Community 56 - "test_baseline_client.py"
Cohesion: 0.25
Nodes (16): _client(), _send(), test_attempt_metrics_include_retry_and_invalid_acceptance(), test_baseline_shutdown_waits_for_attempt_and_closes_once(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request() (+8 more)

### Community 57 - "test_gateway_compose_e2e.py"
Cohesion: 0.23
Nodes (13): _compose(), _measurement(), _metrics(), _port(), _send(), test_compose_cloud_restart_recovers_readiness_and_delivery(), test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback(), test_compose_gateway_restart_establishes_a_fresh_mlkem_session() (+5 more)

### Community 58 - "measure_modernized_e2e.py"
Cohesion: 0.14
Nodes (8): _load(), run(), distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve()

### Community 59 - "CloudMetrics"
Cohesion: 0.13
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 60 - "test_cloud_response_failures.py"
Cohesion: 0.18
Nodes (10): assert_unavailable(), Cloud, Handler, Reply, test_complete_malformed_acceptance_maps_to_503_without_retry(), test_connection_reset_while_reading_preserves_retry_policy(), open_response(), test_malformed_error_body_preserves_http_retry_classification() (+2 more)

### Community 61 - "test_failure_safety.py"
Cohesion: 0.12
Nodes (7): test_default_configuration_failure_injection_disabled(), test_domain_measurement_immutability_under_failure_injection(), test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), test_strict_absence_of_simulation_metadata_on_wire()

### Community 62 - "sessions.py"
Cohesion: 0.18
Nodes (10): health(), ready(), _crypto_dependencies_ready(), _unavailable(), derive_session_key(), _decode_ciphertext(), _error(), _establish() (+2 more)

### Community 63 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 64 - "test_docker_assets.py"
Cohesion: 0.11
Nodes (3): test_compose_empty_failure_seed_keeps_legacy_selection_nondeterministic(), test_compose_environment_loads_valid_legacy_config(), test_compose_environment_with_custom_failure_settings_loads_valid_legacy_config()

### Community 65 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 66 - "_start_loopback_receiver"
Cohesion: 0.12
Nodes (8): _BaselineLoopbackServer, _calculate_distribution(), _start_loopback_receiver(), test_baseline_device_controller_graceful_continuity_on_failure(), test_baseline_receiver_422_no_retries(), test_baseline_receiver_http_503_controlled_failure(), test_baseline_receiver_unavailable_bounded_retries(), test_client_loopback_workload_100_measurements()

### Community 67 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 68 - "BaselineCloudError"
Cohesion: 0.18
Nodes (6): BaselineAcceptance, BaselineCloudError, _dump(), _error_code(), _parse_acceptance(), _RejectRedirect

### Community 69 - "test_crypto_failures.py"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), measurement_url(), _MeasurementCloud, test_same_seed_makes_the_same_decisions()

### Community 70 - "build_aad"
Cohesion: 0.22
Nodes (7): AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 71 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 72 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 73 - "test_gateway_correlation.py"
Cohesion: 0.23
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 74 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 75 - "ErrorCategory"
Cohesion: 0.18
Nodes (8): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable(), test_unserializable_payload_is_non_retryable()

### Community 76 - "GatewayClient"
Cohesion: 0.21
Nodes (3): GatewayClient, GatewayResult, test_theoretical_retry_amplification_product_is_explicit_and_bounded()

### Community 77 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 78 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 79 - "test_gateway_application_metrics.py"
Cohesion: 0.23
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 80 - "BaselineCloudClient"
Cohesion: 0.18
Nodes (5): BaselineCloudClient, _endpoint(), _live_gateway(), test_real_gateway_failure_chain_is_bounded_by_committed_sequence_state(), unavailable()

### Community 81 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 82 - "test_handshake_counter_shows_reuse_then_expiry"
Cohesion: 0.18
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 83 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 84 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.22
Nodes (8): _aad(), _injector(), _plaintext(), test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_rate_one_selects_only_the_configured_mode()

### Community 85 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 86 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 87 - "test_static_checks.py"
Cohesion: 0.29
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 88 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 89 - "_Server"
Cohesion: 0.18
Nodes (3): cloud(), LiveCloud, _Server

### Community 91 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 92 - "clean_container_crypto.py"
Cohesion: 0.29
Nodes (3): _install(), main(), _serve()

### Community 93 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 94 - "KeyService"
Cohesion: 0.22
Nodes (3): lifespan(), StartupError, KeyService

### Community 96 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 97 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.28
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 98 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 99 - "queries.py"
Cohesion: 0.46
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 100 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 101 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 102 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 107 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 110 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 116 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 123 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 125 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

### Community 130 - "_deliver"
Cohesion: 0.50
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 131 - "test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries"
Cohesion: 0.40
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1055 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **53 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_legacy_gateway.py`, `edge_gateway/app.py`, `test_gateway_cloud_secure.py`, `load_config`, `secure_transport.py`, `test_public_key_client.py`, `encapsulate`, `test_gateway_measurements.py`, `CryptoFailureInjector`, `SecureTransport`, `test_mode_evaluation.py`, `session_client.py`, `test_session.py`, `parse_public_key_response`, `test_session_expiry_system.py`, `test_handshake_counter_shows_reuse_then_expiry`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `clean_container_crypto.py`, `KdfError`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `measurements.py`, `test_legacy_gateway.py`, `test_baseline_gateway_measurements`, `edge_gateway/app.py`, `test_body_limit_before_sequence_and_delivery`, `LegacyMeasurement`, `test_gateway_validation_bypass.py`, `test_gateway_routes.py`, `log_application`, `test_gateway_application_metrics.py`, `BaselineCloudClient`, `_Gateway`, `test_gateway_measurements.py`, `test_secure_transport.py`, `test_gateway_validation.py`, `SecureTransport`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `SecureSession` connect `SecureSession` to `test_dispatch.py`, `secure_transport.py`, `test_session.py`, `log_security`, `SessionManager`, `test_secure_transport.py`, `SecureTransport`, `_Sessions`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 63 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._