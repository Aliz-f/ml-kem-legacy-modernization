# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1350 nodes · 3254 edges · 81 communities (47 shown, 34 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 428 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- decrypt
- cli.py
- FailureMode
- load_config
- test_client.py
- test_public_key_client.py
- test_sensor.py
- test_session.py
- SessionManager
- MeasurementRepository
- load_config
- test_gateway_models.py
- create_app
- secure_transport.py
- test_cloud_mlkem.py
- validate_measurement
- CanonicalMeasurement
- repository.py
- PqcMetrics
- measure_baseline.py
- test_cloud_session_api.py
- session_client.py
- cloud_service/app.py
- encapsulate
- SessionManager
- test_dispatch.py
- test_cloud_queries.py
- SecureTransportError
- test_secure_transport.py
- cloud_service/crypto/mlkem.py
- test_cloud_baseline.py
- test_cloud_kdf.py
- SecureTransport
- _fixture
- CryptoFailureInjector
- SecureSession
- test_security_logging.py
- test_failure_injection.py
- encoding.py
- pytest
- refresh_graphify.py
- test_cloud_public_key.py
- sessions.py
- derive_session_key
- CloudDispatch
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- edge_gateway/crypto/kdf.py
- edge_gateway/crypto/mlkem.py
- _Clock
- _HandshakeHandler
- _Clock
- cloud_service/crypto/symmetric.py
- .__init__
- json
- test_session_recovery_is_counted
- test_repository_hygiene.py
- get_measurement
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- test_fetch_does_not_encapsulate
- _Handler
- BaselineTransport
- crypto/failure.py
- KdfError
- _Handler
- _Handler
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 41 edges
2. `SecureTransport` - 36 edges
3. `create_app()` - 34 edges
4. `FailureMode` - 33 edges
5. `PqcMetrics` - 32 edges
6. `MeasurementRepository` - 32 edges
7. `load_config()` - 32 edges
8. `FailureInjector` - 31 edges
9. `SessionManager` - 31 edges
10. `SecureTransportError` - 28 edges

## Surprising Connections (you probably didn't know these)
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_protocol_example_and_independent_round_trip()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_models.py → cloud_service/tests/test_cloud_aead.py
- `test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged()` --calls--> `encapsulate()`  [EXTRACTED]
  cloud_service/tests/test_cloud_mlkem.py → edge_gateway/src/edge_gateway/crypto/mlkem.py
- `test_invalid_metadata_and_domain_are_rejected()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_gateway_cloud_mlkem_and_kdf_interoperability()` --calls--> `encapsulate()`  [EXTRACTED]
  cloud_service/tests/test_cloud_kdf.py → edge_gateway/src/edge_gateway/crypto/mlkem.py

## Import Cycles
- None detected.

## Communities (81 total, 34 thin omitted)

### Community 0 - "decrypt"
Cohesion: 0.05
Nodes (54): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+46 more)

### Community 1 - "cli.py"
Cohesion: 0.07
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "load_config"
Cohesion: 0.08
Nodes (34): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+26 more)

### Community 4 - "test_client.py"
Cohesion: 0.10
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (18): validate_public_key(), _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected (+10 more)

### Community 6 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 7 - "test_session.py"
Cohesion: 0.09
Nodes (13): SessionState, _Clock, _Cloud, cloud_url(), _Handler, _manager(), _stamp(), test_close_wipes_the_session_key() (+5 more)

### Community 8 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 9 - "MeasurementRepository"
Cohesion: 0.12
Nodes (20): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+12 more)

### Community 10 - "load_config"
Cohesion: 0.14
Nodes (18): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+10 more)

### Community 11 - "test_gateway_models.py"
Cohesion: 0.17
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 12 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+9 more)

### Community 14 - "test_cloud_mlkem.py"
Cohesion: 0.10
Nodes (6): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 15 - "validate_measurement"
Cohesion: 0.16
Nodes (13): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema() (+5 more)

### Community 16 - "CanonicalMeasurement"
Cohesion: 0.20
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+4 more)

### Community 17 - "repository.py"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 19 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 20 - "test_cloud_session_api.py"
Cohesion: 0.13
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 21 - "session_client.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 23 - "encapsulate"
Cohesion: 0.16
Nodes (11): encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged(), test_valid_public_key_round_trip_matches_decapsulation() (+3 more)

### Community 24 - "SessionManager"
Cohesion: 0.17
Nodes (3): log_security(), SessionEstablishmentError, SessionManager

### Community 25 - "test_dispatch.py"
Cohesion: 0.25
Nodes (12): _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline(), test_failure_log_omits_the_measurement() (+4 more)

### Community 26 - "test_cloud_queries.py"
Cohesion: 0.14
Nodes (12): test_unrelated_record_id_collision_is_not_idempotent_success(), client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail() (+4 more)

### Community 27 - "SecureTransportError"
Cohesion: 0.16
Nodes (7): _error_code(), _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance, SecureTransportError, _SessionRecovery

### Community 28 - "test_secure_transport.py"
Cohesion: 0.33
Nodes (15): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+7 more)

### Community 29 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 30 - "test_cloud_baseline.py"
Cohesion: 0.15
Nodes (7): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 31 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 32 - "SecureTransport"
Cohesion: 0.21
Nodes (4): SecureEnvelope, _dump(), _Measurement, SecureTransport

### Community 33 - "_fixture"
Cohesion: 0.14
Nodes (10): client(), payload(), payload(), database(), payload(), cloud(), payload(), _Cloud (+2 more)

### Community 34 - "CryptoFailureInjector"
Cohesion: 0.17
Nodes (3): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_same_seed_makes_the_same_decisions()

### Community 35 - "SecureSession"
Cohesion: 0.17
Nodes (5): _Sessions, SecureSession, _session(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish()

### Community 36 - "test_security_logging.py"
Cohesion: 0.20
Nodes (7): _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback(), test_unsafe_log_values_are_dropped()

### Community 37 - "test_failure_injection.py"
Cohesion: 0.21
Nodes (10): clock(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode() (+2 more)

### Community 38 - "encoding.py"
Cohesion: 0.24
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 39 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 40 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 41 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 42 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 43 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 45 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 47 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.33
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 48 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 50 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 56 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 58 - "test_fetch_does_not_encapsulate"
Cohesion: 0.40
Nodes (4): _body(), _public_key(), test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 437 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `SecureTransport` to `decrypt`, `CryptoFailureInjector`, `SecureSession`, `load_config`, `test_security_logging.py`, `encoding.py`, `CloudDispatch`, `secure_transport.py`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `PqcMetrics`, `.__init__`, `test_session_recovery_is_counted`, `SessionManager`, `test_dispatch.py`, `SecureTransportError`, `test_secure_transport.py`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `SecureTransport`, `load_config`, `test_security_logging.py`, `SecureSession`, `CloudDispatch`, `secure_transport.py`, `.__init__`, `test_session_recovery_is_counted`, `SessionManager`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `_fixture`, `SessionManager`, `MeasurementRepository`, `load_config`, `sessions.py`, `test_cloud_public_key.py`, `test_cloud_mlkem.py`, `measure_baseline.py`, `test_cloud_session_api.py`, `cloud_service/app.py`, `test_cloud_queries.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._