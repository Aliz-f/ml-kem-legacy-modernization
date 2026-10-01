# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1803 nodes · 4455 edges · 92 communities (60 shown, 32 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 610 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_secure_message_tamper.py
- test_gateway_cloud_secure.py
- test_cloud_secure.py
- LegacyMeasurement
- test_session.py
- cli.py
- test_crypto_failures.py
- FailureMode
- cloud_service/app.py
- edge_gateway/crypto/session.py
- test_sensor.py
- SessionManager
- MeasurementRepository
- SecureTransport
- dataclasses
- GatewayClient
- test_cloud_mlkem.py
- test_security_logging.py
- create_app
- test_dispatch.py
- derive_session_key
- CanonicalMeasurement
- edge_gateway/crypto/symmetric.py
- PqcMetrics
- load_config
- create_app
- datetime
- encapsulate
- SessionManager
- GatewayErrorCode
- load_config
- CryptoFailureInjector
- test_secure_transport.py
- test_cloud_session_api.py
- validate_measurement
- secure_transport.py
- measure_baseline.py
- test_legacy_compatibility.py
- SecureSession
- test_cloud_baseline.py
- test_cloud_queries.py
- plaintext.py
- test_gateway_validation.py
- build_aad
- cloud_service/crypto/mlkem.py
- edge_gateway/validation.py
- test_gateway_correlation.py
- json
- clean_container_crypto.py
- edge_gateway/app.py
- test_gateway_crypto_image.py
- test_cloud_public_key.py
- dispatch.py
- test_secure_envelope.py
- test_clean_container_crypto.py
- sessions.py
- refresh_graphify.py
- client.py
- _DroppedResponse
- pytest
- test_public_key.py
- .send
- test_refresh_graphify.py
- test_repository_hygiene.py
- get_measurement
- _Gateway
- test_shared_integration_assets.py
- _Handler
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
3. `SecureTransport` - 42 edges
4. `create_app()` - 42 edges
5. `load_config()` - 38 edges
6. `SessionManager` - 37 edges
7. `create_app()` - 36 edges
8. `FailureMode` - 33 edges
9. `SecureTransportError` - 33 edges
10. `CloudHarness` - 33 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `PublicKeyRejected`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/public_key.py

## Import Cycles
- None detected.

## Communities (92 total, 32 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 1 - "test_secure_message_tamper.py"
Cohesion: 0.05
Nodes (34): AadError, build_aad(), decode_binary(), encode_binary(), EncodingError, _endpoint(), _parse_expires_at(), parse_session_response() (+26 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 3 - "test_cloud_secure.py"
Cohesion: 0.06
Nodes (37): decode_binary(), encode_binary(), EncodingError, KeyService, AeadError, decrypt(), _decode_ciphertext(), test_binary_round_trip_padded_and_unpadded() (+29 more)

### Community 4 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (31): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+23 more)

### Community 5 - "test_session.py"
Cohesion: 0.05
Nodes (23): SessionState, _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+15 more)

### Community 6 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 7 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (21): _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url(), _MeasurementCloud (+13 more)

### Community 8 - "FailureMode"
Cohesion: 0.11
Nodes (23): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+15 more)

### Community 9 - "cloud_service/app.py"
Cohesion: 0.10
Nodes (8): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error(), _error(), _ingest(), secure_measurement()

### Community 10 - "edge_gateway/crypto/session.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+11 more)

### Community 11 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 12 - "SessionManager"
Cohesion: 0.09
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 13 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 14 - "SecureTransport"
Cohesion: 0.10
Nodes (11): lifespan(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+3 more)

### Community 15 - "dataclasses"
Cohesion: 0.11
Nodes (16): EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope (+8 more)

### Community 16 - "GatewayClient"
Cohesion: 0.15
Nodes (18): GatewayClient, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability(), opener(), test_invalid_retry_counts_are_rejected() (+10 more)

### Community 17 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (10): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent() (+2 more)

### Community 18 - "test_security_logging.py"
Cohesion: 0.09
Nodes (13): _Baseline, _Clock, _Cloud, cloud_url(), _Handler, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings() (+5 more)

### Community 19 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+10 more)

### Community 20 - "test_dispatch.py"
Cohesion: 0.15
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 21 - "derive_session_key"
Cohesion: 0.11
Nodes (12): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+4 more)

### Community 22 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 23 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 25 - "load_config"
Cohesion: 0.16
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 26 - "create_app"
Cohesion: 0.13
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+10 more)

### Community 27 - "datetime"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 28 - "encapsulate"
Cohesion: 0.15
Nodes (11): main(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+3 more)

### Community 29 - "SessionManager"
Cohesion: 0.14
Nodes (4): log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 30 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 31 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 32 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 33 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (17): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+9 more)

### Community 34 - "test_cloud_session_api.py"
Cohesion: 0.14
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 35 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 36 - "secure_transport.py"
Cohesion: 0.13
Nodes (6): build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), generate_nonce(), test_generate_nonce_returns_distinct_12_byte_values()

### Community 37 - "measure_baseline.py"
Cohesion: 0.14
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 38 - "test_legacy_compatibility.py"
Cohesion: 0.19
Nodes (13): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), PostedRequest, _recording_opener(), opener(), _send() (+5 more)

### Community 39 - "SecureSession"
Cohesion: 0.13
Nodes (6): _Sessions, SecureSession, test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 40 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 41 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 42 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 43 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 44 - "build_aad"
Cohesion: 0.26
Nodes (10): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+2 more)

### Community 45 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 46 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 47 - "test_gateway_correlation.py"
Cohesion: 0.21
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 48 - "json"
Cohesion: 0.20
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 49 - "clean_container_crypto.py"
Cohesion: 0.21
Nodes (3): _install(), main(), _serve()

### Community 50 - "edge_gateway/app.py"
Cohesion: 0.19
Nodes (6): get_config(), _logging_level(), main(), GatewayConfig, test_cli_uses_configured_server_settings_and_loads_once(), settings()

### Community 51 - "test_gateway_crypto_image.py"
Cohesion: 0.22
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 52 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 55 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 56 - "test_clean_container_crypto.py"
Cohesion: 0.18
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 57 - "sessions.py"
Cohesion: 0.40
Nodes (5): derive_session_key(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 58 - "refresh_graphify.py"
Cohesion: 0.31
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 60 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 62 - "test_public_key.py"
Cohesion: 0.48
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 64 - "test_refresh_graphify.py"
Cohesion: 0.43
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 66 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 585 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `secure_transport.py`, `test_crypto_failures.py`, `edge_gateway/crypto/session.py`, `SecureTransport`, `edge_gateway/app.py`, `test_security_logging.py`, `SessionManager`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `CryptoFailureInjector`, `secure_transport.py`, `SecureSession`, `edge_gateway/crypto/session.py`, `SecureTransport`, `edge_gateway/app.py`, `test_security_logging.py`, `test_dispatch.py`, `dispatch.py`, `create_app`, `SessionManager`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `CryptoFailureInjector`, `test_secure_message_tamper.py`, `test_secure_transport.py`, `test_gateway_cloud_secure.py`, `secure_transport.py`, `test_session.py`, `SecureSession`, `test_crypto_failures.py`, `plaintext.py`, `json`, `clean_container_crypto.py`, `test_security_logging.py`, `test_dispatch.py`, `dispatch.py`, `edge_gateway/crypto/symmetric.py`, `PqcMetrics`, `SessionManager`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._