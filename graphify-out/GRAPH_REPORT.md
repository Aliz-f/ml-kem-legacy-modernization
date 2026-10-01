# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2120 nodes · 5241 edges · 126 communities (82 shown, 44 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 743 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- GatewayErrorCode
- cli.py
- secure_transport.py
- test_baseline_client.py
- GatewayClient
- MeasurementRepository
- SessionManager
- SecureTransport
- pathlib
- test_public_key_client.py
- test_sensor.py
- test_gateway_crypto_image.py
- cloud_service/crypto/session.py
- create_app
- test_cloud_secure.py
- CloudDispatch
- FailureMode
- SessionManager
- PqcMetrics
- edge_gateway/crypto/symmetric.py
- _dispatch
- CryptoFailureInjector
- SecureSession
- routes.py
- CanonicalMeasurement
- test_gateway_cloud_secure.py
- StoredMeasurement
- encapsulate
- LegacyMeasurement
- load_config
- SecureEnvelope
- test_secure_transport.py
- test_cloud_mlkem.py
- validate_measurement
- test_secure_message_tamper.py
- session_client.py
- test_gateway_validation.py
- encode_binary
- secure.py
- test_session.py
- CanonicalMeasurement
- test_legacy_compatibility.py
- sessions.py
- fields
- validate_legacy_measurement
- FailureInjector
- test_cloud_baseline.py
- create_app
- pytest
- load_config
- plaintext.py
- test_crypto_failures.py
- cloud_service/app.py
- CloudMetrics
- test_cloud_queries.py
- build_aad
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- test_cloud_session_api.py
- edge_gateway/config.py
- Transport
- CloudHarness
- run
- build_secure_envelope
- _Sessions
- test_refresh_graphify.py
- test_cloud_public_key.py
- GatewayConfig
- cloud
- envelope_validation.py
- derive_session_key
- _Clock
- parse_public_key_response
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- test_secure_failure_does_not_call_baseline
- _HandshakeHandler
- KdfError
- FailureSelection
- main
- Clock
- test_repository_hygiene.py
- StartupError
- test_gateway_config.py
- _Handler
- _Handler
- _measurement
- _seal
- _Gateway
- test_shared_integration_assets.py
- edge_gateway/models.py
- _Handler
- _Opener
- _Handler
- test_gateway_security_components_share_the_metrics_registry_by_default
- test_gateway_crypto_ci.py
- scenario
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 52 edges
2. `load_config()` - 50 edges
3. `create_app()` - 48 edges
4. `load_config()` - 48 edges
5. `SecureTransport` - 46 edges
6. `FailureMode` - 45 edges
7. `SessionManager` - 39 edges
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
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `PublicKeyRejected`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/public_key.py

## Import Cycles
- None detected.

## Communities (126 total, 44 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "GatewayErrorCode"
Cohesion: 0.07
Nodes (21): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail() (+13 more)

### Community 3 - "cli.py"
Cohesion: 0.14
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 5 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (24): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+16 more)

### Community 6 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 7 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 8 - "SessionManager"
Cohesion: 0.08
Nodes (14): clock(), lifespan(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager, _injector() (+6 more)

### Community 9 - "SecureTransport"
Cohesion: 0.10
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 10 - "pathlib"
Cohesion: 0.07
Nodes (5): _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 11 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, PublicKeyRejected, _body(), cloud_server(), _Handler (+11 more)

### Community 12 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 13 - "test_gateway_crypto_image.py"
Cohesion: 0.08
Nodes (11): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version() (+3 more)

### Community 14 - "cloud_service/crypto/session.py"
Cohesion: 0.09
Nodes (10): SecureSession, SessionAccessError, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed() (+2 more)

### Community 15 - "create_app"
Cohesion: 0.09
Nodes (19): create_app(), test_apps_have_independent_lifecycle_state(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics(), test_mlkem_readiness_requires_initialized_dependencies_not_an_active_session(), test_secure_route_unavailable_in_classical_mode() (+11 more)

### Community 16 - "test_cloud_secure.py"
Cohesion: 0.14
Nodes (24): canonical(), envelope(), forbid(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted(), test_extra_missing_and_duplicate_fields(), test_gateway_envelope_persistence_query_and_identical_retry() (+16 more)

### Community 17 - "CloudDispatch"
Cohesion: 0.15
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions (+7 more)

### Community 18 - "FailureMode"
Cohesion: 0.17
Nodes (21): FailureMode, canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently() (+13 more)

### Community 19 - "SessionManager"
Cohesion: 0.13
Nodes (14): SessionManager, DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection (+6 more)

### Community 20 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 21 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 22 - "_dispatch"
Cohesion: 0.09
Nodes (11): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+3 more)

### Community 23 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (5): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), test_same_seed_makes_the_same_decisions()

### Community 24 - "SecureSession"
Cohesion: 0.10
Nodes (11): _Sessions, SecureSession, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 25 - "routes.py"
Cohesion: 0.12
Nodes (7): public_key(), _unavailable(), _error(), get_measurement(), list_measurements(), baseline_measurement(), _error()

### Community 26 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 27 - "test_gateway_cloud_secure.py"
Cohesion: 0.10
Nodes (5): CloudPublicKey, LegacyJSONError, LegacyMeasurementDomainError, test_simulated_decapsulation_failure_leaves_no_session(), test_tampered_secure_message_is_rejected()

### Community 28 - "StoredMeasurement"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 29 - "encapsulate"
Cohesion: 0.15
Nodes (11): main(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+3 more)

### Community 30 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 31 - "load_config"
Cohesion: 0.18
Nodes (16): main(), ConfigurationError, load_config(), integer(), number(), text(), value(), test_cli_uses_configured_server_settings() (+8 more)

### Community 32 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 33 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (17): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+9 more)

### Community 34 - "test_cloud_mlkem.py"
Cohesion: 0.11
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 35 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 36 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 37 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 38 - "test_gateway_validation.py"
Cohesion: 0.17
Nodes (16): parse_legacy_measurement(), _reject_constant(), assert_rejection(), client(), payload(), test_domain_bounds_remain_a_separate_stage(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model() (+8 more)

### Community 39 - "encode_binary"
Cohesion: 0.17
Nodes (11): decode_binary(), encode_binary(), EncodingError, _decode_ciphertext(), test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet() (+3 more)

### Community 40 - "secure.py"
Cohesion: 0.14
Nodes (7): AadError, build_aad(), _DroppedResponse, _error(), _ingest(), _NoMetrics, secure_measurement()

### Community 41 - "test_session.py"
Cohesion: 0.15
Nodes (10): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active() (+2 more)

### Community 42 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 43 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 44 - "sessions.py"
Cohesion: 0.18
Nodes (7): SecurityMode, derive_session_key(), KdfError, _error(), _establish(), establish_session(), session_access_error_handler()

### Community 45 - "fields"
Cohesion: 0.19
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 46 - "validate_legacy_measurement"
Cohesion: 0.15
Nodes (8): measurements(), normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_legacy_values_survive_secure_delivery()

### Community 47 - "FailureInjector"
Cohesion: 0.14
Nodes (6): Config, FailureInjector, test_custom_environment(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_injected_fault_is_counted_only_when_its_boundary_applies(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 48 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 49 - "create_app"
Cohesion: 0.15
Nodes (12): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+4 more)

### Community 50 - "pytest"
Cohesion: 0.16
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 51 - "load_config"
Cohesion: 0.18
Nodes (12): _logging_level(), main(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health() (+4 more)

### Community 52 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 53 - "test_crypto_failures.py"
Cohesion: 0.16
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 54 - "cloud_service/app.py"
Cohesion: 0.17
Nodes (6): health(), ready(), _crypto_dependencies_ready(), _unavailable(), AeadError, decrypt()

### Community 55 - "CloudMetrics"
Cohesion: 0.15
Nodes (3): CloudMetrics, _labels(), _render_labels()

### Community 56 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 57 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 58 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 59 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 60 - "test_cloud_session_api.py"
Cohesion: 0.21
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 61 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 62 - "Transport"
Cohesion: 0.19
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 63 - "CloudHarness"
Cohesion: 0.17
Nodes (9): CloudHarness, _deliver(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope(), test_expired_session_returns_409_and_recovers_once(), test_invalid_session_returns_409_and_recovers_once(), test_secure_envelope_round_trip_stores_canonical_measurement(), test_valid_length_mlkem_mutation_is_not_required_to_raise() (+1 more)

### Community 64 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 65 - "build_secure_envelope"
Cohesion: 0.24
Nodes (10): build_secure_envelope(), _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement() (+2 more)

### Community 66 - "_Sessions"
Cohesion: 0.19
Nodes (7): _Baseline, _measurement(), _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 67 - "test_refresh_graphify.py"
Cohesion: 0.19
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 68 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 69 - "GatewayConfig"
Cohesion: 0.17
Nodes (4): _baseline_transport(), get_config(), GatewayConfig, BaselineTransport

### Community 70 - "cloud"
Cohesion: 0.20
Nodes (4): cloud(), _install_trace(), test_production_cloud_app_has_secure_measurement_route(), Trace

### Community 71 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 72 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 73 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 74 - "parse_public_key_response"
Cohesion: 0.33
Nodes (6): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 75 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 76 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 77 - "test_secure_failure_does_not_call_baseline"
Cohesion: 0.20
Nodes (3): BaselineSpy, test_secure_failure_does_not_call_baseline(), test_valid_encapsulation_matches_shared_secret_and_hkdf()

### Community 79 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 81 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 85 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 90 - "_measurement"
Cohesion: 0.33
Nodes (5): _measurement(), test_duplicate_sequence_is_stored_once(), send_twice(), test_one_handshake_is_reused_for_three_measurements(), send_three()

### Community 91 - "_seal"
Cohesion: 0.33
Nodes (5): _seal(), test_malformed_mlkem_ciphertext_is_rejected(), test_unsupported_protocol_version_is_rejected(), unreachable(), test_wrong_gateway_ownership_is_rejected_before_decrypt()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 723 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app` to `GatewayErrorCode`, `secure_transport.py`, `GatewayConfig`, `test_gateway_validation.py`, `SessionManager`, `SecureTransport`, `test_gateway_security_components_share_the_metrics_registry_by_default`, `scenario`, `validate_legacy_measurement`, `CloudDispatch`, `load_config`, `PqcMetrics`, `Transport`, `test_gateway_cloud_secure.py`, `_Gateway`, `LegacyMeasurement`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `secure_transport.py`, `SessionManager`, `SecureTransport`, `pathlib`, `create_app`, `CloudDispatch`, `_dispatch`, `CryptoFailureInjector`, `SecureSession`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `MeasurementRepository`, `cloud_service/crypto/session.py`, `create_app`, `test_cloud_secure.py`, `cloud_service/app.py`, `test_cloud_session_api.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.060191518467852256 - nodes in this community are weakly interconnected._