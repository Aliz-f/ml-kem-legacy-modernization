# Graph Report - ml-kem-legacy-modernization  (2026-10-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1676 nodes · 4061 edges · 89 communities (59 shown, 30 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 533 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- LegacyMeasurement
- test_legacy_compatibility.py
- FailureMode
- test_secure_message_tamper.py
- test_session.py
- cli.py
- measure_baseline.py
- test_crypto_failures.py
- MeasurementRepository
- secure_transport.py
- test_sensor.py
- edge_gateway/crypto/session.py
- test_dispatch.py
- test_secure_transport.py
- test_security_logging.py
- PqcMetrics
- decrypt
- load_config
- CanonicalMeasurement
- test_cloud_public_key.py
- SessionManager
- GatewayErrorCode
- cloud_service/app.py
- datetime
- load_config
- validate_measurement
- encapsulate
- CryptoFailureInjector
- create_app
- test_cloud_session_api.py
- dispatch.py
- session_client.py
- build_aad
- test_cloud_baseline.py
- Policy
- SecureSession
- decode_binary
- test_cloud_queries.py
- parse_public_key_response
- test_cloud_kdf.py
- test_cloud_mlkem.py
- edge_gateway/app.py
- edge_gateway/config.py
- envelope.py
- test_gateway_cloud_secure.py
- test_gateway_crypto_image.py
- json
- derive_session_key
- pathlib
- pytest
- test_gateway_correlation.py
- refresh_graphify.py
- CloudHarness
- sessions.py
- test_secure_envelope.py
- _error_response
- edge_gateway/crypto/kdf.py
- test_refresh_graphify.py
- test_legacy_values_survive_secure_delivery
- test_repository_hygiene.py
- get_measurement
- test_gateway_config.py
- Clock
- _measurement
- test_valid_encapsulation_matches_shared_secret_and_hkdf
- test_shared_integration_assets.py
- test_crypto_failure_is_classified_and_recorded
- _Handler
- cloud_server
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `SecureTransport` - 42 edges
2. `load_config()` - 42 edges
3. `load_config()` - 38 edges
4. `SessionManager` - 37 edges
5. `create_app()` - 37 edges
6. `create_app()` - 36 edges
7. `FailureMode` - 33 edges
8. `SecureTransportError` - 33 edges
9. `PqcMetrics` - 32 edges
10. `MeasurementRepository` - 32 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_legacy_values_survive_secure_delivery()` --uses--> `Sensor`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → legacy_system/src/legacy_system/sensor.py
- `test_security_mode_preserves_the_legacy_measurement_contract()` --uses--> `Sensor`  [INFERRED]
  tests/integration/test_legacy_compatibility.py → legacy_system/src/legacy_system/sensor.py

## Import Cycles
- None detected.

## Communities (89 total, 30 thin omitted)

### Community 0 - "LegacyMeasurement"
Cohesion: 0.05
Nodes (47): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), parse_legacy_measurement(), _reject_constant() (+39 more)

### Community 1 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (35): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+27 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "test_secure_message_tamper.py"
Cohesion: 0.05
Nodes (26): decapsulate(), generate_keypair(), MlKemError, PrivateKey, SecureSession, SessionAccessError, SessionManager, SessionState (+18 more)

### Community 4 - "test_session.py"
Cohesion: 0.05
Nodes (23): SessionState, _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+15 more)

### Community 5 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 6 - "measure_baseline.py"
Cohesion: 0.06
Nodes (18): AadError, build_aad(), AeadError, decrypt(), canonical(), Capture, distribution(), live_cloud() (+10 more)

### Community 7 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.10
Nodes (25): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database() (+17 more)

### Community 9 - "secure_transport.py"
Cohesion: 0.10
Nodes (12): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport (+4 more)

### Community 10 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 11 - "edge_gateway/crypto/session.py"
Cohesion: 0.11
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, PublicKeyRejected, _body(), _public_key(), test_cloud_url_and_timeout_are_validated() (+8 more)

### Community 12 - "test_dispatch.py"
Cohesion: 0.16
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 13 - "test_secure_transport.py"
Cohesion: 0.17
Nodes (18): _Cloud, _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried() (+10 more)

### Community 14 - "test_security_logging.py"
Cohesion: 0.10
Nodes (12): _Baseline, _Clock, _Cloud, cloud_url(), _Handler, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings() (+4 more)

### Community 16 - "decrypt"
Cohesion: 0.21
Nodes (18): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), test_existing_secure_envelope_authenticates_same_request_context(), _aad() (+10 more)

### Community 17 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+9 more)

### Community 18 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 19 - "test_cloud_public_key.py"
Cohesion: 0.11
Nodes (11): StartupError, KeyService, secure_app(), test_classical_does_not_generate_keys(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail() (+3 more)

### Community 20 - "SessionManager"
Cohesion: 0.13
Nodes (4): lifespan(), log_security(), SessionEstablishmentError, SessionManager

### Community 21 - "GatewayErrorCode"
Cohesion: 0.11
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 22 - "cloud_service/app.py"
Cohesion: 0.16
Nodes (5): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 23 - "datetime"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 24 - "load_config"
Cohesion: 0.14
Nodes (14): create_app(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration() (+6 more)

### Community 25 - "validate_measurement"
Cohesion: 0.17
Nodes (13): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+5 more)

### Community 26 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 27 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 28 - "create_app"
Cohesion: 0.13
Nodes (14): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+6 more)

### Community 29 - "test_cloud_session_api.py"
Cohesion: 0.14
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 30 - "dispatch.py"
Cohesion: 0.11
Nodes (5): GatewayConfig, corrupt_ciphertext_copy(), _token(), BaselineTransport, DispatchMetrics

### Community 31 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 32 - "build_aad"
Cohesion: 0.19
Nodes (13): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+5 more)

### Community 33 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 34 - "Policy"
Cohesion: 0.12
Nodes (8): cloud(), _install(), secure_measurements(), Policy, _reject(), _require_envelope(), SecureRejection, test_production_cloud_app_has_no_secure_measurement_route()

### Community 35 - "SecureSession"
Cohesion: 0.13
Nodes (6): _Sessions, SecureSession, test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 36 - "decode_binary"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 37 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 38 - "parse_public_key_response"
Cohesion: 0.17
Nodes (9): CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 39 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 40 - "test_cloud_mlkem.py"
Cohesion: 0.15
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 41 - "edge_gateway/app.py"
Cohesion: 0.15
Nodes (5): get_config(), _logging_level(), main(), LegacyJSONError, LegacyMeasurementDomainError

### Community 42 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 43 - "envelope.py"
Cohesion: 0.24
Nodes (7): build_secure_envelope(), PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement()

### Community 44 - "test_gateway_cloud_secure.py"
Cohesion: 0.17
Nodes (9): _seal(), test_malformed_mlkem_ciphertext_is_rejected(), test_simulated_decapsulation_failure_leaves_no_session(), test_tampered_secure_message_is_rejected(), test_unsupported_protocol_version_is_rejected(), unreachable(), test_versioned_public_key_retrieval(), test_wrong_gateway_ownership_is_rejected_before_decrypt() (+1 more)

### Community 45 - "test_gateway_crypto_image.py"
Cohesion: 0.18
Nodes (6): test_clean_container_image_runs_when_docker_is_available(), _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 46 - "json"
Cohesion: 0.20
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 47 - "derive_session_key"
Cohesion: 0.22
Nodes (8): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 49 - "pytest"
Cohesion: 0.21
Nodes (5): test_harness_rejects_invalid_sample_count(), _measurement(), test_explicit_utc_offsets_are_preserved(), test_non_finite_numbers_booleans_and_local_timestamps_are_rejected(), test_protocol_example_is_deterministic_utf8_json()

### Community 50 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 51 - "refresh_graphify.py"
Cohesion: 0.24
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 52 - "CloudHarness"
Cohesion: 0.24
Nodes (9): CloudHarness, _deliver(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope(), test_expired_session_returns_409_and_recovers_once(), test_invalid_session_returns_409_and_recovers_once(), test_local_session_expiry_reestablishes_before_the_next_send(), test_secure_envelope_round_trip_stores_canonical_measurement() (+1 more)

### Community 53 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 54 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 55 - "_error_response"
Cohesion: 0.22
Nodes (9): application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready(), _error_response() (+1 more)

### Community 57 - "test_refresh_graphify.py"
Cohesion: 0.38
Nodes (3): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 60 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 61 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 65 - "_measurement"
Cohesion: 0.33
Nodes (5): _measurement(), test_duplicate_sequence_is_stored_once(), send_twice(), test_one_handshake_is_reused_for_three_measurements(), send_three()

### Community 68 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.40
Nodes (3): test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 556 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `secure_transport.py` to `SecureSession`, `decode_binary`, `test_session.py`, `measure_baseline.py`, `test_crypto_failures.py`, `envelope.py`, `test_dispatch.py`, `test_secure_transport.py`, `json`, `PqcMetrics`, `decrypt`, `test_security_logging.py`, `SessionManager`, `CloudHarness`, `CryptoFailureInjector`, `dispatch.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `SecureSession`, `edge_gateway/app.py`, `secure_transport.py`, `edge_gateway/crypto/session.py`, `test_dispatch.py`, `test_security_logging.py`, `SessionManager`, `load_config`, `CryptoFailureInjector`, `dispatch.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `Clock`, `test_session.py`, `test_crypto_failure_is_classified_and_recorded`, `measure_baseline.py`, `test_crypto_failures.py`, `parse_public_key_response`, `secure_transport.py`, `edge_gateway/crypto/session.py`, `test_security_logging.py`, `derive_session_key`, `PqcMetrics`, `CloudHarness`, `encapsulate`, `CryptoFailureInjector`, `test_cloud_session_api.py`, `session_client.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `SessionManager` (e.g. with `test_existing_gateway_session_client_over_real_http()` and `main()`) actually correct?**
  _`SessionManager` has 21 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `LegacyMeasurement` be split into smaller, more focused modules?**
  _Cohesion score 0.05185779203421545 - nodes in this community are weakly interconnected._