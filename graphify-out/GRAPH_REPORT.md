# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1958 nodes · 4799 edges · 116 communities (73 shown, 43 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 669 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_cloud_secure.py
- test_gateway_cloud_secure.py
- LegacyMeasurement
- cli.py
- GatewayClient
- MeasurementRepository
- FailureMode
- load_config
- json
- SessionManager
- test_sensor.py
- test_crypto_failures.py
- SecureTransportError
- test_session.py
- secure_transport.py
- cloud_service/app.py
- test_device.py
- edge_gateway/crypto/symmetric.py
- secure.py
- CanonicalMeasurement
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- create_app
- CryptoFailureInjector
- test_security_logging.py
- make_config
- test_mode_evaluation.py
- PqcMetrics
- test_dispatch.py
- load_config
- load_config
- GatewayErrorCode
- validate_measurement
- SecureSession
- session_client.py
- edge_gateway/crypto/mlkem.py
- StoredMeasurement
- test_cloud_failure_injection.py
- measure_baseline.py
- FailureMode
- derive_session_key
- test_secure_transport.py
- encapsulate
- SessionManager
- test_cloud_baseline.py
- _Sessions
- test_cloud_kdf.py
- encode_binary
- plaintext.py
- DeviceController
- test_gateway_validation.py
- Config
- test_cloud_config.py
- build_aad
- test_cloud_queries.py
- SecureTransport
- test_permanent_gateway_failures_are_logged_without_retry
- test_cloud_session_api.py
- edge_gateway/validation.py
- KeyService
- edge_gateway/app.py
- test_gateway_correlation.py
- edge_gateway/crypto/aad.py
- test_clean_container_crypto.py
- test_cloud_mlkem.py
- test_cloud_public_key.py
- edge_gateway/crypto/envelope.py
- test_gateway_crypto_image.py
- sessions.py
- clean_container_crypto.py
- test_secure_envelope.py
- test_shutdown_after_gateway_unavailable_delivery
- refresh_graphify.py
- _Clock
- _HandshakeHandler
- KdfError
- test_refresh_graphify.py
- pathlib
- test_public_key.py
- test_repository_hygiene.py
- pytest
- _Handler
- _Handler
- test_shared_integration_assets.py
- BaselineTransport
- _Handler
- _Response
- _Handler
- _Handler
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 47 edges
2. `FailureMode` - 44 edges
3. `SecureTransport` - 43 edges
4. `create_app()` - 43 edges
5. `SessionManager` - 38 edges
6. `load_config()` - 38 edges
7. `create_app()` - 36 edges
8. `FailureMode` - 35 edges
9. `SecureTransportError` - 34 edges
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
- `CloudHarness` --uses--> `FailureMode`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → cloud_service/src/cloud_service/config.py

## Import Cycles
- None detected.

## Communities (116 total, 43 thin omitted)

### Community 0 - "test_cloud_secure.py"
Cohesion: 0.05
Nodes (47): decode_binary(), encode_binary(), EncodingError, EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object() (+39 more)

### Community 1 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 2 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (31): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+23 more)

### Community 3 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 4 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 5 - "MeasurementRepository"
Cohesion: 0.10
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 6 - "FailureMode"
Cohesion: 0.14
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 7 - "load_config"
Cohesion: 0.09
Nodes (27): create_app(), health(), ready(), main(), _unavailable(), ConfigurationError, load_config(), integer() (+19 more)

### Community 8 - "json"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+11 more)

### Community 9 - "SessionManager"
Cohesion: 0.09
Nodes (13): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes() (+5 more)

### Community 10 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 11 - "test_crypto_failures.py"
Cohesion: 0.09
Nodes (16): _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud, _plaintext() (+8 more)

### Community 12 - "SecureTransportError"
Cohesion: 0.11
Nodes (11): _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance, SecureTransportError (+3 more)

### Community 13 - "test_session.py"
Cohesion: 0.11
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 15 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (8): SecurityMode, public_key(), _unavailable(), _error(), get_measurement(), list_measurements(), baseline_measurement(), _error()

### Community 16 - "test_device.py"
Cohesion: 0.12
Nodes (5): FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, test_falsey_injected_dependencies_are_preserved()

### Community 17 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), test_existing_secure_envelope_authenticates_same_request_context(), _aad() (+10 more)

### Community 18 - "secure.py"
Cohesion: 0.11
Nodes (9): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement() (+1 more)

### Community 19 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 20 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 21 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 22 - "create_app"
Cohesion: 0.13
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+10 more)

### Community 23 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (4): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 24 - "test_security_logging.py"
Cohesion: 0.12
Nodes (13): _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_metrics_endpoint_exposes_the_same_registry() (+5 more)

### Community 25 - "make_config"
Cohesion: 0.12
Nodes (13): FakeMeasurement, FakeSensor, make_config(), RaisingClient, RecordingClient, RecordingFailureInjector, test_client_exception_is_logged_then_loop_continues_and_closes(), test_delivery_failure_does_not_stop_loop_or_roll_back_sequence() (+5 more)

### Community 26 - "test_mode_evaluation.py"
Cohesion: 0.12
Nodes (9): _Baseline, _Calls, measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate(), test_injected_crypto_failure_does_not_call_baseline() (+1 more)

### Community 28 - "test_dispatch.py"
Cohesion: 0.18
Nodes (13): _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 29 - "load_config"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 30 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 31 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 32 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 33 - "SecureSession"
Cohesion: 0.11
Nodes (4): SecureSession, SessionEstablishmentError, _session(), get_or_establish()

### Community 34 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 35 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.12
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 36 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 37 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 38 - "measure_baseline.py"
Cohesion: 0.15
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 39 - "FailureMode"
Cohesion: 0.15
Nodes (7): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes()

### Community 40 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 41 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 42 - "encapsulate"
Cohesion: 0.18
Nodes (11): test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+3 more)

### Community 43 - "SessionManager"
Cohesion: 0.13
Nodes (4): lifespan(), SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 44 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 45 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 46 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 47 - "encode_binary"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 48 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 50 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 51 - "Config"
Cohesion: 0.19
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 52 - "test_cloud_config.py"
Cohesion: 0.17
Nodes (10): Config, test_custom_environment(), test_defaults_do_not_create_database(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries(), test_invalid_configuration(), test_invalid_database_url(), test_process_environment_and_explicit_mapping() (+2 more)

### Community 53 - "build_aad"
Cohesion: 0.26
Nodes (10): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+2 more)

### Community 54 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 55 - "SecureTransport"
Cohesion: 0.17
Nodes (5): _endpoint(), SecureTransport, CloudDispatch, DispatchMetrics, _dispatch()

### Community 56 - "test_permanent_gateway_failures_are_logged_without_retry"
Cohesion: 0.17
Nodes (6): FakeResponse, ScriptedOpener, test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure(), stop_after_first_measurement()

### Community 57 - "test_cloud_session_api.py"
Cohesion: 0.23
Nodes (9): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), test_shutdown_and_classical_mode() (+1 more)

### Community 58 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 59 - "KeyService"
Cohesion: 0.15
Nodes (5): lifespan(), StartupError, KeyService, fail(), test_session_initialization_failure_releases_keys()

### Community 60 - "edge_gateway/app.py"
Cohesion: 0.19
Nodes (6): get_config(), _logging_level(), main(), GatewayConfig, test_cli_uses_configured_server_settings_and_loads_once(), settings()

### Community 61 - "test_gateway_correlation.py"
Cohesion: 0.22
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 62 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 63 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 64 - "test_cloud_mlkem.py"
Cohesion: 0.20
Nodes (4): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 65 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 66 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.20
Nodes (5): main(), build_secure_envelope(), SecureEnvelope, generate_nonce(), test_generate_nonce_returns_distinct_12_byte_values()

### Community 67 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 68 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 70 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 71 - "test_shutdown_after_gateway_unavailable_delivery"
Cohesion: 0.22
Nodes (4): test_shutdown_after_gateway_unavailable_delivery(), test_sigint_stops_after_delivery_and_restores_handlers(), test_sigterm_stops_during_wait_and_logs_shutdown(), fake_signal()

### Community 72 - "refresh_graphify.py"
Cohesion: 0.27
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 73 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 75 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 76 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 78 - "test_public_key.py"
Cohesion: 0.48
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 659 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `SecureSession`, `session_client.py`, `test_gateway_cloud_secure.py`, `load_config`, `json`, `encapsulate`, `KdfError`, `test_crypto_failures.py`, `test_session.py`, `secure_transport.py`, `SecureTransport`, `test_secure_message_tamper.py`, `CryptoFailureInjector`, `test_security_logging.py`, `PqcMetrics`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `SessionManager`, `secure_transport.py`, `CryptoFailureInjector`, `create_app`, `SecureTransport`, `test_security_logging.py`, `edge_gateway/app.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `SecureTransportError` connect `SecureTransportError` to `test_gateway_cloud_secure.py`, `test_secure_transport.py`, `_Sessions`, `secure_transport.py`, `SecureTransport`, `CryptoFailureInjector`, `test_security_logging.py`, `test_mode_evaluation.py`, `test_dispatch.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_cloud_secure.py` be split into smaller, more focused modules?**
  _Cohesion score 0.051791629027401385 - nodes in this community are weakly interconnected._