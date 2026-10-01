# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2089 nodes · 5188 edges · 119 communities (79 shown, 40 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 736 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_secure_transport.py
- FailureMode
- test_gateway_cloud_secure.py
- cli.py
- test_baseline_client.py
- GatewayErrorCode
- GatewayClient
- test_public_key_client.py
- MeasurementRepository
- secure_transport.py
- test_sensor.py
- test_gateway_crypto_image.py
- test_crypto_failures.py
- logging
- create_app
- test_cloud_secure.py
- create_app
- CloudDispatch
- FailureMode
- secure.py
- SessionManager
- CanonicalMeasurement
- SessionManager
- edge_gateway/crypto/symmetric.py
- pytest
- test_secure_message_tamper.py
- PqcMetrics
- test_session_recovery_is_counted
- LegacyMeasurement
- edge_gateway/crypto/session.py
- CryptoFailureInjector
- decode_binary
- cloud_service/app.py
- SecureEnvelope
- StoredMeasurement
- encapsulate
- load_config
- validate_measurement
- session_client.py
- load_config
- derive_session_key
- CanonicalMeasurement
- _dispatch
- test_legacy_compatibility.py
- database.py
- measure_baseline.py
- edge_gateway/crypto/envelope.py
- test_cloud_baseline.py
- edge_gateway/app.py
- _Sessions
- fields
- test_cloud_queries.py
- SecureTransport
- encode_binary
- test_gateway_validation.py
- test_cloud_session_api.py
- test_cloud_mlkem.py
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- edge_gateway/validation.py
- build_aad
- DeviceController
- Transport
- make_config
- test_refresh_graphify.py
- test_gateway_correlation.py
- normalize
- sessions.py
- test_cloud_public_key.py
- test_gateway_app.py
- test_gateway_errors.py
- SecurityMode
- envelope_validation.py
- test_secure_envelope.py
- test_shutdown_after_gateway_unavailable_delivery
- RecordingClient
- parse_public_key_response
- _Clock
- _HandshakeHandler
- test_falsey_injected_dependencies_are_preserved
- FailureInjector
- KdfError
- StartupError
- SessionAccessError
- FailureSelection
- FakeResponse
- test_repository_hygiene.py
- _Handler
- test_client_exception_is_logged_then_loop_continues_and_closes
- _Gateway
- edge_gateway/models.py
- _Handler
- scenario
- FakeMeasurement
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 57 edges
2. `load_config()` - 53 edges
3. `load_config()` - 48 edges
4. `SecureTransport` - 45 edges
5. `FailureMode` - 44 edges
6. `create_app()` - 44 edges
7. `SessionManager` - 38 edges
8. `SecureTransportError` - 37 edges
9. `FailureMode` - 35 edges
10. `FailureInjector` - 34 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `SessionEstablishmentError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/session.py

## Import Cycles
- None detected.

## Communities (119 total, 40 thin omitted)

### Community 0 - "test_secure_transport.py"
Cohesion: 0.06
Nodes (35): SessionEstablishmentError, SessionState, _Cloud, _error(), _Handler, _send(), _session(), _Sessions (+27 more)

### Community 1 - "FailureMode"
Cohesion: 0.07
Nodes (46): ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value(), FailureInjector (+38 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 3 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 4 - "test_baseline_client.py"
Cohesion: 0.08
Nodes (27): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+19 more)

### Community 5 - "GatewayErrorCode"
Cohesion: 0.09
Nodes (15): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once() (+7 more)

### Community 6 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 7 - "test_public_key_client.py"
Cohesion: 0.08
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, PublicKeyRejected, _body(), cloud_server(), _Handler (+11 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 9 - "secure_transport.py"
Cohesion: 0.11
Nodes (12): build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect (+4 more)

### Community 10 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 11 - "test_gateway_crypto_image.py"
Cohesion: 0.08
Nodes (11): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version() (+3 more)

### Community 12 - "test_crypto_failures.py"
Cohesion: 0.09
Nodes (18): _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud, _plaintext() (+10 more)

### Community 13 - "logging"
Cohesion: 0.12
Nodes (7): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero()

### Community 14 - "create_app"
Cohesion: 0.08
Nodes (21): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+13 more)

### Community 15 - "test_cloud_secure.py"
Cohesion: 0.16
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 16 - "create_app"
Cohesion: 0.11
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+10 more)

### Community 17 - "CloudDispatch"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 18 - "FailureMode"
Cohesion: 0.17
Nodes (21): FailureMode, canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently() (+13 more)

### Community 19 - "secure.py"
Cohesion: 0.11
Nodes (9): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement() (+1 more)

### Community 20 - "SessionManager"
Cohesion: 0.12
Nodes (11): SecureSession, SessionManager, SessionState, clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 21 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 22 - "SessionManager"
Cohesion: 0.12
Nodes (4): log_security(), _token(), SecureSession, SessionManager

### Community 23 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 24 - "pytest"
Cohesion: 0.09
Nodes (4): test_rendered_metrics_keep_bounded_labels_and_zero_fallback(), test_quality_workflow_names_the_gateway_crypto_suites(), _fixture(), test_shared_fixtures_match_the_frozen_legacy_and_canonical_shapes()

### Community 25 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 27 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (12): _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 28 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 30 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (4): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 31 - "decode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 32 - "cloud_service/app.py"
Cohesion: 0.11
Nodes (3): _install(), _serve(), _Server

### Community 33 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 34 - "StoredMeasurement"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 35 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 36 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 37 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 38 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 39 - "load_config"
Cohesion: 0.20
Nodes (15): ConfigurationError, load_config(), integer(), number(), text(), value(), test_unrelated_record_id_collision_is_not_idempotent_success(), test_defaults_do_not_create_database() (+7 more)

### Community 40 - "derive_session_key"
Cohesion: 0.14
Nodes (9): KdfError, main(), derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+1 more)

### Community 41 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 42 - "_dispatch"
Cohesion: 0.13
Nodes (9): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Sizes, test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline() (+1 more)

### Community 43 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 44 - "database.py"
Cohesion: 0.15
Nodes (5): _error(), get_measurement(), list_measurements(), baseline_measurement(), _error()

### Community 45 - "measure_baseline.py"
Cohesion: 0.16
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 46 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.19
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 47 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 48 - "edge_gateway/app.py"
Cohesion: 0.14
Nodes (6): _baseline_transport(), get_config(), _logging_level(), main(), GatewayConfig, BaselineTransport

### Community 49 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 50 - "fields"
Cohesion: 0.22
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 51 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 52 - "SecureTransport"
Cohesion: 0.14
Nodes (4): lifespan(), _endpoint(), SecureTransport, DispatchMetrics

### Community 53 - "encode_binary"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 54 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 55 - "test_cloud_session_api.py"
Cohesion: 0.20
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 56 - "test_cloud_mlkem.py"
Cohesion: 0.15
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 57 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 58 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 59 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 60 - "build_aad"
Cohesion: 0.22
Nodes (7): AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 62 - "Transport"
Cohesion: 0.19
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 63 - "make_config"
Cohesion: 0.25
Nodes (8): FakeSensor, make_config(), test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure(), test_runtime_logs_lifecycle_and_delivery_events(), stop_after_first_measurement(), test_stop_prevents_work_and_closes_client()

### Community 64 - "test_refresh_graphify.py"
Cohesion: 0.19
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 65 - "test_gateway_correlation.py"
Cohesion: 0.23
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 66 - "normalize"
Cohesion: 0.22
Nodes (5): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 67 - "sessions.py"
Cohesion: 0.32
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 68 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 69 - "test_gateway_app.py"
Cohesion: 0.18
Nodes (9): test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration(), test_settings_dependency_can_be_overridden_and_isolated() (+1 more)

### Community 70 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 71 - "SecurityMode"
Cohesion: 0.24
Nodes (4): SecurityMode, public_key(), _unavailable(), test_custom_environment()

### Community 72 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 73 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 74 - "test_shutdown_after_gateway_unavailable_delivery"
Cohesion: 0.22
Nodes (4): test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown(), fake_signal()

### Community 75 - "RecordingClient"
Cohesion: 0.20
Nodes (4): RecordingClient, RecordingFailureInjector, test_delivery_failure_does_not_stop_loop_or_roll_back_sequence(), test_runtime_pipeline_serializes_before_failure_injection_and_sends()

### Community 76 - "parse_public_key_response"
Cohesion: 0.33
Nodes (6): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 77 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 79 - "test_falsey_injected_dependencies_are_preserved"
Cohesion: 0.22
Nodes (5): FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, test_falsey_injected_dependencies_are_preserved()

### Community 81 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 82 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 90 - "test_client_exception_is_logged_then_loop_continues_and_closes"
Cohesion: 0.33
Nodes (4): RaisingClient, test_client_exception_is_logged_then_loop_continues_and_closes(), test_stop_during_delivery_skips_interval_wait(), send()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 706 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `secure_transport.py`, `_dispatch`, `edge_gateway/app.py`, `create_app`, `CloudDispatch`, `SecureTransport`, `SessionManager`, `pytest`, `test_session_recovery_is_counted`, `edge_gateway/crypto/session.py`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_secure_transport.py`, `test_gateway_cloud_secure.py`, `secure_transport.py`, `_dispatch`, `test_crypto_failures.py`, `create_app`, `edge_gateway/crypto/envelope.py`, `edge_gateway/app.py`, `create_app`, `CloudDispatch`, `_Sessions`, `encode_binary`, `SessionManager`, `edge_gateway/crypto/symmetric.py`, `PqcMetrics`, `test_session_recovery_is_counted`, `build_aad`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `secure_transport.py`, `_dispatch`, `test_crypto_failures.py`, `edge_gateway/app.py`, `SecureTransport`, `SessionManager`, `test_session_recovery_is_counted`, `edge_gateway/crypto/session.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_secure_transport.py` be split into smaller, more focused modules?**
  _Cohesion score 0.056338028169014086 - nodes in this community are weakly interconnected._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.07418788410886742 - nodes in this community are weakly interconnected._