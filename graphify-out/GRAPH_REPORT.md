# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1450 nodes · 3506 edges · 82 communities (51 shown, 31 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 468 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- cli.py
- FailureMode
- test_cloud_public_key.py
- test_client.py
- secure_transport.py
- load_config
- test_sensor.py
- SessionManager
- MeasurementRepository
- test_public_key_client.py
- SessionManager
- cloud_service/app.py
- encapsulate
- edge_gateway/crypto/session.py
- create_app
- LegacyMeasurement
- measure_baseline.py
- load_config
- test_session.py
- decrypt
- test_dispatch.py
- PqcMetrics
- test_gateway_validation.py
- derive_session_key
- test_public_key.py
- CanonicalMeasurement
- repository.py
- GatewayErrorCode
- test_cloud_session_api.py
- test_secure_transport.py
- validate_measurement
- build_aad
- test_gateway_canonical_model.py
- test_cloud_aead.py
- edge_gateway/config.py
- test_cloud_baseline.py
- CryptoFailureInjector
- plaintext.py
- test_security_logging.py
- test_cloud_queries.py
- test_failure_injection.py
- _fixture
- encoding.py
- validate_legacy_measurement
- test_gateway_correlation.py
- refresh_graphify.py
- test_envelope.py
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- .__init__
- _Clock
- _HandshakeHandler
- _Clock
- cloud_service/crypto/symmetric.py
- json
- test_session_recovery_is_counted
- test_repository_hygiene.py
- cloud_service/crypto/aad.py
- get_measurement
- pytest
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- test_gateway_config.py
- _Handler
- _Handler
- public_key
- _Handler
- _Handler
- _Handler
- test_enabled_warning_names_the_mode_and_not_the_seed
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
- `test_gateway_cloud_mlkem_and_kdf_interoperability()` --calls--> `encapsulate()`  [EXTRACTED]
  cloud_service/tests/test_cloud_kdf.py → edge_gateway/src/edge_gateway/crypto/mlkem.py

## Import Cycles
- None detected.

## Communities (82 total, 31 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.07
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 1 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 2 - "test_cloud_public_key.py"
Cohesion: 0.05
Nodes (19): KeyService, test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged() (+11 more)

### Community 3 - "test_client.py"
Cohesion: 0.08
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 4 - "secure_transport.py"
Cohesion: 0.09
Nodes (15): SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect (+7 more)

### Community 5 - "load_config"
Cohesion: 0.09
Nodes (24): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+16 more)

### Community 6 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 7 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.12
Nodes (22): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+14 more)

### Community 9 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, PublicKeyRejected, _body(), cloud_server(), _public_key() (+10 more)

### Community 10 - "SessionManager"
Cohesion: 0.09
Nodes (5): _Sessions, SecureSession, SessionEstablishmentError, SessionManager, _session()

### Community 11 - "cloud_service/app.py"
Cohesion: 0.15
Nodes (9): SecurityMode, derive_session_key(), baseline_measurement(), _error(), _decode_ciphertext(), _error(), _establish(), establish_session() (+1 more)

### Community 12 - "encapsulate"
Cohesion: 0.11
Nodes (14): encapsulate(), MlKemError, validate_public_key(), CloudPublicKey, parse_public_key_response(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+6 more)

### Community 13 - "edge_gateway/crypto/session.py"
Cohesion: 0.13
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 14 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+9 more)

### Community 15 - "LegacyMeasurement"
Cohesion: 0.18
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 16 - "measure_baseline.py"
Cohesion: 0.11
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 17 - "load_config"
Cohesion: 0.15
Nodes (17): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+9 more)

### Community 18 - "test_session.py"
Cohesion: 0.12
Nodes (12): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+4 more)

### Community 19 - "decrypt"
Cohesion: 0.22
Nodes (17): AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad(), _key() (+9 more)

### Community 20 - "test_dispatch.py"
Cohesion: 0.17
Nodes (13): CloudDispatch, _Baseline, _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 22 - "test_gateway_validation.py"
Cohesion: 0.15
Nodes (16): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), assert_rejection(), test_domain_bounds_remain_a_separate_stage(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model() (+8 more)

### Community 23 - "derive_session_key"
Cohesion: 0.13
Nodes (10): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+2 more)

### Community 24 - "test_public_key.py"
Cohesion: 0.12
Nodes (9): decapsulate(), generate_keypair(), MlKemError, PrivateKey, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected() (+1 more)

### Community 25 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 26 - "repository.py"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 27 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 28 - "test_cloud_session_api.py"
Cohesion: 0.15
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 29 - "test_secure_transport.py"
Cohesion: 0.28
Nodes (16): _Cloud, _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+8 more)

### Community 30 - "validate_measurement"
Cohesion: 0.21
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 31 - "build_aad"
Cohesion: 0.16
Nodes (9): AadError, build_aad(), _require_id(), build_secure_envelope(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected() (+1 more)

### Community 32 - "test_gateway_canonical_model.py"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 33 - "test_cloud_aead.py"
Cohesion: 0.19
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 34 - "edge_gateway/config.py"
Cohesion: 0.23
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 35 - "test_cloud_baseline.py"
Cohesion: 0.14
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 37 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 38 - "test_security_logging.py"
Cohesion: 0.18
Nodes (11): _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_metrics_endpoint_exposes_the_same_registry(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback() (+3 more)

### Community 39 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 40 - "test_failure_injection.py"
Cohesion: 0.17
Nodes (11): clock(), _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode() (+3 more)

### Community 41 - "_fixture"
Cohesion: 0.14
Nodes (11): client(), payload(), payload(), database(), measurement(), payload(), cloud(), payload() (+3 more)

### Community 42 - "encoding.py"
Cohesion: 0.24
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 43 - "validate_legacy_measurement"
Cohesion: 0.22
Nodes (6): normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 44 - "test_gateway_correlation.py"
Cohesion: 0.22
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 45 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 46 - "test_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 47 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 49 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 51 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 53 - "json"
Cohesion: 0.32
Nodes (3): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 57 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 60 - "test_gateway_config.py"
Cohesion: 0.33
Nodes (3): test_load_config_accepts_valid_explicit_values(), test_load_config_rejects_invalid_values(), test_load_config_uses_frozen_defaults()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 460 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `edge_gateway/config.py`, `secure_transport.py`, `load_config`, `test_enabled_warning_names_the_mode_and_not_the_seed`, `test_security_logging.py`, `test_failure_injection.py`, `SessionManager`, `edge_gateway/crypto/session.py`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `secure_transport.py`, `load_config`, `CryptoFailureInjector`, `test_security_logging.py`, `SessionManager`, `edge_gateway/crypto/session.py`, `.__init__`, `test_dispatch.py`, `test_session_recovery_is_counted`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `create_app()` connect `load_config` to `test_security_logging.py`, `validate_legacy_measurement`, `LegacyMeasurement`, `PqcMetrics`, `test_gateway_validation.py`, `GatewayErrorCode`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cli.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06876285630326183 - nodes in this community are weakly interconnected._