# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2290 nodes · 5719 edges · 145 communities (87 shown, 58 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 819 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- test_gateway_cloud_secure.py
- cli.py
- GatewayClient
- test_handshake_failure_stays_closed_without_a_session
- secure_transport.py
- MeasurementRepository
- test_gateway_crypto_image.py
- CryptoFailureInjector
- test_public_key_client.py
- SecureTransport
- edge_gateway/crypto/symmetric.py
- CanonicalMeasurement
- SecureSession
- CloudDispatch
- test_cloud_secure.py
- SessionManager
- secure.py
- test_sensor.py
- create_app
- PqcMetrics
- test_secure_message_tamper.py
- load_config
- test_legacy_compatibility.py
- validate_measurement
- FailureInjector
- test_session.py
- encode_binary
- SessionManager
- test_cloud_failure_injection.py
- LegacyMeasurement
- test_secure_transport.py
- SecureEnvelope
- CloudMetrics
- load_config
- edge_gateway/crypto/encoding.py
- edge_gateway/crypto/envelope.py
- session_client.py
- CanonicalMeasurement
- FailureMode
- StoredMeasurement
- build_aad
- test_cloud_baseline.py
- SequenceTracker
- test_secure_shutdown.py
- sessions.py
- test_cloud_queries.py
- create_app
- derive_session_key
- cloud_service/crypto/mlkem.py
- encapsulate
- MeasurementProcessor
- test_cloud_kdf.py
- test_baseline_client.py
- edge_gateway/config.py
- Transport
- run
- test_crypto_failures.py
- edge_gateway/crypto/mlkem.py
- test_gateway_validation.py
- validate_legacy_measurement
- BaselineCloudClient
- test_refresh_graphify.py
- edge_gateway/crypto/aad.py
- test_cloud_public_key.py
- test_gateway_correlation.py
- GatewayError
- edge_gateway/validation.py
- live_cloud
- test_gateway_response_mapping.py
- envelope_validation.py
- handshake
- test_gateway_application_failures.py
- test_secure_envelope.py
- test_pqc_observability.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- _baseline_transport
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- queries.py
- _HandshakeHandler
- SessionState
- ApplicationFailures
- test_baseline_gateway_measurements
- test_public_key.py
- Measurement
- SessionAccessError
- test_repository_hygiene.py
- _crypto_dependencies_ready
- StartupError
- GatewayErrorCode
- test_gateway_config.py
- _Handler
- _Handler
- test_shared_integration_assets.py
- public_key
- .shutdown
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- edge_gateway/models.py
- _Handler
- _Handler
- _Response
- _Handler
- _Handler
- test_gateway_crypto_ci.py
- .send
- _RejectRedirect
- _Cloud
- test_faults_preserve_real_cloud_storage_and_mode_boundaries
- scenario
- _Cloud
- payload
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 67 edges
2. `create_app()` - 67 edges
3. `SecureTransport` - 50 edges
4. `load_config()` - 50 edges
5. `create_app()` - 48 edges
6. `FailureMode` - 46 edges
7. `SessionManager` - 44 edges
8. `PqcMetrics` - 42 edges
9. `SecureTransportError` - 37 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `PublicKeyRejected`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/public_key.py
- `_deliver()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py
- `test_duplicate_sequence_is_stored_once()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py
- `test_one_handshake_is_reused_for_three_measurements()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py
- `test_corrupted_ciphertext_is_rejected_and_not_stored()` --uses--> `SecureTransport`  [INFERRED]
  tests/integration/test_corrupt_ciphertext_demo.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py

## Import Cycles
- None detected.

## Communities (145 total, 58 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 3 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 4 - "GatewayClient"
Cohesion: 0.07
Nodes (24): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener (+16 more)

### Community 5 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.05
Nodes (19): _install(), main(), _serve(), _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session() (+11 more)

### Community 6 - "secure_transport.py"
Cohesion: 0.11
Nodes (3): get_config(), GatewayConfig, corrupt_ciphertext_copy()

### Community 7 - "MeasurementRepository"
Cohesion: 0.11
Nodes (23): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+15 more)

### Community 8 - "test_gateway_crypto_image.py"
Cohesion: 0.08
Nodes (11): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version() (+3 more)

### Community 9 - "CryptoFailureInjector"
Cohesion: 0.07
Nodes (8): _secure_transport(), CryptoFailureInjector, _endpoint(), _SessionRecovery, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), test_same_seed_makes_the_same_decisions()

### Community 10 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+10 more)

### Community 11 - "SecureTransport"
Cohesion: 0.12
Nodes (12): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+4 more)

### Community 12 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.18
Nodes (21): main(), AeadError, decrypt(), encrypt(), generate_nonce(), _require_bytes(), _require_key(), _require_nonce() (+13 more)

### Community 13 - "CanonicalMeasurement"
Cohesion: 0.12
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 14 - "SecureSession"
Cohesion: 0.08
Nodes (12): _Sessions, SecureSession, _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 15 - "CloudDispatch"
Cohesion: 0.14
Nodes (14): CloudDispatch, DispatchMetrics, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 16 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (26): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+18 more)

### Community 17 - "SessionManager"
Cohesion: 0.09
Nodes (10): clock(), SessionEstablishmentError, SessionManager, _injector(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode() (+2 more)

### Community 18 - "secure.py"
Cohesion: 0.11
Nodes (9): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+1 more)

### Community 19 - "test_sensor.py"
Cohesion: 0.11
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 21 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+9 more)

### Community 22 - "PqcMetrics"
Cohesion: 0.08
Nodes (5): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 23 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 24 - "load_config"
Cohesion: 0.16
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), SecurityMode (+9 more)

### Community 25 - "test_legacy_compatibility.py"
Cohesion: 0.14
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 26 - "validate_measurement"
Cohesion: 0.15
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 27 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 28 - "test_session.py"
Cohesion: 0.13
Nodes (13): _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+5 more)

### Community 29 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 30 - "SessionManager"
Cohesion: 0.15
Nodes (10): SecureSession, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed() (+2 more)

### Community 31 - "test_cloud_failure_injection.py"
Cohesion: 0.17
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 32 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (14): LegacyMeasurement, LegacyMeasurementSchemaError, test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values(), test_extra_fields_are_rejected() (+6 more)

### Community 33 - "test_secure_transport.py"
Cohesion: 0.24
Nodes (18): session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable() (+10 more)

### Community 34 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 35 - "CloudMetrics"
Cohesion: 0.11
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 36 - "load_config"
Cohesion: 0.13
Nodes (15): _logging_level(), main(), load_config(), test_classical_app_constructs_and_uses_baseline_client(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health() (+7 more)

### Community 37 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.16
Nodes (10): decode_binary(), encode_binary(), EncodingError, _HandshakeCloud, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip() (+2 more)

### Community 38 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.17
Nodes (11): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement() (+3 more)

### Community 39 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 40 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 41 - "FailureMode"
Cohesion: 0.16
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 42 - "StoredMeasurement"
Cohesion: 0.15
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 43 - "build_aad"
Cohesion: 0.18
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 44 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+1 more)

### Community 45 - "SequenceTracker"
Cohesion: 0.16
Nodes (11): SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap(), test_gap_is_logged_and_advances_state() (+3 more)

### Community 46 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 47 - "sessions.py"
Cohesion: 0.18
Nodes (7): derive_session_key(), KdfError, _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 48 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (12): test_unrelated_record_id_collision_is_not_idempotent_success(), client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail() (+4 more)

### Community 49 - "create_app"
Cohesion: 0.14
Nodes (12): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+4 more)

### Community 50 - "derive_session_key"
Cohesion: 0.15
Nodes (11): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+3 more)

### Community 51 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 52 - "encapsulate"
Cohesion: 0.19
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 53 - "MeasurementProcessor"
Cohesion: 0.14
Nodes (7): MeasurementProcessor, CloudDeliveryError, CloudTransport, _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 54 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 56 - "test_baseline_client.py"
Cohesion: 0.30
Nodes (13): BaselineAcceptance, _client(), _send(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request(), test_redirect_is_rejected_and_constructor_validates_inputs() (+5 more)

### Community 57 - "edge_gateway/config.py"
Cohesion: 0.26
Nodes (12): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float() (+4 more)

### Community 58 - "Transport"
Cohesion: 0.17
Nodes (12): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook() (+4 more)

### Community 59 - "run"
Cohesion: 0.16
Nodes (11): test_existing_gateway_session_client_over_real_http(), canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run() (+3 more)

### Community 60 - "test_crypto_failures.py"
Cohesion: 0.16
Nodes (4): _Clock, handshake_url(), measurement_url(), _MeasurementCloud

### Community 61 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.16
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 62 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 65 - "validate_legacy_measurement"
Cohesion: 0.19
Nodes (7): measurements(), normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 66 - "BaselineCloudClient"
Cohesion: 0.19
Nodes (7): BaselineCloudClient, BaselineCloudError, _endpoint(), _error_code(), _parse_acceptance(), post(), test_timeout_and_connection_failures_are_retryable()

### Community 68 - "test_refresh_graphify.py"
Cohesion: 0.19
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 69 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 70 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 71 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 72 - "GatewayError"
Cohesion: 0.20
Nodes (5): GatewayError, test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized()

### Community 73 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 74 - "live_cloud"
Cohesion: 0.21
Nodes (7): live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(), test_legacy_to_sqlite_preserves_gateway_transformations()

### Community 75 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 76 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 77 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 78 - "test_gateway_application_failures.py"
Cohesion: 0.25
Nodes (6): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 79 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 80 - "test_pqc_observability.py"
Cohesion: 0.27
Nodes (5): _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 81 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 82 - "_baseline_transport"
Cohesion: 0.20
Nodes (3): _baseline_transport(), BaselineTransport, UnavailableBaseline

### Community 83 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 84 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 85 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 89 - "test_baseline_gateway_measurements"
Cohesion: 0.25
Nodes (4): cloud(), test_baseline_gateway_measurements(), _post(), send()

### Community 90 - "test_public_key.py"
Cohesion: 0.39
Nodes (5): _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 94 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 98 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 108 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 110 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 784 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **58 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeviceController` connect `test_device.py` to `FailureMode`, `test_sensor.py`, `GatewayClient`, `threading`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `GatewayClient` connect `GatewayClient` to `test_device.py`, `json`, `live_cloud`, `test_sensor.py`, `test_baseline_gateway_measurements`, `test_legacy_compatibility.py`, `threading`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_gateway_cloud_secure.py`, `test_handshake_failure_stays_closed_without_a_session`, `secure_transport.py`, `session_client.py`, `CryptoFailureInjector`, `test_public_key_client.py`, `.shutdown`, `SecureSession`, `test_gateway_application_failures.py`, `test_pqc_observability.py`, `create_app`, `derive_session_key`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `encapsulate`, `PqcMetrics`, `test_secure_message_tamper.py`, `run`, `test_session.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `SecureTransport` (e.g. with `main()` and `create_app()`) actually correct?**
  _`SecureTransport` has 31 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._