# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1902 nodes · 4746 edges · 109 communities (74 shown, 35 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 670 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_gateway_cloud_secure.py
- test_cloud_secure.py
- GatewayClient
- cli.py
- GatewayErrorCode
- FailureMode
- SecureTransport
- load_config
- MeasurementRepository
- SessionManager
- pathlib
- SecureSession
- secure_transport.py
- SessionManager
- test_public_key_client.py
- test_session.py
- test_secure_transport.py
- cloud_service/app.py
- CloudDispatch
- edge_gateway/crypto/symmetric.py
- PqcMetrics
- CanonicalMeasurement
- test_baseline_client.py
- create_app
- LegacyMeasurement
- StoredMeasurement
- SecureEnvelope
- load_config
- test_secure_message_tamper.py
- measure_baseline.py
- test_cloud_public_key.py
- validate_measurement
- edge_gateway/app.py
- json
- session_client.py
- test_gateway_crypto_image.py
- secure.py
- edge_gateway/crypto/envelope.py
- CanonicalMeasurement
- test_secure_shutdown.py
- derive_session_key
- encapsulate
- test_gateway_measurements.py
- build_aad
- test_cloud_session_api.py
- test_sensor.py
- test_legacy_compatibility.py
- test_cloud_baseline.py
- refresh_graphify.py
- encode_binary
- CryptoFailureInjector
- test_gateway_validation.py
- test_cloud_queries.py
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- edge_gateway/validation.py
- pytest
- test_gateway_correlation.py
- parse_public_key_response
- test_cloud_mlkem.py
- edge_gateway/crypto/aad.py
- normalize
- test_crypto_failures.py
- fastapi_testclient
- test_cloud_config.py
- datetime
- validate
- envelope_validation.py
- sessions.py
- test_secure_envelope.py
- clean_container_crypto.py
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- _Clock
- _HandshakeHandler
- Config
- KdfError
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- get_measurement
- _Handler
- _Handler
- _Gateway
- FalseyClock
- test_session_missing_and_expired_force_a_new_handshake
- edge_gateway/models.py
- _Handler
- _Handler
- _Handler
- _Cloud
- test_legacy_sources_do_not_learn_gateway_crypto
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 52 edges
2. `load_config()` - 48 edges
3. `load_config()` - 47 edges
4. `FailureMode` - 44 edges
5. `SecureTransport` - 44 edges
6. `create_app()` - 42 edges
7. `SessionManager` - 37 edges
8. `SecureTransportError` - 36 edges
9. `FailureMode` - 33 edges
10. `CloudHarness` - 33 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `CloudHarness` --uses--> `FailureMode`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → cloud_service/src/cloud_service/config.py
- `CloudHarness` --uses--> `StoredMeasurement`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → cloud_service/src/cloud_service/storage/models.py

## Import Cycles
- None detected.

## Communities (109 total, 35 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 1 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 2 - "test_cloud_secure.py"
Cohesion: 0.10
Nodes (31): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet(), canonical() (+23 more)

### Community 3 - "GatewayClient"
Cohesion: 0.10
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 4 - "cli.py"
Cohesion: 0.18
Nodes (30): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+22 more)

### Community 5 - "GatewayErrorCode"
Cohesion: 0.10
Nodes (14): GatewayError, GatewayErrorCode, MeasurementProcessor, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit() (+6 more)

### Community 6 - "FailureMode"
Cohesion: 0.11
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 7 - "SecureTransport"
Cohesion: 0.09
Nodes (12): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+4 more)

### Community 8 - "load_config"
Cohesion: 0.09
Nodes (27): create_app(), health(), ready(), main(), _unavailable(), ConfigurationError, load_config(), integer() (+19 more)

### Community 9 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+16 more)

### Community 10 - "SessionManager"
Cohesion: 0.10
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 12 - "SecureSession"
Cohesion: 0.08
Nodes (13): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+5 more)

### Community 13 - "secure_transport.py"
Cohesion: 0.13
Nodes (4): corrupt_ciphertext_copy(), _Duration, _RejectRedirect, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 14 - "SessionManager"
Cohesion: 0.10
Nodes (5): lifespan(), log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 15 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (17): _endpoint(), fetch_public_key(), PublicKeyTransportError, PublicKeyRejected, _body(), cloud_server(), _public_key(), _Response (+9 more)

### Community 16 - "test_session.py"
Cohesion: 0.11
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 17 - "test_secure_transport.py"
Cohesion: 0.17
Nodes (19): _Cloud, _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried() (+11 more)

### Community 18 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (5): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 19 - "CloudDispatch"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 20 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 22 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 23 - "test_baseline_client.py"
Cohesion: 0.14
Nodes (15): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _send() (+7 more)

### Community 24 - "create_app"
Cohesion: 0.12
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+10 more)

### Community 25 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 26 - "StoredMeasurement"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 27 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 28 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 29 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 30 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 31 - "test_cloud_public_key.py"
Cohesion: 0.13
Nodes (10): StartupError, KeyService, secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary() (+2 more)

### Community 32 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 33 - "edge_gateway/app.py"
Cohesion: 0.12
Nodes (8): _baseline_transport(), get_config(), _logging_level(), main(), GatewayConfig, BaselineTransport, UnavailableBaseline, test_cli_uses_configured_server_settings_and_loads_once()

### Community 34 - "json"
Cohesion: 0.12
Nodes (3): _RejectRedirect, _RejectRedirect, CloudPublicKey

### Community 35 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 36 - "test_gateway_crypto_image.py"
Cohesion: 0.12
Nodes (7): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 37 - "secure.py"
Cohesion: 0.15
Nodes (7): AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement(), fail()

### Community 38 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.17
Nodes (11): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement() (+3 more)

### Community 39 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 40 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 41 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 42 - "encapsulate"
Cohesion: 0.16
Nodes (12): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+4 more)

### Community 43 - "test_gateway_measurements.py"
Cohesion: 0.17
Nodes (12): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook() (+4 more)

### Community 44 - "build_aad"
Cohesion: 0.21
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 45 - "test_cloud_session_api.py"
Cohesion: 0.17
Nodes (11): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail() (+3 more)

### Community 46 - "test_sensor.py"
Cohesion: 0.18
Nodes (15): Sensor, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc(), test_payload_has_exact_field_names_and_serialized_values() (+7 more)

### Community 47 - "test_legacy_compatibility.py"
Cohesion: 0.22
Nodes (12): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+4 more)

### Community 48 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 49 - "refresh_graphify.py"
Cohesion: 0.14
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 50 - "encode_binary"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 51 - "CryptoFailureInjector"
Cohesion: 0.15
Nodes (3): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings()

### Community 52 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 53 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 54 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 55 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 56 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 57 - "pytest"
Cohesion: 0.18
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 58 - "test_gateway_correlation.py"
Cohesion: 0.21
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 59 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 60 - "test_cloud_mlkem.py"
Cohesion: 0.18
Nodes (4): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 61 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 62 - "normalize"
Cohesion: 0.22
Nodes (5): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 63 - "test_crypto_failures.py"
Cohesion: 0.22
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 64 - "fastapi_testclient"
Cohesion: 0.19
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 65 - "test_cloud_config.py"
Cohesion: 0.24
Nodes (9): test_custom_environment(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries(), test_invalid_configuration(), test_invalid_database_url(), test_process_environment_and_explicit_mapping(), test_sqlite_paths() (+1 more)

### Community 67 - "validate"
Cohesion: 0.39
Nodes (10): validate(), run(), start(), test_cannot_start_while_active_or_corrupt_state(), test_first_id_slug_and_multiline_prompt(), test_full_acceptance_lifecycle(), test_modified_requires_changes_and_revision_preserves_rounds(), test_rejection_and_second_task() (+2 more)

### Community 68 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 69 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 70 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 72 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 73 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 74 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 77 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 80 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 87 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 621 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `edge_gateway/app.py`, `SecureTransport`, `SecureSession`, `secure_transport.py`, `SessionManager`, `test_crypto_failures.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `edge_gateway/app.py`, `SecureTransport`, `SecureSession`, `secure_transport.py`, `SessionManager`, `CloudDispatch`, `create_app`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_gateway_cloud_secure.py`, `session_client.py`, `SecureTransport`, `load_config`, `encapsulate`, `SecureSession`, `KdfError`, `secure_transport.py`, `test_public_key_client.py`, `test_session.py`, `CryptoFailureInjector`, `PqcMetrics`, `test_session_missing_and_expired_force_a_new_handshake`, `parse_public_key_response`, `test_crypto_failures.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.07191780821917808 - nodes in this community are weakly interconnected._