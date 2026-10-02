# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2252 nodes · 5578 edges · 123 communities (79 shown, 44 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 781 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- logging
- edge_gateway/crypto/symmetric.py
- test_device.py
- LegacyMeasurement
- test_legacy_compatibility.py
- GatewayClient
- cli.py
- GatewayErrorCode
- create_app
- test_gateway_cloud_secure.py
- SecureTransport
- load_config
- secure_transport.py
- MeasurementRepository
- edge_gateway/app.py
- test_public_key_client.py
- FailureMode
- SessionManager
- SessionManager
- secure.py
- pytest
- test_crypto_failures.py
- test_session.py
- validate_measurement
- test_cloud_secure.py
- edge_gateway/crypto/session.py
- CloudDispatch
- PqcMetrics
- edge_gateway/config.py
- test_dispatch.py
- CanonicalMeasurement
- dataclasses
- test_cloud_mlkem.py
- StoredMeasurement
- test_mode_evaluation.py
- session_client.py
- FailureInjector
- test_secure_shutdown.py
- test_secure_message_tamper.py
- test_baseline_client.py
- test_cloud_baseline.py
- test_cloud_failure_injection.py
- measure_baseline.py
- CloudMetrics
- edge_gateway/crypto/encoding.py
- test_secure_transport.py
- json
- cloud_service/app.py
- test_cloud_session_api.py
- queries.py
- SecureSession
- pathlib
- encode_binary
- test_cloud_queries.py
- test_pqc_observability.py
- parse_public_key_response
- test_mlkem_handshake_failure_demo.py
- cloud_service/crypto/mlkem.py
- test_corrupt_ciphertext_demo.py
- test_refresh_graphify.py
- BaselineCloudClient
- test_gateway_correlation.py
- sessions.py
- test_clean_container_crypto.py
- test_cloud_public_key.py
- test_gateway_errors.py
- test_gateway_response_mapping.py
- refresh_graphify.py
- cloud
- test_gateway_crypto_image.py
- test_static_checks.py
- clean_container_crypto.py
- _Clock
- test_baseline_gateway_measurements
- _error_response
- _HandshakeHandler
- test_dependency_review.py
- AeadError
- test_repository_hygiene.py
- StartupError
- parametrize
- _Handler
- _Handler
- Clock
- test_shared_integration_assets.py
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _DroppedResponse
- _Handler
- _Handler
- _Handler
- _Handler
- BaselineSpy
- _Server
- KdfError
- _RejectRedirect
- _Cloud
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 59 edges
2. `load_config()` - 56 edges
3. `load_config()` - 50 edges
4. `SecureTransport` - 49 edges
5. `create_app()` - 48 edges
6. `FailureMode` - 46 edges
7. `SessionManager` - 43 edges
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
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/aad.py

## Import Cycles
- None detected.

## Communities (123 total, 44 thin omitted)

### Community 0 - "logging"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.05
Nodes (55): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+47 more)

### Community 2 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 3 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (32): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+24 more)

### Community 4 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (32): Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp() (+24 more)

### Community 5 - "GatewayClient"
Cohesion: 0.06
Nodes (24): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener (+16 more)

### Community 6 - "cli.py"
Cohesion: 0.14
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 7 - "GatewayErrorCode"
Cohesion: 0.09
Nodes (15): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once() (+7 more)

### Community 8 - "create_app"
Cohesion: 0.10
Nodes (28): create_app(), _logging_level(), main(), load_config(), test_classical_app_constructs_and_uses_baseline_client(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests() (+20 more)

### Community 9 - "test_gateway_cloud_secure.py"
Cohesion: 0.10
Nodes (26): CloudHarness, _deliver(), _measurement(), _seal(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope(), test_cloud_failure_retries_the_same_secure_request_without_storage(), test_duplicate_sequence_is_stored_once() (+18 more)

### Community 10 - "SecureTransport"
Cohesion: 0.07
Nodes (16): lifespan(), SecureTransport, _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default() (+8 more)

### Community 11 - "load_config"
Cohesion: 0.10
Nodes (25): create_app(), main(), load_config(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage() (+17 more)

### Community 12 - "secure_transport.py"
Cohesion: 0.10
Nodes (13): build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance() (+5 more)

### Community 13 - "MeasurementRepository"
Cohesion: 0.11
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 14 - "edge_gateway/app.py"
Cohesion: 0.11
Nodes (20): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), payload() (+12 more)

### Community 15 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+10 more)

### Community 16 - "FailureMode"
Cohesion: 0.10
Nodes (11): Config, FailureMode, SecurityMode, FailureInjector, FailureSelection, test_custom_environment(), test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request() (+3 more)

### Community 17 - "SessionManager"
Cohesion: 0.12
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 18 - "SessionManager"
Cohesion: 0.09
Nodes (7): clock(), log_security(), _token(), SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 19 - "secure.py"
Cohesion: 0.11
Nodes (14): AadError, build_aad(), _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+6 more)

### Community 20 - "pytest"
Cohesion: 0.10
Nodes (11): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact() (+3 more)

### Community 21 - "test_crypto_failures.py"
Cohesion: 0.11
Nodes (16): CryptoFailureInjector, _aad(), _injector(), measurement_url(), _MeasurementCloud, _plaintext(), test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates() (+8 more)

### Community 22 - "test_session.py"
Cohesion: 0.11
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 23 - "validate_measurement"
Cohesion: 0.13
Nodes (14): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries() (+6 more)

### Community 24 - "test_cloud_secure.py"
Cohesion: 0.16
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 25 - "edge_gateway/crypto/session.py"
Cohesion: 0.13
Nodes (12): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+4 more)

### Community 26 - "CloudDispatch"
Cohesion: 0.10
Nodes (6): _baseline_transport(), get_config(), GatewayConfig, BaselineTransport, CloudDispatch, DispatchMetrics

### Community 27 - "PqcMetrics"
Cohesion: 0.09
Nodes (3): _secure_transport(), _Duration, PqcMetrics

### Community 28 - "edge_gateway/config.py"
Cohesion: 0.14
Nodes (14): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+6 more)

### Community 29 - "test_dispatch.py"
Cohesion: 0.16
Nodes (13): _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 30 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 31 - "dataclasses"
Cohesion: 0.16
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 32 - "test_cloud_mlkem.py"
Cohesion: 0.10
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 33 - "StoredMeasurement"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 34 - "test_mode_evaluation.py"
Cohesion: 0.14
Nodes (9): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Sizes, test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline() (+1 more)

### Community 35 - "session_client.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 36 - "FailureInjector"
Cohesion: 0.15
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 37 - "test_secure_shutdown.py"
Cohesion: 0.13
Nodes (9): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_lifespan_runs_security_cleanup_after_stopping_work(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+1 more)

### Community 38 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 39 - "test_baseline_client.py"
Cohesion: 0.23
Nodes (16): BaselineAcceptance, BaselineCloudError, _client(), _send(), test_client_normalizes_idempotent_acceptance(), test_client_posts_exact_canonical_body_and_request_header(), test_http_failures_are_classified_without_retry(), test_permanent_failure_stops_without_sleep_or_second_request() (+8 more)

### Community 40 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 41 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 42 - "measure_baseline.py"
Cohesion: 0.15
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 43 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 44 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.17
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 45 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 46 - "json"
Cohesion: 0.18
Nodes (7): live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(), test_legacy_to_sqlite_preserves_gateway_transformations()

### Community 47 - "cloud_service/app.py"
Cohesion: 0.13
Nodes (9): health(), ready(), _crypto_dependencies_ready(), _unavailable(), ConfigurationError, integer(), number(), text() (+1 more)

### Community 48 - "test_cloud_session_api.py"
Cohesion: 0.16
Nodes (10): handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail() (+2 more)

### Community 49 - "queries.py"
Cohesion: 0.17
Nodes (5): public_key(), _unavailable(), _error(), get_measurement(), list_measurements()

### Community 50 - "SecureSession"
Cohesion: 0.13
Nodes (5): _Sessions, SecureSession, _Sessions, _session(), get_or_establish()

### Community 52 - "encode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 53 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 54 - "test_pqc_observability.py"
Cohesion: 0.16
Nodes (7): test_shared_canonical_fixture_is_accepted_and_preserves_the_baseline_contract(), _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 55 - "parse_public_key_response"
Cohesion: 0.19
Nodes (9): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 56 - "test_mlkem_handshake_failure_demo.py"
Cohesion: 0.16
Nodes (5): _Baseline, _Cloud, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 57 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 58 - "test_corrupt_ciphertext_demo.py"
Cohesion: 0.18
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 59 - "test_refresh_graphify.py"
Cohesion: 0.19
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 60 - "BaselineCloudClient"
Cohesion: 0.17
Nodes (5): BaselineCloudClient, _dump(), _endpoint(), _error_code(), _parse_acceptance()

### Community 61 - "test_gateway_correlation.py"
Cohesion: 0.22
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 62 - "sessions.py"
Cohesion: 0.32
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 63 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 64 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 65 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 66 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 67 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 68 - "cloud"
Cohesion: 0.20
Nodes (4): cloud(), _install_trace(), test_production_cloud_app_has_secure_measurement_route(), Trace

### Community 69 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 70 - "test_static_checks.py"
Cohesion: 0.27
Nodes (7): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked()

### Community 71 - "clean_container_crypto.py"
Cohesion: 0.29
Nodes (3): _install(), main(), _serve()

### Community 73 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 74 - "test_baseline_gateway_measurements"
Cohesion: 0.20
Nodes (4): test_baseline_gateway_measurements(), _post(), send(), Measurement

### Community 75 - "_error_response"
Cohesion: 0.25
Nodes (8): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response(), _unavailable()

### Community 78 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 79 - "AeadError"
Cohesion: 0.29
Nodes (3): AeadError, test_rejection_has_one_public_message(), fail()

### Community 82 - "parametrize"
Cohesion: 0.33
Nodes (3): test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 90 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 92 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 769 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `.__init__`, `test_mode_evaluation.py`, `test_corrupt_ciphertext_demo.py`, `create_app`, `SecureTransport`, `secure_transport.py`, `edge_gateway/app.py`, `SessionManager`, `test_pqc_observability.py`, `test_mlkem_handshake_failure_demo.py`, `edge_gateway/crypto/session.py`, `CloudDispatch`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `edge_gateway/crypto/symmetric.py`, `create_app`, `test_gateway_cloud_secure.py`, `secure_transport.py`, `edge_gateway/app.py`, `SessionManager`, `test_crypto_failures.py`, `CloudDispatch`, `PqcMetrics`, `test_dispatch.py`, `test_mode_evaluation.py`, `test_secure_shutdown.py`, `edge_gateway/crypto/encoding.py`, `test_secure_transport.py`, `SecureSession`, `test_pqc_observability.py`, `test_mlkem_handshake_failure_demo.py`, `test_corrupt_ciphertext_demo.py`, `clean_container_crypto.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `create_app()` connect `load_config` to `MeasurementRepository`, `FailureMode`, `SessionManager`, `test_cloud_secure.py`, `test_cloud_mlkem.py`, `test_mode_evaluation.py`, `test_cloud_baseline.py`, `test_cloud_failure_injection.py`, `measure_baseline.py`, `CloudMetrics`, `cloud_service/app.py`, `test_cloud_session_api.py`, `test_cloud_queries.py`, `test_pqc_observability.py`, `sessions.py`, `test_cloud_public_key.py`, `cloud`, `clean_container_crypto.py`, `StartupError`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `logging` be split into smaller, more focused modules?**
  _Cohesion score 0.05513612445664608 - nodes in this community are weakly interconnected._
- **Should `edge_gateway/crypto/symmetric.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05236091631603553 - nodes in this community are weakly interconnected._