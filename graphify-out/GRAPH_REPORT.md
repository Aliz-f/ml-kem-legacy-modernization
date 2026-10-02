# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2232 nodes · 5544 edges · 112 communities (77 shown, 35 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 781 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- GatewayClient
- FailureMode
- test_gateway_cloud_secure.py
- SecureTransportError
- test_mode_evaluation.py
- cli.py
- test_baseline_client.py
- GatewayErrorCode
- load_config
- secure_transport.py
- secure.py
- MeasurementRepository
- load_config
- cloud_service/app.py
- create_app
- SessionManager
- test_public_key_client.py
- CryptoFailureInjector
- SecureTransport
- test_session.py
- test_cloud_secure.py
- SessionManager
- edge_gateway/crypto/symmetric.py
- SecureSession
- LegacyMeasurement
- test_cloud_session_api.py
- CanonicalMeasurement
- PqcMetrics
- dataclasses
- test_crypto_failures.py
- encapsulate
- json
- FailureInjector
- test_secure_message_tamper.py
- validate_measurement
- test_secure_shutdown.py
- measure_baseline.py
- build_aad
- StoredMeasurement
- test_sensor.py
- derive_session_key
- CanonicalMeasurement
- encode_binary
- test_cloud_baseline.py
- edge_gateway/crypto/encoding.py
- parse_public_key_response
- test_gateway_crypto_image.py
- refresh_graphify.py
- test_cloud_kdf.py
- queries.py
- edge_gateway/validation.py
- CloudDispatch
- edge_gateway/models.py
- test_gateway_validation.py
- test_cloud_queries.py
- cloud_service/crypto/mlkem.py
- edge_gateway/crypto/envelope.py
- test_cloud_public_key.py
- test_gateway_baseline_integration.py
- test_corrupt_ciphertext_demo.py
- edge_gateway/crypto/aad.py
- _Clock
- fastapi_testclient
- pathlib
- sessions.py
- pytest
- test_cloud_mlkem.py
- test_gateway_correlation.py
- test_secure_envelope.py
- sensor.py
- _Clock
- KeyService
- _HandshakeHandler
- KdfError
- test_baseline_gateway_measurements
- test_refresh_graphify.py
- test_repository_hygiene.py
- _Handler
- _Handler
- test_shared_integration_assets.py
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- FalseyClock
- _Handler
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
- `_receive()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → cloud_service/src/cloud_service/crypto/aad.py

## Import Cycles
- None detected.

## Communities (112 total, 35 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "GatewayClient"
Cohesion: 0.05
Nodes (36): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+28 more)

### Community 3 - "FailureMode"
Cohesion: 0.06
Nodes (29): FailureMode, FailureInjector, FailureSelection, CloudMetrics, _labels(), _render_labels(), canonical(), config() (+21 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+25 more)

### Community 5 - "SecureTransportError"
Cohesion: 0.08
Nodes (33): SecureTransportError, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+25 more)

### Community 6 - "test_mode_evaluation.py"
Cohesion: 0.05
Nodes (20): _install(), main(), _serve(), _Cloud, _Baseline, _Calls, _dispatch(), measure_modes() (+12 more)

### Community 7 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 8 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (25): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+17 more)

### Community 9 - "GatewayErrorCode"
Cohesion: 0.08
Nodes (19): GatewayError, GatewayErrorCode, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized() (+11 more)

### Community 10 - "load_config"
Cohesion: 0.09
Nodes (32): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+24 more)

### Community 11 - "secure_transport.py"
Cohesion: 0.09
Nodes (7): _baseline_transport(), get_config(), GatewayConfig, corrupt_ciphertext_copy(), BaselineTransport, MeasurementProcessor, UnavailableBaseline

### Community 12 - "secure.py"
Cohesion: 0.08
Nodes (16): AadError, build_aad(), _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+8 more)

### Community 13 - "MeasurementRepository"
Cohesion: 0.10
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 14 - "load_config"
Cohesion: 0.11
Nodes (26): _logging_level(), main(), _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config() (+18 more)

### Community 15 - "cloud_service/app.py"
Cohesion: 0.08
Nodes (10): health(), ready(), _crypto_dependencies_ready(), _unavailable(), SecurityMode, baseline_measurement(), _error(), _serve() (+2 more)

### Community 16 - "create_app"
Cohesion: 0.10
Nodes (23): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+15 more)

### Community 17 - "SessionManager"
Cohesion: 0.10
Nodes (13): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes() (+5 more)

### Community 18 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+10 more)

### Community 19 - "CryptoFailureInjector"
Cohesion: 0.08
Nodes (8): _secure_transport(), CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _Baseline, _count(), _serve(), test_handshake_failure_stays_closed_without_a_session()

### Community 20 - "SecureTransport"
Cohesion: 0.11
Nodes (10): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+2 more)

### Community 21 - "test_session.py"
Cohesion: 0.10
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 22 - "test_cloud_secure.py"
Cohesion: 0.15
Nodes (26): canonical(), client(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable() (+18 more)

### Community 23 - "SessionManager"
Cohesion: 0.10
Nodes (6): lifespan(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 24 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 25 - "SecureSession"
Cohesion: 0.10
Nodes (11): _Sessions, SecureSession, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 26 - "LegacyMeasurement"
Cohesion: 0.18
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 27 - "test_cloud_session_api.py"
Cohesion: 0.12
Nodes (13): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+5 more)

### Community 28 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 29 - "PqcMetrics"
Cohesion: 0.09
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 30 - "dataclasses"
Cohesion: 0.16
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 31 - "test_crypto_failures.py"
Cohesion: 0.13
Nodes (14): _aad(), _injector(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates(), test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault() (+6 more)

### Community 32 - "encapsulate"
Cohesion: 0.15
Nodes (10): test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 33 - "json"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 34 - "FailureInjector"
Cohesion: 0.15
Nodes (12): FailureInjector, test_defaults_are_disabled(), test_ineligible_calls_do_not_consume_seeded_decisions(), test_invalid_mode_rejected(), test_invalid_rate_rejected(), test_invalid_seed_rejected(), test_logs_distinguish_selection_from_execution_and_omit_seed(), test_non_application_modes_are_inert() (+4 more)

### Community 35 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 36 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 37 - "test_secure_shutdown.py"
Cohesion: 0.14
Nodes (9): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_lifespan_runs_security_cleanup_after_stopping_work(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+1 more)

### Community 38 - "measure_baseline.py"
Cohesion: 0.14
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 39 - "build_aad"
Cohesion: 0.18
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 40 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 41 - "test_sensor.py"
Cohesion: 0.15
Nodes (15): Sensor, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc(), test_payload_has_exact_field_names_and_serialized_values() (+7 more)

### Community 42 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 43 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 44 - "encode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 45 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 46 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 47 - "parse_public_key_response"
Cohesion: 0.16
Nodes (10): validate_public_key(), parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key() (+2 more)

### Community 48 - "test_gateway_crypto_image.py"
Cohesion: 0.14
Nodes (6): test_clean_container_image_runs_when_docker_is_available(), _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 49 - "refresh_graphify.py"
Cohesion: 0.15
Nodes (5): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_script_stores_one_secure_measurement()

### Community 50 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 51 - "queries.py"
Cohesion: 0.18
Nodes (5): public_key(), _unavailable(), _error(), get_measurement(), list_measurements()

### Community 52 - "edge_gateway/validation.py"
Cohesion: 0.15
Nodes (9): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), canonical(), test_domain_bounds_remain_a_separate_stage() (+1 more)

### Community 53 - "CloudDispatch"
Cohesion: 0.14
Nodes (4): CloudDispatch, DispatchMetrics, _Baseline, test_gateway_security_components_share_the_metrics_registry_by_default()

### Community 54 - "edge_gateway/models.py"
Cohesion: 0.17
Nodes (5): _timestamp(), normalize(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 55 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 56 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 57 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 58 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.24
Nodes (7): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement()

### Community 59 - "test_cloud_public_key.py"
Cohesion: 0.22
Nodes (9): secure_app(), test_classical_does_not_generate_keys(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized() (+1 more)

### Community 60 - "test_gateway_baseline_integration.py"
Cohesion: 0.24
Nodes (7): live_baseline_gateway(), live_cloud(), live_service(), test_baseline_client_classifies_real_cloud_failures_without_persisting(), test_baseline_client_preserves_fields_correlation_and_persistence(), test_baseline_e2e_rejections_and_failed_delivery_preserve_sequence_policy(), test_legacy_to_sqlite_preserves_gateway_transformations()

### Community 61 - "test_corrupt_ciphertext_demo.py"
Cohesion: 0.20
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 62 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 63 - "_Clock"
Cohesion: 0.17
Nodes (5): _Clock, handshake_url(), _HandshakeCloud, measurement_url(), _MeasurementCloud

### Community 64 - "fastapi_testclient"
Cohesion: 0.24
Nodes (6): test_cloud_and_secure_delivery_failures_map_to_safe_503(), test_confirmed_cloud_acceptance_maps_to_202(), test_invalid_legacy_input_uses_frozen_client_error_mapping(), test_sequence_rejections_use_frozen_conflict_mapping(), test_unexpected_gateway_failure_maps_to_safe_500(), _Transport

### Community 66 - "sessions.py"
Cohesion: 0.32
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 67 - "pytest"
Cohesion: 0.21
Nodes (5): test_harness_rejects_invalid_sample_count(), _measurement(), test_explicit_utc_offsets_are_preserved(), test_non_finite_numbers_booleans_and_local_timestamps_are_rejected(), test_protocol_example_is_deterministic_utf8_json()

### Community 68 - "test_cloud_mlkem.py"
Cohesion: 0.22
Nodes (4): test_bad_vendor_secret_rejected(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 69 - "test_gateway_correlation.py"
Cohesion: 0.27
Nodes (5): create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 70 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 72 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 73 - "KeyService"
Cohesion: 0.22
Nodes (3): lifespan(), StartupError, KeyService

### Community 75 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 76 - "test_baseline_gateway_measurements"
Cohesion: 0.25
Nodes (4): cloud(), test_baseline_gateway_measurements(), _post(), send()

### Community 77 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 87 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 89 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 764 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `encapsulate`, `json`, `test_gateway_cloud_secure.py`, `test_mode_evaluation.py`, `secure_transport.py`, `KdfError`, `parse_public_key_response`, `test_public_key_client.py`, `CryptoFailureInjector`, `test_corrupt_ciphertext_demo.py`, `CloudDispatch`, `test_session.py`, `SecureSession`, `test_cloud_session_api.py`, `PqcMetrics`, `test_crypto_failures.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `create_app()` connect `load_config` to `sessions.py`, `FailureMode`, `test_gateway_cloud_secure.py`, `measure_baseline.py`, `test_mode_evaluation.py`, `test_cloud_session_api.py`, `KeyService`, `MeasurementRepository`, `cloud_service/app.py`, `SessionManager`, `test_cloud_secure.py`, `test_cloud_public_key.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `SecureTransportError`, `test_mode_evaluation.py`, `test_secure_shutdown.py`, `secure_transport.py`, `edge_gateway/crypto/encoding.py`, `create_app`, `CryptoFailureInjector`, `test_corrupt_ciphertext_demo.py`, `CloudDispatch`, `SessionManager`, `edge_gateway/crypto/symmetric.py`, `SecureSession`, `edge_gateway/crypto/envelope.py`, `PqcMetrics`, `edge_gateway/crypto/aad.py`, `test_crypto_failures.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.055921855921855924 - nodes in this community are weakly interconnected._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._