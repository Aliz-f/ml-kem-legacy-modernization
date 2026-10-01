# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1585 nodes · 3937 edges · 81 communities (59 shown, 22 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 550 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- decrypt
- FailureMode
- LegacyMeasurement
- test_session.py
- test_client.py
- FailureMode
- secure_transport.py
- test_sensor.py
- SessionManager
- MeasurementRepository
- create_app
- test_failure_injection.py
- test_dispatch.py
- test_cloud_secure.py
- test_gateway_validation.py
- test_security_logging.py
- test_secure_transport.py
- CanonicalMeasurement
- measure_baseline.py
- cloud_service/app.py
- json
- SessionManager
- load_config
- create_app
- PqcMetrics
- test_public_key_client.py
- GatewayErrorCode
- cli.py
- CryptoFailureInjector
- SecureEnvelope
- derive_session_key
- test_cloud_session_api.py
- load_config
- encapsulate
- HistoryError
- decode_binary
- refresh_graphify.py
- StoredMeasurement
- validate_measurement
- test_cloud_queries.py
- plaintext.py
- cloud_service/crypto/mlkem.py
- test_cloud_baseline.py
- _fixture
- test_cloud_kdf.py
- edge_gateway/crypto/encoding.py
- test_cloud_mlkem.py
- edge_gateway/config.py
- edge_gateway/crypto/session.py
- dispatch.py
- test_cloud_public_key.py
- public_key_client.py
- validate
- envelope_validation.py
- sessions.py
- parse_public_key_response
- _Clock
- _HandshakeHandler
- _Clock
- KdfError
- test_refresh_graphify.py
- test_repository_hygiene.py
- get_measurement
- pytest
- _Handler
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 46 edges
2. `create_app()` - 39 edges
3. `FailureMode` - 38 edges
4. `SecureTransport` - 36 edges
5. `load_config()` - 35 edges
6. `create_app()` - 34 edges
7. `FailureMode` - 33 edges
8. `PqcMetrics` - 32 edges
9. `MeasurementRepository` - 32 edges
10. `FailureInjector` - 31 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_existing_gateway_session_client_over_real_http()` --uses--> `SessionManager`  [INFERRED]
  cloud_service/tests/test_cloud_session_api.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_exact_protocol_fields_and_json_serialization()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_canonical_model.py → cloud_service/tests/test_cloud_aead.py
- `test_protocol_example_and_independent_round_trip()` --calls--> `fields()`  [INFERRED]
  edge_gateway/tests/test_gateway_models.py → cloud_service/tests/test_cloud_aead.py
- `test_gateway_cloud_mlkem_and_kdf_interoperability()` --calls--> `encapsulate()`  [EXTRACTED]
  cloud_service/tests/test_cloud_kdf.py → edge_gateway/src/edge_gateway/crypto/mlkem.py

## Import Cycles
- None detected.

## Communities (81 total, 22 thin omitted)

### Community 0 - "decrypt"
Cohesion: 0.05
Nodes (49): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+41 more)

### Community 1 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 2 - "LegacyMeasurement"
Cohesion: 0.08
Nodes (29): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+21 more)

### Community 3 - "test_session.py"
Cohesion: 0.06
Nodes (22): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+14 more)

### Community 4 - "test_client.py"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "FailureMode"
Cohesion: 0.10
Nodes (23): FailureMode, FailureInjector, FailureSelection, canonical(), config(), envelope(), handshake(), secure_client() (+15 more)

### Community 6 - "secure_transport.py"
Cohesion: 0.09
Nodes (14): build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance() (+6 more)

### Community 7 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 8 - "SessionManager"
Cohesion: 0.10
Nodes (12): SecureSession, SessionAccessError, SessionManager, SessionState, fail(), test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary() (+4 more)

### Community 9 - "MeasurementRepository"
Cohesion: 0.11
Nodes (20): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+12 more)

### Community 10 - "create_app"
Cohesion: 0.08
Nodes (18): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), KeyService (+10 more)

### Community 11 - "test_failure_injection.py"
Cohesion: 0.09
Nodes (18): clock(), SessionState, _aad(), _injector(), measurement_url(), _MeasurementCloud, _plaintext(), _Sessions (+10 more)

### Community 12 - "test_dispatch.py"
Cohesion: 0.14
Nodes (14): CloudDispatch, _Baseline, _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 13 - "test_cloud_secure.py"
Cohesion: 0.16
Nodes (25): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+17 more)

### Community 14 - "test_gateway_validation.py"
Cohesion: 0.14
Nodes (19): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), assert_rejection() (+11 more)

### Community 15 - "test_security_logging.py"
Cohesion: 0.10
Nodes (14): _Sessions, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_metrics_endpoint_exposes_the_same_registry() (+6 more)

### Community 16 - "test_secure_transport.py"
Cohesion: 0.17
Nodes (19): _Cloud, _error(), _Handler, _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried() (+11 more)

### Community 17 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 18 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 19 - "cloud_service/app.py"
Cohesion: 0.15
Nodes (5): SecurityMode, public_key(), _unavailable(), baseline_measurement(), _error()

### Community 20 - "json"
Cohesion: 0.13
Nodes (8): AadError, build_aad(), AeadError, decrypt(), _DroppedResponse, _error(), _ingest(), secure_measurement()

### Community 21 - "SessionManager"
Cohesion: 0.14
Nodes (4): log_security(), SecureSession, SessionEstablishmentError, SessionManager

### Community 22 - "load_config"
Cohesion: 0.17
Nodes (16): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), test_custom_environment() (+8 more)

### Community 23 - "create_app"
Cohesion: 0.13
Nodes (13): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+5 more)

### Community 25 - "test_public_key_client.py"
Cohesion: 0.14
Nodes (15): fetch_public_key(), PublicKeyRejected, _body(), cloud_server(), _public_key(), _Response, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+7 more)

### Community 26 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 27 - "cli.py"
Cohesion: 0.28
Nodes (16): start(), state_name(), Status, active_task(), atomic_write(), find_task(), git_changes(), load_state() (+8 more)

### Community 28 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 30 - "SecureEnvelope"
Cohesion: 0.20
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 31 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 32 - "test_cloud_session_api.py"
Cohesion: 0.16
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 33 - "load_config"
Cohesion: 0.15
Nodes (13): load_config(), test_cli_uses_configured_server_settings_and_loads_once(), settings(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration() (+5 more)

### Community 34 - "encapsulate"
Cohesion: 0.18
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 35 - "HistoryError"
Cohesion: 0.23
Nodes (14): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+6 more)

### Community 36 - "decode_binary"
Cohesion: 0.19
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 37 - "refresh_graphify.py"
Cohesion: 0.13
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 38 - "StoredMeasurement"
Cohesion: 0.17
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 39 - "validate_measurement"
Cohesion: 0.23
Nodes (11): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+3 more)

### Community 40 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (12): test_unrelated_record_id_collision_is_not_idempotent_success(), client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail() (+4 more)

### Community 41 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 42 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 43 - "test_cloud_baseline.py"
Cohesion: 0.15
Nodes (8): client(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 44 - "_fixture"
Cohesion: 0.13
Nodes (12): payload(), payload(), client(), database(), measurement(), payload(), cloud(), values() (+4 more)

### Community 45 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 46 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 47 - "test_cloud_mlkem.py"
Cohesion: 0.15
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 48 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 50 - "dispatch.py"
Cohesion: 0.18
Nodes (3): GatewayConfig, BaselineTransport, DispatchMetrics

### Community 51 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 52 - "public_key_client.py"
Cohesion: 0.20
Nodes (4): _endpoint(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey

### Community 53 - "validate"
Cohesion: 0.39
Nodes (10): validate(), run(), start(), test_cannot_start_while_active_or_corrupt_state(), test_first_id_slug_and_multiline_prompt(), test_full_acceptance_lifecycle(), test_modified_requires_changes_and_revision_preserves_rounds(), test_rejection_and_second_task() (+2 more)

### Community 54 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 55 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 56 - "parse_public_key_response"
Cohesion: 0.33
Nodes (6): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 57 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 59 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 60 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 61 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 63 - "get_measurement"
Cohesion: 0.60
Nodes (3): _error(), get_measurement(), list_measurements()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 489 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `secure_transport.py`, `test_dispatch.py`, `test_security_logging.py`, `edge_gateway/crypto/session.py`, `dispatch.py`, `SessionManager`, `create_app`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `SecureSession` connect `SessionManager` to `secure_transport.py`, `test_failure_injection.py`, `test_dispatch.py`, `test_security_logging.py`, `test_secure_transport.py`, `edge_gateway/crypto/session.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `FailureSelection`) actually correct?**
  _`FailureMode` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `decrypt` be split into smaller, more focused modules?**
  _Cohesion score 0.05286006128702758 - nodes in this community are weakly interconnected._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.07191780821917808 - nodes in this community are weakly interconnected._