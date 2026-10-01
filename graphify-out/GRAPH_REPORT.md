# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2081 nodes · 5158 edges · 124 communities (79 shown, 45 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 733 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_gateway_cloud_secure.py
- cli.py
- test_baseline_client.py
- GatewayClient
- SecureTransport
- secure_transport.py
- MeasurementRepository
- load_config
- SessionManager
- load_config
- test_public_key_client.py
- GatewayErrorCode
- test_gateway_validation.py
- test_session.py
- validate_measurement
- PqcMetrics
- test_cloud_mlkem.py
- CloudDispatch
- secure.py
- edge_gateway/crypto/symmetric.py
- CanonicalMeasurement
- test_cloud_secure.py
- test_session_recovery_is_counted
- SessionManager
- test_sensor.py
- database.py
- encapsulate
- test_legacy_compatibility.py
- LegacyMeasurement
- test_mode_evaluation.py
- cloud_service/app.py
- derive_session_key
- test_cloud_failure_injection.py
- test_secure_message_tamper.py
- measure_baseline.py
- session_client.py
- SecureEnvelope
- CanonicalMeasurement
- test_secure_shutdown.py
- make_config
- FailureMode
- test_gateway_measurements.py
- test_secure_transport.py
- decode_binary
- build_aad
- edge_gateway/crypto/envelope.py
- public_key.py
- cloud_service/crypto/mlkem.py
- edge_gateway/app.py
- test_cloud_queries.py
- test_cloud_session_api.py
- create_app
- DeviceController
- test_cloud_config.py
- test_cloud_baseline.py
- edge_gateway/models.py
- test_device.py
- test_gateway_correlation.py
- encode_binary
- CryptoFailureInjector
- test_crypto_failures.py
- envelope_validation.py
- edge_gateway/crypto/aad.py
- pathlib
- KeyService
- test_clean_container_crypto.py
- test_cloud_public_key.py
- test_gateway_errors.py
- test_gateway_response_mapping.py
- refresh_graphify.py
- test_gateway_crypto_image.py
- handshake
- measurements.py
- test_secure_envelope.py
- test_shutdown_after_gateway_unavailable_delivery
- RecordingClient
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- _Clock
- _HandshakeHandler
- ConfigurationError
- queries.py
- test_refresh_graphify.py
- Measurement
- test_repository_hygiene.py
- pytest
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- _Handler
- _Handler
- test_client_exception_is_logged_then_loop_continues_and_closes
- _Gateway
- test_shared_integration_assets.py
- .shutdown
- test_session_missing_and_expired_force_a_new_handshake
- _Handler
- _Response
- _Handler
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 57 edges
2. `load_config()` - 53 edges
3. `load_config()` - 47 edges
4. `SecureTransport` - 45 edges
5. `FailureMode` - 44 edges
6. `create_app()` - 43 edges
7. `SessionManager` - 38 edges
8. `SecureTransportError` - 37 edges
9. `FailureMode` - 35 edges
10. `FailureInjector` - 34 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `CloudHarness` --uses--> `FailureMode`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → cloud_service/src/cloud_service/config.py
- `CloudHarness` --uses--> `StoredMeasurement`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → cloud_service/src/cloud_service/storage/models.py

## Import Cycles
- None detected.

## Communities (124 total, 45 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+25 more)

### Community 2 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 3 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (24): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+16 more)

### Community 4 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 5 - "SecureTransport"
Cohesion: 0.09
Nodes (14): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport (+6 more)

### Community 7 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 8 - "load_config"
Cohesion: 0.10
Nodes (23): create_app(), health(), ready(), main(), _unavailable(), load_config(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings() (+15 more)

### Community 9 - "SessionManager"
Cohesion: 0.10
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 10 - "load_config"
Cohesion: 0.13
Nodes (23): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+15 more)

### Community 11 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (17): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), _Handler, _public_key() (+9 more)

### Community 12 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (13): GatewayError, GatewayErrorCode, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state() (+5 more)

### Community 13 - "test_gateway_validation.py"
Cohesion: 0.11
Nodes (21): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), assert_rejection() (+13 more)

### Community 14 - "test_session.py"
Cohesion: 0.10
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 15 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 16 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, DispatchMetrics

### Community 17 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (9): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected() (+1 more)

### Community 18 - "CloudDispatch"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 19 - "secure.py"
Cohesion: 0.11
Nodes (9): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement() (+1 more)

### Community 20 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 21 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 22 - "test_cloud_secure.py"
Cohesion: 0.18
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 23 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (12): _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 24 - "SessionManager"
Cohesion: 0.11
Nodes (4): SecureSession, SessionEstablishmentError, SessionManager, _session()

### Community 25 - "test_sensor.py"
Cohesion: 0.12
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 26 - "database.py"
Cohesion: 0.12
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 27 - "encapsulate"
Cohesion: 0.13
Nodes (13): test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+5 more)

### Community 28 - "test_legacy_compatibility.py"
Cohesion: 0.14
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 29 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 30 - "test_mode_evaluation.py"
Cohesion: 0.13
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 31 - "cloud_service/app.py"
Cohesion: 0.15
Nodes (9): SecurityMode, derive_session_key(), public_key(), _unavailable(), _decode_ciphertext(), _error(), _establish(), establish_session() (+1 more)

### Community 32 - "derive_session_key"
Cohesion: 0.13
Nodes (10): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+2 more)

### Community 33 - "test_cloud_failure_injection.py"
Cohesion: 0.17
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 34 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 35 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 36 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 37 - "SecureEnvelope"
Cohesion: 0.19
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 38 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 39 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 40 - "make_config"
Cohesion: 0.16
Nodes (10): FakeResponse, FakeSensor, make_config(), ScriptedOpener, test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure(), test_runtime_logs_lifecycle_and_delivery_events() (+2 more)

### Community 41 - "FailureMode"
Cohesion: 0.15
Nodes (7): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes()

### Community 42 - "test_gateway_measurements.py"
Cohesion: 0.17
Nodes (12): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook() (+4 more)

### Community 43 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 44 - "decode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 45 - "build_aad"
Cohesion: 0.21
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 46 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.19
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 47 - "public_key.py"
Cohesion: 0.18
Nodes (9): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 48 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 49 - "edge_gateway/app.py"
Cohesion: 0.14
Nodes (6): _baseline_transport(), get_config(), _logging_level(), main(), GatewayConfig, BaselineTransport

### Community 50 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 52 - "create_app"
Cohesion: 0.16
Nodes (12): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+4 more)

### Community 54 - "test_cloud_config.py"
Cohesion: 0.17
Nodes (10): Config, test_custom_environment(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries(), test_invalid_configuration(), test_invalid_database_url(), test_process_environment_and_explicit_mapping() (+2 more)

### Community 55 - "test_cloud_baseline.py"
Cohesion: 0.15
Nodes (7): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 56 - "edge_gateway/models.py"
Cohesion: 0.17
Nodes (5): _timestamp(), normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input()

### Community 57 - "test_device.py"
Cohesion: 0.17
Nodes (6): FakeMeasurement, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, test_falsey_injected_dependencies_are_preserved()

### Community 58 - "test_gateway_correlation.py"
Cohesion: 0.19
Nodes (7): baseline_headers(), create_request_id(), build_secure_envelope(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 59 - "encode_binary"
Cohesion: 0.24
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _different_nonce(), _tamper()

### Community 61 - "test_crypto_failures.py"
Cohesion: 0.20
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 62 - "envelope_validation.py"
Cohesion: 0.22
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 63 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 65 - "KeyService"
Cohesion: 0.17
Nodes (4): lifespan(), StartupError, KeyService, test_session_initialization_failure_releases_keys()

### Community 66 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 67 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 68 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 69 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 70 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 71 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 72 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 74 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 75 - "test_shutdown_after_gateway_unavailable_delivery"
Cohesion: 0.22
Nodes (4): test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown(), fake_signal()

### Community 76 - "RecordingClient"
Cohesion: 0.20
Nodes (4): RecordingClient, RecordingFailureInjector, test_delivery_failure_does_not_stop_loop_or_roll_back_sequence(), test_runtime_pipeline_serializes_before_failure_injection_and_sends()

### Community 77 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 78 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 79 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 81 - "ConfigurationError"
Cohesion: 0.32
Nodes (6): ConfigurationError, integer(), number(), text(), value(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 82 - "queries.py"
Cohesion: 0.46
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 83 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 92 - "test_client_exception_is_logged_then_loop_continues_and_closes"
Cohesion: 0.33
Nodes (4): RaisingClient, test_client_exception_is_logged_then_loop_continues_and_closes(), test_stop_during_delivery_skips_interval_wait(), send()

### Community 105 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 702 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `SecureTransport`, `secure_transport.py`, `edge_gateway/app.py`, `CloudDispatch`, `create_app`, `test_session_recovery_is_counted`, `SessionManager`, `test_mode_evaluation.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `secure_transport.py`, `load_config`, `PqcMetrics`, `CloudDispatch`, `edge_gateway/crypto/symmetric.py`, `test_session_recovery_is_counted`, `SessionManager`, `test_mode_evaluation.py`, `test_secure_shutdown.py`, `test_secure_transport.py`, `edge_gateway/crypto/envelope.py`, `edge_gateway/app.py`, `create_app`, `encode_binary`, `CryptoFailureInjector`, `edge_gateway/crypto/aad.py`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `.shutdown`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `derive_session_key`, `test_gateway_cloud_secure.py`, `session_client.py`, `SecureTransport`, `secure_transport.py`, `load_config`, `test_session_missing_and_expired_force_a_new_handshake`, `test_public_key_client.py`, `test_session.py`, `public_key.py`, `PqcMetrics`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `test_session_recovery_is_counted`, `encapsulate`, `CryptoFailureInjector`, `test_crypto_failures.py`, `test_mode_evaluation.py`, `.shutdown`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.060191518467852256 - nodes in this community are weakly interconnected._
- **Should `test_gateway_cloud_secure.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05314685314685315 - nodes in this community are weakly interconnected._