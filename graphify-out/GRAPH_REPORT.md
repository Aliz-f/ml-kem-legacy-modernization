# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 3010 nodes · 7474 edges · 138 communities (97 shown, 41 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1044 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- edge_gateway/app.py
- pathlib
- fields
- DeviceController
- baseline.py
- measurements.py
- cli.py
- test_gateway_cloud_secure.py
- test_cloud_secure.py
- load_config
- create_app
- test_crypto_failures.py
- derive_session_key
- FailureMode
- cloud_service/app.py
- pytest
- SecureTransport
- FailureMode
- Sensor
- MeasurementRepository
- test_public_key_client.py
- test_secure_transport.py
- CloudDispatch
- run_evaluation.py
- test_mode_evaluation.py
- SessionManager
- dashboard/app.py
- load_config
- SessionManager
- secure_transport.py
- load_config
- test_session.py
- test_gateway_measurements.py
- test_legacy_gateway.py
- app.js
- SecureSession
- Measurement
- test_legacy_compatibility.py
- LegacyMeasurement
- test_gateway_crypto_image.py
- GatewayClient
- CanonicalMeasurement
- FailureInjector
- test_secure_message_tamper.py
- dataclasses
- fastapi_testclient
- test_sensor.py
- measure_baseline_e2e.py
- test_cloud_public_key.py
- session_client.py
- test_network_failures.py
- validate_measurement
- encapsulate
- CanonicalMeasurement
- test_cloud_response_failures.py
- Config
- test_cloud_baseline.py
- test_cloud_session_api.py
- test_secure_shutdown.py
- test_baseline_measurements.py
- test_gateway_compose_e2e.py
- CloudMetrics
- sessions.py
- cloud_service/crypto/mlkem.py
- plaintext.py
- test_docker_assets.py
- test_static_quality.py
- encode_binary
- test_cloud_kdf.py
- test_gateway_validation.py
- measure_modernized_e2e.py
- test_mlkem_handshake_failure_demo.py
- test_cloud_queries.py
- measure_baseline.py
- validate_legacy_measurement
- parse_public_key_response
- test_cloud_mlkem.py
- test_gateway_routes.py
- _Handler
- test_pqc_observability.py
- test_dashboard.py
- edge_gateway/validation.py
- test_gateway_application_metrics.py
- test_static_checks.py
- test_failure_paths.py
- test_metrics_sanity.py
- test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively
- clean_container_crypto.py
- ErrorCategory
- queries.py
- test_body_limit_before_sequence_and_delivery
- _Cloud
- GatewayResult
- _LegacyContractReceiver
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_measure_modernized_e2e.py
- test_refresh_graphify.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- test_final_secure_transport_review.py
- _Handler
- _BaselineLoopbackReceiver
- _ScriptedNetworkHandler
- live_cloud
- test_shared_integration_assets.py
- baseline_measurement
- test_baseline_integration.py
- BaselineTransport
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- test_domain_measurement_immutability_under_failure_injection
- _deliver
- test_measure_baseline_e2e.py
- edge_gateway/models.py
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
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `open_response()` --indirect_call--> `status()`  [INFERRED]
  edge_gateway/tests/test_cloud_response_failures.py → src/ai_history/cli.py
- `test_handshake_failure_stays_closed_without_a_session()` --uses--> `CryptoFailureInjector`  [INFERRED]
  tests/integration/test_mlkem_handshake_failure_demo.py → edge_gateway/src/edge_gateway/crypto/failure.py

## Import Cycles
- None detected.

## Communities (138 total, 41 thin omitted)

### Community 0 - "edge_gateway/app.py"
Cohesion: 0.04
Nodes (23): _baseline_transport(), get_config(), _logging_level(), _secure_transport(), GatewayConfig, CryptoFailureInjector, _Duration, PqcMetrics (+15 more)

### Community 2 - "fields"
Cohesion: 0.05
Nodes (50): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+42 more)

### Community 3 - "DeviceController"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 4 - "baseline.py"
Cohesion: 0.05
Nodes (39): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+31 more)

### Community 5 - "measurements.py"
Cohesion: 0.05
Nodes (24): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, GatewayMetrics, SequenceTracker, CloudTransport, test_application_errors_have_stable_http_contract() (+16 more)

### Community 6 - "cli.py"
Cohesion: 0.09
Nodes (47): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+39 more)

### Community 7 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (34): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+26 more)

### Community 8 - "test_cloud_secure.py"
Cohesion: 0.07
Nodes (41): EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+33 more)

### Community 9 - "load_config"
Cohesion: 0.07
Nodes (38): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+30 more)

### Community 10 - "create_app"
Cohesion: 0.06
Nodes (31): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements() (+23 more)

### Community 11 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 12 - "derive_session_key"
Cohesion: 0.06
Nodes (17): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+9 more)

### Community 13 - "FailureMode"
Cohesion: 0.10
Nodes (25): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+17 more)

### Community 14 - "cloud_service/app.py"
Cohesion: 0.08
Nodes (11): SecurityMode, AeadError, decrypt(), public_key(), _unavailable(), _DroppedResponse, _error(), _ingest() (+3 more)

### Community 15 - "pytest"
Cohesion: 0.15
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 16 - "SecureTransport"
Cohesion: 0.08
Nodes (10): _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport, _SessionRecovery (+2 more)

### Community 17 - "FailureMode"
Cohesion: 0.13
Nodes (27): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+19 more)

### Community 18 - "Sensor"
Cohesion: 0.05
Nodes (16): Sensor, test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), _LegacyContractServer, _start_contract_receiver(), test_contract_receiver_rejects_extra_fields_without_retry(), test_contract_receiver_rejects_wrong_types_and_domains_without_retry(), test_data_failure_modes_rejected_or_accepted_without_retry() (+8 more)

### Community 19 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_unrelated_record_id_collision_is_not_idempotent_success(), database() (+17 more)

### Community 20 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (20): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+12 more)

### Community 21 - "test_secure_transport.py"
Cohesion: 0.15
Nodes (29): SecureTransportError, session(), _Cloud, _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again() (+21 more)

### Community 22 - "CloudDispatch"
Cohesion: 0.10
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions (+7 more)

### Community 23 - "run_evaluation.py"
Cohesion: 0.10
Nodes (17): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), distribution(), flatten(), git(), invoke() (+9 more)

### Community 24 - "test_mode_evaluation.py"
Cohesion: 0.08
Nodes (12): cloud(), LiveCloud, _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server (+4 more)

### Community 25 - "SessionManager"
Cohesion: 0.10
Nodes (13): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_metrics_excludes_expired_sessions_after_replacement(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes() (+5 more)

### Community 26 - "dashboard/app.py"
Cohesion: 0.09
Nodes (17): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), _container(), _container_info(), DashboardHandler, _decode_chunks(), _decode_logs() (+9 more)

### Community 27 - "load_config"
Cohesion: 0.13
Nodes (22): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+14 more)

### Community 28 - "SessionManager"
Cohesion: 0.07
Nodes (6): SessionEstablishmentError, SessionManager, test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), test_crypto_failure_is_classified_and_recorded(), fail_encapsulation(), test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 29 - "secure_transport.py"
Cohesion: 0.09
Nodes (12): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _RejectRedirect (+4 more)

### Community 30 - "load_config"
Cohesion: 0.11
Nodes (24): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+16 more)

### Community 31 - "test_session.py"
Cohesion: 0.10
Nodes (16): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+8 more)

### Community 32 - "test_gateway_measurements.py"
Cohesion: 0.11
Nodes (20): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_processing_fault_is_visible_and_preserves_sequence() (+12 more)

### Community 33 - "test_legacy_gateway.py"
Cohesion: 0.15
Nodes (15): AcceptedBaseline, FailingBaseline, fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry() (+7 more)

### Community 34 - "app.js"
Cohesion: 0.12
Nodes (27): applyRuntimeConfig(), charts(), config(), configHelp, draw(), esc(), failureModes, formatMetricValue() (+19 more)

### Community 35 - "SecureSession"
Cohesion: 0.09
Nodes (7): _Sessions, SecureSession, Sessions, test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 36 - "Measurement"
Cohesion: 0.11
Nodes (13): Measurement, _validate_number(), _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model() (+5 more)

### Community 37 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 38 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 39 - "test_gateway_crypto_image.py"
Cohesion: 0.10
Nodes (8): test_gateway_process_exits_cleanly_on_signal(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 40 - "GatewayClient"
Cohesion: 0.19
Nodes (15): GatewayClient, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_statuses_are_classified_by_retryability(), opener(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately() (+7 more)

### Community 41 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 42 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 43 - "test_secure_message_tamper.py"
Cohesion: 0.16
Nodes (13): DecryptSpy, _different_nonce(), _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection (+5 more)

### Community 44 - "dataclasses"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 45 - "fastapi_testclient"
Cohesion: 0.10
Nodes (9): test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_service(), client(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent(), test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections() (+1 more)

### Community 46 - "test_sensor.py"
Cohesion: 0.13
Nodes (17): FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp() (+9 more)

### Community 47 - "measure_baseline_e2e.py"
Cohesion: 0.11
Nodes (8): sleep(), distribution(), _persisted_rows(), run(), serve(), TimedRepository, _load(), run()

### Community 48 - "test_cloud_public_key.py"
Cohesion: 0.12
Nodes (11): lifespan(), StartupError, KeyService, secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail() (+3 more)

### Community 50 - "session_client.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 51 - "test_network_failures.py"
Cohesion: 0.14
Nodes (9): _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_device_controller_discards_failed_measurement_and_advances_sequence(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout(), test_gateway_stopped_or_connection_refused() (+1 more)

### Community 52 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 53 - "encapsulate"
Cohesion: 0.16
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 54 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 55 - "test_cloud_response_failures.py"
Cohesion: 0.16
Nodes (11): assert_unavailable(), Cloud, delivery(), Handler, Reply, test_complete_malformed_acceptance_maps_to_503_without_retry(), test_connection_reset_while_reading_preserves_retry_policy(), open_response() (+3 more)

### Community 56 - "Config"
Cohesion: 0.14
Nodes (10): Config, main(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory() (+2 more)

### Community 57 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_duplicate_and_lost_response_retry_preserve_original(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+1 more)

### Community 58 - "test_cloud_session_api.py"
Cohesion: 0.15
Nodes (10): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_session_initialization_failure_releases_keys() (+2 more)

### Community 59 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 60 - "test_baseline_measurements.py"
Cohesion: 0.14
Nodes (8): _BaselineLoopbackServer, _calculate_distribution(), _start_loopback_receiver(), test_baseline_device_controller_graceful_continuity_on_failure(), test_baseline_receiver_422_no_retries(), test_baseline_receiver_http_503_controlled_failure(), test_baseline_receiver_unavailable_bounded_retries(), test_client_loopback_workload_100_measurements()

### Community 61 - "test_gateway_compose_e2e.py"
Cohesion: 0.23
Nodes (13): _compose(), _measurement(), _metrics(), _port(), _send(), test_compose_cloud_restart_recovers_readiness_and_delivery(), test_compose_cloud_restart_recovers_stale_mlkem_session_without_fallback(), test_compose_gateway_restart_establishes_a_fresh_mlkem_session() (+5 more)

### Community 62 - "CloudMetrics"
Cohesion: 0.13
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 63 - "sessions.py"
Cohesion: 0.18
Nodes (10): health(), ready(), _crypto_dependencies_ready(), _unavailable(), derive_session_key(), _decode_ciphertext(), _error(), _establish() (+2 more)

### Community 64 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 65 - "plaintext.py"
Cohesion: 0.21
Nodes (11): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_device_id_whitespace_is_preserved_like_baseline_delivery() (+3 more)

### Community 66 - "test_docker_assets.py"
Cohesion: 0.11
Nodes (3): test_compose_empty_failure_seed_keeps_legacy_selection_nondeterministic(), test_compose_environment_loads_valid_legacy_config(), test_compose_environment_with_custom_failure_settings_loads_valid_legacy_config()

### Community 67 - "test_static_quality.py"
Cohesion: 0.12
Nodes (7): test_legacy_ai_decisions_register_exists(), test_legacy_architecture_operations_documentation_exists(), test_legacy_technical_debt_register_exists(), test_no_cloud_or_crypto_imports_in_legacy_src(), test_no_debug_prints_or_breakpoints_in_legacy_src(), test_no_keys_or_env_files_in_legacy_system(), test_no_private_key_blocks_in_legacy_files()

### Community 68 - "encode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 69 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 70 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 71 - "measure_modernized_e2e.py"
Cohesion: 0.16
Nodes (7): distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve(), TimedRepository

### Community 72 - "test_mlkem_handshake_failure_demo.py"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 73 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 74 - "measure_baseline.py"
Cohesion: 0.21
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 75 - "validate_legacy_measurement"
Cohesion: 0.20
Nodes (6): normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 76 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 77 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 78 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 79 - "_Handler"
Cohesion: 0.21
Nodes (4): _Handler, _reset_mid_body(), _Handler, _reset_mid_body()

### Community 80 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 82 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 83 - "test_gateway_application_metrics.py"
Cohesion: 0.23
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 84 - "test_static_checks.py"
Cohesion: 0.29
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 85 - "test_failure_paths.py"
Cohesion: 0.31
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 86 - "test_metrics_sanity.py"
Cohesion: 0.38
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 87 - "test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively"
Cohesion: 0.18
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 89 - "clean_container_crypto.py"
Cohesion: 0.29
Nodes (3): _install(), main(), _serve()

### Community 90 - "ErrorCategory"
Cohesion: 0.22
Nodes (5): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable()

### Community 91 - "queries.py"
Cohesion: 0.46
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 92 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 96 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 97 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 99 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 102 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 108 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 114 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 115 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

### Community 119 - "_deliver"
Cohesion: 0.50
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

## Knowledge Gaps
- **12 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`, `configHelp` (+7 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1090 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app` to `edge_gateway/app.py`, `baseline.py`, `measurements.py`, `SecureTransport`, `test_secure_transport.py`, `CloudDispatch`, `load_config`, `test_gateway_measurements.py`, `test_legacy_gateway.py`, `test_legacy_compatibility.py`, `LegacyMeasurement`, `fastapi_testclient`, `test_cloud_response_failures.py`, `test_gateway_validation.py`, `validate_legacy_measurement`, `test_gateway_routes.py`, `edge_gateway/validation.py`, `test_gateway_application_metrics.py`, `test_failure_paths.py`, `test_body_limit_before_sequence_and_delivery`, `BaselineTransport`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `edge_gateway/app.py`, `fields`, `measurements.py`, `test_gateway_cloud_secure.py`, `create_app`, `test_crypto_failures.py`, `test_secure_transport.py`, `CloudDispatch`, `test_mode_evaluation.py`, `SessionManager`, `secure_transport.py`, `test_gateway_measurements.py`, `test_legacy_gateway.py`, `SecureSession`, `test_cloud_response_failures.py`, `test_secure_shutdown.py`, `plaintext.py`, `test_mlkem_handshake_failure_demo.py`, `test_pqc_observability.py`, `test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively`, `clean_container_crypto.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `log_application()` connect `create_app` to `edge_gateway/app.py`, `fields`, `baseline.py`, `measurements.py`, `SecureTransport`, `CloudDispatch`, `secure_transport.py`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 63 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._