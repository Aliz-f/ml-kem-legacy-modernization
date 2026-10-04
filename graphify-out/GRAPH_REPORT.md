# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2870 nodes · 7193 edges · 164 communities (103 shown, 61 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1029 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- DeviceController
- test_legacy_gateway.py
- load_config
- test_gateway_cloud_secure.py
- test_gateway_compose_e2e.py
- measurements.py
- derive_session_key
- edge_gateway/app.py
- FailureMode
- CryptoFailureInjector
- threading
- load_config
- test_crypto_failures.py
- MeasurementRepository
- GatewayClient
- test_public_key_client.py
- test_secure_transport.py
- secure.py
- pytest
- SecureTransport
- SessionManager
- SecureSession
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- envelope_validation.py
- PqcMetrics
- CloudDispatch
- test_gateway_validation.py
- test_measure_modernized_e2e.py
- LegacyMeasurement
- create_app
- SessionManager
- FailureMode
- test_cloud_secure.py
- Sensor
- CanonicalMeasurement
- create_app
- edge_gateway/crypto/symmetric.py
- test_secure_message_tamper.py
- encode_binary
- test_gateway_correlation.py
- test_session.py
- FailureInjector
- cloud_service/app.py
- test_cloud_session_api.py
- encapsulate
- ErrorCategory
- test_sensor.py
- validate_measurement
- session_client.py
- test_gateway_measurements.py
- CloudMetrics
- StoredMeasurement
- fields
- test_cloud_failure_injection.py
- CanonicalMeasurement
- test_baseline_gateway_measurements
- load_config
- test_cloud_baseline.py
- build_aad
- test_baseline_client.py
- test_secure_shutdown.py
- _start_gateway_server
- edge_gateway/crypto/encoding.py
- test_failure_safety.py
- test_cloud_kdf.py
- plaintext.py
- test_security_mode_preserves_the_legacy_measurement_contract
- BaselineCloudError
- _dispatch
- cloud_service/crypto/mlkem.py
- test_cloud_queries.py
- run
- test_cloud_mlkem.py
- parse_public_key_response
- test_gateway_routes.py
- run
- test_pqc_observability.py
- test_session_expiry_system.py
- test_full_path_integration.py
- test_cloud_public_key.py
- test_gateway_application_metrics.py
- ApplicationFailures
- test_gateway_errors.py
- test_gateway_response_mapping.py
- test_gateway_application_failures.py
- test_secure_envelope.py
- _Clock
- run
- sleep
- types
- test_gateway_transport_interface.py
- _HandshakeHandler
- test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row
- BaselineCloudClient
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- establish_session
- main
- _Handler
- GatewayResult
- _GatewayValidationHandler
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_repository_hygiene.py
- get_measurement
- test_final_secure_transport_review.py
- _Handler
- _Handler
- _BaselineGatewayHandler
- _ScriptedNetworkHandler
- _Sizes
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- live_cloud
- _Gateway
- test_handshake_failure_stays_closed_without_a_session
- test_shared_integration_assets.py
- baseline_measurement
- BaselineTransport
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- StartupError
- derive_session_key
- _Handler
- test_gateway_crypto_ci.py
- client
- _Cloud
- test_faults_preserve_real_cloud_storage_and_mode_boundaries
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
- `test_legacy_controller_continues_after_bounded_cloud_delivery_failure()` --uses--> `DeviceController`  [INFERRED]
  tests/integration/test_end_to_end.py → legacy_system/src/legacy_system/device.py

## Import Cycles
- None detected.

## Communities (164 total, 61 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.07
Nodes (50): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), test_no_cloud_or_crypto_imports_in_legacy_src(), test_no_debug_prints_or_breakpoints_in_legacy_src() (+42 more)

### Community 1 - "DeviceController"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 2 - "test_legacy_gateway.py"
Cohesion: 0.05
Nodes (33): Measurement, _validate_number(), _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model() (+25 more)

### Community 3 - "load_config"
Cohesion: 0.05
Nodes (33): Config, ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), main() (+25 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 5 - "test_gateway_compose_e2e.py"
Cohesion: 0.05
Nodes (31): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+23 more)

### Community 6 - "measurements.py"
Cohesion: 0.07
Nodes (17): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, GatewayMetrics, SequenceTracker, CloudTransport, test_committed_sequence_survives_later_cloud_failure() (+9 more)

### Community 7 - "derive_session_key"
Cohesion: 0.05
Nodes (19): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+11 more)

### Community 9 - "FailureMode"
Cohesion: 0.13
Nodes (28): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+20 more)

### Community 10 - "CryptoFailureInjector"
Cohesion: 0.06
Nodes (11): get_config(), _secure_transport(), GatewayConfig, CryptoFailureInjector, _endpoint(), DispatchMetrics, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline() (+3 more)

### Community 11 - "threading"
Cohesion: 0.11
Nodes (7): test_legacy_sources_do_not_learn_gateway_crypto(), _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes(), _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 12 - "load_config"
Cohesion: 0.09
Nodes (28): _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer() (+20 more)

### Community 13 - "test_crypto_failures.py"
Cohesion: 0.08
Nodes (20): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud (+12 more)

### Community 14 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 15 - "GatewayClient"
Cohesion: 0.12
Nodes (20): GatewayClient, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_invalid_retry_counts_are_rejected() (+12 more)

### Community 16 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+11 more)

### Community 17 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 18 - "secure.py"
Cohesion: 0.09
Nodes (11): AadError, build_aad(), EnvelopeValidationError, AeadError, decrypt(), _DroppedResponse, _error(), _ingest() (+3 more)

### Community 20 - "SecureTransport"
Cohesion: 0.10
Nodes (9): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport (+1 more)

### Community 21 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 22 - "SecureSession"
Cohesion: 0.08
Nodes (13): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+5 more)

### Community 23 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.06
Nodes (7): _Cloud, _Cloud, _serve(), cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract(), _Server

### Community 24 - "envelope_validation.py"
Cohesion: 0.13
Nodes (15): EnvelopeSchemaError, SecureEnvelope, _constant(), _object(), parse_json(), validate_envelope(), ValidatedEnvelope, payload() (+7 more)

### Community 25 - "PqcMetrics"
Cohesion: 0.07
Nodes (5): _Duration, PqcMetrics, _Cloud, __init__(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 26 - "CloudDispatch"
Cohesion: 0.14
Nodes (14): CloudDispatch, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 27 - "test_gateway_validation.py"
Cohesion: 0.12
Nodes (19): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client(), payload() (+11 more)

### Community 28 - "test_measure_modernized_e2e.py"
Cohesion: 0.08
Nodes (9): test_harness_rejects_invalid_sample_count(), _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed() (+1 more)

### Community 29 - "LegacyMeasurement"
Cohesion: 0.16
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 30 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+10 more)

### Community 31 - "SessionManager"
Cohesion: 0.11
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 32 - "FailureMode"
Cohesion: 0.11
Nodes (9): Config, FailureMode, FailureInjector, FailureSelection, test_custom_environment(), test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects() (+1 more)

### Community 33 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 34 - "Sensor"
Cohesion: 0.08
Nodes (10): Sensor, _BaselineServer, _calculate_distribution(), _start_loopback_gateway(), test_baseline_device_controller_graceful_continuity_on_failure(), test_baseline_gateway_http_503_controlled_failure(), test_baseline_gateway_unavailable_bounded_retries(), test_baseline_healthy_workload_100_measurements() (+2 more)

### Community 35 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 36 - "create_app"
Cohesion: 0.11
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements() (+10 more)

### Community 37 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 38 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 39 - "encode_binary"
Cohesion: 0.13
Nodes (9): decode_binary(), encode_binary(), EncodingError, KeyService, _decode_ciphertext(), test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo() (+1 more)

### Community 40 - "test_gateway_correlation.py"
Cohesion: 0.11
Nodes (10): baseline_headers(), create_request_id(), normalize(), canonical(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids(), test_invalid_receipt_time_is_rejected_by_canonical_model() (+2 more)

### Community 41 - "test_session.py"
Cohesion: 0.13
Nodes (12): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_connection_reset_during_session_post_is_retryable(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced() (+4 more)

### Community 42 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 43 - "cloud_service/app.py"
Cohesion: 0.16
Nodes (3): SecurityMode, public_key(), _unavailable()

### Community 44 - "test_cloud_session_api.py"
Cohesion: 0.13
Nodes (12): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail() (+4 more)

### Community 45 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 46 - "ErrorCategory"
Cohesion: 0.11
Nodes (10): ErrorCategory, _sample_payload(), _ScriptedNetworkServer, _start_scripted_server(), test_data_vs_transient_failure_classification_matrix(), test_device_controller_discards_failed_measurement_and_advances_sequence(), test_gateway_server_errors_trigger_bounded_retries(), test_gateway_slow_request_timeout() (+2 more)

### Community 47 - "test_sensor.py"
Cohesion: 0.13
Nodes (17): FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp() (+9 more)

### Community 49 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 50 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 51 - "test_gateway_measurements.py"
Cohesion: 0.16
Nodes (14): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline() (+6 more)

### Community 52 - "CloudMetrics"
Cohesion: 0.11
Nodes (6): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_injected_fault_is_counted_only_when_its_boundary_applies(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 53 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 54 - "fields"
Cohesion: 0.16
Nodes (13): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+5 more)

### Community 55 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 56 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 57 - "test_baseline_gateway_measurements"
Cohesion: 0.12
Nodes (12): cloud(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy() (+4 more)

### Community 58 - "load_config"
Cohesion: 0.21
Nodes (14): ConfigurationError, load_config(), integer(), number(), text(), value(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values() (+6 more)

### Community 59 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 60 - "build_aad"
Cohesion: 0.16
Nodes (9): AadError, build_aad(), _require_id(), build_secure_envelope(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected() (+1 more)

### Community 61 - "test_baseline_client.py"
Cohesion: 0.25
Nodes (16): _client(), _send(), test_attempt_metrics_include_retry_and_invalid_acceptance(), test_baseline_shutdown_waits_for_attempt_and_closes_once(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request() (+8 more)

### Community 62 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 63 - "_start_gateway_server"
Cohesion: 0.10
Nodes (8): _GatewayValidationServer, _start_gateway_server(), test_data_failure_modes_rejected_or_accepted_without_retry(), test_device_controller_runs_through_fault_injections_without_crashing(), test_failure_rejections_logged_with_structured_attributes(), test_malformed_wire_body_is_400_without_retry(), test_random_failure_mode_generates_mixed_controlled_outcomes(), test_sequence_failure_modes_trigger_409_without_retry()

### Community 64 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 65 - "test_failure_safety.py"
Cohesion: 0.12
Nodes (7): test_default_configuration_failure_injection_disabled(), test_domain_measurement_immutability_under_failure_injection(), test_failure_mode_none_preserves_payload_verbatim(), test_sequence_fault_injection_preserves_internal_monotonicity(), test_startup_warning_absent_when_failure_injection_disabled(), test_startup_warning_logged_when_failure_injection_active(), test_strict_absence_of_simulation_metadata_on_wire()

### Community 66 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 67 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 68 - "test_security_mode_preserves_the_legacy_measurement_contract"
Cohesion: 0.18
Nodes (12): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+4 more)

### Community 69 - "BaselineCloudError"
Cohesion: 0.18
Nodes (6): BaselineAcceptance, BaselineCloudError, _dump(), _error_code(), _parse_acceptance(), _RejectRedirect

### Community 71 - "_dispatch"
Cohesion: 0.20
Nodes (8): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 72 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.19
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 73 - "test_cloud_queries.py"
Cohesion: 0.19
Nodes (8): test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503(), test_safe_query_errors()

### Community 74 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 75 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 76 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 77 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 78 - "run"
Cohesion: 0.15
Nodes (6): distribution(), _metrics(), _persisted_rows(), run(), _sample(), TimedRepository

### Community 79 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 80 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 81 - "test_full_path_integration.py"
Cohesion: 0.23
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 82 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 83 - "test_gateway_application_metrics.py"
Cohesion: 0.23
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 84 - "ApplicationFailures"
Cohesion: 0.21
Nodes (4): _baseline_transport(), ApplicationFailures, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario()

### Community 85 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 86 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 87 - "test_gateway_application_failures.py"
Cohesion: 0.25
Nodes (6): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 88 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 89 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 90 - "run"
Cohesion: 0.18
Nodes (4): distribution(), _persisted_rows(), run(), TimedRepository

### Community 92 - "sleep"
Cohesion: 0.20
Nodes (7): test_existing_gateway_session_client_over_real_http(), sleep(), serve(), serve(), _live_gateway(), test_real_gateway_failure_chain_is_bounded_by_committed_sequence_state(), unavailable()

### Community 93 - "types"
Cohesion: 0.24
Nodes (4): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 94 - "test_gateway_transport_interface.py"
Cohesion: 0.29
Nodes (4): _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 96 - "test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row"
Cohesion: 0.39
Nodes (6): _metrics(), _payload(), _serve(), test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(), test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(), test_five_valid_measurements_increment_gateway_and_cloud_counters()

### Community 98 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 99 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 100 - "establish_session"
Cohesion: 0.52
Nodes (4): _error(), _establish(), establish_session(), session_access_error_handler()

### Community 101 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 105 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 107 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 108 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 116 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.47
Nodes (5): _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 117 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 119 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.33
Nodes (3): _Baseline, _count(), test_handshake_failure_stays_closed_without_a_session()

### Community 126 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 128 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 1040 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **61 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `SecureTransport` to `test_legacy_gateway.py`, `test_gateway_cloud_secure.py`, `measurements.py`, `edge_gateway/app.py`, `CryptoFailureInjector`, `test_crypto_failures.py`, `test_secure_transport.py`, `SecureSession`, `PqcMetrics`, `CloudDispatch`, `SessionManager`, `create_app`, `edge_gateway/crypto/symmetric.py`, `build_aad`, `test_secure_shutdown.py`, `edge_gateway/crypto/encoding.py`, `plaintext.py`, `_dispatch`, `test_pqc_observability.py`, `test_session_expiry_system.py`, `test_gateway_application_failures.py`, `main`, `test_handshake_failure_stays_closed_without_a_session`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `FailureMode` connect `FailureMode` to `test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row`, `test_legacy_gateway.py`, `establish_session`, `test_gateway_cloud_secure.py`, `baseline_measurement`, `cloud_service/app.py`, `secure.py`, `CloudMetrics`, `test_cloud_failure_injection.py`, `load_config`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `test_legacy_gateway.py`, `measurements.py`, `edge_gateway/app.py`, `CryptoFailureInjector`, `load_config`, `test_secure_transport.py`, `SecureTransport`, `SecureSession`, `test_faults_preserve_real_cloud_storage_and_mode_boundaries`, `PqcMetrics`, `test_gateway_validation.py`, `CloudDispatch`, `LegacyMeasurement`, `test_gateway_measurements.py`, `test_baseline_gateway_measurements`, `test_gateway_routes.py`, `test_gateway_application_metrics.py`, `ApplicationFailures`, `test_gateway_response_mapping.py`, `test_gateway_application_failures.py`, `sleep`, `types`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_validation_bypass.py`, `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `_Gateway`, `BaselineTransport`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `GatewayClient` (e.g. with `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` and `live_baseline_gateway()`) actually correct?**
  _`GatewayClient` has 61 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._