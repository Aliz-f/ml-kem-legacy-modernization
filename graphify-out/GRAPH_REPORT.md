# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2195 nodes · 5423 edges · 100 communities (66 shown, 34 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 758 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_cloud_secure.py
- test_device.py
- test_secure_message_tamper.py
- LegacyMeasurement
- test_legacy_compatibility.py
- test_gateway_cloud_secure.py
- cli.py
- load_config
- GatewayClient
- GatewayErrorCode
- test_gateway_crypto_image.py
- test_baseline_client.py
- secure_transport.py
- SecureTransport
- test_crypto_failures.py
- create_app
- pathlib
- MeasurementRepository
- load_config
- cloud_service/app.py
- edge_gateway/app.py
- test_gateway_validation.py
- test_public_key_client.py
- edge_gateway/crypto/symmetric.py
- json
- SecureTransportError
- test_cloud_mlkem.py
- FailureMode
- CanonicalMeasurement
- SecureSession
- test_mode_evaluation.py
- edge_gateway/crypto/envelope.py
- test_cloud_public_key.py
- test_dispatch.py
- test_cloud_failure_injection.py
- StoredMeasurement
- session_client.py
- SessionManager
- test_secure_transport.py
- measure_baseline.py
- validate_measurement
- encapsulate
- PqcMetrics
- pytest
- derive_session_key
- test_cloud_baseline.py
- test_session.py
- CloudMetrics
- edge_gateway/crypto/encoding.py
- sessions.py
- cloud_service/crypto/mlkem.py
- test_cloud_queries.py
- test_pqc_observability.py
- test_security_logging.py
- _ingest
- test_refresh_graphify.py
- test_cloud_session_api.py
- test_gateway_correlation.py
- parse_public_key_response
- threading
- test_secure_envelope.py
- _Clock
- test_corrupted_ciphertext_is_rejected_and_not_stored
- _HandshakeHandler
- test_dependency_review.py
- KdfError
- _Cloud
- test_repository_hygiene.py
- get_measurement
- _Handler
- _Handler
- test_shared_integration_assets.py
- baseline_measurement
- test_cloud_crypto_review.py
- test_member2_integration_review.py
- _Handler
- _Handler
- _Handler
- test_synthetic_secret_markers_never_appear_in_cloud_logs
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 53 edges
2. `load_config()` - 50 edges
3. `SecureTransport` - 49 edges
4. `load_config()` - 48 edges
5. `create_app()` - 48 edges
6. `FailureMode` - 46 edges
7. `SessionManager` - 43 edges
8. `SecureTransportError` - 38 edges
9. `PqcMetrics` - 37 edges
10. `FailureMode` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_corrupted_ciphertext_is_rejected_and_not_stored()` --uses--> `CryptoFailureInjector`  [INFERRED]
  tests/integration/test_corrupt_ciphertext_demo.py → edge_gateway/src/edge_gateway/crypto/failure.py

## Import Cycles
- None detected.

## Communities (100 total, 34 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_cloud_secure.py"
Cohesion: 0.05
Nodes (48): decode_binary(), encode_binary(), EncodingError, EnvelopeSchemaError, SecureEnvelope, _constant(), EnvelopeValidationError, _object() (+40 more)

### Community 2 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 3 - "test_secure_message_tamper.py"
Cohesion: 0.06
Nodes (27): AadError, build_aad(), SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes() (+19 more)

### Community 4 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (32): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+24 more)

### Community 5 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (33): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+25 more)

### Community 6 - "test_gateway_cloud_secure.py"
Cohesion: 0.06
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _install_trace(), _measurement(), _seal() (+24 more)

### Community 7 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 8 - "load_config"
Cohesion: 0.08
Nodes (33): create_app(), main(), ConfigurationError, load_config(), integer(), number(), text(), value() (+25 more)

### Community 9 - "GatewayClient"
Cohesion: 0.09
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 10 - "GatewayErrorCode"
Cohesion: 0.08
Nodes (19): GatewayError, GatewayErrorCode, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized() (+11 more)

### Community 11 - "test_gateway_crypto_image.py"
Cohesion: 0.06
Nodes (18): _log_calls(), _python_files(), test_no_key_or_env_files_are_tracked(), test_no_private_key_blocks_or_debug_prints(), test_source_logs_do_not_receive_secret_material(), _text(), _tracked(), clear_incremental_state() (+10 more)

### Community 12 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (24): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+16 more)

### Community 13 - "secure_transport.py"
Cohesion: 0.08
Nodes (6): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement(), corrupt_ciphertext_copy(), _Duration, _Baseline

### Community 14 - "SecureTransport"
Cohesion: 0.07
Nodes (12): lifespan(), _secure_transport(), CryptoFailureInjector, _endpoint(), SecureTransport, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _Baseline (+4 more)

### Community 15 - "test_crypto_failures.py"
Cohesion: 0.08
Nodes (20): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud (+12 more)

### Community 16 - "create_app"
Cohesion: 0.09
Nodes (24): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+16 more)

### Community 18 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 19 - "load_config"
Cohesion: 0.12
Nodes (25): main(), _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int() (+17 more)

### Community 20 - "cloud_service/app.py"
Cohesion: 0.11
Nodes (6): SecurityMode, AeadError, decrypt(), public_key(), _unavailable(), fail()

### Community 21 - "edge_gateway/app.py"
Cohesion: 0.09
Nodes (9): _baseline_transport(), get_config(), _logging_level(), GatewayConfig, BaselineTransport, CloudDispatch, DispatchMetrics, MeasurementProcessor (+1 more)

### Community 22 - "test_gateway_validation.py"
Cohesion: 0.10
Nodes (21): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client() (+13 more)

### Community 23 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), cloud_server(), _public_key() (+10 more)

### Community 24 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.19
Nodes (20): main(), AeadError, decrypt(), encrypt(), generate_nonce(), _require_bytes(), _require_key(), _require_nonce() (+12 more)

### Community 25 - "json"
Cohesion: 0.13
Nodes (16): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+8 more)

### Community 26 - "SecureTransportError"
Cohesion: 0.12
Nodes (11): _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance, SecureTransportError (+3 more)

### Community 27 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (9): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected() (+1 more)

### Community 28 - "FailureMode"
Cohesion: 0.11
Nodes (9): Config, FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes() (+1 more)

### Community 29 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 30 - "SecureSession"
Cohesion: 0.10
Nodes (10): _Sessions, SecureSession, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted() (+2 more)

### Community 31 - "test_mode_evaluation.py"
Cohesion: 0.13
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 32 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.14
Nodes (12): build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement() (+4 more)

### Community 33 - "test_cloud_public_key.py"
Cohesion: 0.11
Nodes (12): lifespan(), StartupError, KeyService, secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail() (+4 more)

### Community 34 - "test_dispatch.py"
Cohesion: 0.18
Nodes (13): _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 35 - "test_cloud_failure_injection.py"
Cohesion: 0.19
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 36 - "StoredMeasurement"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 37 - "session_client.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 39 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (17): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+9 more)

### Community 40 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 41 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 42 - "encapsulate"
Cohesion: 0.16
Nodes (11): test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated() (+3 more)

### Community 44 - "pytest"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 45 - "derive_session_key"
Cohesion: 0.14
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 46 - "test_cloud_baseline.py"
Cohesion: 0.11
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 47 - "test_session.py"
Cohesion: 0.15
Nodes (10): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active() (+2 more)

### Community 48 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 49 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.19
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 50 - "sessions.py"
Cohesion: 0.18
Nodes (10): health(), ready(), _crypto_dependencies_ready(), _unavailable(), derive_session_key(), _decode_ciphertext(), _error(), _establish() (+2 more)

### Community 51 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 52 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 53 - "test_pqc_observability.py"
Cohesion: 0.19
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 54 - "test_security_logging.py"
Cohesion: 0.19
Nodes (4): _Clock, _Cloud, cloud_url(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 55 - "_ingest"
Cohesion: 0.19
Nodes (5): _DroppedResponse, _error(), _ingest(), _NoMetrics, secure_measurement()

### Community 56 - "test_refresh_graphify.py"
Cohesion: 0.19
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 57 - "test_cloud_session_api.py"
Cohesion: 0.26
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 58 - "test_gateway_correlation.py"
Cohesion: 0.23
Nodes (6): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 59 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 60 - "threading"
Cohesion: 0.25
Nodes (3): _install(), main(), _serve()

### Community 61 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 62 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 63 - "test_corrupted_ciphertext_is_rejected_and_not_stored"
Cohesion: 0.22
Nodes (4): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored()

### Community 65 - "test_dependency_review.py"
Cohesion: 0.39
Nodes (6): _locked(), _source_files(), test_one_crypto_library_is_locked(), test_random_module_is_not_a_key_or_nonce_source(), test_source_imports_only_the_reviewed_crypto_api(), _text()

### Community 66 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 69 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 77 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

### Community 78 - "test_member2_integration_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_bounded_session_recovery(), test_review_matches_dispatch_and_correlation(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 751 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `SessionManager`, `secure_transport.py`, `SecureTransport`, `create_app`, `edge_gateway/app.py`, `test_security_logging.py`, `test_pqc_observability.py`, `test_mode_evaluation.py`, `SecureSession`, `test_corrupted_ciphertext_is_rejected_and_not_stored`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `test_gateway_cloud_secure.py`, `secure_transport.py`, `test_crypto_failures.py`, `create_app`, `edge_gateway/app.py`, `edge_gateway/crypto/symmetric.py`, `json`, `SecureTransportError`, `SecureSession`, `test_mode_evaluation.py`, `edge_gateway/crypto/envelope.py`, `test_dispatch.py`, `SessionManager`, `test_secure_transport.py`, `PqcMetrics`, `pytest`, `edge_gateway/crypto/encoding.py`, `test_pqc_observability.py`, `threading`, `test_corrupted_ciphertext_is_rejected_and_not_stored`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `SessionEstablishmentError` connect `SessionManager` to `test_dispatch.py`, `KdfError`, `test_secure_message_tamper.py`, `test_secure_transport.py`, `secure_transport.py`, `SecureTransport`, `test_crypto_failures.py`, `test_session.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `SecureTransport` (e.g. with `main()` and `create_app()`) actually correct?**
  _`SecureTransport` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.055900621118012424 - nodes in this community are weakly interconnected._