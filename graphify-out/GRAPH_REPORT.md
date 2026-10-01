# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1918 nodes · 4717 edges · 102 communities (65 shown, 37 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 661 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- FailureMode
- test_device.py
- test_legacy_compatibility.py
- test_gateway_cloud_secure.py
- LegacyMeasurement
- FailureMode
- test_crypto_failures.py
- SecureSession
- test_sensor.py
- SessionManager
- measure_baseline.py
- test_dispatch.py
- cloud_service/app.py
- SecureTransport
- load_config
- SessionManager
- json
- validate_measurement
- secure_transport.py
- load_config
- CanonicalMeasurement
- test_cloud_secure.py
- PqcMetrics
- test_secure_transport.py
- edge_gateway/crypto/envelope.py
- cloud_service/config.py
- SecureEnvelope
- GatewayErrorCode
- test_secure_message_tamper.py
- test_cloud_session_api.py
- StoredMeasurement
- MeasurementRepository
- secure.py
- session_client.py
- test_secure_shutdown.py
- CryptoFailureInjector
- decode_binary
- StorageError
- test_cloud_baseline.py
- encode_binary
- encapsulate
- test_cloud_kdf.py
- fields
- plaintext.py
- parse_public_key_response
- test_gateway_validation.py
- test_cloud_queries.py
- encrypt
- test_session.py
- cloud_service/crypto/mlkem.py
- edge_gateway/crypto/symmetric.py
- edge_gateway/config.py
- edge_gateway/validation.py
- edge_gateway/app.py
- test_cloud_mlkem.py
- test_cloud_public_key.py
- test_gateway_correlation.py
- _Clock
- envelope_validation.py
- derive_session_key
- test_secure_envelope.py
- queries.py
- _Clock
- edge_gateway/crypto/kdf.py
- .__init__
- KdfError
- test_refresh_graphify.py
- pathlib
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- pytest
- test_gateway_config.py
- _Handler
- _Handler
- test_shared_integration_assets.py
- KeyService
- _Response
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
10. `SecureTransportError` - 33 edges

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

## Communities (102 total, 37 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (51): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), main(), parser(), record_work(), recorded_changes() (+43 more)

### Community 1 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 2 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 3 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (36): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+28 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+24 more)

### Community 5 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (31): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+23 more)

### Community 6 - "FailureMode"
Cohesion: 0.11
Nodes (24): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+16 more)

### Community 7 - "test_crypto_failures.py"
Cohesion: 0.07
Nodes (20): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+12 more)

### Community 8 - "SecureSession"
Cohesion: 0.07
Nodes (15): _Sessions, SecureSession, SessionState, _Sessions, _session(), _Baseline, _measurement(), _send() (+7 more)

### Community 9 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 10 - "SessionManager"
Cohesion: 0.10
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 11 - "measure_baseline.py"
Cohesion: 0.09
Nodes (12): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+4 more)

### Community 12 - "test_dispatch.py"
Cohesion: 0.12
Nodes (16): CloudDispatch, _Baseline, cloud(), _config(), _Handler, _measurement(), _Secure, _Sessions (+8 more)

### Community 13 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (19): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+11 more)

### Community 14 - "SecureTransport"
Cohesion: 0.12
Nodes (10): _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance, SecureTransport (+2 more)

### Community 15 - "load_config"
Cohesion: 0.12
Nodes (22): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+14 more)

### Community 16 - "SessionManager"
Cohesion: 0.10
Nodes (6): lifespan(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager

### Community 17 - "json"
Cohesion: 0.12
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, _body(), _public_key(), test_cloud_url_and_timeout_are_validated() (+8 more)

### Community 18 - "validate_measurement"
Cohesion: 0.13
Nodes (15): baseline_measurement(), _error(), MeasurementValidationError, validate_measurement(), test_unrelated_record_id_collision_is_not_idempotent_success(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match() (+7 more)

### Community 20 - "load_config"
Cohesion: 0.14
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+9 more)

### Community 21 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 22 - "test_cloud_secure.py"
Cohesion: 0.18
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 23 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 24 - "test_secure_transport.py"
Cohesion: 0.19
Nodes (18): _Cloud, _error(), _Handler, _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable() (+10 more)

### Community 25 - "edge_gateway/crypto/envelope.py"
Cohesion: 0.13
Nodes (10): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract() (+2 more)

### Community 26 - "cloud_service/config.py"
Cohesion: 0.15
Nodes (9): SecurityMode, derive_session_key(), public_key(), _unavailable(), _decode_ciphertext(), _error(), _establish(), establish_session() (+1 more)

### Community 27 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 28 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 29 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 30 - "test_cloud_session_api.py"
Cohesion: 0.14
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 31 - "StoredMeasurement"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 32 - "MeasurementRepository"
Cohesion: 0.16
Nodes (18): MeasurementRepository, database(), measurement(), test_closed_database_errors_are_safe(), test_concurrent_repository_access(), test_corrupted_stored_row_is_translated(), test_database_uniqueness_is_a_conflict_not_idempotent_success(), test_invalid_repository_limits() (+10 more)

### Community 33 - "secure.py"
Cohesion: 0.15
Nodes (7): AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement(), fail()

### Community 34 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 35 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 37 - "decode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 38 - "StorageError"
Cohesion: 0.16
Nodes (5): Database, StorageConflictError, StorageError, test_concurrent_duplicates_across_connections(), save()

### Community 39 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 40 - "encode_binary"
Cohesion: 0.20
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _different_nonce(), _tamper()

### Community 41 - "encapsulate"
Cohesion: 0.19
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 42 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 43 - "fields"
Cohesion: 0.22
Nodes (12): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+4 more)

### Community 44 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 45 - "parse_public_key_response"
Cohesion: 0.19
Nodes (9): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 46 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 47 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 48 - "encrypt"
Cohesion: 0.37
Nodes (12): encrypt(), _aad(), _key(), _plaintext(), test_authentication_failure_does_not_return_plaintext(), test_independent_cloud_aad_authenticates_and_each_field_change_fails(), test_invalid_key_and_nonce_lengths_are_rejected(), test_keys_and_plaintext_are_not_logged() (+4 more)

### Community 49 - "test_session.py"
Cohesion: 0.18
Nodes (8): _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active(), test_unavailable_cloud_is_retryable_and_leaves_no_session()

### Community 50 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.17
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 51 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.21
Nodes (7): test_vendor_error_diagnostics_are_suppressed(), AeadError, decrypt(), _require_bytes(), _require_key(), _require_nonce(), test_corrupt_ciphertext_mutates_only_the_outgoing_copy()

### Community 52 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 53 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 54 - "edge_gateway/app.py"
Cohesion: 0.18
Nodes (5): get_config(), _logging_level(), main(), GatewayConfig, test_from_config_uses_gateway_failure_settings()

### Community 55 - "test_cloud_mlkem.py"
Cohesion: 0.20
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 56 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 57 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 58 - "_Clock"
Cohesion: 0.20
Nodes (5): _Clock, _Cloud, cloud_url(), _stamp(), test_session_response_must_be_in_the_future_and_explicitly_zoned()

### Community 59 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 60 - "derive_session_key"
Cohesion: 0.29
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 61 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 62 - "queries.py"
Cohesion: 0.33
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 63 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 66 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 67 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 73 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

## Knowledge Gaps
- **4 isolated node(s):** `legacy-system`, `ml-kem-legacy-modernization`, `cloud-service`, `edge-gateway`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 637 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `SecureTransport` to `.__init__`, `test_secure_shutdown.py`, `CryptoFailureInjector`, `test_gateway_cloud_secure.py`, `test_crypto_failures.py`, `encode_binary`, `SecureSession`, `measure_baseline.py`, `plaintext.py`, `test_dispatch.py`, `fields`, `load_config`, `SessionManager`, `secure_transport.py`, `edge_gateway/crypto/symmetric.py`, `PqcMetrics`, `test_secure_transport.py`, `edge_gateway/crypto/envelope.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `.__init__`, `CryptoFailureInjector`, `SecureSession`, `fields`, `test_dispatch.py`, `SecureTransport`, `load_config`, `SessionManager`, `secure_transport.py`, `edge_gateway/app.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `StorageError`, `FailureMode`, `test_cloud_baseline.py`, `measure_baseline.py`, `cloud_service/app.py`, `test_cloud_secure.py`, `test_cloud_public_key.py`, `cloud_service/config.py`, `test_cloud_session_api.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `legacy-system`, `ml-kem-legacy-modernization`, `cloud-service` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.061156235069278544 - nodes in this community are weakly interconnected._