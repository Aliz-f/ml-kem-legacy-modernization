# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2364 nodes · 5893 edges · 145 communities (98 shown, 47 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 804 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- test_baseline_client.py
- GatewayErrorCode
- cli.py
- test_sensor.py
- SessionManager
- SecureTransport
- test_public_key_client.py
- cloud_service/app.py
- edge_gateway/app.py
- CloudDispatch
- test_gateway_cloud_secure.py
- SessionManager
- SecureSession
- test_session.py
- secure.py
- test_cloud_secure.py
- validate_measurement
- edge_gateway/crypto/symmetric.py
- CanonicalMeasurement
- PqcMetrics
- test_secure_message_tamper.py
- create_app
- load_config
- LegacyMeasurement
- test_secure_transport.py
- MeasurementRepository
- test_public_key.py
- encode_binary
- FailureMode
- SecureEnvelope
- StoredMeasurement
- encapsulate
- test_cloud_queries.py
- session_client.py
- test_cloud_failure_injection.py
- CanonicalMeasurement
- _dispatch
- test_legacy_compatibility.py
- test_client.py
- CloudMetrics
- test_cloud_baseline.py
- CryptoFailureInjector
- test_crypto_failures.py
- edge_gateway/crypto/envelope.py
- sessions.py
- fields
- build_aad
- derive_session_key
- create_app
- _Sessions
- test_handshake_failure_stays_closed_without_a_session
- load_config
- edge_gateway/crypto/encoding.py
- test_gateway_measurements.py
- test_gateway_validation.py
- json
- StorageError
- test_cloud_kdf.py
- edge_gateway/validation.py
- test_gateway_correlation.py
- test_legacy_values_survive_secure_delivery
- test_cloud_mlkem.py
- run
- test_legacy_gateway.py
- ConfigurationError
- normalize
- _Clock
- ErrorCategory
- run
- test_pqc_observability.py
- test_clean_container_crypto.py
- pytest
- test_cloud_public_key.py
- test_gateway_response_mapping.py
- cloud
- test_gateway_crypto_image.py
- GatewayClient
- envelope_validation.py
- handshake
- test_secure_envelope.py
- test_static_checks.py
- refresh_graphify.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- test_legacy_gateway_cloud_http_path_persists_canonical_measurement
- GatewayConfig
- _Clock
- _HandshakeHandler
- test_dependency_review.py
- test_gateway_cloud_secure_session.py
- LiveCloud
- test_end_to_end.py
- StartupError
- main
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_refresh_graphify.py
- test_repository_hygiene.py
- _crypto_dependencies_ready
- test_final_secure_transport_review.py
- test_gateway_config.py
- _Handler
- _Handler
- live_cloud
- Clock
- _Gateway
- test_shared_integration_assets.py
- public_key
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- edge_gateway/models.py
- _Response
- _Handler
- _Handler
- test_gateway_crypto_ci.py
- scenario
- client
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
6. `FailureMode` - 47 edges
7. `SessionManager` - 44 edges
8. `SecureTransportError` - 38 edges
9. `PqcMetrics` - 37 edges
10. `GatewayClient` - 37 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_legacy_values_survive_secure_delivery()` --uses--> `CloudDispatch`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/dispatch.py
- `test_secure_failure_does_not_call_baseline()` --uses--> `CloudDispatch`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/dispatch.py
- `_dispatch()` --uses--> `CloudDispatch`  [INFERRED]
  tests/integration/test_mode_evaluation.py → edge_gateway/src/edge_gateway/dispatch.py
- `_time_sends()` --uses--> `CloudDispatch`  [INFERRED]
  tests/integration/test_mode_evaluation.py → edge_gateway/src/edge_gateway/dispatch.py

## Import Cycles
- None detected.

## Communities (145 total, 47 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "test_baseline_client.py"
Cohesion: 0.05
Nodes (37): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+29 more)

### Community 3 - "GatewayErrorCode"
Cohesion: 0.06
Nodes (23): _baseline_transport(), BaselineTransport, GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, client() (+15 more)

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 5 - "test_sensor.py"
Cohesion: 0.06
Nodes (28): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+20 more)

### Community 6 - "SessionManager"
Cohesion: 0.08
Nodes (11): clock(), lifespan(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake() (+3 more)

### Community 7 - "SecureTransport"
Cohesion: 0.10
Nodes (12): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+4 more)

### Community 8 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+11 more)

### Community 9 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 11 - "CloudDispatch"
Cohesion: 0.12
Nodes (15): CloudDispatch, DispatchMetrics, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions (+7 more)

### Community 12 - "test_gateway_cloud_secure.py"
Cohesion: 0.11
Nodes (23): CloudHarness, _deliver(), _measurement(), _seal(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope(), test_cloud_failure_retries_the_same_secure_request_without_storage(), test_duplicate_sequence_is_stored_once() (+15 more)

### Community 13 - "SessionManager"
Cohesion: 0.11
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 14 - "SecureSession"
Cohesion: 0.08
Nodes (13): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+5 more)

### Community 15 - "test_session.py"
Cohesion: 0.11
Nodes (15): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+7 more)

### Community 16 - "secure.py"
Cohesion: 0.10
Nodes (10): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), _NoMetrics (+2 more)

### Community 17 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 18 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 19 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.20
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 20 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 21 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 22 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 23 - "create_app"
Cohesion: 0.10
Nodes (16): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+8 more)

### Community 24 - "load_config"
Cohesion: 0.16
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), SecurityMode (+9 more)

### Community 25 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 26 - "test_secure_transport.py"
Cohesion: 0.21
Nodes (18): _Cloud, _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable() (+10 more)

### Community 27 - "MeasurementRepository"
Cohesion: 0.14
Nodes (18): lifespan(), Database, MeasurementRepository, test_acceptance_is_committed_and_correlated(), test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+10 more)

### Community 28 - "test_public_key.py"
Cohesion: 0.11
Nodes (8): decapsulate(), generate_keypair(), MlKemError, PrivateKey, _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 29 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 30 - "FailureMode"
Cohesion: 0.14
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 31 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 32 - "StoredMeasurement"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 33 - "encapsulate"
Cohesion: 0.16
Nodes (11): test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+3 more)

### Community 34 - "test_cloud_queries.py"
Cohesion: 0.12
Nodes (15): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+7 more)

### Community 35 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 36 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 37 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 38 - "_dispatch"
Cohesion: 0.13
Nodes (9): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Sizes, test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline() (+1 more)

### Community 39 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 40 - "test_client.py"
Cohesion: 0.22
Nodes (11): FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_invalid_retry_counts_are_rejected(), test_non_retryable_http_status_stops_immediately(), test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff(), test_retry_logging_exposes_failed_attempts_and_retry_events(), test_retry_stops_after_non_retryable_result() (+3 more)

### Community 41 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 42 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): client(), payload(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500() (+1 more)

### Community 43 - "CryptoFailureInjector"
Cohesion: 0.13
Nodes (3): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_same_seed_makes_the_same_decisions()

### Community 44 - "test_crypto_failures.py"
Cohesion: 0.16
Nodes (10): _aad(), _injector(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault() (+2 more)

### Community 45 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.19
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 46 - "sessions.py"
Cohesion: 0.19
Nodes (7): derive_session_key(), KdfError, _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 47 - "fields"
Cohesion: 0.20
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 48 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 49 - "derive_session_key"
Cohesion: 0.18
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 50 - "create_app"
Cohesion: 0.15
Nodes (12): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+4 more)

### Community 51 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 52 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.12
Nodes (6): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session(), _Server

### Community 53 - "load_config"
Cohesion: 0.18
Nodes (12): _logging_level(), main(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health() (+4 more)

### Community 54 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 55 - "test_gateway_measurements.py"
Cohesion: 0.22
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 56 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 57 - "json"
Cohesion: 0.20
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 58 - "StorageError"
Cohesion: 0.20
Nodes (5): _error(), get_measurement(), list_measurements(), StorageConflictError, StorageError

### Community 60 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 62 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 63 - "test_gateway_correlation.py"
Cohesion: 0.19
Nodes (7): baseline_headers(), create_request_id(), build_secure_envelope(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 64 - "test_legacy_values_survive_secure_delivery"
Cohesion: 0.13
Nodes (5): BaselineSpy, test_legacy_values_survive_secure_delivery(), test_secure_failure_does_not_call_baseline(), test_tampered_secure_message_is_rejected(), test_valid_encapsulation_matches_shared_secret_and_hkdf()

### Community 65 - "test_cloud_mlkem.py"
Cohesion: 0.16
Nodes (4): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 66 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 67 - "test_legacy_gateway.py"
Cohesion: 0.30
Nodes (8): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_legacy_serializer_and_client_reach_live_gateway(), test_malformed_legacy_json_is_rejected_without_delivery(), test_parsed_invalid_legacy_payload_is_rejected_without_delivery()

### Community 68 - "ConfigurationError"
Cohesion: 0.24
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 69 - "normalize"
Cohesion: 0.22
Nodes (5): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 70 - "_Clock"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 71 - "ErrorCategory"
Cohesion: 0.18
Nodes (8): ErrorCategory, test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_send_posts_prepared_payload_to_gateway(), opener(), test_transport_failures_are_stable_and_retryable(), test_unserializable_payload_is_non_retryable()

### Community 72 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 73 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 74 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 76 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 77 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 78 - "cloud"
Cohesion: 0.20
Nodes (4): cloud(), _install_trace(), test_production_cloud_app_has_secure_measurement_route(), Trace

### Community 79 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 81 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 82 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 83 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 84 - "test_static_checks.py"
Cohesion: 0.27
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 85 - "refresh_graphify.py"
Cohesion: 0.27
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 86 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 87 - "test_legacy_gateway_cloud_http_path_persists_canonical_measurement"
Cohesion: 0.22
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 88 - "GatewayConfig"
Cohesion: 0.22
Nodes (4): get_config(), _secure_transport(), GatewayConfig, test_from_config_uses_gateway_failure_settings()

### Community 89 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 91 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 92 - "test_gateway_cloud_secure_session.py"
Cohesion: 0.28
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 94 - "test_end_to_end.py"
Cohesion: 0.32
Nodes (3): query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row()

### Community 95 - "StartupError"
Cohesion: 0.29
Nodes (3): StartupError, test_storage_initialization_failure_stops_startup(), test_session_initialization_failure_releases_keys()

### Community 96 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 97 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 98 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 100 - "_crypto_dependencies_ready"
Cohesion: 0.33
Nodes (4): health(), ready(), _crypto_dependencies_ready(), _unavailable()

### Community 101 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 102 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 107 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 114 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 116 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 819 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `SecureTransport`, `test_public_key_client.py`, `edge_gateway/app.py`, `test_gateway_cloud_secure.py`, `SecureSession`, `test_session.py`, `PqcMetrics`, `test_secure_message_tamper.py`, `create_app`, `encapsulate`, `session_client.py`, `_dispatch`, `CryptoFailureInjector`, `test_crypto_failures.py`, `derive_session_key`, `test_handshake_failure_stays_closed_without_a_session`, `test_legacy_gateway.py`, `test_pqc_observability.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `GatewayConfig`, `main`, `Clock`, `test_valid_mlkem_handshake_uses_the_frozen_session_contract`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `SessionManager`, `edge_gateway/app.py`, `CloudDispatch`, `test_gateway_cloud_secure.py`, `SecureSession`, `edge_gateway/crypto/symmetric.py`, `PqcMetrics`, `test_secure_transport.py`, `_dispatch`, `CryptoFailureInjector`, `test_crypto_failures.py`, `edge_gateway/crypto/envelope.py`, `build_aad`, `create_app`, `_Sessions`, `test_handshake_failure_stays_closed_without_a_session`, `edge_gateway/crypto/encoding.py`, `test_legacy_gateway.py`, `test_pqc_observability.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `GatewayConfig`, `main`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `CloudMetrics` connect `CloudMetrics` to `cloud_service/app.py`, `create_app`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.05616605616605617 - nodes in this community are weakly interconnected._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._