# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2095 nodes · 5208 edges · 122 communities (77 shown, 45 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 741 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_legacy_compatibility.py
- GatewayErrorCode
- test_gateway_baseline_integration.py
- test_secure_message_tamper.py
- test_gateway_cloud_secure.py
- cli.py
- SecureTransport
- test_device.py
- FailureMode
- FailureMode
- MeasurementRepository
- SecureTransportError
- edge_gateway/crypto/symmetric.py
- test_public_key_client.py
- test_sensor.py
- test_cloud_secure.py
- secure_transport.py
- SecureSession
- test_dispatch.py
- measure_baseline.py
- logging
- create_app
- test_mode_evaluation.py
- SessionManager
- load_config
- test_cloud_session_api.py
- load_config
- CanonicalMeasurement
- device.py
- edge_gateway/crypto/session.py
- dataclasses
- LegacyMeasurement
- test_cloud_mlkem.py
- validate_measurement
- encapsulate
- fields
- StoredMeasurement
- CanonicalMeasurement
- test_secure_shutdown.py
- json
- test_session.py
- test_secure_transport.py
- test_security_logging.py
- test_cloud_baseline.py
- edge_gateway/validation.py
- load_config
- decode_binary
- test_cloud_queries.py
- create_app
- plaintext.py
- parse_public_key_response
- DeviceController
- test_gateway_measurements.py
- test_gateway_validation.py
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- encode_binary
- edge_gateway/config.py
- _ingest
- CryptoFailureInjector
- test_crypto_failures.py
- pathlib
- test_clean_container_crypto.py
- test_cloud_public_key.py
- edge_gateway/app.py
- test_gateway_response_mapping.py
- refresh_graphify.py
- test_gateway_crypto_image.py
- envelope_validation.py
- clean_container_crypto.py
- derive_session_key
- test_secure_envelope.py
- _Clock
- test_shutdown_after_gateway_unavailable_delivery
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- edge_gateway/crypto/kdf.py
- _HandshakeHandler
- queries.py
- _DroppedResponse
- KdfError
- test_refresh_graphify.py
- test_repository_hygiene.py
- pytest
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- _Handler
- test_shared_integration_assets.py
- public_key
- baseline_measurement
- .shutdown
- test_session_missing_and_expired_force_a_new_handshake
- crypto/failure.py
- _Handler
- _Handler
- scenario
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 58 edges
2. `load_config()` - 54 edges
3. `load_config()` - 47 edges
4. `SecureTransport` - 45 edges
5. `FailureMode` - 44 edges
6. `create_app()` - 43 edges
7. `SessionManager` - 38 edges
8. `SecureTransportError` - 37 edges
9. `FailureMode` - 35 edges
10. `FailureInjector` - 34 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `live_baseline_gateway()` --uses--> `GatewayClient`  [INFERRED]
  edge_gateway/tests/test_gateway_baseline_integration.py → legacy_system/src/legacy_system/client.py
- `_deliver()` --uses--> `SecureAcceptance`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/secure_transport.py

## Import Cycles
- None detected.

## Communities (122 total, 45 thin omitted)

### Community 0 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (36): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+28 more)

### Community 1 - "GatewayErrorCode"
Cohesion: 0.05
Nodes (26): baseline_headers(), create_request_id(), GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, test_baseline_request_carries_id_in_header_and_keeps_body_unchanged() (+18 more)

### Community 2 - "test_gateway_baseline_integration.py"
Cohesion: 0.06
Nodes (33): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+25 more)

### Community 3 - "test_secure_message_tamper.py"
Cohesion: 0.06
Nodes (25): AadError, build_aad(), SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes() (+17 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+24 more)

### Community 5 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 6 - "SecureTransport"
Cohesion: 0.05
Nodes (10): _Duration, PqcMetrics, _endpoint(), SecureTransport, BaselineTransport, CloudDispatch, DispatchMetrics, _Baseline (+2 more)

### Community 7 - "test_device.py"
Cohesion: 0.08
Nodes (24): FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, make_config() (+16 more)

### Community 8 - "FailureMode"
Cohesion: 0.10
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 9 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 10 - "MeasurementRepository"
Cohesion: 0.11
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 11 - "SecureTransportError"
Cohesion: 0.12
Nodes (10): _dump(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransportError, _SessionRecovery (+2 more)

### Community 12 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.19
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 13 - "test_public_key_client.py"
Cohesion: 0.12
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), _public_key(), test_cloud_url_and_timeout_are_validated() (+8 more)

### Community 14 - "test_sensor.py"
Cohesion: 0.10
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 15 - "test_cloud_secure.py"
Cohesion: 0.16
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 16 - "secure_transport.py"
Cohesion: 0.12
Nodes (11): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, _RejectRedirect, _independent(), test_each_authenticated_field_changes_the_aad_bytes() (+3 more)

### Community 17 - "SecureSession"
Cohesion: 0.10
Nodes (11): _Sessions, SecureSession, _session(), _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 18 - "test_dispatch.py"
Cohesion: 0.15
Nodes (14): _Baseline, cloud(), _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 19 - "measure_baseline.py"
Cohesion: 0.11
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 20 - "logging"
Cohesion: 0.17
Nodes (7): SecurityMode, derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 21 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+9 more)

### Community 22 - "test_mode_evaluation.py"
Cohesion: 0.12
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 24 - "load_config"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 25 - "test_cloud_session_api.py"
Cohesion: 0.12
Nodes (13): StartupError, client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject() (+5 more)

### Community 26 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 27 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 28 - "device.py"
Cohesion: 0.12
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 29 - "edge_gateway/crypto/session.py"
Cohesion: 0.15
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 30 - "dataclasses"
Cohesion: 0.16
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 31 - "LegacyMeasurement"
Cohesion: 0.22
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 32 - "test_cloud_mlkem.py"
Cohesion: 0.11
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 33 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 34 - "encapsulate"
Cohesion: 0.16
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 35 - "fields"
Cohesion: 0.16
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 36 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 37 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 38 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 39 - "json"
Cohesion: 0.15
Nodes (5): _timestamp(), normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input()

### Community 40 - "test_session.py"
Cohesion: 0.16
Nodes (10): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active() (+2 more)

### Community 41 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 42 - "test_security_logging.py"
Cohesion: 0.13
Nodes (6): _Clock, _Cloud, cloud_url(), _Handler, test_metrics_endpoint_exposes_the_same_registry(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 43 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500() (+1 more)

### Community 44 - "edge_gateway/validation.py"
Cohesion: 0.15
Nodes (10): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage() (+2 more)

### Community 45 - "load_config"
Cohesion: 0.16
Nodes (12): load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration(), test_settings_dependency_can_be_overridden_and_isolated() (+4 more)

### Community 46 - "decode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 47 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 48 - "create_app"
Cohesion: 0.16
Nodes (11): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+3 more)

### Community 49 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 50 - "parse_public_key_response"
Cohesion: 0.19
Nodes (9): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 52 - "test_gateway_measurements.py"
Cohesion: 0.22
Nodes (10): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook(), test_sequence_rejections_gaps_independence_and_unique_ids(), test_sequence_state_is_isolated_between_app_instances() (+2 more)

### Community 53 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 54 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 55 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 56 - "encode_binary"
Cohesion: 0.23
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _different_nonce(), _tamper()

### Community 57 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 58 - "_ingest"
Cohesion: 0.20
Nodes (5): AeadError, decrypt(), _error(), _ingest(), secure_measurement()

### Community 60 - "test_crypto_failures.py"
Cohesion: 0.22
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 62 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 63 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 64 - "edge_gateway/app.py"
Cohesion: 0.23
Nodes (5): _baseline_transport(), get_config(), _logging_level(), main(), GatewayConfig

### Community 65 - "test_gateway_response_mapping.py"
Cohesion: 0.27
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 66 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 67 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 68 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 69 - "clean_container_crypto.py"
Cohesion: 0.25
Nodes (3): _install(), main(), _serve()

### Community 70 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 71 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 72 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 73 - "test_shutdown_after_gateway_unavailable_delivery"
Cohesion: 0.22
Nodes (4): test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown(), fake_signal()

### Community 74 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 75 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 78 - "queries.py"
Cohesion: 0.46
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 79 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 80 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 81 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 101 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 707 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `SecureTransport` to `edge_gateway/app.py`, `test_security_logging.py`, `secure_transport.py`, `create_app`, `SecureSession`, `test_mode_evaluation.py`, `SessionManager`, `edge_gateway/crypto/session.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `SecureTransportError`, `edge_gateway/crypto/symmetric.py`, `secure_transport.py`, `SecureSession`, `test_dispatch.py`, `test_mode_evaluation.py`, `SessionManager`, `test_secure_shutdown.py`, `test_secure_transport.py`, `create_app`, `plaintext.py`, `encode_binary`, `CryptoFailureInjector`, `edge_gateway/app.py`, `clean_container_crypto.py`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `.shutdown`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `SessionEstablishmentError` connect `SessionManager` to `SecureTransport`, `test_session.py`, `test_secure_transport.py`, `secure_transport.py`, `KdfError`, `test_dispatch.py`, `parse_public_key_response`, `test_crypto_failures.py`, `edge_gateway/crypto/session.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_legacy_compatibility.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05333333333333334 - nodes in this community are weakly interconnected._
- **Should `GatewayErrorCode` be split into smaller, more focused modules?**
  _Cohesion score 0.05341614906832298 - nodes in this community are weakly interconnected._