# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2685 nodes · 6755 edges · 164 communities (105 shown, 59 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 908 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- GatewayClient
- cli.py
- test_gateway_cloud_secure.py
- test_baseline_client.py
- SessionManager
- test_gateway_crypto_image.py
- cloud_service/app.py
- test_security_logging.py
- test_crypto_failures.py
- pathlib
- secure_transport.py
- edge_gateway/app.py
- MeasurementRepository
- test_secure_transport.py
- test_public_key_client.py
- dispatch.py
- CloudDispatch
- SessionManager
- test_measure_modernized_e2e.py
- CryptoFailureInjector
- PqcMetrics
- test_cloud_secure.py
- GatewayError
- edge_gateway/crypto/symmetric.py
- create_app
- CanonicalMeasurement
- create_app
- load_config
- test_legacy_compatibility.py
- load_config
- test_session.py
- FailureInjector
- test_baseline_gateway_measurements
- encode_binary
- test_cloud_failure_injection.py
- LegacyMeasurement
- SecureEnvelope
- encapsulate
- edge_gateway/crypto/encoding.py
- test_secure_message_tamper.py
- StoredMeasurement
- validate_measurement
- session_client.py
- test_gateway_measurements.py
- measurements.py
- CanonicalMeasurement
- test_secure_shutdown.py
- FailureMode
- derive_session_key
- test_cloud_baseline.py
- test_sensor.py
- fields
- build_aad
- test_mode_evaluation.py
- CloudMetrics
- test_cloud_queries.py
- test_gateway_app.py
- plaintext.py
- test_cloud_mlkem.py
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- validate_legacy_measurement
- test_gateway_validation.py
- run
- test_pqc_observability.py
- handshake
- run
- parse_public_key_response
- _ingest
- test_gateway_routes.py
- run
- live_gateway
- test_session_expiry_system.py
- test_cloud_public_key.py
- test_gateway_correlation.py
- edge_gateway/validation.py
- test_gateway_errors.py
- test_gateway_response_mapping.py
- test_valid_mlkem_handshake_uses_the_frozen_session_contract
- test_live_end_to_end_trace_is_correlated_safe_and_observable
- envelope_validation.py
- test_gateway_application_failures.py
- test_secure_envelope.py
- _Clock
- test_gateway_transport_interface.py
- ApplicationFailures
- _Server
- _HandshakeHandler
- test_gateway_operations.py
- test_gateway_cloud_secure_session.py
- _DroppedResponse
- KdfError
- test_body_limit_before_sequence_and_delivery
- test_gateway_validation_bypass.py
- Measurement
- test_end_to_end.py
- test_handshake_failure_stays_closed_without_a_session
- StartupError
- main
- test_untrusted_values_do_not_create_metric_labels
- _Handler
- test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path
- test_session_reuse_system.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- get_measurement
- test_final_secure_transport_review.py
- _Handler
- _Handler
- _Sizes
- _Cloud
- live_cloud
- test_shared_integration_assets.py
- baseline_measurement
- _baseline_transport
- CloudTransport
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- FalseyClock
- edge_gateway/models.py
- test_gateway_crypto_ci.py
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 86 edges
2. `load_config()` - 83 edges
3. `SecureTransport` - 55 edges
4. `load_config()` - 51 edges
5. `GatewayClient` - 50 edges
6. `create_app()` - 49 edges
7. `FailureMode` - 48 edges
8. `SessionManager` - 46 edges
9. `PqcMetrics` - 46 edges
10. `SecureTransportError` - 41 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `_receive()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → cloud_service/src/cloud_service/crypto/aad.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → cloud_service/src/cloud_service/crypto/aad.py

## Import Cycles
- None detected.

## Communities (164 total, 59 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.05
Nodes (59): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+51 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "GatewayClient"
Cohesion: 0.06
Nodes (39): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+31 more)

### Community 3 - "cli.py"
Cohesion: 0.09
Nodes (46): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text(), main(), parser() (+38 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (34): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+26 more)

### Community 5 - "test_baseline_client.py"
Cohesion: 0.08
Nodes (29): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+21 more)

### Community 6 - "SessionManager"
Cohesion: 0.06
Nodes (21): derive_session_key(), SecureSession, SessionAccessError, SessionManager, SessionState, _decode_ciphertext(), _error(), _establish() (+13 more)

### Community 7 - "test_gateway_crypto_image.py"
Cohesion: 0.06
Nodes (18): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+10 more)

### Community 8 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (8): health(), ready(), _crypto_dependencies_ready(), _unavailable(), SecurityMode, decrypt(), public_key(), _unavailable()

### Community 9 - "test_security_logging.py"
Cohesion: 0.07
Nodes (16): _Sessions, SecureSession, _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings() (+8 more)

### Community 10 - "test_crypto_failures.py"
Cohesion: 0.07
Nodes (20): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud (+12 more)

### Community 11 - "pathlib"
Cohesion: 0.15
Nodes (3): _deliver(), serve(), test_same_legacy_client_payload_succeeds_in_both_security_modes()

### Community 12 - "secure_transport.py"
Cohesion: 0.09
Nodes (11): SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport (+3 more)

### Community 14 - "MeasurementRepository"
Cohesion: 0.11
Nodes (25): Database, StorageConflictError, StorageError, MeasurementRepository, test_acceptance_is_committed_and_correlated(), test_concurrent_duplicates_across_connections(), save(), test_unrelated_record_id_collision_is_not_idempotent_success() (+17 more)

### Community 15 - "test_secure_transport.py"
Cohesion: 0.18
Nodes (27): SecureTransportError, session(), _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_attempt_metrics_preserve_retry_and_recovery_semantics() (+19 more)

### Community 16 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), _public_key() (+10 more)

### Community 17 - "dispatch.py"
Cohesion: 0.07
Nodes (5): get_config(), GatewayConfig, BaselineTransport, DispatchMetrics, CloudDeliveryError

### Community 18 - "CloudDispatch"
Cohesion: 0.13
Nodes (14): CloudDispatch, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 19 - "SessionManager"
Cohesion: 0.10
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 20 - "test_measure_modernized_e2e.py"
Cohesion: 0.08
Nodes (9): test_harness_rejects_invalid_sample_count(), _load(), run(), test_harness_rejects_invalid_sample_counts(), test_modernized_harness_and_comparison_reject_uncomparable_workloads(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed() (+1 more)

### Community 21 - "CryptoFailureInjector"
Cohesion: 0.09
Nodes (7): _secure_transport(), CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 22 - "PqcMetrics"
Cohesion: 0.07
Nodes (4): _Duration, PqcMetrics, _Cloud, __init__()

### Community 23 - "test_cloud_secure.py"
Cohesion: 0.16
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 24 - "GatewayError"
Cohesion: 0.12
Nodes (12): GatewayError, GatewayErrorCode, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit(), test_devices_have_independent_state(), test_first_and_next_sequence_are_accepted_without_gap() (+4 more)

### Community 25 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 26 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), main(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config(), test_invalid_config_exits_without_server_start(), test_lifecycle_liveness_and_unready_storage(), test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics() (+9 more)

### Community 27 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 28 - "create_app"
Cohesion: 0.11
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), lifespan(), measurements() (+10 more)

### Community 29 - "load_config"
Cohesion: 0.14
Nodes (18): _allowed_value(), ConfigurationError, _failure_delay(), _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+10 more)

### Community 30 - "test_legacy_compatibility.py"
Cohesion: 0.14
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 31 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 32 - "test_session.py"
Cohesion: 0.13
Nodes (12): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_connection_reset_during_session_post_is_retryable(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced() (+4 more)

### Community 33 - "FailureInjector"
Cohesion: 0.13
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 34 - "test_baseline_gateway_measurements"
Cohesion: 0.09
Nodes (14): cloud(), test_faults_preserve_real_cloud_storage_and_mode_boundaries(), test_seeded_random_execution_repeats_without_leaking_to_later_requests(), sleep(), live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_preserves_fields_correlation_and_persistence() (+6 more)

### Community 35 - "encode_binary"
Cohesion: 0.14
Nodes (8): decode_binary(), encode_binary(), EncodingError, KeyService, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 36 - "test_cloud_failure_injection.py"
Cohesion: 0.17
Nodes (17): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+9 more)

### Community 37 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 39 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 40 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 41 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.15
Nodes (10): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), test_existing_secure_envelope_authenticates_same_request_context() (+2 more)

### Community 42 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 43 - "StoredMeasurement"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 44 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 45 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 46 - "test_gateway_measurements.py"
Cohesion: 0.16
Nodes (14): test_processing_delay_yields_and_waits_before_delivery(), scenario(), test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline() (+6 more)

### Community 47 - "measurements.py"
Cohesion: 0.14
Nodes (4): MeasurementProcessor, GatewayMetrics, SequenceTracker, test_registry_updates_are_thread_safe_and_instances_are_isolated()

### Community 48 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 49 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 50 - "FailureMode"
Cohesion: 0.16
Nodes (8): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes(), test_injected_fault_is_counted_only_when_its_boundary_applies()

### Community 51 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 52 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): client(), payload(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 53 - "test_sensor.py"
Cohesion: 0.18
Nodes (15): Sensor, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc(), test_payload_has_exact_field_names_and_serialized_values() (+7 more)

### Community 54 - "fields"
Cohesion: 0.20
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 55 - "build_aad"
Cohesion: 0.17
Nodes (8): test_synthetic_secret_markers_never_appear_in_cloud_logs(), AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 56 - "test_mode_evaluation.py"
Cohesion: 0.20
Nodes (8): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline(), _time_sends()

### Community 57 - "CloudMetrics"
Cohesion: 0.14
Nodes (4): CloudMetrics, _labels(), _render_labels(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 58 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 59 - "test_gateway_app.py"
Cohesion: 0.13
Nodes (11): _logging_level(), main(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_mlkem_readiness_requires_initialized_transport_but_not_active_session(), test_readiness_is_local_and_delivery_still_requires_cloud() (+3 more)

### Community 60 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 61 - "test_cloud_mlkem.py"
Cohesion: 0.15
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 62 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 63 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 64 - "validate_legacy_measurement"
Cohesion: 0.17
Nodes (6): normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 65 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 66 - "run"
Cohesion: 0.13
Nodes (7): distribution(), _metrics(), _persisted_rows(), run(), _sample(), serve(), TimedRepository

### Community 67 - "test_pqc_observability.py"
Cohesion: 0.19
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 68 - "handshake"
Cohesion: 0.16
Nodes (10): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail() (+2 more)

### Community 69 - "run"
Cohesion: 0.19
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 70 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 71 - "_ingest"
Cohesion: 0.19
Nodes (6): AeadError, _error(), _ingest(), _NoMetrics, secure_measurement(), fail()

### Community 72 - "test_gateway_routes.py"
Cohesion: 0.27
Nodes (6): _client(), test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate(), test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery(), test_invalid_route_input_is_rejected_before_cloud(), test_valid_route_returns_202_only_after_cloud_success(), Transport

### Community 73 - "run"
Cohesion: 0.15
Nodes (5): distribution(), _persisted_rows(), run(), serve(), TimedRepository

### Community 74 - "live_gateway"
Cohesion: 0.24
Nodes (8): AcceptedBaseline, fixture_payload(), live_gateway(), post_raw(), test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery(), test_legacy_serializer_and_client_reach_live_gateway(), test_malformed_legacy_json_is_rejected_without_delivery(), test_parsed_invalid_legacy_payload_is_rejected_without_delivery()

### Community 75 - "test_session_expiry_system.py"
Cohesion: 0.22
Nodes (5): Clock, _measurement(), _metric(), serve(), test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively()

### Community 76 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 77 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 78 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 79 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 80 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 81 - "test_valid_mlkem_handshake_uses_the_frozen_session_contract"
Cohesion: 0.17
Nodes (3): cloud(), LiveCloud, test_valid_mlkem_handshake_uses_the_frozen_session_contract()

### Community 82 - "test_live_end_to_end_trace_is_correlated_safe_and_observable"
Cohesion: 0.17
Nodes (4): _get_json(), _get_metrics(), _serve(), test_live_end_to_end_trace_is_correlated_safe_and_observable()

### Community 83 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 84 - "test_gateway_application_failures.py"
Cohesion: 0.25
Nodes (6): test_cloud_fault_uses_existing_retries(), test_delay_configuration_accepts_bounded_values(), test_delay_configuration_rejects_unbounded_or_invalid_values(), test_disabled_faults_leave_valid_requests_unchanged(), test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(), test_processing_fault_is_visible_and_preserves_sequence()

### Community 85 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 86 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 88 - "test_gateway_transport_interface.py"
Cohesion: 0.29
Nodes (4): _measurement(), test_concrete_transport_errors_share_one_application_boundary(), test_processor_accepts_the_mode_independent_transport_protocol(), _Transport

### Community 89 - "ApplicationFailures"
Cohesion: 0.27
Nodes (3): ApplicationFailures, test_request_context_is_isolated_in_threads_and_cleared_after_failure(), scenario()

### Community 92 - "test_gateway_operations.py"
Cohesion: 0.28
Nodes (4): test_application_events_cover_success_validation_and_sequence_paths(), test_application_logger_rejects_unknown_events_and_unsafe_fields(), test_application_logs_drop_payload_secrets_and_exception_text(), _Transport

### Community 93 - "test_gateway_cloud_secure_session.py"
Cohesion: 0.28
Nodes (3): _query_one(), serve(), test_gateway_secure_session_encrypts_and_delivers_to_live_cloud()

### Community 95 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 96 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 97 - "test_body_limit_before_sequence_and_delivery"
Cohesion: 0.29
Nodes (4): test_body_limit_before_sequence_and_delivery(), test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(), scenario(), Transport

### Community 98 - "test_gateway_validation_bypass.py"
Cohesion: 0.36
Nodes (3): test_configured_failure_never_bypasses_domain_validation(), test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(), TransportSpy

### Community 100 - "test_end_to_end.py"
Cohesion: 0.32
Nodes (3): query_single_measurement(), serve(), test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row()

### Community 101 - "test_handshake_failure_stays_closed_without_a_session"
Cohesion: 0.29
Nodes (4): _Baseline, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 102 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 103 - "main"
Cohesion: 0.33
Nodes (3): _install(), main(), _serve()

### Community 104 - "test_untrusted_values_do_not_create_metric_labels"
Cohesion: 0.33
Nodes (4): test_injected_failures_are_exported_once_and_attempts_are_not_invented(), test_metrics_distinguish_local_acceptance_from_cloud_delivery(), test_untrusted_values_do_not_create_metric_labels(), Transport

### Community 106 - "test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path"
Cohesion: 0.29
Nodes (3): _query_one(), serve(), test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path()

### Community 107 - "test_session_reuse_system.py"
Cohesion: 0.38
Nodes (3): _metric(), serve(), test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries()

### Community 110 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 111 - "test_final_secure_transport_review.py"
Cohesion: 0.53
Nodes (4): test_every_checklist_item_has_a_result(), test_invalidate_is_scoped_to_the_rejected_session(), test_review_matches_the_secure_path(), _text()

### Community 118 - "live_cloud"
Cohesion: 0.40
Nodes (3): get_json(), live_cloud(), test_gateway_baseline_client_preserves_canonical_contract_and_storage_mapping()

### Community 126 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 128 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 951 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **59 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `secure_transport.py` to `test_gateway_cloud_secure.py`, `test_security_logging.py`, `test_crypto_failures.py`, `edge_gateway/app.py`, `test_secure_transport.py`, `dispatch.py`, `CloudDispatch`, `SessionManager`, `CryptoFailureInjector`, `PqcMetrics`, `edge_gateway/crypto/symmetric.py`, `create_app`, `edge_gateway/crypto/encoding.py`, `measurements.py`, `test_secure_shutdown.py`, `build_aad`, `test_mode_evaluation.py`, `plaintext.py`, `test_pqc_observability.py`, `live_gateway`, `test_session_expiry_system.py`, `test_gateway_application_failures.py`, `test_handshake_failure_stays_closed_without_a_session`, `main`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `FailureMode`, `secure_transport.py`, `edge_gateway/app.py`, `test_secure_transport.py`, `dispatch.py`, `CloudDispatch`, `CryptoFailureInjector`, `PqcMetrics`, `GatewayError`, `load_config`, `test_baseline_gateway_measurements`, `LegacyMeasurement`, `test_gateway_measurements.py`, `measurements.py`, `test_gateway_app.py`, `validate_legacy_measurement`, `test_gateway_routes.py`, `live_gateway`, `edge_gateway/validation.py`, `test_gateway_response_mapping.py`, `test_gateway_application_failures.py`, `ApplicationFailures`, `test_gateway_operations.py`, `test_body_limit_before_sequence_and_delivery`, `test_gateway_validation_bypass.py`, `test_untrusted_values_do_not_create_metric_labels`, `_baseline_transport`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `GatewayClient` connect `GatewayClient` to `FailureMode`, `test_device.py`, `test_baseline_gateway_measurements`, `run`, `test_end_to_end.py`, `test_baseline_client.py`, `SessionManager`, `run`, `live_gateway`, `pathlib`, `test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path`, `test_session_expiry_system.py`, `test_session_reuse_system.py`, `test_live_end_to_end_trace_is_correlated_safe_and_observable`, `test_legacy_compatibility.py`, `collections_abc`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `load_config()` (e.g. with `test_faults_preserve_real_cloud_storage_and_mode_boundaries()` and `test_seeded_random_execution_repeats_without_leaking_to_later_requests()`) actually correct?**
  _`load_config()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.0509020618556701 - nodes in this community are weakly interconnected._