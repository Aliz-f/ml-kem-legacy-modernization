# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1517 nodes · 3718 edges · 69 communities (49 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 509 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- LegacyMeasurement
- test_secure_transport.py
- FailureMode
- secure.py
- test_session.py
- test_cloud_secure.py
- test_client.py
- test_sensor.py
- SessionManager
- test_failure_injection.py
- create_app
- MeasurementRepository
- test_public_key_client.py
- load_config
- decrypt
- measure_baseline.py
- secure_transport.py
- PqcMetrics
- edge_gateway/crypto/session.py
- CryptoFailureInjector
- repository.py
- SecureTransport
- SecureSession
- GatewayErrorCode
- CanonicalMeasurement
- load_config
- test_security_logging.py
- test_cloud_session_api.py
- cloud_service/app.py
- build_aad
- SessionManager
- validate_measurement
- test_cloud_baseline.py
- test_cloud_mlkem.py
- create_app
- plaintext.py
- test_cloud_kdf.py
- test_cloud_queries.py
- edge_gateway/app.py
- cloud_service/crypto/mlkem.py
- _fixture
- json
- pytest
- refresh_graphify.py
- test_cloud_public_key.py
- test_gateway_correlation.py
- dispatch.py
- test_gateway_app.py
- sessions.py
- test_envelope.py
- _HandshakeHandler
- test_repository_hygiene.py
- get_measurement
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 43 edges
2. `SecureTransport` - 36 edges
3. `create_app()` - 36 edges
4. `load_config()` - 35 edges
5. `create_app()` - 34 edges
6. `FailureMode` - 33 edges
7. `MeasurementRepository` - 32 edges
8. `PqcMetrics` - 32 edges
9. `FailureInjector` - 31 edges
10. `SessionManager` - 31 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_exact_protocol_fields_and_json_serialization()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_canonical_model.py → cloud_service/tests/test_cloud_aead.py

## Import Cycles
- None detected.

## Communities (69 total, 20 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (44): test_harness_rejects_invalid_sample_count(), main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details() (+36 more)

### Community 1 - "LegacyMeasurement"
Cohesion: 0.06
Nodes (46): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), parse_legacy_measurement(), _reject_constant() (+38 more)

### Community 2 - "test_secure_transport.py"
Cohesion: 0.06
Nodes (38): _error_code(), _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransportError, _SessionRecovery, CloudDispatch, _Baseline (+30 more)

### Community 3 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 4 - "secure.py"
Cohesion: 0.07
Nodes (24): AadError, build_aad(), EnvelopeSchemaError, SecureEnvelope, _binary(), _constant(), EnvelopeValidationError, _object() (+16 more)

### Community 5 - "test_session.py"
Cohesion: 0.06
Nodes (23): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+15 more)

### Community 6 - "test_cloud_secure.py"
Cohesion: 0.07
Nodes (31): KdfError, canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable() (+23 more)

### Community 7 - "test_client.py"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 8 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 9 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 10 - "test_failure_injection.py"
Cohesion: 0.09
Nodes (19): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud (+11 more)

### Community 11 - "create_app"
Cohesion: 0.08
Nodes (18): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), KeyService (+10 more)

### Community 12 - "MeasurementRepository"
Cohesion: 0.12
Nodes (21): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+13 more)

### Community 13 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+10 more)

### Community 14 - "load_config"
Cohesion: 0.14
Nodes (18): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+10 more)

### Community 15 - "decrypt"
Cohesion: 0.21
Nodes (18): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), test_existing_secure_envelope_authenticates_same_request_context(), _aad() (+10 more)

### Community 16 - "measure_baseline.py"
Cohesion: 0.11
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 17 - "secure_transport.py"
Cohesion: 0.14
Nodes (9): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), SecureEnvelope, _dump(), test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally() (+1 more)

### Community 19 - "edge_gateway/crypto/session.py"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 20 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (5): CryptoFailureInjector, _endpoint(), test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 21 - "repository.py"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 22 - "SecureTransport"
Cohesion: 0.13
Nodes (6): corrupt_ciphertext_copy(), _Measurement, _RejectRedirect, SecureTransport, log_security(), _token()

### Community 23 - "SecureSession"
Cohesion: 0.11
Nodes (10): _Sessions, SecureSession, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted() (+2 more)

### Community 24 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 25 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 26 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 27 - "test_security_logging.py"
Cohesion: 0.11
Nodes (7): _Baseline, _Clock, _Cloud, cloud_url(), _Handler, test_injected_handshake_failure_stays_fail_closed(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 28 - "test_cloud_session_api.py"
Cohesion: 0.15
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 29 - "cloud_service/app.py"
Cohesion: 0.16
Nodes (4): public_key(), _unavailable(), baseline_measurement(), _error()

### Community 30 - "build_aad"
Cohesion: 0.18
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 32 - "validate_measurement"
Cohesion: 0.21
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 33 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 34 - "test_cloud_mlkem.py"
Cohesion: 0.14
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 35 - "create_app"
Cohesion: 0.16
Nodes (13): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+5 more)

### Community 36 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 37 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 38 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 39 - "edge_gateway/app.py"
Cohesion: 0.16
Nodes (6): get_config(), _logging_level(), main(), GatewayConfig, LegacyJSONError, LegacyMeasurementDomainError

### Community 40 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 41 - "_fixture"
Cohesion: 0.15
Nodes (10): payload(), client(), database(), measurement(), payload(), cloud(), payload(), payload() (+2 more)

### Community 42 - "json"
Cohesion: 0.20
Nodes (6): AadError, _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 43 - "pytest"
Cohesion: 0.23
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 44 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 45 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 46 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 48 - "test_gateway_app.py"
Cohesion: 0.18
Nodes (8): test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration(), test_settings_dependency_can_be_overridden_and_isolated(), test_shutdown_runs_on_exception()

### Community 49 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 50 - "test_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 53 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 474 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `test_secure_transport.py`, `create_app`, `edge_gateway/app.py`, `dispatch.py`, `secure_transport.py`, `edge_gateway/crypto/session.py`, `CryptoFailureInjector`, `SecureTransport`, `SecureSession`, `test_security_logging.py`, `SessionManager`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `log_security()` connect `SecureTransport` to `test_secure_transport.py`, `dispatch.py`, `secure_transport.py`, `edge_gateway/crypto/session.py`, `SecureSession`, `SessionManager`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `edge_gateway/app.py`, `test_failure_injection.py`, `secure_transport.py`, `edge_gateway/crypto/session.py`, `SecureTransport`, `test_security_logging.py`, `SessionManager`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05576707726763718 - nodes in this community are weakly interconnected._