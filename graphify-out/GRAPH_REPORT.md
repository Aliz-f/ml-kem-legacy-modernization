# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2445 nodes · 6146 edges · 130 communities (88 shown, 42 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 861 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_cloud_secure.py
- test_device.py
- measurements.py
- test_gateway_cloud_secure.py
- LegacyMeasurement
- cli.py
- FailureInjector
- cloud_service/app.py
- GatewayClient
- test_security_logging.py
- SessionManager
- MeasurementRepository
- test_public_key_client.py
- json
- edge_gateway/app.py
- SessionManager
- test_crypto_failures.py
- create_app
- test_gateway_measurements.py
- create_app
- test_gateway_validation.py
- test_session.py
- PqcMetrics
- derive_session_key
- edge_gateway/crypto/symmetric.py
- test_baseline_gateway_measurements
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- secure_transport.py
- test_mode_evaluation.py
- load_config
- test_public_key.py
- CanonicalMeasurement
- FailureMode
- load_config
- test_secure_transport.py
- pathlib
- CryptoFailureInjector
- test_secure_shutdown.py
- validate_measurement
- session_client.py
- test_dispatch.py
- StoredMeasurement
- test_cloud_failure_injection.py
- CloudMetrics
- fields
- test_cloud_baseline.py
- SecureTransport
- encapsulate
- test_cloud_session_api.py
- BaselineCloudClient
- edge_gateway/crypto/envelope.py
- build_aad
- test_legacy_gateway.py
- encode_binary
- test_cloud_queries.py
- edge_gateway/crypto/encoding.py
- test_baseline_client.py
- test_mlkem_handshake_failure_demo.py
- SecureTransportError
- GatewayMetrics
- test_cloud_kdf.py
- test_gateway_correlation.py
- CloudDispatch
- test_pqc_observability.py
- run
- test_cloud_mlkem.py
- test_gateway_routes.py
- test_gateway_shutdown.py
- test_cloud_public_key.py
- test_gateway_application_metrics.py
- BaselineCloudError
- test_gateway_response_mapping.py
- test_gateway_crypto_image.py
- test_secure_envelope.py
- test_static_checks.py
- refresh_graphify.py
- test_corrupted_ciphertext_is_rejected_and_not_stored
- keys.py
- _HandshakeHandler
- test_dependency_review.py
- test_gateway_operations.py
- test_clean_container_crypto.py
- _DroppedResponse
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- test_refresh_graphify.py
- sleep
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- get_measurement
- pytest
- test_final_secure_transport_review.py
- _Handler
- _Handler
- public_key
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- _Handler
- _Handler
- _Handler
- _Cloud
- test_faults_preserve_real_cloud_storage_and_mode_boundaries
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 85 edges
2. `load_config()` - 83 edges
3. `SecureTransport` - 54 edges
4. `load_config()` - 51 edges
5. `create_app()` - 49 edges
6. `FailureMode` - 46 edges
7. `SessionManager` - 44 edges
8. `PqcMetrics` - 42 edges
9. `SecureTransportError` - 39 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_gateway_canonical_json_and_correlation_are_accepted_and_mapped()` --uses--> `BaselineCloudClient`  [INFERRED]
  tests/integration/test_gateway_cloud_baseline.py → edge_gateway/src/edge_gateway/cloud/baseline.py
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py

## Import Cycles
- None detected.

## Communities (130 total, 42 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_cloud_secure.py"
Cohesion: 0.05
Nodes (48): EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+40 more)

### Community 2 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 3 - "measurements.py"
Cohesion: 0.06
Nodes (26): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, CloudDeliveryError, client(), test_application_errors_have_stable_http_contract() (+18 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 5 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (32): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+24 more)

### Community 6 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 7 - "FailureInjector"
Cohesion: 0.06
Nodes (28): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+20 more)

### Community 8 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (10): _crypto_dependencies_ready(), SecurityMode, derive_session_key(), SessionAccessError, decrypt(), _decode_ciphertext(), _error(), _establish() (+2 more)

### Community 9 - "GatewayClient"
Cohesion: 0.09
Nodes (22): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+14 more)

### Community 10 - "test_security_logging.py"
Cohesion: 0.07
Nodes (17): _Sessions, _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings() (+9 more)

### Community 11 - "SessionManager"
Cohesion: 0.08
Nodes (14): SecureSession, SessionManager, SessionState, clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+6 more)

### Community 12 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 13 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+11 more)

### Community 14 - "json"
Cohesion: 0.12
Nodes (3): _post(), test_cloud_rejects_missing_or_unknown_canonical_fields(), test_gateway_canonical_json_and_correlation_are_accepted_and_mapped()

### Community 15 - "edge_gateway/app.py"
Cohesion: 0.08
Nodes (7): _baseline_transport(), get_config(), _secure_transport(), _token(), GatewayConfig, BaselineTransport, ApplicationFailures

### Community 16 - "SessionManager"
Cohesion: 0.09
Nodes (7): _RejectRedirect, log_security(), _token(), SecureSession, SessionEstablishmentError, SessionManager, _session()

### Community 17 - "test_crypto_failures.py"
Cohesion: 0.08
Nodes (19): _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud, _plaintext() (+11 more)

### Community 18 - "create_app"
Cohesion: 0.09
Nodes (25): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), ready() (+17 more)

### Community 19 - "test_gateway_measurements.py"
Cohesion: 0.10
Nodes (21): test_cloud_fault_uses_existing_retries(), session(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_delay_yields_and_waits_before_delivery(), scenario() (+13 more)

### Community 20 - "create_app"
Cohesion: 0.08
Nodes (20): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+12 more)

### Community 21 - "test_gateway_validation.py"
Cohesion: 0.12
Nodes (20): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client() (+12 more)

### Community 22 - "test_session.py"
Cohesion: 0.11
Nodes (15): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+7 more)

### Community 23 - "PqcMetrics"
Cohesion: 0.08
Nodes (4): _Duration, PqcMetrics, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario()

### Community 24 - "derive_session_key"
Cohesion: 0.11
Nodes (12): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+4 more)

### Community 25 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 26 - "test_baseline_gateway_measurements"
Cohesion: 0.09
Nodes (14): cloud(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy() (+6 more)

### Community 27 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 28 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 30 - "test_mode_evaluation.py"
Cohesion: 0.13
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 31 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 32 - "test_public_key.py"
Cohesion: 0.11
Nodes (8): decapsulate(), generate_keypair(), MlKemError, PrivateKey, _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 33 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 34 - "FailureMode"
Cohesion: 0.13
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 35 - "load_config"
Cohesion: 0.20
Nodes (16): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+8 more)

### Community 36 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (19): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_gateway_exports_secure_attempt_metrics_from_shared_registry() (+11 more)

### Community 37 - "pathlib"
Cohesion: 0.11
Nodes (6): _install(), main(), _serve(), test_quality_workflow_names_the_gateway_crypto_suites(), _fixture(), test_shared_fixtures_match_the_frozen_legacy_and_canonical_shapes()

### Community 38 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 39 - "test_secure_shutdown.py"
Cohesion: 0.13
Nodes (9): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_lifespan_runs_security_cleanup_after_stopping_work(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+1 more)

### Community 40 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 41 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 42 - "test_dispatch.py"
Cohesion: 0.21
Nodes (12): _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline(), test_failure_log_omits_the_measurement() (+4 more)

### Community 43 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 44 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 45 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 46 - "fields"
Cohesion: 0.17
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 47 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 48 - "SecureTransport"
Cohesion: 0.16
Nodes (4): SecureEnvelope, _dump(), _Measurement, SecureTransport

### Community 49 - "encapsulate"
Cohesion: 0.18
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 50 - "test_cloud_session_api.py"
Cohesion: 0.17
Nodes (11): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail() (+3 more)

### Community 51 - "BaselineCloudClient"
Cohesion: 0.14
Nodes (6): BaselineAcceptance, BaselineCloudClient, _dump(), _endpoint(), _error_code(), _parse_acceptance()

### Community 52 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.19
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 53 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 54 - "test_legacy_gateway.py"
Cohesion: 0.16
Nodes (9): AcceptedCloud, _client(), gateway(), _live_gateway(), _raw(), test_invalid_json_is_400_and_non_retryable(), test_parsed_invalid_legacy_fixtures_are_non_retryable_422(), test_sequence_conflicts_are_non_retryable_and_gap_is_accepted_and_counted() (+1 more)

### Community 55 - "encode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 56 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 57 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 58 - "test_baseline_client.py"
Cohesion: 0.30
Nodes (14): _client(), _send(), test_attempt_metrics_include_retry_and_invalid_acceptance(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request(), test_redirect_is_rejected_and_constructor_validates_inputs() (+6 more)

### Community 59 - "test_mlkem_handshake_failure_demo.py"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 60 - "SecureTransportError"
Cohesion: 0.17
Nodes (6): _endpoint(), _error_code(), _parse_acceptance(), _RetryableTransport, SecureTransportError, _SessionRecovery

### Community 62 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 63 - "test_gateway_correlation.py"
Cohesion: 0.19
Nodes (7): baseline_headers(), create_request_id(), build_secure_envelope(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 64 - "CloudDispatch"
Cohesion: 0.17
Nodes (3): SecureAcceptance, CloudDispatch, DispatchMetrics

### Community 65 - "test_pqc_observability.py"
Cohesion: 0.19
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 66 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 67 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 68 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 70 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 71 - "test_gateway_application_metrics.py"
Cohesion: 0.23
Nodes (5): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_registry_updates_are_thread_safe_and_instances_are_isolated(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 72 - "BaselineCloudError"
Cohesion: 0.20
Nodes (7): BaselineCloudError, _RejectRedirect, test_baseline_shutdown_waits_for_attempt_and_closes_once(), post(), _live_gateway(), test_real_gateway_failure_chain_is_bounded_by_committed_sequence_state(), unavailable()

### Community 73 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 74 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 75 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 76 - "test_static_checks.py"
Cohesion: 0.27
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 77 - "refresh_graphify.py"
Cohesion: 0.27
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 78 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 81 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 82 - "test_gateway_operations.py"
Cohesion: 0.28
Nodes (4): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 83 - "test_clean_container_crypto.py"
Cohesion: 0.22
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 84 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 85 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 86 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 87 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 88 - "sleep"
Cohesion: 0.33
Nodes (4): test_existing_gateway_session_client_over_real_http(), sleep(), cloud(), _live_cloud()

### Community 91 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 93 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 102 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 104 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 837 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `test_security_logging.py`, `edge_gateway/app.py`, `SessionManager`, `test_crypto_failures.py`, `create_app`, `test_gateway_measurements.py`, `PqcMetrics`, `edge_gateway/crypto/symmetric.py`, `secure_transport.py`, `test_mode_evaluation.py`, `test_secure_transport.py`, `pathlib`, `CryptoFailureInjector`, `test_secure_shutdown.py`, `test_dispatch.py`, `edge_gateway/crypto/envelope.py`, `build_aad`, `edge_gateway/crypto/encoding.py`, `test_mlkem_handshake_failure_demo.py`, `SecureTransportError`, `GatewayMetrics`, `CloudDispatch`, `test_pqc_observability.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `CloudDispatch`, `test_pqc_observability.py`, `CryptoFailureInjector`, `test_security_logging.py`, `test_corrupted_ciphertext_is_rejected_and_not_stored`, `edge_gateway/app.py`, `SecureTransport`, `SessionManager`, `create_app`, `test_mlkem_handshake_failure_demo.py`, `SecureTransportError`, `secure_transport.py`, `test_mode_evaluation.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `measurements.py`, `LegacyMeasurement`, `test_security_logging.py`, `edge_gateway/app.py`, `test_gateway_measurements.py`, `test_gateway_validation.py`, `PqcMetrics`, `test_baseline_gateway_measurements`, `test_legacy_compatibility.py`, `load_config`, `test_secure_transport.py`, `test_secure_shutdown.py`, `SecureTransport`, `test_legacy_gateway.py`, `GatewayMetrics`, `CloudDispatch`, `test_gateway_routes.py`, `test_gateway_shutdown.py`, `test_gateway_application_metrics.py`, `BaselineCloudError`, `test_gateway_response_mapping.py`, `test_gateway_operations.py`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_validation_bypass.py`, `test_faults_preserve_real_cloud_storage_and_mode_boundaries`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `SecureTransport` (e.g. with `main()` and `create_app()`) actually correct?**
  _`SecureTransport` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._