# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2784 nodes · 7004 edges · 170 communities (108 shown, 62 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 967 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_device.py
- GatewayClient
- cli.py
- test_gateway_cloud_secure.py
- edge_gateway/app.py
- load_config
- SecureTransport
- test_gateway_crypto_image.py
- test_security_logging.py
- FailureMode
- run
- FailureMode
- MeasurementRepository
- SessionManager
- create_app
- CloudDispatch
- test_session.py
- load_config
- test_secure_transport.py
- SessionManager
- PqcMetrics
- test_public_key_client.py
- secure.py
- validate_measurement
- test_cloud_secure.py
- edge_gateway/crypto/symmetric.py
- test_cloud_session_api.py
- CanonicalMeasurement
- load_config
- session_client.py
- LegacyMeasurement
- test_crypto_failures.py
- test_measure_modernized_e2e.py
- FailureInjector
- SecureEnvelope
- repository.py
- test_gateway_measurements.py
- live_gateway
- test_secure_message_tamper.py
- test_cloud_mlkem.py
- CryptoFailureInjector
- encapsulate
- derive_session_key
- fields
- test_cloud_baseline.py
- CanonicalMeasurement
- test_baseline_gateway_measurements
- _dispatch
- test_legacy_compatibility.py
- edge_gateway/crypto/envelope.py
- CloudMetrics
- BaselineCloudClient
- SequenceTracker
- sessions.py
- cloud_service/crypto/mlkem.py
- MeasurementProcessor
- _Sessions
- encode_binary
- test_cloud_queries.py
- measurements.py
- edge_gateway/crypto/encoding.py
- test_baseline_client.py
- test_gateway_validation.py
- Measurement
- test_docker_assets.py
- test_cloud_kdf.py
- edge_gateway/validation.py
- Sensor
- test_pqc_observability.py
- test_cloud_response_failures.py
- Config
- test_handshake_failure_stays_closed_without_a_session
- test_gateway_correlation.py
- edge_gateway/crypto/aad.py
- normalize
- test_gateway_routes.py
- _Handler
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_session_expiry_system.py
- test_cloud_public_key.py
- BaselineCloudError
- parse_public_key_response
- test_gateway_errors.py
- test_gateway_response_mapping.py
- test_sensor.py
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- envelope_validation.py
- GatewayMetrics
- test_secure_envelope.py
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- _Clock
- test_gateway_application_failures.py
- _HandshakeHandler
- test_gateway_operations.py
- test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery
- LiveCloud
- GatewayErrorCode
- ApplicationFailures
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- test_fixtures.py
- FalseyClock
- main
- _baseline_transport
- test_untrusted_values_do_not_create_metric_labels
- test_gateway_secure_session_encrypts_and_delivers_to_live_cloud
- test_legacy_mode_success_compatibility.py
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_session_reuse_system.py
- test_repository_hygiene.py
- _crypto_dependencies_ready
- get_measurement
- test_final_secure_transport_review.py
- live_cloud
- _Gateway
- test_shared_integration_assets.py
- public_key
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- measure_mode_comparison.py
- test_sequence_state_timing_awareness_no_rollback_on_downstream_failure
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- edge_gateway/models.py
- _Handler
- Handler
- _Response
- test_multiple_device_controllers_deliver_independently_to_gateway_interface
- test_gateway_crypto_ci.py
- _Cloud
- test_lifespan_closes_baseline_and_rejects_late_requests
- test_multiple_devices_configured_via_environment_without_code_changes
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 87 edges
2. `load_config()` - 83 edges
3. `GatewayClient` - 56 edges
4. `SecureTransport` - 56 edges
5. `load_config()` - 51 edges
6. `FailureMode` - 49 edges
7. `create_app()` - 49 edges
8. `FailureMode` - 47 edges
9. `SessionManager` - 46 edges
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

## Communities (170 total, 62 thin omitted)

### Community 0 - "test_device.py"
Cohesion: 0.05
Nodes (31): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+23 more)

### Community 1 - "GatewayClient"
Cohesion: 0.06
Nodes (41): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+33 more)

### Community 2 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 3 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 4 - "edge_gateway/app.py"
Cohesion: 0.07
Nodes (5): get_config(), _logging_level(), GatewayConfig, corrupt_ciphertext_copy(), test_gateway_process_exits_cleanly_on_signal()

### Community 6 - "load_config"
Cohesion: 0.08
Nodes (32): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+24 more)

### Community 7 - "SecureTransport"
Cohesion: 0.07
Nodes (14): build_secure_envelope(), SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect (+6 more)

### Community 8 - "test_gateway_crypto_image.py"
Cohesion: 0.06
Nodes (18): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+10 more)

### Community 9 - "test_security_logging.py"
Cohesion: 0.06
Nodes (18): _Sessions, _Baseline, _Clock, _Cloud, cloud_url(), _Handler, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default() (+10 more)

### Community 10 - "FailureMode"
Cohesion: 0.10
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 11 - "run"
Cohesion: 0.05
Nodes (23): test_existing_gateway_session_client_over_real_http(), canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run() (+15 more)

### Community 12 - "FailureMode"
Cohesion: 0.13
Nodes (28): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+20 more)

### Community 13 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 14 - "SessionManager"
Cohesion: 0.07
Nodes (10): clock(), SecureSession, SessionEstablishmentError, SessionManager, Sessions, test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), test_session_missing_and_expired_force_a_new_handshake(), _run() (+2 more)

### Community 15 - "create_app"
Cohesion: 0.08
Nodes (23): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), ready() (+15 more)

### Community 16 - "CloudDispatch"
Cohesion: 0.11
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions (+7 more)

### Community 17 - "test_session.py"
Cohesion: 0.09
Nodes (16): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+8 more)

### Community 18 - "load_config"
Cohesion: 0.12
Nodes (24): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), main(), test_default_configuration() (+16 more)

### Community 19 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 20 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 21 - "PqcMetrics"
Cohesion: 0.07
Nodes (6): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), _Cloud, __init__()

### Community 22 - "test_public_key_client.py"
Cohesion: 0.12
Nodes (17): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, PublicKeyRejected, _body(), _public_key(), test_cloud_url_and_timeout_are_validated() (+9 more)

### Community 23 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 25 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 26 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 27 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 28 - "test_cloud_session_api.py"
Cohesion: 0.11
Nodes (13): StartupError, client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+5 more)

### Community 29 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 30 - "load_config"
Cohesion: 0.14
Nodes (19): main(), _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config() (+11 more)

### Community 31 - "session_client.py"
Cohesion: 0.14
Nodes (12): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+4 more)

### Community 32 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 33 - "test_crypto_failures.py"
Cohesion: 0.12
Nodes (14): _aad(), _injector(), measurement_url(), _MeasurementCloud, _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates() (+6 more)

### Community 34 - "test_measure_modernized_e2e.py"
Cohesion: 0.09
Nodes (7): test_harness_rejects_invalid_sample_count(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 35 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 36 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 37 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 38 - "test_gateway_measurements.py"
Cohesion: 0.15
Nodes (15): test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario() (+7 more)

### Community 39 - "live_gateway"
Cohesion: 0.16
Nodes (13): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_all_invalid_integration_fixtures_are_rejected_without_delivery(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_injected_duplicate_sequence_is_rejected_without_retry(), test_injected_out_of_order_sequence_is_rejected_without_retry() (+5 more)

### Community 40 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 41 - "test_cloud_mlkem.py"
Cohesion: 0.11
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 42 - "CryptoFailureInjector"
Cohesion: 0.12
Nodes (3): _secure_transport(), CryptoFailureInjector, test_from_config_uses_gateway_failure_settings()

### Community 43 - "encapsulate"
Cohesion: 0.16
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 44 - "derive_session_key"
Cohesion: 0.15
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 45 - "fields"
Cohesion: 0.18
Nodes (13): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+5 more)

### Community 46 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (11): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_duplicate_and_lost_response_retry_preserve_original(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape() (+3 more)

### Community 47 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 48 - "test_baseline_gateway_measurements"
Cohesion: 0.12
Nodes (12): cloud(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy() (+4 more)

### Community 49 - "_dispatch"
Cohesion: 0.13
Nodes (9): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Sizes, test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline() (+1 more)

### Community 50 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 51 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.18
Nodes (11): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_device_id_whitespace_is_preserved_like_baseline_delivery() (+3 more)

### Community 52 - "CloudMetrics"
Cohesion: 0.13
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 53 - "BaselineCloudClient"
Cohesion: 0.14
Nodes (6): BaselineAcceptance, BaselineCloudClient, _dump(), _endpoint(), _error_code(), _parse_acceptance()

### Community 54 - "SequenceTracker"
Cohesion: 0.17
Nodes (11): SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap(), test_gap_is_logged_and_advances_state() (+3 more)

### Community 55 - "sessions.py"
Cohesion: 0.18
Nodes (8): SecurityMode, derive_session_key(), KdfError, _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 56 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 57 - "MeasurementProcessor"
Cohesion: 0.14
Nodes (7): MeasurementProcessor, CloudDeliveryError, CloudTransport, _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 58 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 59 - "encode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 60 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 61 - "measurements.py"
Cohesion: 0.17
Nodes (4): log_application(), _token(), GatewayError, UnavailableBaseline

### Community 62 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 63 - "test_baseline_client.py"
Cohesion: 0.30
Nodes (14): _client(), _send(), test_attempt_metrics_include_retry_and_invalid_acceptance(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request(), test_redirect_is_rejected_and_constructor_validates_inputs() (+6 more)

### Community 64 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 65 - "Measurement"
Cohesion: 0.15
Nodes (7): Measurement, _validate_number(), query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(), test_legacy_controller_continues_after_bounded_cloud_delivery_failure(), read()

### Community 67 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 68 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 69 - "Sensor"
Cohesion: 0.13
Nodes (6): Sensor, test_multiple_sensor_instances_maintain_independent_monotonic_sequences(), test_sensor_assigns_utc_timestamp_at_creation(), test_sensor_generates_valid_normal_measurements(), test_sensor_increments_sequence_for_each_created_measurement(), test_sensor_seeded_random_generation_is_reproducible()

### Community 70 - "test_pqc_observability.py"
Cohesion: 0.19
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 71 - "test_cloud_response_failures.py"
Cohesion: 0.27
Nodes (9): assert_unavailable(), Cloud, Reply, test_complete_malformed_acceptance_maps_to_503_without_retry(), test_connection_reset_while_reading_preserves_retry_policy(), open_response(), test_malformed_error_body_preserves_http_retry_classification(), test_truncated_acceptance_exhausts_the_existing_retry_bound() (+1 more)

### Community 72 - "Config"
Cohesion: 0.18
Nodes (7): Config, make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression(), read()

### Community 73 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 74 - "test_gateway_correlation.py"
Cohesion: 0.23
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 75 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 76 - "normalize"
Cohesion: 0.22
Nodes (5): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 77 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 78 - "_Handler"
Cohesion: 0.21
Nodes (4): _Handler, _reset_mid_body(), _Handler, _reset_mid_body()

### Community 79 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.18
Nodes (5): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored(), _Server

### Community 80 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 81 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 82 - "BaselineCloudError"
Cohesion: 0.20
Nodes (7): BaselineCloudError, _RejectRedirect, test_baseline_shutdown_waits_for_attempt_and_closes_once(), post(), _live_gateway(), test_real_gateway_failure_chain_is_bounded_by_committed_sequence_state(), unavailable()

### Community 83 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 84 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 85 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 86 - "test_sensor.py"
Cohesion: 0.32
Nodes (10): make_measurement(), test_measurement_accepts_valid_boundary_values(), test_measurement_accepts_valid_internal_state(), test_measurement_is_immutable(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc(), test_payload_has_exact_field_names_and_serialized_values() (+2 more)

### Community 87 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 88 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 90 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 92 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 93 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 94 - "test_gateway_application_failures.py"
Cohesion: 0.29
Nodes (5): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 96 - "test_gateway_operations.py"
Cohesion: 0.28
Nodes (4): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 97 - "test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery"
Cohesion: 0.28
Nodes (6): AcceptedCloud, _gateway(), _payload(), test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(), test_legacy_injected_sequence_faults_are_409_without_retry(), test_malformed_legacy_wire_body_is_400_without_cloud_delivery()

### Community 101 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 102 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 103 - "test_fixtures.py"
Cohesion: 0.43
Nodes (6): _load_fixture(), test_invalid_humidity_fixture_fails_domain_validation(), test_invalid_temperature_fixture_fails_domain_validation(), test_invalid_timestamp_fixture_cannot_be_parsed_as_iso_timestamp(), test_missing_field_fixture_omits_timestamp(), test_valid_legacy_measurement_fixture_reconstitutes_valid_domain_model()

### Community 104 - "FalseyClock"
Cohesion: 0.29
Nodes (3): FalseyClock, FalseyRandomSource, test_sensor_preserves_falsey_supplied_dependencies()

### Community 105 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 107 - "test_untrusted_values_do_not_create_metric_labels"
Cohesion: 0.33
Nodes (4): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 108 - "test_gateway_secure_session_encrypts_and_delivers_to_live_cloud"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 109 - "test_legacy_mode_success_compatibility.py"
Cohesion: 0.43
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 110 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 111 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 113 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 114 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 115 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 118 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 125 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 127 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 991 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **62 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_gateway_cloud_secure.py`, `edge_gateway/app.py`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`, `SecureTransport`, `test_security_logging.py`, `run`, `test_session.py`, `PqcMetrics`, `test_public_key_client.py`, `session_client.py`, `test_crypto_failures.py`, `live_gateway`, `CryptoFailureInjector`, `encapsulate`, `derive_session_key`, `_dispatch`, `test_pqc_observability.py`, `test_handshake_failure_stays_closed_without_a_session`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_session_expiry_system.py`, `test_gateway_application_failures.py`, `main`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `edge_gateway/app.py`, `test_security_logging.py`, `SessionManager`, `create_app`, `CloudDispatch`, `test_secure_transport.py`, `PqcMetrics`, `edge_gateway/crypto/symmetric.py`, `test_crypto_failures.py`, `live_gateway`, `CryptoFailureInjector`, `_dispatch`, `edge_gateway/crypto/envelope.py`, `_Sessions`, `edge_gateway/crypto/encoding.py`, `test_pqc_observability.py`, `test_handshake_failure_stays_closed_without_a_session`, `edge_gateway/crypto/aad.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_session_expiry_system.py`, `GatewayMetrics`, `test_gateway_application_failures.py`, `main`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `edge_gateway/app.py`, `SecureTransport`, `test_security_logging.py`, `CloudDispatch`, `test_secure_transport.py`, `PqcMetrics`, `test_lifespan_closes_baseline_and_rejects_late_requests`, `load_config`, `LegacyMeasurement`, `test_gateway_measurements.py`, `live_gateway`, `CryptoFailureInjector`, `test_baseline_gateway_measurements`, `MeasurementProcessor`, `measurements.py`, `test_gateway_validation.py`, `edge_gateway/validation.py`, `test_gateway_routes.py`, `BaselineCloudError`, `test_gateway_response_mapping.py`, `GatewayMetrics`, `test_gateway_application_failures.py`, `test_gateway_operations.py`, `test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery`, `GatewayErrorCode`, `ApplicationFailures`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_validation_bypass.py`, `_baseline_transport`, `test_untrusted_values_do_not_create_metric_labels`, `_Gateway`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05258033106134372 - nodes in this community are weakly interconnected._