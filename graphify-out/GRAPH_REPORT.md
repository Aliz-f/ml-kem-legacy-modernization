# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2347 nodes · 5848 edges · 139 communities (87 shown, 52 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 805 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_secure_transport.py
- test_device.py
- test_gateway_cloud_secure.py
- cli.py
- test_gateway_crypto_image.py
- test_baseline_client.py
- GatewayClient
- SecureTransport
- GatewayErrorCode
- SessionManager
- secure_transport.py
- load_config
- test_gateway_validation.py
- test_session.py
- validate_measurement
- create_app
- test_public_key_client.py
- FailureMode
- secure.py
- test_cloud_secure.py
- CanonicalMeasurement
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- edge_gateway/app.py
- LegacyMeasurement
- MeasurementRepository
- edge_gateway/crypto/symmetric.py
- edge_gateway/crypto/envelope.py
- encode_binary
- PqcMetrics
- SecureEnvelope
- test_cloud_failure_injection.py
- SessionManager
- FailureInjector
- test_crypto_failures.py
- StoredMeasurement
- test_cloud_queries.py
- session_client.py
- CanonicalMeasurement
- load_config
- CloudMetrics
- test_cloud_baseline.py
- CloudDispatch
- edge_gateway/crypto/encoding.py
- encapsulate
- test_gateway_measurements.py
- sessions.py
- public_key.py
- test_cloud_kdf.py
- _Sessions
- build_aad
- SecureSession
- StorageError
- log_security
- encrypt
- test_sensor.py
- cloud_service/crypto/mlkem.py
- edge_gateway/crypto/mlkem.py
- derive_session_key
- normalize
- test_legacy_gateway.py
- run
- edge_gateway/crypto/aad.py
- run
- test_pqc_observability.py
- test_full_path_integration.py
- pytest
- test_cloud_public_key.py
- test_gateway_correlation.py
- live_cloud
- test_gateway_errors.py
- test_gateway_response_mapping.py
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- envelope_validation.py
- handshake
- test_secure_envelope.py
- measure_modes
- _Clock
- _HandshakeHandler
- test_dependency_review.py
- test_session_recovery_is_counted
- test_baseline_gateway_measurements
- Measurement
- FalseyClock
- _Cloud
- test_end_to_end.py
- _Cloud
- _Handler
- test_refresh_graphify.py
- test_repository_hygiene.py
- _crypto_dependencies_ready
- StartupError
- _install
- test_final_secure_transport_review.py
- _Handler
- _Handler
- _Sizes
- live_cloud
- _Server
- test_shared_integration_assets.py
- public_key
- SessionState
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _DroppedResponse
- edge_gateway/models.py
- _Response
- test_gateway_crypto_ci.py
- test_synthetic_secret_markers_never_appear_in_cloud_logs
- _Baseline
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 60 edges
2. `load_config()` - 57 edges
3. `load_config()` - 51 edges
4. `SecureTransport` - 49 edges
5. `create_app()` - 49 edges
6. `FailureMode` - 46 edges
7. `SessionManager` - 44 edges
8. `SecureTransportError` - 40 edges
9. `PqcMetrics` - 39 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `_deliver()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py
- `test_duplicate_sequence_is_stored_once()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py
- `test_one_handshake_is_reused_for_three_measurements()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py
- `test_a_second_session_rejection_is_not_recovered()` --uses--> `SecureTransportError`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py

## Import Cycles
- None detected.

## Communities (139 total, 52 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_secure_transport.py"
Cohesion: 0.05
Nodes (47): _dump(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransportError, _SessionRecovery (+39 more)

### Community 2 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 3 - "test_gateway_cloud_secure.py"
Cohesion: 0.06
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 5 - "test_gateway_crypto_image.py"
Cohesion: 0.06
Nodes (18): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+10 more)

### Community 6 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (24): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+16 more)

### Community 7 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 8 - "SecureTransport"
Cohesion: 0.07
Nodes (13): main(), _secure_transport(), CryptoFailureInjector, _endpoint(), SecureTransport, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _count() (+5 more)

### Community 9 - "GatewayErrorCode"
Cohesion: 0.11
Nodes (14): GatewayError, GatewayErrorCode, UnavailableBaseline, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit() (+6 more)

### Community 10 - "SessionManager"
Cohesion: 0.09
Nodes (13): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes() (+5 more)

### Community 12 - "load_config"
Cohesion: 0.10
Nodes (27): _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config() (+19 more)

### Community 13 - "test_gateway_validation.py"
Cohesion: 0.10
Nodes (21): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client() (+13 more)

### Community 14 - "test_session.py"
Cohesion: 0.10
Nodes (15): _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+7 more)

### Community 16 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 17 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+10 more)

### Community 18 - "test_public_key_client.py"
Cohesion: 0.13
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, _body(), _public_key(), test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+8 more)

### Community 19 - "FailureMode"
Cohesion: 0.12
Nodes (10): Config, FailureMode, FailureInjector, FailureSelection, test_custom_environment(), test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects() (+2 more)

### Community 20 - "secure.py"
Cohesion: 0.11
Nodes (10): SecurityMode, AadError, build_aad(), AeadError, decrypt(), _error(), _ingest(), _NoMetrics (+2 more)

### Community 21 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 22 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 23 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 24 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 25 - "edge_gateway/app.py"
Cohesion: 0.11
Nodes (13): _baseline_transport(), create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready() (+5 more)

### Community 26 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 27 - "MeasurementRepository"
Cohesion: 0.14
Nodes (18): lifespan(), Database, MeasurementRepository, test_acceptance_is_committed_and_correlated(), test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+10 more)

### Community 28 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.12
Nodes (12): test_vendor_error_diagnostics_are_suppressed(), main(), AeadError, decrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+4 more)

### Community 29 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.14
Nodes (12): build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement() (+4 more)

### Community 30 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 32 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 33 - "test_cloud_failure_injection.py"
Cohesion: 0.19
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 34 - "SessionManager"
Cohesion: 0.11
Nodes (8): lifespan(), SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run(), _Baseline, test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), test_injected_handshake_failure_stays_fail_closed()

### Community 35 - "FailureInjector"
Cohesion: 0.15
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 36 - "test_crypto_failures.py"
Cohesion: 0.12
Nodes (11): _Clock, handshake_url(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_enabled_warning_names_the_mode_and_not_the_seed() (+3 more)

### Community 37 - "StoredMeasurement"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 38 - "test_cloud_queries.py"
Cohesion: 0.12
Nodes (15): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+7 more)

### Community 39 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 41 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 42 - "load_config"
Cohesion: 0.21
Nodes (14): ConfigurationError, load_config(), integer(), number(), text(), value(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values() (+6 more)

### Community 43 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 44 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): client(), payload(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500() (+1 more)

### Community 45 - "CloudDispatch"
Cohesion: 0.13
Nodes (5): get_config(), GatewayConfig, CloudDispatch, DispatchMetrics, MeasurementProcessor

### Community 46 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.17
Nodes (10): decode_binary(), encode_binary(), EncodingError, _HandshakeCloud, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip() (+2 more)

### Community 47 - "encapsulate"
Cohesion: 0.16
Nodes (11): encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged(), test_valid_public_key_round_trip_matches_decapsulation() (+3 more)

### Community 48 - "test_gateway_measurements.py"
Cohesion: 0.17
Nodes (12): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook() (+4 more)

### Community 49 - "sessions.py"
Cohesion: 0.18
Nodes (7): derive_session_key(), KdfError, _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 50 - "public_key.py"
Cohesion: 0.18
Nodes (9): validate_public_key(), CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected() (+1 more)

### Community 51 - "test_cloud_kdf.py"
Cohesion: 0.12
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 53 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 54 - "build_aad"
Cohesion: 0.25
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 55 - "SecureSession"
Cohesion: 0.15
Nodes (5): _Sessions, SecureSession, _Sessions, test_seal_failure_is_counted_without_the_session_key(), get_or_establish()

### Community 56 - "StorageError"
Cohesion: 0.20
Nodes (5): _error(), get_measurement(), list_measurements(), StorageConflictError, StorageError

### Community 57 - "log_security"
Cohesion: 0.16
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, test_unsafe_log_values_are_dropped()

### Community 58 - "encrypt"
Cohesion: 0.37
Nodes (12): encrypt(), _aad(), _key(), _plaintext(), test_authentication_failure_does_not_return_plaintext(), test_independent_cloud_aad_authenticates_and_each_field_change_fails(), test_invalid_key_and_nonce_lengths_are_rejected(), test_keys_and_plaintext_are_not_logged() (+4 more)

### Community 59 - "test_sensor.py"
Cohesion: 0.21
Nodes (13): Sensor, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc(), test_payload_has_exact_field_names_and_serialized_values(), test_payload_is_independent_from_model_and_other_payloads() (+5 more)

### Community 60 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 61 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.16
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 62 - "derive_session_key"
Cohesion: 0.20
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 63 - "normalize"
Cohesion: 0.18
Nodes (5): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 64 - "test_legacy_gateway.py"
Cohesion: 0.27
Nodes (8): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_legacy_serializer_and_client_reach_live_gateway(), test_malformed_legacy_json_is_rejected_without_delivery(), test_parsed_invalid_legacy_payload_is_rejected_without_delivery()

### Community 65 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 66 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 67 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 68 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 69 - "test_full_path_integration.py"
Cohesion: 0.23
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 71 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 72 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 73 - "live_cloud"
Cohesion: 0.21
Nodes (7): live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(), test_legacy_to_sqlite_preserves_gateway_transformations()

### Community 74 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 75 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 76 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.17
Nodes (3): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 77 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 78 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 79 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 80 - "measure_modes"
Cohesion: 0.25
Nodes (6): _Calls, measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 81 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 83 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 84 - "test_session_recovery_is_counted"
Cohesion: 0.22
Nodes (4): _measurement(), _send(), test_session_recovery_is_counted(), get_or_establish()

### Community 85 - "test_baseline_gateway_measurements"
Cohesion: 0.25
Nodes (4): cloud(), test_baseline_gateway_measurements(), _post(), send()

### Community 87 - "FalseyClock"
Cohesion: 0.29
Nodes (3): FalseyClock, FalseyRandomSource, test_sensor_preserves_falsey_supplied_dependencies()

### Community 89 - "test_end_to_end.py"
Cohesion: 0.32
Nodes (3): query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row()

### Community 92 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 94 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 97 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 103 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 110 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 112 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 800 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **52 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureSession` connect `SecureSession` to `test_secure_transport.py`, `SessionManager`, `SecureTransport`, `edge_gateway/crypto/session.py`, `secure_transport.py`, `SessionState`, `test_session.py`, `test_session_recovery_is_counted`, `_Sessions`, `log_security`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_legacy_gateway.py`, `test_gateway_cloud_secure.py`, `test_crypto_failures.py`, `test_pqc_observability.py`, `session_client.py`, `SecureTransport`, `edge_gateway/crypto/session.py`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`, `test_session.py`, `encapsulate`, `create_app`, `test_public_key_client.py`, `public_key.py`, `test_secure_message_tamper.py`, `edge_gateway/app.py`, `log_security`, `derive_session_key`, `PqcMetrics`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `FailureMode` connect `FailureMode` to `test_cloud_failure_injection.py`, `test_gateway_cloud_secure.py`, `load_config`, `public_key`, `cloud_service/app.py`, `validate_measurement`, `sessions.py`, `secure.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.05616605616605617 - nodes in this community are weakly interconnected._
- **Should `test_secure_transport.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05459770114942529 - nodes in this community are weakly interconnected._