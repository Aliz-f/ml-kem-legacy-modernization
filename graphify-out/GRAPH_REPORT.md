# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1456 nodes · 3512 edges · 75 communities (54 shown, 21 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 468 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- LegacyMeasurement
- FailureMode
- test_session.py
- test_client.py
- load_config
- test_dispatch.py
- derive_session_key
- MeasurementRepository
- SecureTransport
- test_sensor.py
- secure_transport.py
- SessionManager
- test_failure_injection.py
- SecureSession
- decrypt
- PqcMetrics
- SessionManager
- measure_baseline.py
- cloud_service/app.py
- CanonicalMeasurement
- test_public_key_client.py
- GatewayErrorCode
- repository.py
- CryptoFailureInjector
- test_secure_transport.py
- test_cloud_mlkem.py
- test_cloud_session_api.py
- validate_measurement
- encapsulate
- cloud_service/config.py
- test_cloud_baseline.py
- _fixture
- create_app
- load_config
- plaintext.py
- test_cloud_kdf.py
- test_cloud_queries.py
- encoding.py
- edge_gateway/config.py
- build_aad
- test_cloud_aead.py
- test_gateway_correlation.py
- refresh_graphify.py
- MlKemError
- test_cloud_public_key.py
- parse_public_key_response
- public_key_client.py
- test_envelope.py
- _Clock
- _HandshakeHandler
- cloud_service/crypto/symmetric.py
- json
- pytest
- envelope.py
- test_repository_hygiene.py
- get_measurement
- test_gateway_config.py
- _Handler
- test_refresh_graphify.py
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 41 edges
2. `SecureTransport` - 36 edges
3. `load_config()` - 35 edges
4. `create_app()` - 34 edges
5. `create_app()` - 34 edges
6. `FailureMode` - 33 edges
7. `PqcMetrics` - 32 edges
8. `MeasurementRepository` - 32 edges
9. `SessionManager` - 31 edges
10. `FailureInjector` - 31 edges

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

## Communities (75 total, 21 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 1 - "LegacyMeasurement"
Cohesion: 0.05
Nodes (48): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), LegacyJSONError, LegacyMeasurementDomainError (+40 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "test_session.py"
Cohesion: 0.06
Nodes (23): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+15 more)

### Community 4 - "test_client.py"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "load_config"
Cohesion: 0.09
Nodes (31): create_app(), health(), ready(), main(), _unavailable(), ConfigurationError, load_config(), integer() (+23 more)

### Community 6 - "test_dispatch.py"
Cohesion: 0.09
Nodes (16): BaselineTransport, CloudDispatch, DispatchMetrics, _Baseline, _config(), _Handler, _measurement(), _Secure (+8 more)

### Community 7 - "derive_session_key"
Cohesion: 0.08
Nodes (15): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+7 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.12
Nodes (23): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe() (+15 more)

### Community 9 - "SecureTransport"
Cohesion: 0.11
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 10 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 11 - "secure_transport.py"
Cohesion: 0.12
Nodes (3): get_config(), GatewayConfig, corrupt_ciphertext_copy()

### Community 12 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 13 - "test_failure_injection.py"
Cohesion: 0.09
Nodes (17): clock(), _aad(), _injector(), measurement_url(), _MeasurementCloud, _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy() (+9 more)

### Community 14 - "SecureSession"
Cohesion: 0.08
Nodes (14): _Sessions, SecureSession, _session(), _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send() (+6 more)

### Community 15 - "decrypt"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 16 - "PqcMetrics"
Cohesion: 0.09
Nodes (4): _Duration, PqcMetrics, test_metrics_endpoint_exposes_the_same_registry(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 17 - "SessionManager"
Cohesion: 0.12
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 18 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 19 - "cloud_service/app.py"
Cohesion: 0.15
Nodes (8): derive_session_key(), baseline_measurement(), _error(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 20 - "CanonicalMeasurement"
Cohesion: 0.16
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 21 - "test_public_key_client.py"
Cohesion: 0.14
Nodes (15): fetch_public_key(), PublicKeyRejected, _body(), cloud_server(), _public_key(), _Response, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+7 more)

### Community 22 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 23 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 24 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 25 - "test_secure_transport.py"
Cohesion: 0.24
Nodes (16): _error(), _Handler, _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+8 more)

### Community 26 - "test_cloud_mlkem.py"
Cohesion: 0.11
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 27 - "test_cloud_session_api.py"
Cohesion: 0.13
Nodes (10): StartupError, handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail() (+2 more)

### Community 28 - "validate_measurement"
Cohesion: 0.21
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 29 - "encapsulate"
Cohesion: 0.18
Nodes (9): encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged(), test_valid_public_key_round_trip_matches_decapsulation() (+1 more)

### Community 30 - "cloud_service/config.py"
Cohesion: 0.17
Nodes (7): Config, FailureMode, SecurityMode, public_key(), _unavailable(), test_custom_environment(), test_defaults_do_not_create_database()

### Community 31 - "test_cloud_baseline.py"
Cohesion: 0.14
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 32 - "_fixture"
Cohesion: 0.12
Nodes (12): client(), payload(), payload(), database(), measurement(), payload(), cloud(), payload() (+4 more)

### Community 33 - "create_app"
Cohesion: 0.17
Nodes (11): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+3 more)

### Community 34 - "load_config"
Cohesion: 0.18
Nodes (11): _logging_level(), main(), load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance() (+3 more)

### Community 35 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 36 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 37 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 38 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 39 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 40 - "build_aad"
Cohesion: 0.22
Nodes (7): AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 41 - "test_cloud_aead.py"
Cohesion: 0.27
Nodes (9): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+1 more)

### Community 42 - "test_gateway_correlation.py"
Cohesion: 0.21
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 43 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 44 - "MlKemError"
Cohesion: 0.18
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 45 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 46 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): validate_public_key(), parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 47 - "public_key_client.py"
Cohesion: 0.20
Nodes (4): _endpoint(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey

### Community 48 - "test_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 49 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 54 - "envelope.py"
Cohesion: 0.33
Nodes (3): build_secure_envelope(), generate_nonce(), test_generate_nonce_returns_distinct_12_byte_values()

### Community 56 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 57 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

### Community 59 - "test_refresh_graphify.py"
Cohesion: 0.47
Nodes (3): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 465 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `create_app`, `test_dispatch.py`, `SecureTransport`, `secure_transport.py`, `SecureSession`, `SessionManager`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_session.py`, `load_config`, `derive_session_key`, `secure_transport.py`, `test_failure_injection.py`, `SecureSession`, `public_key_client.py`, `PqcMetrics`, `test_public_key_client.py`, `CryptoFailureInjector`, `encapsulate`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `create_app()` connect `load_config` to `_fixture`, `test_cloud_queries.py`, `MeasurementRepository`, `SessionManager`, `test_cloud_public_key.py`, `measure_baseline.py`, `cloud_service/app.py`, `test_cloud_mlkem.py`, `test_cloud_session_api.py`, `cloud_service/config.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06128702757916241 - nodes in this community are weakly interconnected._