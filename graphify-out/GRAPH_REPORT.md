# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2117 nodes · 5247 edges · 121 communities (79 shown, 42 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 746 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_device.py
- test_legacy_compatibility.py
- test_gateway_cloud_secure.py
- cli.py
- load_config
- test_baseline_client.py
- measure_baseline.py
- FailureMode
- edge_gateway/crypto/session.py
- GatewayErrorCode
- FailureMode
- MeasurementRepository
- SessionManager
- cloud_service/app.py
- secure_transport.py
- SecureTransport
- test_mode_evaluation.py
- SessionManager
- logging
- test_cloud_secure.py
- PqcMetrics
- CloudDispatch
- edge_gateway/crypto/symmetric.py
- test_gateway_validation.py
- CanonicalMeasurement
- load_config
- create_app
- LegacyMeasurement
- test_cloud_session_api.py
- datetime
- test_sensor.py
- SecureEnvelope
- encapsulate
- test_secure_transport.py
- test_secure_message_tamper.py
- test_cloud_mlkem.py
- validate_measurement
- session_client.py
- test_session.py
- device.py
- asyncio
- CanonicalMeasurement
- test_secure_shutdown.py
- test_cloud_baseline.py
- build_aad
- edge_gateway/crypto/encoding.py
- Config
- edge_gateway/app.py
- SecureSession
- encode_binary
- test_cloud_queries.py
- edge_gateway/models.py
- test_gateway_measurements.py
- CryptoFailureInjector
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- edge_gateway/config.py
- edge_gateway/crypto/envelope.py
- parse_public_key_response
- edge_gateway/crypto/aad.py
- test_crypto_failures.py
- pathlib
- sessions.py
- test_clean_container_crypto.py
- pytest
- test_cloud_public_key.py
- test_gateway_correlation.py
- test_gateway_errors.py
- refresh_graphify.py
- test_gateway_crypto_image.py
- envelope_validation.py
- derive_session_key
- test_secure_envelope.py
- _Clock
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- edge_gateway/crypto/kdf.py
- _error_response
- _HandshakeHandler
- KdfError
- test_refresh_graphify.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- MeasurementProcessor
- test_gateway_config.py
- _Handler
- _Handler
- test_shared_integration_assets.py
- baseline_measurement
- test_session_missing_and_expired_force_a_new_handshake
- _Handler
- client
- _Handler
- _Handler
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 52 edges
2. `load_config()` - 50 edges
3. `load_config()` - 48 edges
4. `create_app()` - 48 edges
5. `SecureTransport` - 46 edges
6. `FailureMode` - 46 edges
7. `SessionManager` - 39 edges
8. `SecureTransportError` - 38 edges
9. `FailureMode` - 35 edges
10. `FailureInjector` - 34 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_legacy_gateway_cloud_http_path_persists_canonical_measurement()` --uses--> `GatewayClient`  [INFERRED]
  cloud_service/tests/test_full_path_integration.py → legacy_system/src/legacy_system/client.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `SessionEstablishmentError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/session.py

## Import Cycles
- None detected.

## Communities (121 total, 42 thin omitted)

### Community 0 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 1 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (36): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+28 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 3 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 4 - "load_config"
Cohesion: 0.08
Nodes (32): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+24 more)

### Community 5 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (25): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+17 more)

### Community 6 - "measure_baseline.py"
Cohesion: 0.07
Nodes (12): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), canonical(), Capture, distribution(), live_cloud(), lifespan() (+4 more)

### Community 7 - "FailureMode"
Cohesion: 0.11
Nodes (25): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+17 more)

### Community 8 - "edge_gateway/crypto/session.py"
Cohesion: 0.09
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+11 more)

### Community 9 - "GatewayErrorCode"
Cohesion: 0.11
Nodes (14): GatewayError, GatewayErrorCode, UnavailableBaseline, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit() (+6 more)

### Community 10 - "FailureMode"
Cohesion: 0.14
Nodes (25): FailureMode, FailureInjector, make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+17 more)

### Community 11 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 12 - "SessionManager"
Cohesion: 0.08
Nodes (6): lifespan(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 13 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (13): health(), ready(), _crypto_dependencies_ready(), _unavailable(), SessionAccessError, AeadError, decrypt(), _DroppedResponse (+5 more)

### Community 14 - "secure_transport.py"
Cohesion: 0.09
Nodes (11): corrupt_ciphertext_copy(), _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send() (+3 more)

### Community 15 - "SecureTransport"
Cohesion: 0.11
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 16 - "test_mode_evaluation.py"
Cohesion: 0.09
Nodes (13): _install(), main(), _serve(), _Baseline, _Calls, _dispatch(), measure_modes(), _serve() (+5 more)

### Community 17 - "SessionManager"
Cohesion: 0.11
Nodes (12): lifespan(), StartupError, SecureSession, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 18 - "logging"
Cohesion: 0.08
Nodes (6): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels(), test_shared_canonical_fixture_is_accepted_and_preserves_the_baseline_contract()

### Community 19 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (26): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+18 more)

### Community 20 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, DispatchMetrics

### Community 21 - "CloudDispatch"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 22 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 23 - "test_gateway_validation.py"
Cohesion: 0.14
Nodes (18): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), test_domain_bounds_remain_a_separate_stage() (+10 more)

### Community 24 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 25 - "load_config"
Cohesion: 0.17
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 26 - "create_app"
Cohesion: 0.14
Nodes (16): create_app(), load_config(), test_classical_app_constructs_and_uses_baseline_client(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance() (+8 more)

### Community 27 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 28 - "test_cloud_session_api.py"
Cohesion: 0.12
Nodes (13): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+5 more)

### Community 29 - "datetime"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 30 - "test_sensor.py"
Cohesion: 0.14
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 31 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 32 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 33 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (17): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+9 more)

### Community 34 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 35 - "test_cloud_mlkem.py"
Cohesion: 0.11
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 36 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 37 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 38 - "test_session.py"
Cohesion: 0.14
Nodes (10): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active() (+2 more)

### Community 39 - "device.py"
Cohesion: 0.10
Nodes (3): _sequence_number(), Measurement, _validate_number()

### Community 40 - "asyncio"
Cohesion: 0.15
Nodes (5): public_key(), _unavailable(), _error(), get_measurement(), list_measurements()

### Community 41 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 42 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 43 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+1 more)

### Community 44 - "build_aad"
Cohesion: 0.21
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 45 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 46 - "Config"
Cohesion: 0.16
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 47 - "edge_gateway/app.py"
Cohesion: 0.14
Nodes (6): _baseline_transport(), get_config(), _logging_level(), main(), GatewayConfig, BaselineTransport

### Community 48 - "SecureSession"
Cohesion: 0.14
Nodes (6): _Sessions, SecureSession, test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 49 - "encode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 50 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 51 - "edge_gateway/models.py"
Cohesion: 0.17
Nodes (6): _timestamp(), normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 52 - "test_gateway_measurements.py"
Cohesion: 0.22
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 54 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 55 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 56 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 57 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.24
Nodes (7): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement()

### Community 58 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 59 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 60 - "test_crypto_failures.py"
Cohesion: 0.22
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 62 - "sessions.py"
Cohesion: 0.32
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 63 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 64 - "pytest"
Cohesion: 0.21
Nodes (5): test_harness_rejects_invalid_sample_count(), _measurement(), test_explicit_utc_offsets_are_preserved(), test_non_finite_numbers_booleans_and_local_timestamps_are_rejected(), test_protocol_example_is_deterministic_utf8_json()

### Community 65 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 66 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 67 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 68 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 69 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 70 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 71 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 72 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 73 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 74 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 75 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 77 - "_error_response"
Cohesion: 0.25
Nodes (8): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response(), _unavailable()

### Community 79 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 80 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 85 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 101 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 721 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `measure_baseline.py`, `SessionManager`, `secure_transport.py`, `test_mode_evaluation.py`, `PqcMetrics`, `CloudDispatch`, `edge_gateway/crypto/symmetric.py`, `create_app`, `test_secure_transport.py`, `test_secure_shutdown.py`, `edge_gateway/crypto/encoding.py`, `edge_gateway/app.py`, `SecureSession`, `CryptoFailureInjector`, `edge_gateway/crypto/envelope.py`, `edge_gateway/crypto/aad.py`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `edge_gateway/crypto/session.py`, `SessionManager`, `secure_transport.py`, `SecureTransport`, `edge_gateway/app.py`, `SecureSession`, `test_mode_evaluation.py`, `CloudDispatch`, `create_app`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `test_session_recovery_is_counted()` connect `SecureSession` to `test_session.py`, `PqcMetrics`, `secure_transport.py`, `SecureTransport`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._
- **Should `test_legacy_compatibility.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05368421052631579 - nodes in this community are weakly interconnected._