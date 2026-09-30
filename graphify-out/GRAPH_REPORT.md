# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1373 nodes · 3307 edges · 65 communities (42 shown, 23 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 443 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- decrypt
- cli.py
- FailureMode
- json
- test_session.py
- load_config
- test_client.py
- derive_session_key
- SecureTransport
- test_sensor.py
- SessionManager
- test_dispatch.py
- MeasurementRepository
- test_security_logging.py
- secure_transport.py
- cloud_service/app.py
- test_gateway_models.py
- create_app
- load_config
- SessionManager
- CanonicalMeasurement
- measure_baseline.py
- repository.py
- PqcMetrics
- test_cloud_envelope.py
- encapsulate
- test_secure_transport.py
- test_cloud_session_api.py
- validate_measurement
- test_cloud_queries.py
- CryptoFailureInjector
- cloud_service/crypto/mlkem.py
- test_cloud_baseline.py
- test_failure_injection.py
- _fixture
- test_cloud_kdf.py
- pytest
- refresh_graphify.py
- test_cloud_public_key.py
- KeyService
- sessions.py
- test_cloud_mlkem.py
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- .__init__
- _Clock
- _HandshakeHandler
- cloud_service/crypto/symmetric.py
- test_repository_hygiene.py
- get_measurement
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
5. `MeasurementRepository` - 32 edges
6. `PqcMetrics` - 32 edges
7. `load_config()` - 32 edges
8. `SessionManager` - 31 edges
9. `FailureInjector` - 31 edges
10. `SecureTransportError` - 28 edges

## Surprising Connections (you probably didn't know these)
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_protocol_example_and_independent_round_trip()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_models.py → cloud_service/tests/test_cloud_aead.py
- `test_concurrent_repository_access()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_database_uniqueness_is_a_conflict_not_idempotent_success()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_list_limit_filter_and_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py

## Import Cycles
- None detected.

## Communities (65 total, 23 thin omitted)

### Community 0 - "decrypt"
Cohesion: 0.06
Nodes (54): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+46 more)

### Community 1 - "cli.py"
Cohesion: 0.07
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "json"
Cohesion: 0.05
Nodes (34): AadError, build_aad(), decode_binary(), encode_binary(), EncodingError, _endpoint(), fetch_public_key(), PublicKeyTransportError (+26 more)

### Community 4 - "test_session.py"
Cohesion: 0.06
Nodes (23): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+15 more)

### Community 5 - "load_config"
Cohesion: 0.08
Nodes (33): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+25 more)

### Community 6 - "test_client.py"
Cohesion: 0.10
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 7 - "derive_session_key"
Cohesion: 0.08
Nodes (15): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+7 more)

### Community 8 - "SecureTransport"
Cohesion: 0.10
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 9 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 10 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 11 - "test_dispatch.py"
Cohesion: 0.13
Nodes (14): CloudDispatch, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 12 - "MeasurementRepository"
Cohesion: 0.12
Nodes (20): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+12 more)

### Community 13 - "test_security_logging.py"
Cohesion: 0.09
Nodes (14): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+6 more)

### Community 15 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (5): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 16 - "test_gateway_models.py"
Cohesion: 0.17
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 17 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+9 more)

### Community 18 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+9 more)

### Community 19 - "SessionManager"
Cohesion: 0.11
Nodes (5): _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 20 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+4 more)

### Community 21 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 22 - "repository.py"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 24 - "test_cloud_envelope.py"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 25 - "encapsulate"
Cohesion: 0.15
Nodes (12): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+4 more)

### Community 26 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (16): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+8 more)

### Community 27 - "test_cloud_session_api.py"
Cohesion: 0.15
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 28 - "validate_measurement"
Cohesion: 0.21
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 29 - "test_cloud_queries.py"
Cohesion: 0.14
Nodes (12): test_unrelated_record_id_collision_is_not_idempotent_success(), client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail() (+4 more)

### Community 30 - "CryptoFailureInjector"
Cohesion: 0.14
Nodes (4): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), test_same_seed_makes_the_same_decisions()

### Community 31 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 32 - "test_cloud_baseline.py"
Cohesion: 0.15
Nodes (7): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 33 - "test_failure_injection.py"
Cohesion: 0.17
Nodes (11): clock(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_enabled_warning_names_the_mode_and_not_the_seed(), test_invalid_failure_rate_is_rejected() (+3 more)

### Community 34 - "_fixture"
Cohesion: 0.14
Nodes (10): client(), payload(), payload(), database(), payload(), cloud(), payload(), _Cloud (+2 more)

### Community 35 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 36 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 37 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 38 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 40 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 41 - "test_cloud_mlkem.py"
Cohesion: 0.22
Nodes (4): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 42 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 44 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 48 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 444 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `load_config`, `SecureTransport`, `test_dispatch.py`, `.__init__`, `test_security_logging.py`, `secure_transport.py`, `SessionManager`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `PublicKeyTransportError` connect `json` to `SessionManager`, `secure_transport.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `test_failure_injection.py`, `json`, `test_session.py`, `derive_session_key`, `test_security_logging.py`, `secure_transport.py`, `PqcMetrics`, `encapsulate`, `test_cloud_session_api.py`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._