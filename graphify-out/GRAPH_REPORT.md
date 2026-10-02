# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2293 nodes · 5700 edges · 142 communities (90 shown, 52 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 793 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- test_gateway_cloud_secure.py
- cli.py
- GatewayErrorCode
- GatewayClient
- test_crypto_failures.py
- test_gateway_crypto_image.py
- secure_transport.py
- SessionManager
- edge_gateway/app.py
- MeasurementRepository
- SecureTransport
- test_public_key_client.py
- CanonicalMeasurement
- test_session.py
- FailureMode
- secure.py
- create_app
- edge_gateway/crypto/symmetric.py
- test_sensor.py
- test_cloud_secure.py
- SecureSession
- PqcMetrics
- validate_measurement
- encode_binary
- LegacyMeasurement
- SecureEnvelope
- load_config
- CloudDispatch
- FailureInjector
- test_secure_message_tamper.py
- session_client.py
- test_cloud_failure_injection.py
- encapsulate
- CanonicalMeasurement
- test_legacy_compatibility.py
- load_config
- derive_session_key
- CloudMetrics
- StoredMeasurement
- test_cloud_baseline.py
- test_baseline_client.py
- Measurement
- test_secure_transport.py
- test_cloud_queries.py
- edge_gateway/crypto/encoding.py
- edge_gateway/crypto/envelope.py
- cloud_service/crypto/mlkem.py
- build_aad
- create_app
- _Sessions
- fields
- parse_public_key_response
- test_cloud_kdf.py
- Transport
- sessions.py
- test_cloud_mlkem.py
- run
- validate_legacy_measurement
- test_handshake_failure_stays_closed_without_a_session
- _dispatch
- test_refresh_graphify.py
- test_gateway_correlation.py
- test_gateway_validation.py
- live_gateway
- SessionState
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- test_cloud_public_key.py
- BaselineCloudClient
- edge_gateway/validation.py
- test_gateway_app.py
- test_gateway_response_mapping.py
- envelope_validation.py
- handshake
- test_secure_envelope.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- SessionManager
- _Clock
- cloud_service/crypto/session.py
- queries.py
- test_dependency_review.py
- KdfError
- test_baseline_gateway_measurements
- test_handshake_counter_shows_reuse_then_expiry
- main
- test_repository_hygiene.py
- _crypto_dependencies_ready
- StartupError
- test_final_secure_transport_review.py
- test_plaintext.py
- test_injected_handshake_failure_stays_fail_closed
- _Handler
- _Handler
- _Sizes
- live_cloud
- _Gateway
- _Server
- test_shared_integration_assets.py
- public_key
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- edge_gateway/models.py
- _Handler
- _Handler
- client
- _Handler
- test_gateway_crypto_ci.py
- .__init__
- _RejectRedirect
- _RejectRedirect
- _Cloud
- scenario
- _Cloud
- payload
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
7. `SessionManager` - 43 edges
8. `SecureTransportError` - 38 edges
9. `PqcMetrics` - 37 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_corrupted_ciphertext_is_rejected_and_not_stored()` --uses--> `CryptoFailureInjector`  [INFERRED]
  tests/integration/test_corrupt_ciphertext_demo.py → edge_gateway/src/edge_gateway/crypto/failure.py
- `test_handshake_failure_stays_closed_without_a_session()` --uses--> `CryptoFailureInjector`  [INFERRED]
  tests/integration/test_mlkem_handshake_failure_demo.py → edge_gateway/src/edge_gateway/crypto/failure.py
- `_dispatch()` --uses--> `CryptoFailureInjector`  [INFERRED]
  tests/integration/test_mode_evaluation.py → edge_gateway/src/edge_gateway/crypto/failure.py
- `_deliver()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py

## Import Cycles
- None detected.

## Communities (142 total, 52 thin omitted)

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

### Community 4 - "GatewayErrorCode"
Cohesion: 0.07
Nodes (20): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed() (+12 more)

### Community 5 - "GatewayClient"
Cohesion: 0.08
Nodes (24): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+16 more)

### Community 6 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 7 - "test_gateway_crypto_image.py"
Cohesion: 0.06
Nodes (18): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+10 more)

### Community 9 - "SessionManager"
Cohesion: 0.07
Nodes (6): lifespan(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 11 - "edge_gateway/app.py"
Cohesion: 0.08
Nodes (10): _baseline_transport(), get_config(), _logging_level(), main(), _secure_transport(), GatewayConfig, CryptoFailureInjector, BaselineTransport (+2 more)

### Community 12 - "MeasurementRepository"
Cohesion: 0.11
Nodes (23): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+15 more)

### Community 13 - "SecureTransport"
Cohesion: 0.10
Nodes (11): _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport (+3 more)

### Community 14 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, PublicKeyRejected, _body(), cloud_server(), _Handler, _public_key() (+10 more)

### Community 16 - "CanonicalMeasurement"
Cohesion: 0.12
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 17 - "test_session.py"
Cohesion: 0.11
Nodes (15): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+7 more)

### Community 18 - "FailureMode"
Cohesion: 0.11
Nodes (11): Config, FailureMode, FailureInjector, FailureSelection, test_custom_environment(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request() (+3 more)

### Community 19 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 20 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+10 more)

### Community 21 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.20
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 22 - "test_sensor.py"
Cohesion: 0.11
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 23 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 24 - "SecureSession"
Cohesion: 0.09
Nodes (10): _Sessions, SecureSession, _session(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted() (+2 more)

### Community 25 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 26 - "validate_measurement"
Cohesion: 0.15
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 27 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 28 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (14): LegacyMeasurement, LegacyMeasurementSchemaError, test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values(), test_extra_fields_are_rejected() (+6 more)

### Community 29 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 30 - "load_config"
Cohesion: 0.16
Nodes (16): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+8 more)

### Community 31 - "CloudDispatch"
Cohesion: 0.22
Nodes (14): CloudDispatch, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+6 more)

### Community 32 - "FailureInjector"
Cohesion: 0.15
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 33 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 34 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 35 - "test_cloud_failure_injection.py"
Cohesion: 0.20
Nodes (15): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_injected_session_failures_are_frozen_409s(), test_none_and_zero_rate_leave_secure_flow_unchanged() (+7 more)

### Community 36 - "encapsulate"
Cohesion: 0.17
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 37 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 38 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 39 - "load_config"
Cohesion: 0.21
Nodes (14): ConfigurationError, load_config(), integer(), number(), text(), value(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values() (+6 more)

### Community 40 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 41 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 42 - "StoredMeasurement"
Cohesion: 0.15
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 43 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+1 more)

### Community 44 - "test_baseline_client.py"
Cohesion: 0.25
Nodes (15): BaselineCloudError, _client(), _send(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request(), test_redirect_is_rejected_and_constructor_validates_inputs() (+7 more)

### Community 45 - "Measurement"
Cohesion: 0.12
Nodes (9): live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(), test_legacy_to_sqlite_preserves_gateway_transformations(), Measurement (+1 more)

### Community 46 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 47 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (12): test_unrelated_record_id_collision_is_not_idempotent_success(), client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail() (+4 more)

### Community 48 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 49 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.18
Nodes (8): build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement()

### Community 50 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 51 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 52 - "create_app"
Cohesion: 0.15
Nodes (12): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+4 more)

### Community 53 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 54 - "fields"
Cohesion: 0.22
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 55 - "parse_public_key_response"
Cohesion: 0.18
Nodes (9): CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 56 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 57 - "Transport"
Cohesion: 0.19
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 58 - "sessions.py"
Cohesion: 0.26
Nodes (7): SecurityMode, derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 59 - "test_cloud_mlkem.py"
Cohesion: 0.16
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 60 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 61 - "validate_legacy_measurement"
Cohesion: 0.19
Nodes (7): measurements(), normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 62 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 63 - "_dispatch"
Cohesion: 0.22
Nodes (7): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline()

### Community 64 - "test_refresh_graphify.py"
Cohesion: 0.19
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 65 - "test_gateway_correlation.py"
Cohesion: 0.23
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 66 - "test_gateway_validation.py"
Cohesion: 0.33
Nodes (10): assert_rejection(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422(), test_parsed_non_measurements_are_422() (+2 more)

### Community 67 - "live_gateway"
Cohesion: 0.24
Nodes (8): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_legacy_serializer_and_client_reach_live_gateway(), test_malformed_legacy_json_is_rejected_without_delivery(), test_parsed_invalid_legacy_payload_is_rejected_without_delivery()

### Community 68 - "SessionState"
Cohesion: 0.21
Nodes (8): SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed(), test_remove_expired_and_shutdown(), test_unknown_wrong_owner_and_invalidation()

### Community 69 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.18
Nodes (4): SecureSession, _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 70 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 71 - "BaselineCloudClient"
Cohesion: 0.23
Nodes (5): BaselineAcceptance, BaselineCloudClient, _dump(), _error_code(), _parse_acceptance()

### Community 72 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 73 - "test_gateway_app.py"
Cohesion: 0.18
Nodes (9): test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration(), test_settings_dependency_can_be_overridden_and_isolated() (+1 more)

### Community 74 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 75 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 76 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 77 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 78 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 80 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 82 - "queries.py"
Cohesion: 0.39
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 83 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 84 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 85 - "test_baseline_gateway_measurements"
Cohesion: 0.25
Nodes (4): cloud(), test_baseline_gateway_measurements(), _post(), send()

### Community 86 - "test_handshake_counter_shows_reuse_then_expiry"
Cohesion: 0.29
Nodes (5): _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 87 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 89 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 91 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 92 - "test_plaintext.py"
Cohesion: 0.53
Nodes (4): _measurement(), test_explicit_utc_offsets_are_preserved(), test_non_finite_numbers_booleans_and_local_timestamps_are_rejected(), test_protocol_example_is_deterministic_utf8_json()

### Community 93 - "test_injected_handshake_failure_stays_fail_closed"
Cohesion: 0.33
Nodes (4): _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_injected_handshake_failure_stays_fail_closed()

### Community 99 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 106 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 108 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 784 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **52 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `secure_transport.py`, `SessionManager`, `edge_gateway/app.py`, `SecureTransport`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `_dispatch`, `create_app`, `test_handshake_counter_shows_reuse_then_expiry`, `SecureSession`, `test_injected_handshake_failure_stays_fail_closed`, `test_handshake_failure_stays_closed_without_a_session`, `CloudDispatch`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `CloudMetrics` connect `CloudMetrics` to `cloud_service/app.py`, `create_app`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `test_crypto_failures.py`, `secure_transport.py`, `SessionManager`, `edge_gateway/app.py`, `edge_gateway/crypto/symmetric.py`, `SecureSession`, `PqcMetrics`, `CloudDispatch`, `test_secure_transport.py`, `edge_gateway/crypto/encoding.py`, `edge_gateway/crypto/envelope.py`, `build_aad`, `create_app`, `_Sessions`, `test_handshake_failure_stays_closed_without_a_session`, `_dispatch`, `live_gateway`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `test_handshake_counter_shows_reuse_then_expiry`, `main`, `test_injected_handshake_failure_stays_fail_closed`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.057967313585291114 - nodes in this community are weakly interconnected._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._