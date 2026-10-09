# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 3001 nodes · 7446 edges · 177 communities (111 shown, 66 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1044 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- create_app
- DeviceController
- test_baseline_client.py
- cli.py
- test_gateway_cloud_secure.py
- test_cloud_secure.py
- test_session.py
- load_config
- SessionManager
- FailureMode
- cloud_service/app.py
- FailureMode
- MeasurementRepository
- test_crypto_failures.py
- test_public_key_client.py
- SecureTransport
- secure_transport.py
- SessionManager
- dashboard/app.py
- PqcMetrics
- CloudDispatch
- fastapi_testclient
- sensor.py
- app.js
- edge_gateway/crypto/symmetric.py
- log_security
- test_secure_transport.py
- CanonicalMeasurement
- load_config
- test_legacy_compatibility.py
- test_cloud_response_failures.py
- Sensor
- test_failure_simulation.py
- FailureInjector
- test_secure_message_tamper.py
- secure.py
- pytest
- test_cloud_session_api.py
- edge_gateway/crypto/encoding.py
- SecureSession
- test_baseline_measurements.py
- repository.py
- encapsulate
- edge_gateway/config.py
- GatewayError
- measurements.py
- test_network_failures.py
- validate_measurement
- fields
- session_client.py
- LegacyMeasurement
- test_cloud_public_key.py
- CanonicalMeasurement
- test_client.py
- test_cloud_baseline.py
- build_aad
- test_gateway_compose_e2e.py
- encode_binary
- CloudMetrics
- test_gateway_transport_interface.py
- Config
- Measurement
- test_failure_safety.py
- test_legacy_gateway.py
- log_application
- plaintext.py
- test_mode_evaluation.py
- test_static_quality.py
- test_cloud_kdf.py
- edge_gateway/models.py
- test_gateway_validation.py
- test_docker_assets.py
- test_cloud_queries.py
- ErrorCategory
- cloud_service/crypto/mlkem.py
- run
- parse_public_key_response
- test_cloud_mlkem.py
- test_gateway_routes.py
- GatewayClient
- test_pqc_observability.py
- test_session_expiry_system.py
- test_clean_container_crypto.py
- run_evaluation.py
- test_dashboard.py
- test_gateway_errors.py
- test_gateway_crypto_image.py
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- GatewayErrorCode
- derive_session_key
- test_secure_envelope.py
- test_static_checks.py
- run
- refresh_graphify.py
- _baseline_transport
- test_gateway_correlation.py
- ApplicationFailures
- edge_gateway/validation.py
- _Clock
- edge_gateway/crypto/kdf.py
- _HandshakeHandler
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- KdfError
- test_fixtures.py
- _LegacyContractReceiver
- test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_refresh_graphify.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- _install
- test_final_secure_transport_review.py
- _Handler
- _Handler
- _ScriptedNetworkHandler
- _Sizes
- _Cloud
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- live_cloud
- _Cloud
- _Server
- test_shared_integration_assets.py
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- test_sequence_state_timing_awareness_no_rollback_on_downstream_failure
- _deliver
- test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries
- .__init__
- _Handler
- _Cloud
- TimedRepository
- test_gateway_crypto_ci.py
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
4. `FailureMode` - 62 edges
5. `SecureTransport` - 56 edges
6. `load_config()` - 52 edges
7. `create_app()` - 50 edges
8. `FailureMode` - 49 edges
9. `FailureInjector` - 48 edges
10. `PqcMetrics` - 46 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `open_response()` --indirect_call--> `status()`  [INFERRED]
  edge_gateway/tests/test_cloud_response_failures.py → src/ai_history/cli.py
- `test_legacy_controller_continues_after_bounded_cloud_delivery_failure()` --uses--> `DeviceController`  [INFERRED]
  tests/integration/test_end_to_end.py → legacy_system/src/legacy_system/device.py

## Import Cycles
- None detected.

## Communities (177 total, 66 thin omitted)

### Community 0 - "create_app"
Cohesion: 0.04
Nodes (57): create_app(), _logging_level(), main(), load_config(), test_app_exports_real_baseline_attempt_metrics(), test_classical_app_constructs_and_uses_baseline_client(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests() (+49 more)

### Community 1 - "DeviceController"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 2 - "test_baseline_client.py"
Cohesion: 0.05
Nodes (39): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+31 more)

### Community 3 - "cli.py"
Cohesion: 0.09
Nodes (47): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+39 more)

### Community 5 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 6 - "test_cloud_secure.py"
Cohesion: 0.07
Nodes (41): EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+33 more)

### Community 7 - "test_session.py"
Cohesion: 0.05
Nodes (27): SessionState, _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_lifespan_runs_security_cleanup_after_stopping_work(), test_shutdown_closes_the_client_before_clearing_the_session() (+19 more)

### Community 8 - "load_config"
Cohesion: 0.07
Nodes (37): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+29 more)

### Community 9 - "SessionManager"
Cohesion: 0.06
Nodes (14): get_config(), _secure_transport(), GatewayConfig, CryptoFailureInjector, SessionManager, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _count() (+6 more)

### Community 10 - "FailureMode"
Cohesion: 0.10
Nodes (25): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+17 more)

### Community 11 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (16): health(), ready(), _crypto_dependencies_ready(), _unavailable(), SecurityMode, derive_session_key(), public_key(), _unavailable() (+8 more)

### Community 12 - "FailureMode"
Cohesion: 0.14
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+18 more)

### Community 13 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_unrelated_record_id_collision_is_not_idempotent_success(), database() (+17 more)

### Community 14 - "test_crypto_failures.py"
Cohesion: 0.08
Nodes (20): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud (+12 more)

### Community 15 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (20): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+12 more)

### Community 16 - "SecureTransport"
Cohesion: 0.10
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 17 - "secure_transport.py"
Cohesion: 0.11
Nodes (9): corrupt_ciphertext_copy(), _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback(), test_seal_failure_is_counted_without_the_session_key() (+1 more)

### Community 18 - "SessionManager"
Cohesion: 0.10
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 19 - "dashboard/app.py"
Cohesion: 0.09
Nodes (17): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), _container(), _container_info(), DashboardHandler, _decode_chunks(), _decode_logs() (+9 more)

### Community 20 - "PqcMetrics"
Cohesion: 0.06
Nodes (8): _Duration, PqcMetrics, distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve()

### Community 21 - "CloudDispatch"
Cohesion: 0.14
Nodes (13): CloudDispatch, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 22 - "fastapi_testclient"
Cohesion: 0.08
Nodes (9): test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport, test_gateway_process_exits_cleanly_on_signal(), test_lifespan_closes_baseline_and_rejects_late_requests(), test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections() (+1 more)

### Community 23 - "sensor.py"
Cohesion: 0.09
Nodes (5): test_multiple_device_controllers_deliver_independently_to_gateway_interface(), test_multiple_device_controllers_have_independent_lifecycle_state(), test_multiple_devices_configured_via_environment_without_code_changes(), test_multiple_failure_injectors_operate_independently(), test_multiple_sensor_instances_maintain_independent_monotonic_sequences()

### Community 24 - "app.js"
Cohesion: 0.12
Nodes (27): applyRuntimeConfig(), charts(), config(), configHelp, draw(), esc(), failureModes, formatMetricValue() (+19 more)

### Community 25 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 26 - "log_security"
Cohesion: 0.09
Nodes (4): _RejectRedirect, log_security(), _token(), SessionEstablishmentError

### Community 27 - "test_secure_transport.py"
Cohesion: 0.23
Nodes (23): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics(), test_application_rejection_is_not_retried(), test_connection_reset_while_reading_retries_the_same_envelope(), test_exhausted_connection_resets_fail_closed_as_retryable() (+15 more)

### Community 28 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 29 - "load_config"
Cohesion: 0.17
Nodes (20): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+12 more)

### Community 30 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 31 - "test_cloud_response_failures.py"
Cohesion: 0.12
Nodes (12): assert_unavailable(), Cloud, delivery(), Handler, Reply, Sessions, test_complete_malformed_acceptance_maps_to_503_without_retry(), test_connection_reset_while_reading_preserves_retry_policy() (+4 more)

### Community 32 - "Sensor"
Cohesion: 0.13
Nodes (18): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 33 - "test_failure_simulation.py"
Cohesion: 0.11
Nodes (10): _LegacyContractServer, _start_contract_receiver(), test_contract_receiver_rejects_extra_fields_without_retry(), test_contract_receiver_rejects_wrong_types_and_domains_without_retry(), test_data_failure_modes_rejected_or_accepted_without_retry(), test_device_controller_runs_through_fault_injections_without_crashing(), test_failure_rejections_logged_with_structured_attributes(), test_malformed_wire_body_is_400_without_retry() (+2 more)

### Community 34 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 35 - "test_secure_message_tamper.py"
Cohesion: 0.16
Nodes (13): DecryptSpy, _different_nonce(), _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection (+5 more)

### Community 36 - "secure.py"
Cohesion: 0.13
Nodes (8): AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics, secure_measurement(), fail()

### Community 37 - "pytest"
Cohesion: 0.09
Nodes (5): test_harness_rejects_invalid_sample_count(), _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads()

### Community 38 - "test_cloud_session_api.py"
Cohesion: 0.13
Nodes (13): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_metrics_excludes_expired_sessions_after_replacement(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+5 more)

### Community 39 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.13
Nodes (10): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _query_one() (+2 more)

### Community 40 - "SecureSession"
Cohesion: 0.10
Nodes (8): _Sessions, SecureSession, session(), _session(), get_or_establish(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 41 - "test_baseline_measurements.py"
Cohesion: 0.11
Nodes (8): _BaselineLoopbackReceiver, _BaselineLoopbackServer, _calculate_distribution(), _start_loopback_receiver(), test_baseline_device_controller_graceful_continuity_on_failure(), test_baseline_receiver_422_no_retries(), test_baseline_receiver_http_503_controlled_failure(), test_client_loopback_workload_100_measurements()

### Community 42 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 43 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 44 - "edge_gateway/config.py"
Cohesion: 0.17
Nodes (15): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float() (+7 more)

### Community 45 - "GatewayError"
Cohesion: 0.13
Nodes (11): GatewayError, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap(), test_gap_is_logged_and_advances_state() (+3 more)

### Community 46 - "measurements.py"
Cohesion: 0.13
Nodes (4): MeasurementProcessor, GatewayMetrics, SequenceTracker, test_registry_updates_are_thread_safe_and_instances_are_isolated()

### Community 47 - "test_network_failures.py"
Cohesion: 0.14
Nodes (9): _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_device_controller_discards_failed_measurement_and_advances_sequence(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout(), test_gateway_stopped_or_connection_refused() (+1 more)

### Community 48 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 49 - "fields"
Cohesion: 0.15
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 50 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 51 - "LegacyMeasurement"
Cohesion: 0.25
Nodes (14): LegacyMeasurement, LegacyMeasurementSchemaError, test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values(), test_extra_fields_are_rejected() (+6 more)

### Community 52 - "test_cloud_public_key.py"
Cohesion: 0.13
Nodes (11): lifespan(), StartupError, KeyService, secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail() (+3 more)

### Community 53 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 54 - "test_client.py"
Cohesion: 0.22
Nodes (11): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff(), test_retry_logging_exposes_failed_attempts_and_retry_events(), test_retry_stops_after_non_retryable_result() (+3 more)

### Community 55 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_duplicate_and_lost_response_retry_preserve_original(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+1 more)

### Community 56 - "build_aad"
Cohesion: 0.16
Nodes (9): AadError, build_aad(), _require_id(), build_secure_envelope(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected() (+1 more)

### Community 57 - "test_gateway_compose_e2e.py"
Cohesion: 0.23
Nodes (13): _compose(), _measurement(), _metrics(), _port(), _send(), test_compose_cloud_restart_recovers_readiness_and_delivery(), test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback(), test_compose_gateway_restart_establishes_a_fresh_mlkem_session() (+5 more)

### Community 58 - "encode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 59 - "CloudMetrics"
Cohesion: 0.13
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 60 - "test_gateway_transport_interface.py"
Cohesion: 0.14
Nodes (6): CloudDeliveryError, CloudTransport, _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 61 - "Config"
Cohesion: 0.16
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 62 - "Measurement"
Cohesion: 0.13
Nodes (7): Measurement, _validate_number(), query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(), test_legacy_controller_continues_after_bounded_cloud_delivery_failure(), read()

### Community 63 - "test_failure_safety.py"
Cohesion: 0.12
Nodes (7): test_default_configuration_failure_injection_disabled(), test_domain_measurement_immutability_under_failure_injection(), test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), test_strict_absence_of_simulation_metadata_on_wire()

### Community 64 - "test_legacy_gateway.py"
Cohesion: 0.27
Nodes (11): fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry(), test_injected_out_of_order_sequence_is_rejected_without_retry(), test_injected_payload_faults_are_rejected_without_retry_or_cloud_delivery() (+3 more)

### Community 65 - "log_application"
Cohesion: 0.14
Nodes (14): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements(), ready() (+6 more)

### Community 66 - "plaintext.py"
Cohesion: 0.21
Nodes (11): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_device_id_whitespace_is_preserved_like_baseline_delivery() (+3 more)

### Community 67 - "test_mode_evaluation.py"
Cohesion: 0.20
Nodes (8): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 68 - "test_static_quality.py"
Cohesion: 0.12
Nodes (7): test_legacy_ai_decisions_register_exists(), test_legacy_architecture_operations_documentation_exists(), test_legacy_technical_debt_register_exists(), test_no_cloud_or_crypto_imports_in_legacy_src(), test_no_debug_prints_or_breakpoints_in_legacy_src(), test_no_keys_or_env_files_in_legacy_system(), test_no_private_key_blocks_in_legacy_files()

### Community 69 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 70 - "edge_gateway/models.py"
Cohesion: 0.17
Nodes (6): _timestamp(), normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 71 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 72 - "test_docker_assets.py"
Cohesion: 0.12
Nodes (3): test_compose_empty_failure_seed_keeps_legacy_selection_nondeterministic(), test_compose_environment_loads_valid_legacy_config(), test_compose_environment_with_custom_failure_settings_loads_valid_legacy_config()

### Community 73 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 74 - "ErrorCategory"
Cohesion: 0.14
Nodes (9): ErrorCategory, test_baseline_receiver_unavailable_bounded_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable() (+1 more)

### Community 75 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 76 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 77 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 78 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 79 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 80 - "GatewayClient"
Cohesion: 0.21
Nodes (3): GatewayClient, GatewayResult, test_theoretical_retry_amplification_product_is_explicit_and_bounded()

### Community 81 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 82 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 83 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 84 - "run_evaluation.py"
Cohesion: 0.33
Nodes (7): distribution(), flatten(), git(), invoke(), load_script(), main(), write_markdown()

### Community 86 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 87 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 88 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.17
Nodes (3): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 89 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 91 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 92 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 93 - "test_static_checks.py"
Cohesion: 0.29
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 94 - "run"
Cohesion: 0.18
Nodes (4): distribution(), _persisted_rows(), run(), TimedRepository

### Community 95 - "refresh_graphify.py"
Cohesion: 0.27
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 97 - "_baseline_transport"
Cohesion: 0.20
Nodes (3): _baseline_transport(), BaselineTransport, UnavailableBaseline

### Community 98 - "test_gateway_correlation.py"
Cohesion: 0.29
Nodes (4): create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 99 - "ApplicationFailures"
Cohesion: 0.27
Nodes (3): ApplicationFailures, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario()

### Community 100 - "edge_gateway/validation.py"
Cohesion: 0.24
Nodes (5): LegacyJSONError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 101 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 104 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 105 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 106 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 108 - "test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression"
Cohesion: 0.29
Nodes (3): test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression(), read(), test_sequence_gap_is_accepted_and_logged()

### Community 109 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 110 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 114 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 122 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.47
Nodes (5): _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 123 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 131 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 133 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

### Community 139 - "_deliver"
Cohesion: 0.50
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 140 - "test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries"
Cohesion: 0.40
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

## Knowledge Gaps
- **12 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`, `configHelp` (+7 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1090 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **66 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `create_app`, `ApplicationFailures`, `edge_gateway/app.py`, `test_mode_evaluation.py`, `SecureSession`, `SessionManager`, `SecureTransport`, `secure_transport.py`, `test_pqc_observability.py`, `test_session_expiry_system.py`, `CloudDispatch`, `.__init__`, `_Cloud`, `GatewayErrorCode`, `test_secure_transport.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `create_app`, `edge_gateway/app.py`, `test_gateway_cloud_secure.py`, `test_session.py`, `load_config`, `SessionManager`, `test_crypto_failures.py`, `secure_transport.py`, `PqcMetrics`, `CloudDispatch`, `.__init__`, `edge_gateway/crypto/symmetric.py`, `log_security`, `test_secure_transport.py`, `test_cloud_response_failures.py`, `edge_gateway/crypto/encoding.py`, `SecureSession`, `measurements.py`, `build_aad`, `test_legacy_gateway.py`, `plaintext.py`, `test_mode_evaluation.py`, `test_pqc_observability.py`, `test_session_expiry_system.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `create_app`, `edge_gateway/app.py`, `test_gateway_cloud_secure.py`, `test_session.py`, `load_config`, `test_crypto_failures.py`, `test_public_key_client.py`, `secure_transport.py`, `PqcMetrics`, `log_security`, `encapsulate`, `session_client.py`, `test_legacy_gateway.py`, `test_mode_evaluation.py`, `parse_public_key_response`, `test_pqc_observability.py`, `test_session_expiry_system.py`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`, `KdfError`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 63 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._