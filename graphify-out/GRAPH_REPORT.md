# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1459 nodes · 3520 edges · 89 communities (57 shown, 32 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 470 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- LegacyMeasurement
- FailureMode
- test_client.py
- MeasurementRepository
- SecureTransport
- test_sensor.py
- SessionManager
- encoding.py
- SessionManager
- PqcMetrics
- decrypt
- test_dispatch.py
- test_public_key_client.py
- secure_transport.py
- create_app
- SecureSession
- create_app
- CanonicalMeasurement
- repository.py
- encapsulate
- load_config
- GatewayErrorCode
- measure_baseline.py
- cloud_service/app.py
- test_secure_transport.py
- test_cloud_mlkem.py
- session_client.py
- validate_measurement
- load_config
- CryptoFailureInjector
- test_session.py
- _fixture
- test_cloud_baseline.py
- plaintext.py
- cloud_service/crypto/mlkem.py
- test_cloud_session_api.py
- test_cloud_aead.py
- test_cloud_queries.py
- test_failure_injection.py
- test_cloud_kdf.py
- build_aad
- test_security_logging.py
- pytest
- edge_gateway/app.py
- test_gateway_correlation.py
- refresh_graphify.py
- test_cloud_public_key.py
- json
- cloud_service/config.py
- sessions.py
- derive_session_key
- test_envelope.py
- _Clock
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- edge_gateway/crypto/kdf.py
- _Clock
- _HandshakeHandler
- cloud_service/crypto/symmetric.py
- KdfError
- StartupError
- envelope.py
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- _Handler
- _Handler
- public_key
- BaselineTransport
- baseline_measurement
- _Handler
- _Handler
- _Handler
- test_gateway_security_components_share_the_metrics_registry_by_default
- client
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
9. `SessionManager` - 32 edges
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

## Communities (89 total, 32 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 1 - "LegacyMeasurement"
Cohesion: 0.05
Nodes (47): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), LegacyJSONError, LegacyMeasurementDomainError (+39 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "test_client.py"
Cohesion: 0.10
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 4 - "MeasurementRepository"
Cohesion: 0.12
Nodes (23): lifespan(), Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe() (+15 more)

### Community 5 - "SecureTransport"
Cohesion: 0.11
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 6 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 7 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 8 - "encoding.py"
Cohesion: 0.12
Nodes (14): decode_binary(), encode_binary(), EncodingError, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally() (+6 more)

### Community 9 - "SessionManager"
Cohesion: 0.10
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 10 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, DispatchMetrics

### Community 11 - "decrypt"
Cohesion: 0.21
Nodes (18): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), test_existing_secure_envelope_authenticates_same_request_context(), _aad() (+10 more)

### Community 12 - "test_dispatch.py"
Cohesion: 0.17
Nodes (13): CloudDispatch, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 13 - "test_public_key_client.py"
Cohesion: 0.14
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _body(), cloud_server(), _public_key(), _Response, test_cloud_url_and_timeout_are_validated() (+8 more)

### Community 15 - "create_app"
Cohesion: 0.13
Nodes (18): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+10 more)

### Community 16 - "SecureSession"
Cohesion: 0.11
Nodes (11): _Sessions, SecureSession, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 17 - "create_app"
Cohesion: 0.12
Nodes (16): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+8 more)

### Community 18 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 19 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 20 - "encapsulate"
Cohesion: 0.15
Nodes (12): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+4 more)

### Community 21 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 22 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 23 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 24 - "cloud_service/app.py"
Cohesion: 0.16
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 25 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (16): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+8 more)

### Community 26 - "test_cloud_mlkem.py"
Cohesion: 0.11
Nodes (5): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 27 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 28 - "validate_measurement"
Cohesion: 0.21
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 29 - "load_config"
Cohesion: 0.22
Nodes (13): ConfigurationError, load_config(), integer(), number(), text(), value(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries() (+5 more)

### Community 30 - "CryptoFailureInjector"
Cohesion: 0.14
Nodes (4): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), test_same_seed_makes_the_same_decisions()

### Community 31 - "test_session.py"
Cohesion: 0.17
Nodes (9): SessionState, _manager(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active(), test_replacement_clears_a_held_session_before_the_new_handshake() (+1 more)

### Community 32 - "_fixture"
Cohesion: 0.12
Nodes (13): client(), payload(), payload(), database(), measurement(), payload(), cloud(), values() (+5 more)

### Community 33 - "test_cloud_baseline.py"
Cohesion: 0.14
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 34 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 35 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 36 - "test_cloud_session_api.py"
Cohesion: 0.21
Nodes (9): client(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), test_shutdown_and_classical_mode() (+1 more)

### Community 37 - "test_cloud_aead.py"
Cohesion: 0.23
Nodes (9): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+1 more)

### Community 38 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 39 - "test_failure_injection.py"
Cohesion: 0.17
Nodes (11): clock(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_enabled_warning_names_the_mode_and_not_the_seed(), test_invalid_failure_rate_is_rejected() (+3 more)

### Community 40 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 41 - "build_aad"
Cohesion: 0.22
Nodes (7): AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 42 - "test_security_logging.py"
Cohesion: 0.19
Nodes (4): _Clock, _Cloud, cloud_url(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 43 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 44 - "edge_gateway/app.py"
Cohesion: 0.19
Nodes (5): get_config(), _logging_level(), main(), GatewayConfig, test_cli_uses_configured_server_settings_and_loads_once()

### Community 45 - "test_gateway_correlation.py"
Cohesion: 0.22
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 46 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 47 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 49 - "cloud_service/config.py"
Cohesion: 0.27
Nodes (5): Config, FailureMode, SecurityMode, test_custom_environment(), test_defaults_do_not_create_database()

### Community 50 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 51 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 52 - "test_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 53 - "_Clock"
Cohesion: 0.22
Nodes (5): _Clock, _Cloud, cloud_url(), _stamp(), test_session_response_must_be_in_the_future_and_explicitly_zoned()

### Community 54 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 56 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 59 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 60 - "StartupError"
Cohesion: 0.29
Nodes (3): StartupError, fail(), test_session_initialization_failure_releases_keys()

### Community 61 - "envelope.py"
Cohesion: 0.33
Nodes (3): build_secure_envelope(), generate_nonce(), test_generate_nonce_returns_distinct_12_byte_values()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 466 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `SecureTransport`, `SessionManager`, `test_security_logging.py`, `edge_gateway/app.py`, `test_dispatch.py`, `secure_transport.py`, `create_app`, `SecureSession`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `GatewayErrorCode` connect `GatewayErrorCode` to `edge_gateway/app.py`, `create_app`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `_fixture`, `test_cloud_baseline.py`, `MeasurementRepository`, `test_cloud_session_api.py`, `test_cloud_queries.py`, `test_cloud_public_key.py`, `create_app`, `cloud_service/config.py`, `measure_baseline.py`, `cloud_service/app.py`, `StartupError`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06128702757916241 - nodes in this community are weakly interconnected._