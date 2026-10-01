# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1913 nodes · 4712 edges · 99 communities (67 shown, 32 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 661 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- test_gateway_cloud_secure.py
- test_session.py
- LegacyMeasurement
- cli.py
- test_cloud_secure.py
- GatewayClient
- FailureMode
- SecureTransport
- SessionManager
- secure_transport.py
- create_app
- MeasurementRepository
- test_sensor.py
- test_public_key_client.py
- test_crypto_failures.py
- encapsulate
- test_secure_transport.py
- cloud_service/app.py
- SecureSession
- edge_gateway/crypto/symmetric.py
- test_dispatch.py
- CanonicalMeasurement
- PqcMetrics
- load_config
- SessionManager
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- datetime
- encode_binary
- GatewayErrorCode
- SecureEnvelope
- CryptoFailureInjector
- measure_baseline.py
- validate_measurement
- load_config
- secure.py
- test_cloud_session_api.py
- test_secure_shutdown.py
- build_aad
- edge_gateway/crypto/envelope.py
- test_cloud_baseline.py
- edge_gateway/validation.py
- test_cloud_mlkem.py
- test_gateway_validation.py
- test_cloud_queries.py
- cloud_service/crypto/mlkem.py
- test_cloud_kdf.py
- edge_gateway/config.py
- test_gateway_correlation.py
- derive_session_key
- parse_public_key_response
- edge_gateway/crypto/aad.py
- pathlib
- test_clean_container_crypto.py
- test_cloud_public_key.py
- clean_container_crypto.py
- refresh_graphify.py
- test_gateway_crypto_image.py
- envelope_validation.py
- sessions.py
- test_secure_envelope.py
- edge_gateway/app.py
- _error_response
- _Clock
- edge_gateway/crypto/kdf.py
- .__init__
- _HandshakeHandler
- test_refresh_graphify.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- get_measurement
- pytest
- test_gateway_config.py
- _Handler
- test_shared_integration_assets.py
- _Handler
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
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `_receive()` --uses--> `SessionAccessError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → cloud_service/src/cloud_service/crypto/session.py
- `_establish()` --uses--> `SessionManager`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → cloud_service/src/cloud_service/crypto/session.py

## Import Cycles
- None detected.

## Communities (99 total, 32 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.06
Nodes (30): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+22 more)

### Community 3 - "test_session.py"
Cohesion: 0.06
Nodes (25): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+17 more)

### Community 4 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (30): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+22 more)

### Community 5 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 6 - "test_cloud_secure.py"
Cohesion: 0.10
Nodes (31): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet(), canonical() (+23 more)

### Community 7 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 8 - "FailureMode"
Cohesion: 0.11
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 9 - "SecureTransport"
Cohesion: 0.09
Nodes (14): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport (+6 more)

### Community 10 - "SessionManager"
Cohesion: 0.09
Nodes (13): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), clock(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes() (+5 more)

### Community 12 - "create_app"
Cohesion: 0.07
Nodes (21): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), KeyService (+13 more)

### Community 13 - "MeasurementRepository"
Cohesion: 0.11
Nodes (23): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+15 more)

### Community 14 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 15 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+10 more)

### Community 16 - "test_crypto_failures.py"
Cohesion: 0.09
Nodes (18): _aad(), _Clock, handshake_url(), _injector(), measurement_url(), _MeasurementCloud, _plaintext(), _Sessions (+10 more)

### Community 17 - "encapsulate"
Cohesion: 0.11
Nodes (13): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+5 more)

### Community 18 - "test_secure_transport.py"
Cohesion: 0.17
Nodes (19): _Cloud, _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried() (+11 more)

### Community 19 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (5): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 20 - "SecureSession"
Cohesion: 0.09
Nodes (12): _Sessions, SecureSession, _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key() (+4 more)

### Community 21 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 22 - "test_dispatch.py"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 23 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 24 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 25 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_unrelated_record_id_collision_is_not_idempotent_success() (+9 more)

### Community 26 - "SessionManager"
Cohesion: 0.10
Nodes (3): lifespan(), SessionEstablishmentError, SessionManager

### Community 27 - "test_legacy_compatibility.py"
Cohesion: 0.14
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 28 - "test_secure_message_tamper.py"
Cohesion: 0.15
Nodes (12): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+4 more)

### Community 29 - "datetime"
Cohesion: 0.12
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 30 - "encode_binary"
Cohesion: 0.14
Nodes (11): decode_binary(), encode_binary(), EncodingError, _HandshakeCloud, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip() (+3 more)

### Community 31 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 32 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 33 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 34 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 35 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 36 - "load_config"
Cohesion: 0.17
Nodes (13): create_app(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration() (+5 more)

### Community 37 - "secure.py"
Cohesion: 0.15
Nodes (7): AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement(), fail()

### Community 38 - "test_cloud_session_api.py"
Cohesion: 0.16
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 39 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 40 - "build_aad"
Cohesion: 0.21
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 41 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.19
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 42 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 43 - "edge_gateway/validation.py"
Cohesion: 0.16
Nodes (9): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage() (+1 more)

### Community 44 - "test_cloud_mlkem.py"
Cohesion: 0.14
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 45 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 46 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 47 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 48 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 49 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 50 - "test_gateway_correlation.py"
Cohesion: 0.19
Nodes (7): baseline_headers(), create_request_id(), build_secure_envelope(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 51 - "derive_session_key"
Cohesion: 0.20
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 52 - "parse_public_key_response"
Cohesion: 0.23
Nodes (8): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), reject_public_key()

### Community 53 - "edge_gateway/crypto/aad.py"
Cohesion: 0.21
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 55 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 56 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 57 - "clean_container_crypto.py"
Cohesion: 0.23
Nodes (3): _install(), main(), _serve()

### Community 58 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 59 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 60 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 61 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 62 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 63 - "edge_gateway/app.py"
Cohesion: 0.27
Nodes (4): get_config(), _logging_level(), main(), GatewayConfig

### Community 64 - "_error_response"
Cohesion: 0.22
Nodes (9): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready(), _error_response() (+1 more)

### Community 65 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 69 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 72 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 74 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 633 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `CryptoFailureInjector`, `.__init__`, `load_config`, `SecureTransport`, `secure_transport.py`, `SecureSession`, `test_dispatch.py`, `SessionManager`, `edge_gateway/app.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `CryptoFailureInjector`, `test_gateway_cloud_secure.py`, `test_session.py`, `load_config`, `test_cloud_session_api.py`, `secure_transport.py`, `test_public_key_client.py`, `test_crypto_failures.py`, `encapsulate`, `derive_session_key`, `parse_public_key_response`, `SecureSession`, `PqcMetrics`, `clean_container_crypto.py`, `test_secure_message_tamper.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `SecureTransport`, `secure_transport.py`, `test_crypto_failures.py`, `SecureSession`, `SessionManager`, `edge_gateway/app.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.05720122574055159 - nodes in this community are weakly interconnected._