# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1928 nodes · 4727 edges · 107 communities (65 shown, 42 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 661 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- edge_gateway/crypto/symmetric.py
- test_cloud_secure.py
- test_legacy_compatibility.py
- test_secure_transport.py
- test_gateway_cloud_secure.py
- cli.py
- test_cloud_session_api.py
- test_device.py
- measure_baseline.py
- FailureMode
- SecureTransport
- datetime
- test_public_key_client.py
- FailureMode
- secure_transport.py
- MeasurementRepository
- cloud_service/app.py
- create_app
- CanonicalMeasurement
- SessionManager
- test_dispatch.py
- PqcMetrics
- test_session_recovery_is_counted
- LegacyMeasurement
- load_config
- load_config
- GatewayErrorCode
- StoredMeasurement
- encode_binary
- test_secure_message_tamper.py
- test_cloud_baseline.py
- validate_measurement
- device.py
- session_client.py
- test_gateway_canonical_model.py
- derive_session_key
- encapsulate
- create_app
- CloudDispatch
- json
- _Sessions
- DeviceController
- secure.py
- test_cloud_queries.py
- parse_public_key_response
- cloud_service/crypto/mlkem.py
- edge_gateway/config.py
- test_gateway_validation.py
- test_cloud_kdf.py
- load_config
- CryptoFailureInjector
- StorageError
- test_crypto_failures.py
- pathlib
- test_clean_container_crypto.py
- test_cloud_public_key.py
- refresh_graphify.py
- test_gateway_crypto_image.py
- sessions.py
- test_cloud_mlkem.py
- logging
- normalize
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- keys.py
- edge_gateway/app.py
- _HandshakeHandler
- _DroppedResponse
- KdfError
- test_refresh_graphify.py
- FakeResponse
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- pytest
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- test_gateway_config.py
- _Handler
- test_shared_integration_assets.py
- test_session_missing_and_expired_force_a_new_handshake
- edge_gateway/models.py
- _Handler
- .send
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
10. `SecureTransportError` - 33 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/aad.py

## Import Cycles
- None detected.

## Communities (107 total, 42 thin omitted)

### Community 0 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.06
Nodes (50): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+42 more)

### Community 1 - "test_cloud_secure.py"
Cohesion: 0.05
Nodes (47): decode_binary(), encode_binary(), EncodingError, EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object() (+39 more)

### Community 2 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (36): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+28 more)

### Community 3 - "test_secure_transport.py"
Cohesion: 0.06
Nodes (35): SessionEstablishmentError, SessionState, _Cloud, _error(), _Handler, _send(), _session(), _Sessions (+27 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 5 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 6 - "test_cloud_session_api.py"
Cohesion: 0.07
Nodes (23): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), client(), handshake(), test_expiry_http_mapping_and_replacement() (+15 more)

### Community 7 - "test_device.py"
Cohesion: 0.08
Nodes (25): FakeMeasurement, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, make_config(), RaisingClient (+17 more)

### Community 8 - "measure_baseline.py"
Cohesion: 0.06
Nodes (22): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+14 more)

### Community 9 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 10 - "SecureTransport"
Cohesion: 0.09
Nodes (12): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+4 more)

### Community 11 - "datetime"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 12 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (17): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), _public_key() (+9 more)

### Community 13 - "FailureMode"
Cohesion: 0.15
Nodes (22): FailureMode, FailureInjector, canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage() (+14 more)

### Community 14 - "secure_transport.py"
Cohesion: 0.11
Nodes (5): corrupt_ciphertext_copy(), _Clock, _Cloud, cloud_url(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 15 - "MeasurementRepository"
Cohesion: 0.12
Nodes (23): lifespan(), Database, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement(), test_closed_database_errors_are_safe() (+15 more)

### Community 16 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (6): StartupError, SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 17 - "create_app"
Cohesion: 0.10
Nodes (19): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+11 more)

### Community 18 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 19 - "SessionManager"
Cohesion: 0.11
Nodes (5): lifespan(), _RejectRedirect, log_security(), _token(), SessionManager

### Community 20 - "test_dispatch.py"
Cohesion: 0.15
Nodes (14): _Baseline, cloud(), _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 22 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (12): _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 23 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 24 - "load_config"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 25 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 26 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 27 - "StoredMeasurement"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 28 - "encode_binary"
Cohesion: 0.15
Nodes (10): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip() (+2 more)

### Community 29 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 30 - "test_cloud_baseline.py"
Cohesion: 0.10
Nodes (10): StorageConflictError, payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 31 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 32 - "device.py"
Cohesion: 0.14
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 33 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 34 - "test_gateway_canonical_model.py"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 35 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 36 - "encapsulate"
Cohesion: 0.17
Nodes (12): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+4 more)

### Community 37 - "create_app"
Cohesion: 0.15
Nodes (13): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+5 more)

### Community 38 - "CloudDispatch"
Cohesion: 0.15
Nodes (4): GatewayConfig, BaselineTransport, CloudDispatch, DispatchMetrics

### Community 39 - "json"
Cohesion: 0.16
Nodes (8): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 40 - "_Sessions"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 42 - "secure.py"
Cohesion: 0.21
Nodes (6): AeadError, decrypt(), _error(), _ingest(), secure_measurement(), fail()

### Community 43 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 44 - "parse_public_key_response"
Cohesion: 0.18
Nodes (9): validate_public_key(), parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 45 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 46 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 47 - "test_gateway_validation.py"
Cohesion: 0.27
Nodes (11): assert_rejection(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400(), test_missing_required_fields_are_422() (+3 more)

### Community 48 - "test_cloud_kdf.py"
Cohesion: 0.16
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 49 - "load_config"
Cohesion: 0.22
Nodes (10): load_config(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration() (+2 more)

### Community 51 - "StorageError"
Cohesion: 0.26
Nodes (4): _error(), get_measurement(), list_measurements(), StorageError

### Community 52 - "test_crypto_failures.py"
Cohesion: 0.22
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 54 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 55 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 56 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 57 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 58 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 59 - "test_cloud_mlkem.py"
Cohesion: 0.22
Nodes (3): test_bad_vendor_secret_rejected(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 61 - "normalize"
Cohesion: 0.24
Nodes (4): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input()

### Community 62 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 63 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 65 - "edge_gateway/app.py"
Cohesion: 0.25
Nodes (3): get_config(), _logging_level(), main()

### Community 67 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 68 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 69 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 76 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 90 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 645 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `edge_gateway/app.py`, `create_app`, `CloudDispatch`, `SecureTransport`, `secure_transport.py`, `.__init__`, `SessionManager`, `test_session_recovery_is_counted`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `session_client.py`, `test_secure_transport.py`, `KdfError`, `encapsulate`, `test_gateway_cloud_secure.py`, `measure_baseline.py`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `test_public_key_client.py`, `parse_public_key_response`, `secure_transport.py`, `create_app`, `CryptoFailureInjector`, `.__init__`, `test_crypto_failures.py`, `PqcMetrics`, `test_session_recovery_is_counted`, `test_session_missing_and_expired_force_a_new_handshake`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `SessionState` connect `test_secure_transport.py` to `test_gateway_cloud_secure.py`, `_Sessions`, `secure_transport.py`, `test_dispatch.py`, `test_session_recovery_is_counted`, `test_session_missing_and_expired_force_a_new_handshake`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `edge_gateway/crypto/symmetric.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05742296918767507 - nodes in this community are weakly interconnected._