# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1908 nodes · 4707 edges · 108 communities (71 shown, 37 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 661 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_gateway_cloud_secure.py
- test_secure_message_tamper.py
- LegacyMeasurement
- cli.py
- GatewayClient
- FailureMode
- FailureMode
- make_config
- MeasurementRepository
- test_crypto_failures.py
- measure_baseline.py
- logging
- test_session.py
- create_app
- SecureTransport
- test_secure_transport.py
- edge_gateway/crypto/session.py
- cloud_service/app.py
- derive_session_key
- edge_gateway/crypto/symmetric.py
- PqcMetrics
- secure.py
- CanonicalMeasurement
- test_cloud_secure.py
- load_config
- test_sensor.py
- test_legacy_compatibility.py
- load_config
- test_session_recovery_is_counted
- load_config
- SecureSession
- test_public_key_client.py
- GatewayErrorCode
- test_dispatch.py
- SecureEnvelope
- test_cloud_session_api.py
- test_gateway_validation.py
- CryptoFailureInjector
- validate_measurement
- session_client.py
- encapsulate
- edge_gateway/crypto/mlkem.py
- StoredMeasurement
- SessionManager
- test_cloud_baseline.py
- decode_binary
- plaintext.py
- public_key.py
- DeviceController
- build_aad
- test_cloud_queries.py
- encode_binary
- test_cloud_kdf.py
- edge_gateway/config.py
- secure_transport.py
- CloudDispatch
- Config
- edge_gateway/app.py
- json
- edge_gateway/crypto/aad.py
- test_clean_container_crypto.py
- test_cloud_public_key.py
- refresh_graphify.py
- test_gateway_crypto_image.py
- envelope_validation.py
- sessions.py
- test_cloud_mlkem.py
- test_secure_envelope.py
- keys.py
- _error_response
- .__init__
- _HandshakeHandler
- public_key_client.py
- test_refresh_graphify.py
- Measurement
- pathlib
- FakeResponse
- test_repository_hygiene.py
- get_measurement
- pytest
- test_gateway_config.py
- _Handler
- test_shared_integration_assets.py
- .shutdown
- _Handler
- _Response
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 47 edges
2. `FailureMode` - 44 edges
3. `SecureTransport` - 42 edges
4. `create_app()` - 42 edges
5. `load_config()` - 38 edges
6. `SessionManager` - 37 edges
7. `create_app()` - 36 edges
8. `FailureMode` - 35 edges
9. `FailureInjector` - 34 edges
10. `CloudHarness` - 33 edges

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

## Communities (108 total, 37 thin omitted)

### Community 0 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (31): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+23 more)

### Community 1 - "test_secure_message_tamper.py"
Cohesion: 0.06
Nodes (26): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes() (+18 more)

### Community 2 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (31): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+23 more)

### Community 3 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 4 - "GatewayClient"
Cohesion: 0.08
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 5 - "FailureMode"
Cohesion: 0.11
Nodes (23): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+15 more)

### Community 6 - "FailureMode"
Cohesion: 0.14
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 7 - "make_config"
Cohesion: 0.09
Nodes (18): FakeSensor, make_config(), RaisingClient, RecordingClient, test_client_exception_is_logged_then_loop_continues_and_closes(), test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure() (+10 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.11
Nodes (23): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+15 more)

### Community 9 - "test_crypto_failures.py"
Cohesion: 0.09
Nodes (17): _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud, _plaintext() (+9 more)

### Community 10 - "measure_baseline.py"
Cohesion: 0.09
Nodes (12): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+4 more)

### Community 11 - "logging"
Cohesion: 0.10
Nodes (8): FakeMeasurement, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, RecordingFailureInjector, test_delivery_failure_does_not_stop_loop_or_roll_back_sequence(), test_falsey_injected_dependencies_are_preserved()

### Community 12 - "test_session.py"
Cohesion: 0.10
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 13 - "create_app"
Cohesion: 0.09
Nodes (20): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+12 more)

### Community 14 - "SecureTransport"
Cohesion: 0.14
Nodes (9): _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, SecureAcceptance, SecureTransport, SecureTransportError, log_security() (+1 more)

### Community 15 - "test_secure_transport.py"
Cohesion: 0.17
Nodes (19): _Cloud, _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried() (+11 more)

### Community 16 - "edge_gateway/crypto/session.py"
Cohesion: 0.09
Nodes (6): corrupt_ciphertext_copy(), _Clock, _Cloud, cloud_url(), _Handler, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 17 - "cloud_service/app.py"
Cohesion: 0.13
Nodes (5): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 18 - "derive_session_key"
Cohesion: 0.11
Nodes (12): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+4 more)

### Community 19 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 21 - "secure.py"
Cohesion: 0.11
Nodes (9): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement() (+1 more)

### Community 22 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 23 - "test_cloud_secure.py"
Cohesion: 0.18
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 24 - "load_config"
Cohesion: 0.14
Nodes (17): create_app(), _logging_level(), main(), GatewayConfig, load_config(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests() (+9 more)

### Community 25 - "test_sensor.py"
Cohesion: 0.12
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 26 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 27 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_unrelated_record_id_collision_is_not_idempotent_success() (+9 more)

### Community 28 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (11): _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 29 - "load_config"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 30 - "SecureSession"
Cohesion: 0.12
Nodes (9): SecureSession, _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+1 more)

### Community 31 - "test_public_key_client.py"
Cohesion: 0.15
Nodes (15): _endpoint(), fetch_public_key(), PublicKeyTransportError, _body(), _public_key(), test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable(), test_fetch_does_not_encapsulate() (+7 more)

### Community 32 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 33 - "test_dispatch.py"
Cohesion: 0.18
Nodes (13): _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 34 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 35 - "test_cloud_session_api.py"
Cohesion: 0.13
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 36 - "test_gateway_validation.py"
Cohesion: 0.17
Nodes (17): measurements(), parse_legacy_measurement(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), assert_rejection(), payload(), test_domain_bounds_remain_a_separate_stage(), test_domain_invalid_values_are_422_before_cloud() (+9 more)

### Community 37 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 38 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 39 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 40 - "encapsulate"
Cohesion: 0.15
Nodes (13): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh() (+5 more)

### Community 41 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.13
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 42 - "StoredMeasurement"
Cohesion: 0.16
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 43 - "SessionManager"
Cohesion: 0.16
Nodes (4): SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 44 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 45 - "decode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 46 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 47 - "public_key.py"
Cohesion: 0.20
Nodes (8): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 49 - "build_aad"
Cohesion: 0.26
Nodes (10): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+2 more)

### Community 50 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 51 - "encode_binary"
Cohesion: 0.23
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _different_nonce(), _tamper()

### Community 52 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 53 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 54 - "secure_transport.py"
Cohesion: 0.18
Nodes (6): build_secure_envelope(), SecureEnvelope, _dump(), generate_nonce(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), test_generate_nonce_returns_distinct_12_byte_values()

### Community 55 - "CloudDispatch"
Cohesion: 0.16
Nodes (4): BaselineTransport, CloudDispatch, DispatchMetrics, test_secure_failure_does_not_call_baseline()

### Community 56 - "Config"
Cohesion: 0.21
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 57 - "edge_gateway/app.py"
Cohesion: 0.18
Nodes (4): get_config(), LegacyJSONError, LegacyMeasurementDomainError, _reject_constant()

### Community 58 - "json"
Cohesion: 0.21
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 59 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 60 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 61 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 62 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 63 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 64 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 65 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 66 - "test_cloud_mlkem.py"
Cohesion: 0.22
Nodes (3): test_bad_vendor_secret_rejected(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 67 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 69 - "_error_response"
Cohesion: 0.25
Nodes (8): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response(), _unavailable()

### Community 70 - ".__init__"
Cohesion: 0.22
Nodes (3): _endpoint(), _RetryableTransport, _SessionRecovery

### Community 73 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 79 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 81 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 629 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `CryptoFailureInjector`, `.__init__`, `SessionManager`, `SecureTransport`, `edge_gateway/crypto/session.py`, `secure_transport.py`, `CloudDispatch`, `load_config`, `edge_gateway/app.py`, `test_session_recovery_is_counted`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `FailureMode` connect `FailureMode` to `test_gateway_cloud_secure.py`, `sessions.py`, `cloud_service/app.py`, `secure.py`, `CloudDispatch`, `load_config`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `CloudHarness` connect `test_gateway_cloud_secure.py` to `FailureMode`, `StoredMeasurement`, `SessionManager`, `SecureTransport`, `CloudDispatch`, `test_public_key_client.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_gateway_cloud_secure.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05081585081585081 - nodes in this community are weakly interconnected._