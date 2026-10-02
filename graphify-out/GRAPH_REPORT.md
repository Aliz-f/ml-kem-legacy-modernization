# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2333 nodes · 5796 edges · 143 communities (90 shown, 53 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 799 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_baseline_client.py
- GatewayClient
- test_gateway_cloud_secure.py
- cli.py
- GatewayErrorCode
- test_crypto_failures.py
- test_public_key_client.py
- secure_transport.py
- SecureTransport
- CryptoFailureInjector
- SessionManager
- session_client.py
- MeasurementRepository
- secure.py
- encapsulate
- test_session.py
- CloudDispatch
- create_app
- test_sensor.py
- test_cloud_secure.py
- edge_gateway/crypto/symmetric.py
- load_config
- CanonicalMeasurement
- PqcMetrics
- test_secure_message_tamper.py
- test_session_recovery_is_counted
- LegacyMeasurement
- pathlib
- encode_binary
- test_public_key.py
- test_cloud_failure_injection.py
- SessionManager
- make_config
- SecureEnvelope
- FailureInjector
- test_secure_transport.py
- validate_measurement
- derive_session_key
- StoredMeasurement
- test_cloud_baseline.py
- CanonicalMeasurement
- test_legacy_compatibility.py
- test_secure_shutdown.py
- FailureMode
- edge_gateway/crypto/envelope.py
- sessions.py
- build_aad
- create_app
- test_cloud_kdf.py
- fields
- test_cloud_queries.py
- edge_gateway/crypto/encoding.py
- DeviceController
- test_gateway_measurements.py
- test_gateway_validation.py
- test_permanent_gateway_failures_are_logged_without_retry
- StorageError
- CloudMetrics
- GatewayConfig
- load_config
- edge_gateway/validation.py
- run
- ConfigurationError
- normalize
- test_pqc_observability.py
- live_gateway
- test_clean_container_crypto.py
- pytest
- test_cloud_public_key.py
- test_gateway_response_mapping.py
- test_gateway_crypto_image.py
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- envelope_validation.py
- handshake
- test_secure_envelope.py
- test_static_checks.py
- RecordingClient
- refresh_graphify.py
- measure_modes
- _Clock
- test_dependency_review.py
- test_falsey_injected_dependencies_are_preserved
- test_gateway_correlation.py
- _Cloud
- test_end_to_end.py
- _Cloud
- fastapi_testclient
- main
- test_refresh_graphify.py
- test_repository_hygiene.py
- _crypto_dependencies_ready
- StartupError
- test_final_secure_transport_review.py
- test_gateway_config.py
- test_plaintext.py
- _Handler
- _Handler
- _Sizes
- live_cloud
- _Gateway
- _Server
- test_shared_integration_assets.py
- public_key
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- edge_gateway/models.py
- _Response
- _Handler
- _Handler
- test_gateway_crypto_ci.py
- scenario
- _Cloud
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
8. `SecureTransportError` - 38 edges
9. `PqcMetrics` - 37 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()` --uses--> `BaselineCloudClient`  [INFERRED]
  tests/integration/test_gateway_cloud_baseline.py → edge_gateway/src/edge_gateway/cloud/baseline.py
- `run()` --uses--> `Measurement`  [INFERRED]
  scripts/measure_baseline_e2e.py → legacy_system/src/legacy_system/sensor.py

## Import Cycles
- None detected.

## Communities (143 total, 53 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_baseline_client.py"
Cohesion: 0.05
Nodes (37): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+29 more)

### Community 2 - "GatewayClient"
Cohesion: 0.05
Nodes (29): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener (+21 more)

### Community 3 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 5 - "GatewayErrorCode"
Cohesion: 0.07
Nodes (21): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail() (+13 more)

### Community 6 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (21): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+13 more)

### Community 7 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (20): validate_public_key(), _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected (+12 more)

### Community 10 - "SecureTransport"
Cohesion: 0.11
Nodes (13): _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+5 more)

### Community 11 - "CryptoFailureInjector"
Cohesion: 0.07
Nodes (10): _secure_transport(), CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _count(), test_corrupted_ciphertext_is_rejected_and_not_stored(), _Baseline, _count() (+2 more)

### Community 12 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 13 - "session_client.py"
Cohesion: 0.10
Nodes (14): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+6 more)

### Community 14 - "MeasurementRepository"
Cohesion: 0.12
Nodes (23): lifespan(), Database, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement(), test_closed_database_errors_are_safe() (+15 more)

### Community 15 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 16 - "encapsulate"
Cohesion: 0.10
Nodes (14): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe(), encapsulate(), MlKemError, _raw_public_key() (+6 more)

### Community 17 - "test_session.py"
Cohesion: 0.10
Nodes (13): SecureSession, SessionState, _Sessions, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key() (+5 more)

### Community 18 - "CloudDispatch"
Cohesion: 0.14
Nodes (14): CloudDispatch, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 19 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+10 more)

### Community 20 - "test_sensor.py"
Cohesion: 0.11
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 21 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 22 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 23 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), SecurityMode (+9 more)

### Community 24 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 25 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 26 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 27 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (12): _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 28 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 30 - "encode_binary"
Cohesion: 0.13
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 31 - "test_public_key.py"
Cohesion: 0.11
Nodes (8): decapsulate(), generate_keypair(), MlKemError, PrivateKey, _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 32 - "test_cloud_failure_injection.py"
Cohesion: 0.17
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 33 - "SessionManager"
Cohesion: 0.11
Nodes (3): lifespan(), SessionEstablishmentError, SessionManager

### Community 34 - "make_config"
Cohesion: 0.12
Nodes (12): FakeMeasurement, FakeSensor, make_config(), RaisingClient, test_client_exception_is_logged_then_loop_continues_and_closes(), test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown() (+4 more)

### Community 35 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 36 - "FailureInjector"
Cohesion: 0.15
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 37 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (17): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+9 more)

### Community 38 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 39 - "derive_session_key"
Cohesion: 0.14
Nodes (11): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+3 more)

### Community 40 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 41 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 42 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 43 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 44 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 45 - "FailureMode"
Cohesion: 0.17
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 46 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.18
Nodes (8): build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement()

### Community 47 - "sessions.py"
Cohesion: 0.19
Nodes (7): derive_session_key(), KdfError, _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 48 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 49 - "create_app"
Cohesion: 0.15
Nodes (12): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+4 more)

### Community 50 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 51 - "fields"
Cohesion: 0.22
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 52 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 53 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 55 - "test_gateway_measurements.py"
Cohesion: 0.22
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 56 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 57 - "test_permanent_gateway_failures_are_logged_without_retry"
Cohesion: 0.16
Nodes (7): FakeResponse, ScriptedOpener, test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure(), test_runtime_logs_lifecycle_and_delivery_events(), stop_after_first_measurement()

### Community 58 - "StorageError"
Cohesion: 0.20
Nodes (5): _error(), get_measurement(), list_measurements(), StorageConflictError, StorageError

### Community 59 - "CloudMetrics"
Cohesion: 0.15
Nodes (3): CloudMetrics, _labels(), _render_labels()

### Community 60 - "GatewayConfig"
Cohesion: 0.14
Nodes (5): _baseline_transport(), get_config(), GatewayConfig, BaselineTransport, DispatchMetrics

### Community 61 - "load_config"
Cohesion: 0.20
Nodes (11): _logging_level(), main(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance() (+3 more)

### Community 62 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 63 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 64 - "ConfigurationError"
Cohesion: 0.24
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 65 - "normalize"
Cohesion: 0.22
Nodes (5): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 66 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 67 - "live_gateway"
Cohesion: 0.24
Nodes (8): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_legacy_serializer_and_client_reach_live_gateway(), test_malformed_legacy_json_is_rejected_without_delivery(), test_parsed_invalid_legacy_payload_is_rejected_without_delivery()

### Community 69 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 71 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 72 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 73 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 74 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.17
Nodes (3): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 75 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 76 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 77 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 78 - "test_static_checks.py"
Cohesion: 0.27
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 79 - "RecordingClient"
Cohesion: 0.20
Nodes (4): RecordingClient, RecordingFailureInjector, test_delivery_failure_does_not_stop_loop_or_roll_back_sequence(), test_runtime_pipeline_serializes_before_failure_injection_and_sends()

### Community 80 - "refresh_graphify.py"
Cohesion: 0.27
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 81 - "measure_modes"
Cohesion: 0.25
Nodes (6): _Calls, measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 82 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 83 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 84 - "test_falsey_injected_dependencies_are_preserved"
Cohesion: 0.22
Nodes (5): FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, test_falsey_injected_dependencies_are_preserved()

### Community 85 - "test_gateway_correlation.py"
Cohesion: 0.36
Nodes (5): create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 87 - "test_end_to_end.py"
Cohesion: 0.32
Nodes (3): query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row()

### Community 90 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 91 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 93 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 95 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 96 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 97 - "test_plaintext.py"
Cohesion: 0.53
Nodes (4): _measurement(), test_explicit_utc_offsets_are_preserved(), test_non_finite_numbers_booleans_and_local_timestamps_are_rejected(), test_protocol_example_is_deterministic_utf8_json()

### Community 103 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 111 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 113 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 805 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **53 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `SessionManager`, `test_pqc_observability.py`, `secure_transport.py`, `SecureTransport`, `CryptoFailureInjector`, `create_app`, `CloudDispatch`, `test_session_recovery_is_counted`, `GatewayConfig`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `SessionManager`, `test_crypto_failures.py`, `secure_transport.py`, `SecureTransport`, `test_session_recovery_is_counted`, `GatewayConfig`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_pqc_observability.py`, `test_gateway_cloud_secure.py`, `live_gateway`, `test_secure_message_tamper.py`, `test_crypto_failures.py`, `derive_session_key`, `test_public_key_client.py`, `secure_transport.py`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`, `CryptoFailureInjector`, `session_client.py`, `encapsulate`, `test_session.py`, `create_app`, `PqcMetrics`, `main`, `test_session_recovery_is_counted`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.060191518467852256 - nodes in this community are weakly interconnected._
- **Should `test_baseline_client.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05030181086519115 - nodes in this community are weakly interconnected._