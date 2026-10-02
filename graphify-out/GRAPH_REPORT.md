# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2170 nodes · 5353 edges · 143 communities (87 shown, 56 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 751 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- GatewayErrorCode
- cli.py
- test_baseline_client.py
- GatewayClient
- FailureMode
- test_public_key_client.py
- MeasurementRepository
- secure_transport.py
- test_gateway_crypto_image.py
- SessionManager
- SecureTransport
- test_sensor.py
- test_device.py
- load_config
- CloudDispatch
- secure.py
- test_cloud_secure.py
- test_cloud_mlkem.py
- derive_session_key
- CanonicalMeasurement
- PqcMetrics
- SecureSession
- edge_gateway/crypto/symmetric.py
- test_session.py
- test_secure_message_tamper.py
- load_config
- test_legacy_compatibility.py
- cloud_service/app.py
- encode_binary
- FailureMode
- SecureEnvelope
- test_public_key.py
- test_secure_transport.py
- validate_measurement
- test_cloud_failure_injection.py
- encapsulate
- test_crypto_failures.py
- session_client.py
- SessionState
- LegacyMeasurement
- create_app
- CanonicalMeasurement
- ConfigurationError
- StoredMeasurement
- build_aad
- decode_binary
- test_gateway_validation.py
- sessions.py
- test_cloud_baseline.py
- validate_legacy_measurement
- edge_gateway/crypto/encoding.py
- CloudMetrics
- fields
- plaintext.py
- DeviceController
- test_gateway_measurements.py
- Config
- test_permanent_gateway_failures_are_logged_without_retry
- SessionManager
- test_cloud_queries.py
- load_config
- SessionState
- edge_gateway/config.py
- CryptoFailureInjector
- _dispatch
- pytest
- run
- CloudHarness
- test_handshake_failure_stays_closed_without_a_session
- test_pqc_observability.py
- test_cloud_public_key.py
- GatewayConfig
- cloud
- envelope_validation.py
- handshake
- test_secure_envelope.py
- test_shutdown_after_gateway_unavailable_delivery
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- test_secure_failure_does_not_call_baseline
- _HandshakeHandler
- test_dependency_review.py
- _seal
- StartupError
- main
- edge_gateway/validation.py
- Clock
- test_repository_hygiene.py
- _crypto_dependencies_ready
- get_measurement
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- test_gateway_config.py
- _Handler
- _Handler
- _Sizes
- _measurement
- test_shared_integration_assets.py
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- SessionAccessError
- edge_gateway/models.py
- _Handler
- _Response
- _Handler
- _Handler
- test_gateway_security_components_share_the_metrics_registry_by_default
- _Server
- test_gateway_crypto_ci.py
- check_crypto.py
- scenario
- _Cloud
- payload
- test_valid_length_mlkem_mutation_is_not_required_to_raise
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 52 edges
2. `load_config()` - 50 edges
3. `SecureTransport` - 48 edges
4. `create_app()` - 48 edges
5. `load_config()` - 48 edges
6. `FailureMode` - 45 edges
7. `SessionManager` - 41 edges
8. `SecureTransportError` - 37 edges
9. `PqcMetrics` - 36 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `_deliver()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py
- `test_duplicate_sequence_is_stored_once()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py

## Import Cycles
- None detected.

## Communities (143 total, 56 thin omitted)

### Community 0 - "GatewayErrorCode"
Cohesion: 0.07
Nodes (21): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail() (+13 more)

### Community 1 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (24): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+16 more)

### Community 3 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 4 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 5 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+11 more)

### Community 6 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 8 - "test_gateway_crypto_image.py"
Cohesion: 0.08
Nodes (11): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version() (+3 more)

### Community 9 - "SessionManager"
Cohesion: 0.08
Nodes (8): lifespan(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 10 - "SecureTransport"
Cohesion: 0.11
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 11 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 12 - "test_device.py"
Cohesion: 0.10
Nodes (17): FakeMeasurement, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, make_config(), RaisingClient (+9 more)

### Community 13 - "load_config"
Cohesion: 0.11
Nodes (22): create_app(), main(), load_config(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage() (+14 more)

### Community 14 - "CloudDispatch"
Cohesion: 0.13
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions (+7 more)

### Community 15 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 16 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 17 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (9): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected() (+1 more)

### Community 18 - "derive_session_key"
Cohesion: 0.09
Nodes (14): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+6 more)

### Community 19 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 20 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 21 - "SecureSession"
Cohesion: 0.10
Nodes (11): _Sessions, SecureSession, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 22 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 23 - "test_session.py"
Cohesion: 0.12
Nodes (13): _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+5 more)

### Community 24 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 25 - "load_config"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 26 - "test_legacy_compatibility.py"
Cohesion: 0.14
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 27 - "cloud_service/app.py"
Cohesion: 0.14
Nodes (3): SecurityMode, public_key(), _unavailable()

### Community 28 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 29 - "FailureMode"
Cohesion: 0.13
Nodes (9): Config, FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes() (+1 more)

### Community 30 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 31 - "test_public_key.py"
Cohesion: 0.12
Nodes (8): decapsulate(), generate_keypair(), MlKemError, PrivateKey, _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 32 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (17): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+9 more)

### Community 33 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 34 - "test_cloud_failure_injection.py"
Cohesion: 0.20
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 35 - "encapsulate"
Cohesion: 0.16
Nodes (11): test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+3 more)

### Community 36 - "test_crypto_failures.py"
Cohesion: 0.13
Nodes (9): _Clock, handshake_url(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected() (+1 more)

### Community 37 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 38 - "SessionState"
Cohesion: 0.11
Nodes (9): SessionState, _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+1 more)

### Community 39 - "LegacyMeasurement"
Cohesion: 0.25
Nodes (14): LegacyMeasurement, LegacyMeasurementSchemaError, test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values(), test_extra_fields_are_rejected() (+6 more)

### Community 41 - "create_app"
Cohesion: 0.12
Nodes (13): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+5 more)

### Community 42 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 43 - "ConfigurationError"
Cohesion: 0.15
Nodes (15): ConfigurationError, integer(), number(), text(), value(), test_unrelated_record_id_collision_is_not_idempotent_success(), test_custom_environment(), test_defaults_do_not_create_database() (+7 more)

### Community 45 - "StoredMeasurement"
Cohesion: 0.15
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 46 - "build_aad"
Cohesion: 0.14
Nodes (11): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), build_secure_envelope(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract() (+3 more)

### Community 47 - "decode_binary"
Cohesion: 0.16
Nodes (11): decode_binary(), encode_binary(), EncodingError, _HandshakeCloud, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip() (+3 more)

### Community 48 - "test_gateway_validation.py"
Cohesion: 0.19
Nodes (15): parse_legacy_measurement(), _reject_constant(), assert_rejection(), payload(), test_domain_bounds_remain_a_separate_stage(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved() (+7 more)

### Community 49 - "sessions.py"
Cohesion: 0.18
Nodes (7): derive_session_key(), KdfError, _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 50 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 51 - "validate_legacy_measurement"
Cohesion: 0.15
Nodes (8): measurements(), normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_legacy_values_survive_secure_delivery()

### Community 52 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.15
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 53 - "CloudMetrics"
Cohesion: 0.14
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 54 - "fields"
Cohesion: 0.22
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 55 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 57 - "test_gateway_measurements.py"
Cohesion: 0.22
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 58 - "Config"
Cohesion: 0.19
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 59 - "test_permanent_gateway_failures_are_logged_without_retry"
Cohesion: 0.16
Nodes (7): FakeResponse, ScriptedOpener, test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure(), test_runtime_logs_lifecycle_and_delivery_events(), stop_after_first_measurement()

### Community 61 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 62 - "load_config"
Cohesion: 0.20
Nodes (11): _logging_level(), main(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance() (+3 more)

### Community 63 - "SessionState"
Cohesion: 0.16
Nodes (9): SessionState, clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed(), test_remove_expired_and_shutdown() (+1 more)

### Community 64 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 65 - "CryptoFailureInjector"
Cohesion: 0.17
Nodes (3): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_same_seed_makes_the_same_decisions()

### Community 66 - "_dispatch"
Cohesion: 0.20
Nodes (8): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 68 - "pytest"
Cohesion: 0.18
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 69 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 70 - "CloudHarness"
Cohesion: 0.19
Nodes (8): CloudHarness, _deliver(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope(), test_expired_session_returns_409_and_recovers_once(), test_invalid_session_returns_409_and_recovers_once(), test_secure_envelope_round_trip_stores_canonical_measurement(), test_versioned_public_key_retrieval()

### Community 71 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 72 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 73 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 74 - "GatewayConfig"
Cohesion: 0.17
Nodes (4): _baseline_transport(), get_config(), GatewayConfig, BaselineTransport

### Community 75 - "cloud"
Cohesion: 0.20
Nodes (4): cloud(), _install_trace(), test_production_cloud_app_has_secure_measurement_route(), Trace

### Community 76 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 77 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 78 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 79 - "test_shutdown_after_gateway_unavailable_delivery"
Cohesion: 0.22
Nodes (4): test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown(), fake_signal()

### Community 80 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 81 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 82 - "test_secure_failure_does_not_call_baseline"
Cohesion: 0.20
Nodes (3): BaselineSpy, test_secure_failure_does_not_call_baseline(), test_valid_encapsulation_matches_shared_secret_and_hkdf()

### Community 84 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 85 - "_seal"
Cohesion: 0.25
Nodes (6): _seal(), test_malformed_mlkem_ciphertext_is_rejected(), test_tampered_secure_message_is_rejected(), test_unsupported_protocol_version_is_rejected(), unreachable(), test_wrong_gateway_ownership_is_rejected_before_decrypt()

### Community 86 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 87 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 91 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 92 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 94 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 100 - "_measurement"
Cohesion: 0.33
Nodes (5): _measurement(), test_duplicate_sequence_is_stored_once(), send_twice(), test_one_handshake_is_reused_for_three_measurements(), send_three()

### Community 105 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 107 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 743 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **56 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `_dispatch`, `test_crypto_failures.py`, `secure_transport.py`, `test_handshake_failure_stays_closed_without_a_session`, `SessionManager`, `GatewayConfig`, `SecureTransport`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `SecureSession`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `secure_transport.py`, `SessionManager`, `CloudDispatch`, `PqcMetrics`, `SecureSession`, `edge_gateway/crypto/symmetric.py`, `test_secure_transport.py`, `SessionState`, `create_app`, `build_aad`, `decode_binary`, `plaintext.py`, `CryptoFailureInjector`, `_dispatch`, `CloudHarness`, `test_handshake_failure_stays_closed_without_a_session`, `test_pqc_observability.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `main`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `test_gateway_security_components_share_the_metrics_registry_by_default`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `_dispatch`, `secure_transport.py`, `test_handshake_failure_stays_closed_without_a_session`, `create_app`, `SecureTransport`, `SessionManager`, `test_pqc_observability.py`, `CloudDispatch`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `SecureSession`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `SecureTransport` (e.g. with `main()` and `create_app()`) actually correct?**
  _`SecureTransport` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GatewayErrorCode` be split into smaller, more focused modules?**
  _Cohesion score 0.06954887218045112 - nodes in this community are weakly interconnected._