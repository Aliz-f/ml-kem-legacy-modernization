# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2156 nodes · 5330 edges · 95 communities (63 shown, 32 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 751 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- edge_gateway/crypto/symmetric.py
- test_device.py
- create_app
- test_legacy_compatibility.py
- test_gateway_cloud_secure.py
- cli.py
- test_session.py
- load_config
- test_crypto_failures.py
- test_baseline_client.py
- GatewayErrorCode
- test_mode_evaluation.py
- SessionManager
- cloud_service/app.py
- FailureMode
- test_public_key_client.py
- test_gateway_crypto_image.py
- test_cloud_session_api.py
- SecureTransport
- FailureMode
- json
- load_config
- pytest
- measure_baseline.py
- secure_transport.py
- MeasurementRepository
- CloudDispatch
- test_secure_transport.py
- test_cloud_secure.py
- edge_gateway/crypto/mlkem.py
- CanonicalMeasurement
- LegacyMeasurement
- SessionManager
- CryptoFailureInjector
- PqcMetrics
- test_security_logging.py
- test_sensor.py
- SecureEnvelope
- validate_measurement
- encapsulate
- session_client.py
- StoredMeasurement
- SecureSession
- secure.py
- CanonicalMeasurement
- device.py
- encode_binary
- test_cloud_baseline.py
- edge_gateway/validation.py
- edge_gateway/models.py
- test_gateway_validation.py
- test_cloud_mlkem.py
- CloudMetrics
- test_cloud_queries.py
- test_cloud_kdf.py
- test_refresh_graphify.py
- test_pqc_observability.py
- test_cloud_public_key.py
- Config
- envelope_validation.py
- derive_session_key
- edge_gateway/crypto/kdf.py
- _DroppedResponse
- .__init__
- StartupError
- test_repository_hygiene.py
- get_measurement
- _Handler
- .apply
- test_shared_integration_assets.py
- KeyService
- baseline_measurement
- test_cloud_crypto_review.py
- KdfError
- .__init__
- _Handler
- _Handler
- test_gateway_crypto_ci.py
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 52 edges
2. `load_config()` - 50 edges
3. `SecureTransport` - 48 edges
4. `load_config()` - 48 edges
5. `create_app()` - 48 edges
6. `FailureMode` - 45 edges
7. `SessionManager` - 41 edges
8. `SecureTransportError` - 37 edges
9. `PqcMetrics` - 36 edges
10. `FailureMode` - 35 edges

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

## Communities (95 total, 32 thin omitted)

### Community 0 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.05
Nodes (55): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+47 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "create_app"
Cohesion: 0.06
Nodes (49): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+41 more)

### Community 3 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (36): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+28 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+25 more)

### Community 5 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 6 - "test_session.py"
Cohesion: 0.05
Nodes (23): SessionState, _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+15 more)

### Community 7 - "load_config"
Cohesion: 0.07
Nodes (36): create_app(), main(), Config, ConfigurationError, load_config(), integer(), number(), text() (+28 more)

### Community 9 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 10 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (24): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+16 more)

### Community 11 - "GatewayErrorCode"
Cohesion: 0.08
Nodes (19): GatewayError, GatewayErrorCode, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized() (+11 more)

### Community 12 - "test_mode_evaluation.py"
Cohesion: 0.06
Nodes (16): _Cloud, _count(), _serve(), test_corrupted_ciphertext_is_rejected_and_not_stored(), _Cloud, _serve(), _Baseline, _Calls (+8 more)

### Community 13 - "SessionManager"
Cohesion: 0.07
Nodes (20): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json() (+12 more)

### Community 14 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (12): health(), ready(), _crypto_dependencies_ready(), _unavailable(), derive_session_key(), public_key(), _unavailable(), _decode_ciphertext() (+4 more)

### Community 15 - "FailureMode"
Cohesion: 0.12
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 16 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+11 more)

### Community 17 - "test_gateway_crypto_image.py"
Cohesion: 0.08
Nodes (11): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version() (+3 more)

### Community 18 - "test_cloud_session_api.py"
Cohesion: 0.08
Nodes (8): test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels(), test_existing_gateway_session_client_over_real_http(), test_shared_canonical_fixture_is_accepted_and_preserves_the_baseline_contract(), _install(), main(), _serve(), _Baseline

### Community 19 - "SecureTransport"
Cohesion: 0.12
Nodes (12): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+4 more)

### Community 20 - "FailureMode"
Cohesion: 0.17
Nodes (25): FailureMode, FailureInjector, make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+17 more)

### Community 21 - "json"
Cohesion: 0.11
Nodes (15): AadError, build_aad(), DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope() (+7 more)

### Community 22 - "load_config"
Cohesion: 0.13
Nodes (22): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), main(), test_default_configuration() (+14 more)

### Community 23 - "pytest"
Cohesion: 0.10
Nodes (15): baseline_headers(), create_request_id(), decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally() (+7 more)

### Community 24 - "measure_baseline.py"
Cohesion: 0.10
Nodes (11): StorageConflictError, StorageError, canonical(), Capture, distribution(), live_cloud(), lifespan(), require() (+3 more)

### Community 25 - "secure_transport.py"
Cohesion: 0.11
Nodes (5): _baseline_transport(), corrupt_ciphertext_copy(), BaselineTransport, MeasurementProcessor, UnavailableBaseline

### Community 26 - "MeasurementRepository"
Cohesion: 0.12
Nodes (22): Database, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+14 more)

### Community 27 - "CloudDispatch"
Cohesion: 0.14
Nodes (14): CloudDispatch, _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 28 - "test_secure_transport.py"
Cohesion: 0.17
Nodes (19): _Cloud, _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried() (+11 more)

### Community 29 - "test_cloud_secure.py"
Cohesion: 0.16
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 30 - "edge_gateway/crypto/mlkem.py"
Cohesion: 0.11
Nodes (8): decapsulate(), generate_keypair(), MlKemError, PrivateKey, _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 31 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 32 - "LegacyMeasurement"
Cohesion: 0.18
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 33 - "SessionManager"
Cohesion: 0.10
Nodes (3): lifespan(), SessionEstablishmentError, SessionManager

### Community 34 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (7): get_config(), GatewayConfig, CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline(), _count(), test_handshake_failure_stays_closed_without_a_session()

### Community 36 - "test_security_logging.py"
Cohesion: 0.11
Nodes (12): _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send() (+4 more)

### Community 37 - "test_sensor.py"
Cohesion: 0.14
Nodes (16): Sensor, FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values(), test_measurement_rejects_naive_timestamp(), test_payload_converts_non_utc_timestamp_to_utc() (+8 more)

### Community 38 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 39 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 40 - "encapsulate"
Cohesion: 0.15
Nodes (12): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+4 more)

### Community 41 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 42 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 43 - "SecureSession"
Cohesion: 0.12
Nodes (6): _Sessions, SecureSession, test_seal_failure_is_counted_without_the_session_key(), get_or_establish(), test_session_recovery_is_counted(), get_or_establish()

### Community 44 - "secure.py"
Cohesion: 0.16
Nodes (7): AeadError, decrypt(), _error(), _ingest(), _NoMetrics, secure_measurement(), fail()

### Community 45 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 47 - "encode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 48 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 49 - "edge_gateway/validation.py"
Cohesion: 0.15
Nodes (9): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), canonical(), test_domain_bounds_remain_a_separate_stage() (+1 more)

### Community 50 - "edge_gateway/models.py"
Cohesion: 0.17
Nodes (5): _timestamp(), normalize(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 51 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 52 - "test_cloud_mlkem.py"
Cohesion: 0.14
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 53 - "CloudMetrics"
Cohesion: 0.15
Nodes (3): CloudMetrics, _labels(), _render_labels()

### Community 54 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 55 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 56 - "test_refresh_graphify.py"
Cohesion: 0.19
Nodes (5): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 57 - "test_pqc_observability.py"
Cohesion: 0.23
Nodes (6): _Cloud, _count(), _payload(), _post(), _serve(), test_handshake_counter_shows_reuse_then_expiry()

### Community 58 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 59 - "Config"
Cohesion: 0.21
Nodes (5): Config, make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory()

### Community 60 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 61 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 63 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 65 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 67 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 74 - "test_cloud_crypto_review.py"
Cohesion: 0.60
Nodes (3): test_review_matches_key_exposure_and_secure_ingestion(), test_review_matches_the_cloud_session_key_contract(), _text()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 740 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CloudHarness` connect `test_gateway_cloud_secure.py` to `SessionManager`, `StoredMeasurement`, `SecureTransport`, `FailureMode`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `edge_gateway/crypto/symmetric.py`, `create_app`, `test_gateway_cloud_secure.py`, `test_session.py`, `test_crypto_failures.py`, `test_mode_evaluation.py`, `test_cloud_session_api.py`, `pytest`, `secure_transport.py`, `CloudDispatch`, `test_secure_transport.py`, `SessionManager`, `CryptoFailureInjector`, `PqcMetrics`, `test_security_logging.py`, `SecureSession`, `test_pqc_observability.py`, `.__init__`, `.__init__`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `CryptoFailureInjector`, `PqcMetrics`, `test_security_logging.py`, `test_gateway_cloud_secure.py`, `test_session.py`, `encapsulate`, `session_client.py`, `test_crypto_failures.py`, `KdfError`, `SecureSession`, `test_mode_evaluation.py`, `test_public_key_client.py`, `test_cloud_session_api.py`, `json`, `secure_transport.py`, `test_pqc_observability.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `SecureTransport` (e.g. with `main()` and `create_app()`) actually correct?**
  _`SecureTransport` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `edge_gateway/crypto/symmetric.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05372405372405373 - nodes in this community are weakly interconnected._