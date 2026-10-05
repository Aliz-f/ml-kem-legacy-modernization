# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2989 nodes · 7414 edges · 152 communities (103 shown, 49 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1043 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DeviceController
- measurements.py
- cli.py
- test_legacy_gateway.py
- test_gateway_compose_e2e.py
- test_gateway_cloud_secure.py
- LegacyMeasurement
- load_config
- test_baseline_client.py
- pathlib
- test_crypto_failures.py
- FailureMode
- FailureMode
- cloud_service/app.py
- load_config
- MeasurementRepository
- SessionManager
- test_public_key_client.py
- dashboard/app.py
- edge_gateway/app.py
- test_secure_transport.py
- CloudDispatch
- secure_transport.py
- encapsulate
- PqcMetrics
- SecureTransport
- test_session.py
- test_gateway_measurements.py
- test_gateway_validation.py
- test_cloud_secure.py
- create_app
- SessionManager
- SecureSession
- load_config
- Config
- Sensor
- app.js
- CanonicalMeasurement
- edge_gateway/crypto/symmetric.py
- FailureInjector
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- GatewayClient
- cloud_service/config.py
- test_cloud_response_failures.py
- test_mode_evaluation.py
- legacy_system/config.py
- run
- build_aad
- _start_contract_receiver
- SecureEnvelope
- repository.py
- measure_baseline.py
- validate_measurement
- test_gateway_application_metrics.py
- session_client.py
- test_cloud_public_key.py
- secure.py
- fields
- test_cloud_baseline.py
- test_cloud_session_api.py
- encode_binary
- test_network_failures.py
- plaintext.py
- _Sessions
- test_static_quality.py
- test_cloud_kdf.py
- edge_gateway/crypto/encoding.py
- test_docker_assets.py
- test_cloud_queries.py
- public_key.py
- live_cloud
- cloud_service/crypto/mlkem.py
- CryptoFailureInjector
- pytest
- test_pqc_observability.py
- _start_loopback_receiver
- test_corrupt_ciphertext_demo.py
- test_handshake_failure_stays_closed_without_a_session
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- test_gateway_routes.py
- test_session_expiry_system.py
- test_dashboard.py
- test_gateway_correlation.py
- test_gateway_errors.py
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- envelope_validation.py
- test_baseline_integration.py
- derive_session_key
- test_secure_envelope.py
- test_failure_paths.py
- test_metrics_sanity.py
- database.py
- clean_container_crypto.py
- _Clock
- edge_gateway/crypto/kdf.py
- ErrorCategory
- KdfError
- test_baseline_gateway_measurements
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- _Handler
- GatewayResult
- _LegacyContractReceiver
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_session_reuse_system.py
- test_measure_modernized_e2e.py
- test_refresh_graphify.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- test_final_secure_transport_review.py
- _Handler
- _Handler
- _BaselineLoopbackReceiver
- _ScriptedNetworkHandler
- live_cloud
- test_shared_integration_assets.py
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- test_domain_measurement_immutability_under_failure_injection
- test_multiple_device_controllers_deliver_independently_to_gateway_interface
- TimedRepository
- test_theoretical_retry_amplification_product_is_explicit_and_bounded
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

## Communities (152 total, 49 thin omitted)

### Community 0 - "DeviceController"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 1 - "measurements.py"
Cohesion: 0.05
Nodes (22): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, GatewayMetrics, SequenceTracker, CloudDeliveryError, CloudTransport (+14 more)

### Community 2 - "cli.py"
Cohesion: 0.09
Nodes (47): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+39 more)

### Community 3 - "test_legacy_gateway.py"
Cohesion: 0.05
Nodes (33): Measurement, _validate_number(), _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model() (+25 more)

### Community 4 - "test_gateway_compose_e2e.py"
Cohesion: 0.05
Nodes (31): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+23 more)

### Community 5 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 6 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (32): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+24 more)

### Community 7 - "load_config"
Cohesion: 0.07
Nodes (38): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+30 more)

### Community 8 - "test_baseline_client.py"
Cohesion: 0.07
Nodes (31): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+23 more)

### Community 10 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 12 - "FailureMode"
Cohesion: 0.10
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 13 - "FailureMode"
Cohesion: 0.13
Nodes (27): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+19 more)

### Community 14 - "cloud_service/app.py"
Cohesion: 0.08
Nodes (15): health(), ready(), _crypto_dependencies_ready(), _unavailable(), SecurityMode, derive_session_key(), public_key(), _unavailable() (+7 more)

### Community 15 - "load_config"
Cohesion: 0.10
Nodes (28): _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer() (+20 more)

### Community 16 - "MeasurementRepository"
Cohesion: 0.10
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 17 - "SessionManager"
Cohesion: 0.10
Nodes (13): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_metrics_excludes_expired_sessions_after_replacement(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes() (+5 more)

### Community 18 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, PublicKeyRejected, _body(), cloud_server(), _public_key() (+11 more)

### Community 19 - "dashboard/app.py"
Cohesion: 0.09
Nodes (17): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), _container(), _container_info(), DashboardHandler, _decode_chunks(), _decode_logs() (+9 more)

### Community 20 - "edge_gateway/app.py"
Cohesion: 0.09
Nodes (9): _baseline_transport(), lifespan(), get_config(), _secure_transport(), log_application(), _token(), GatewayConfig, BaselineTransport (+1 more)

### Community 21 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 22 - "CloudDispatch"
Cohesion: 0.12
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions (+7 more)

### Community 23 - "secure_transport.py"
Cohesion: 0.12
Nodes (6): corrupt_ciphertext_copy(), _RejectRedirect, log_security(), _token(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback(), test_unsafe_log_values_are_dropped()

### Community 24 - "encapsulate"
Cohesion: 0.09
Nodes (14): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe(), encapsulate(), MlKemError, _raw_public_key() (+6 more)

### Community 25 - "PqcMetrics"
Cohesion: 0.07
Nodes (6): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__()

### Community 26 - "SecureTransport"
Cohesion: 0.10
Nodes (9): _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport (+1 more)

### Community 27 - "test_session.py"
Cohesion: 0.10
Nodes (16): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+8 more)

### Community 28 - "test_gateway_measurements.py"
Cohesion: 0.11
Nodes (20): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_processing_fault_is_visible_and_preserves_sequence() (+12 more)

### Community 29 - "test_gateway_validation.py"
Cohesion: 0.12
Nodes (20): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client() (+12 more)

### Community 30 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 31 - "create_app"
Cohesion: 0.10
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+10 more)

### Community 32 - "SessionManager"
Cohesion: 0.08
Nodes (3): SessionEstablishmentError, SessionManager, test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 33 - "SecureSession"
Cohesion: 0.08
Nodes (11): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+3 more)

### Community 34 - "load_config"
Cohesion: 0.13
Nodes (23): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+15 more)

### Community 35 - "Config"
Cohesion: 0.09
Nodes (12): Config, main(), test_baseline_device_controller_graceful_continuity_on_failure(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller() (+4 more)

### Community 36 - "Sensor"
Cohesion: 0.11
Nodes (18): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 37 - "app.js"
Cohesion: 0.12
Nodes (27): applyRuntimeConfig(), charts(), config(), configHelp, draw(), esc(), failureModes, formatMetricValue() (+19 more)

### Community 38 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 39 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 40 - "FailureInjector"
Cohesion: 0.12
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 41 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 42 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 43 - "GatewayClient"
Cohesion: 0.18
Nodes (16): GatewayClient, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_statuses_are_classified_by_retryability(), opener(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately() (+8 more)

### Community 44 - "cloud_service/config.py"
Cohesion: 0.10
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 45 - "test_cloud_response_failures.py"
Cohesion: 0.12
Nodes (12): assert_unavailable(), Cloud, delivery(), Handler, Reply, Sessions, test_complete_malformed_acceptance_maps_to_503_without_retry(), test_connection_reset_while_reading_preserves_retry_policy() (+4 more)

### Community 46 - "test_mode_evaluation.py"
Cohesion: 0.13
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 47 - "legacy_system/config.py"
Cohesion: 0.14
Nodes (3): test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), test_multiple_sensor_instances_maintain_independent_monotonic_sequences()

### Community 48 - "run"
Cohesion: 0.08
Nodes (12): sleep(), distribution(), _persisted_rows(), run(), serve(), TimedRepository, distribution(), _metrics() (+4 more)

### Community 49 - "build_aad"
Cohesion: 0.13
Nodes (10): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract() (+2 more)

### Community 50 - "_start_contract_receiver"
Cohesion: 0.09
Nodes (10): _LegacyContractServer, _start_contract_receiver(), test_contract_receiver_rejects_extra_fields_without_retry(), test_contract_receiver_rejects_wrong_types_and_domains_without_retry(), test_data_failure_modes_rejected_or_accepted_without_retry(), test_device_controller_runs_through_fault_injections_without_crashing(), test_failure_rejections_logged_with_structured_attributes(), test_malformed_wire_body_is_400_without_retry() (+2 more)

### Community 51 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 52 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 53 - "measure_baseline.py"
Cohesion: 0.14
Nodes (11): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+3 more)

### Community 54 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 55 - "test_gateway_application_metrics.py"
Cohesion: 0.12
Nodes (9): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport, test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text() (+1 more)

### Community 56 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 57 - "test_cloud_public_key.py"
Cohesion: 0.13
Nodes (11): lifespan(), StartupError, KeyService, secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail() (+3 more)

### Community 58 - "secure.py"
Cohesion: 0.14
Nodes (8): AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics, secure_measurement(), fail()

### Community 59 - "fields"
Cohesion: 0.17
Nodes (13): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+5 more)

### Community 60 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_duplicate_and_lost_response_retry_preserve_original(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 61 - "test_cloud_session_api.py"
Cohesion: 0.15
Nodes (10): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_session_initialization_failure_releases_keys() (+2 more)

### Community 62 - "encode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 63 - "test_network_failures.py"
Cohesion: 0.18
Nodes (8): _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout(), test_gateway_stopped_or_connection_refused(), test_transient_failure_eventual_recovery_succeeds()

### Community 64 - "plaintext.py"
Cohesion: 0.21
Nodes (11): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_device_id_whitespace_is_preserved_like_baseline_delivery() (+3 more)

### Community 65 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 66 - "test_static_quality.py"
Cohesion: 0.12
Nodes (7): test_legacy_ai_decisions_register_exists(), test_legacy_architecture_operations_documentation_exists(), test_legacy_technical_debt_register_exists(), test_no_cloud_or_crypto_imports_in_legacy_src(), test_no_debug_prints_or_breakpoints_in_legacy_src(), test_no_keys_or_env_files_in_legacy_system(), test_no_private_key_blocks_in_legacy_files()

### Community 67 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 68 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 69 - "test_docker_assets.py"
Cohesion: 0.12
Nodes (3): test_compose_empty_failure_seed_keeps_legacy_selection_nondeterministic(), test_compose_environment_loads_valid_legacy_config(), test_compose_environment_with_custom_failure_settings_loads_valid_legacy_config()

### Community 70 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 71 - "public_key.py"
Cohesion: 0.20
Nodes (8): validate_public_key(), CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 72 - "live_cloud"
Cohesion: 0.15
Nodes (9): test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy() (+1 more)

### Community 73 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 75 - "pytest"
Cohesion: 0.17
Nodes (4): test_gateway_process_exits_cleanly_on_signal(), _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 76 - "test_pqc_observability.py"
Cohesion: 0.19
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 77 - "_start_loopback_receiver"
Cohesion: 0.14
Nodes (7): _BaselineLoopbackServer, _calculate_distribution(), _start_loopback_receiver(), test_baseline_receiver_422_no_retries(), test_baseline_receiver_http_503_controlled_failure(), test_baseline_receiver_unavailable_bounded_retries(), test_client_loopback_workload_100_measurements()

### Community 78 - "test_corrupt_ciphertext_demo.py"
Cohesion: 0.20
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 79 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 80 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.14
Nodes (3): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 81 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 82 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 84 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 85 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 86 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 87 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 89 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 90 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 91 - "test_failure_paths.py"
Cohesion: 0.31
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 92 - "test_metrics_sanity.py"
Cohesion: 0.38
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 94 - "database.py"
Cohesion: 0.33
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 95 - "clean_container_crypto.py"
Cohesion: 0.29
Nodes (3): _install(), main(), _serve()

### Community 96 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 98 - "ErrorCategory"
Cohesion: 0.25
Nodes (4): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), opener(), test_transport_failures_are_stable_and_retryable()

### Community 99 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 100 - "test_baseline_gateway_measurements"
Cohesion: 0.25
Nodes (4): cloud(), test_baseline_gateway_measurements(), _post(), send()

### Community 101 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 102 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 106 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 107 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 109 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 112 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 119 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 123 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 125 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **12 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`, `configHelp` (+7 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1087 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **49 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `SessionManager`, `SecureSession`, `test_pqc_observability.py`, `test_corrupt_ciphertext_demo.py`, `test_handshake_failure_stays_closed_without_a_session`, `run`, `test_mode_evaluation.py`, `test_session_expiry_system.py`, `edge_gateway/app.py`, `test_secure_transport.py`, `CloudDispatch`, `secure_transport.py`, `SecureTransport`, `fields`, `create_app`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `measurements.py`, `test_legacy_gateway.py`, `LegacyMeasurement`, `test_baseline_client.py`, `load_config`, `edge_gateway/app.py`, `test_secure_transport.py`, `CloudDispatch`, `PqcMetrics`, `SecureTransport`, `test_gateway_measurements.py`, `test_gateway_validation.py`, `SecureSession`, `test_legacy_compatibility.py`, `test_cloud_response_failures.py`, `test_gateway_application_metrics.py`, `live_cloud`, `test_gateway_routes.py`, `test_failure_paths.py`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_validation_bypass.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `test_session_recovery_is_counted()` connect `SecureSession` to `PqcMetrics`, `SecureTransport`, `test_session.py`, `secure_transport.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 63 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._