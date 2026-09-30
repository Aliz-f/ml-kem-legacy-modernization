# Graph Report - ml-kem-legacy-modernization  (2026-10-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1658 nodes · 4005 edges · 96 communities (59 shown, 37 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 526 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_legacy_compatibility.py
- validate_measurement
- FailureMode
- LegacyMeasurement
- cli.py
- test_crypto_failures.py
- test_dispatch.py
- json
- MeasurementRepository
- SecureTransport
- test_sensor.py
- cloud_service/app.py
- pytest
- load_config
- secure_transport.py
- SecureSession
- create_app
- SessionManager
- CryptoFailureInjector
- encapsulate
- create_app
- PqcMetrics
- GatewayErrorCode
- load_config
- test_secure_message_tamper.py
- test_cloud_session_api.py
- session_client.py
- test_secure_shutdown.py
- test_secure_transport.py
- cloud_service/crypto/session.py
- StoredMeasurement
- test_session.py
- test_cloud_baseline.py
- build_aad
- Policy
- derive_session_key
- test_cloud_queries.py
- decode_binary
- plaintext.py
- test_gateway_validation.py
- cloud_service/crypto/mlkem.py
- decrypt
- edge_gateway/app.py
- encrypt
- test_cloud_aead.py
- edge_gateway/validation.py
- test_gateway_cloud_secure.py
- test_gateway_crypto_image.py
- SessionManager
- refresh_graphify.py
- test_refresh_graphify.py
- test_cloud_public_key.py
- test_gateway_correlation.py
- SessionEstablishmentError
- CloudHarness
- sessions.py
- test_secure_envelope.py
- _Clock
- test_protocol_version_999_is_rejected_before_secure_processing
- _Clock
- cloud_service/crypto/symmetric.py
- test_public_key.py
- test_legacy_values_survive_secure_delivery
- test_repository_hygiene.py
- _Handler
- _Handler
- Clock
- _measurement
- test_valid_encapsulation_matches_shared_secret_and_hkdf
- test_shared_integration_assets.py
- KeyService
- cloud_server
- _Handler
- _Handler
- KdfError
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `SecureTransport` - 41 edges
2. `load_config()` - 41 edges
3. `load_config()` - 38 edges
4. `SessionManager` - 36 edges
5. `create_app()` - 36 edges
6. `create_app()` - 36 edges
7. `FailureMode` - 33 edges
8. `SecureTransportError` - 33 edges
9. `PqcMetrics` - 32 edges
10. `MeasurementRepository` - 32 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `_receive()` --uses--> `MeasurementValidationError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → cloud_service/src/cloud_service/validation.py
- `test_legacy_values_survive_secure_delivery()` --uses--> `Sensor`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → legacy_system/src/legacy_system/sensor.py

## Import Cycles
- None detected.

## Communities (96 total, 37 thin omitted)

### Community 0 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (35): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+27 more)

### Community 1 - "validate_measurement"
Cohesion: 0.05
Nodes (32): public_key(), _unavailable(), _error(), get_measurement(), list_measurements(), baseline_measurement(), _error(), CanonicalMeasurement (+24 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "LegacyMeasurement"
Cohesion: 0.07
Nodes (32): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization() (+24 more)

### Community 4 - "cli.py"
Cohesion: 0.13
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 5 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 6 - "test_dispatch.py"
Cohesion: 0.08
Nodes (17): BaselineTransport, CloudDispatch, DispatchMetrics, _Baseline, cloud(), _config(), _Handler, _measurement() (+9 more)

### Community 7 - "json"
Cohesion: 0.10
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _body() (+11 more)

### Community 8 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 9 - "SecureTransport"
Cohesion: 0.12
Nodes (12): SecureEnvelope, _dump(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+4 more)

### Community 10 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 11 - "cloud_service/app.py"
Cohesion: 0.09
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 12 - "pytest"
Cohesion: 0.08
Nodes (7): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 13 - "load_config"
Cohesion: 0.14
Nodes (18): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+10 more)

### Community 15 - "SecureSession"
Cohesion: 0.10
Nodes (13): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+5 more)

### Community 16 - "create_app"
Cohesion: 0.10
Nodes (17): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+9 more)

### Community 18 - "CryptoFailureInjector"
Cohesion: 0.10
Nodes (4): CryptoFailureInjector, _endpoint(), _SessionRecovery, test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 19 - "encapsulate"
Cohesion: 0.14
Nodes (13): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh() (+5 more)

### Community 20 - "create_app"
Cohesion: 0.13
Nodes (17): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+9 more)

### Community 21 - "PqcMetrics"
Cohesion: 0.09
Nodes (4): _Duration, PqcMetrics, test_metrics_endpoint_exposes_the_same_registry(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 22 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 23 - "load_config"
Cohesion: 0.21
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 24 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 25 - "test_cloud_session_api.py"
Cohesion: 0.14
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 26 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 27 - "test_secure_shutdown.py"
Cohesion: 0.14
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 28 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (16): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+8 more)

### Community 29 - "cloud_service/crypto/session.py"
Cohesion: 0.13
Nodes (10): SecureSession, SessionAccessError, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed() (+2 more)

### Community 30 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 31 - "test_session.py"
Cohesion: 0.15
Nodes (10): SessionState, _manager(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active() (+2 more)

### Community 32 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (10): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+2 more)

### Community 33 - "build_aad"
Cohesion: 0.16
Nodes (9): AadError, build_aad(), _require_id(), build_secure_envelope(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected() (+1 more)

### Community 34 - "Policy"
Cohesion: 0.12
Nodes (8): cloud(), _install(), secure_measurements(), Policy, _reject(), _require_envelope(), SecureRejection, test_production_cloud_app_has_no_secure_measurement_route()

### Community 35 - "derive_session_key"
Cohesion: 0.19
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 36 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 37 - "decode_binary"
Cohesion: 0.21
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 38 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 39 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 40 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 41 - "decrypt"
Cohesion: 0.19
Nodes (7): test_vendor_error_diagnostics_are_suppressed(), main(), AeadError, decrypt(), _require_bytes(), _require_key(), _require_nonce()

### Community 42 - "edge_gateway/app.py"
Cohesion: 0.15
Nodes (6): get_config(), _logging_level(), main(), GatewayConfig, test_from_config_uses_gateway_failure_settings(), test_cli_uses_configured_server_settings_and_loads_once()

### Community 43 - "encrypt"
Cohesion: 0.37
Nodes (12): encrypt(), _aad(), _key(), _plaintext(), test_authentication_failure_does_not_return_plaintext(), test_independent_cloud_aad_authenticates_and_each_field_change_fails(), test_invalid_key_and_nonce_lengths_are_rejected(), test_keys_and_plaintext_are_not_logged() (+4 more)

### Community 44 - "test_cloud_aead.py"
Cohesion: 0.27
Nodes (10): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+2 more)

### Community 45 - "edge_gateway/validation.py"
Cohesion: 0.18
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 46 - "test_gateway_cloud_secure.py"
Cohesion: 0.17
Nodes (9): _seal(), test_malformed_mlkem_ciphertext_is_rejected(), test_simulated_decapsulation_failure_leaves_no_session(), test_tampered_secure_message_is_rejected(), test_unsupported_protocol_version_is_rejected(), unreachable(), test_versioned_public_key_retrieval(), test_wrong_gateway_ownership_is_rejected_before_decrypt() (+1 more)

### Community 47 - "test_gateway_crypto_image.py"
Cohesion: 0.20
Nodes (5): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 49 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 50 - "test_refresh_graphify.py"
Cohesion: 0.20
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 51 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 52 - "test_gateway_correlation.py"
Cohesion: 0.24
Nodes (5): baseline_headers(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 53 - "SessionEstablishmentError"
Cohesion: 0.18
Nodes (5): KdfError, SessionEstablishmentError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 54 - "CloudHarness"
Cohesion: 0.24
Nodes (9): CloudHarness, _deliver(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope(), test_expired_session_returns_409_and_recovers_once(), test_invalid_session_returns_409_and_recovers_once(), test_local_session_expiry_reestablishes_before_the_next_send(), test_secure_envelope_round_trip_stores_canonical_measurement() (+1 more)

### Community 55 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 56 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 57 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 58 - "test_protocol_version_999_is_rejected_before_secure_processing"
Cohesion: 0.22
Nodes (4): AadError, build_aad(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 59 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 62 - "test_public_key.py"
Cohesion: 0.48
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 70 - "_measurement"
Cohesion: 0.33
Nodes (5): _measurement(), test_duplicate_sequence_is_stored_once(), send_twice(), test_one_handshake_is_reused_for_three_measurements(), send_three()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 550 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `test_dispatch.py`, `SecureTransport`, `edge_gateway/app.py`, `secure_transport.py`, `SecureSession`, `SessionManager`, `CryptoFailureInjector`, `create_app`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `StorageError` connect `MeasurementRepository` to `create_app`, `validate_measurement`, `cloud_service/app.py`, `StoredMeasurement`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `test_legacy_compatibility.py`, `LegacyMeasurement`, `test_gateway_validation.py`, `edge_gateway/app.py`, `edge_gateway/validation.py`, `SecureSession`, `SessionManager`, `PqcMetrics`, `GatewayErrorCode`, `load_config`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `SessionManager` (e.g. with `test_existing_gateway_session_client_over_real_http()` and `CryptoFailureInjector`) actually correct?**
  _`SessionManager` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_legacy_compatibility.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05369369369369369 - nodes in this community are weakly interconnected._