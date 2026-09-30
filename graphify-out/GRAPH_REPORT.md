# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 854 nodes · 1969 edges · 51 communities (28 shown, 23 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 262 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_symmetric.py
- cli.py
- CanonicalMeasurement
- LegacyMeasurement
- FailureMode
- test_sensor.py
- load_config
- test_public_key_client.py
- load_config
- test_session.py
- create_app
- GatewayErrorCode
- load_config
- test_cloud_storage.py
- MlKemError
- create_app
- SessionManager
- cloud_service/app.py
- session_client.py
- json
- test_gateway_validation.py
- encoding.py
- StoredMeasurement
- test_kdf.py
- edge_gateway/app.py
- parse_legacy_measurement
- parse_public_key_response
- public_key.py
- session.py
- test_crypto_failure_is_classified_and_recorded
- _Handler
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `FailureMode` - 33 edges
2. `load_config()` - 33 edges
3. `FailureInjector` - 31 edges
4. `create_app()` - 31 edges
5. `load_config()` - 27 edges
6. `MeasurementRepository` - 25 edges
7. `create_app()` - 23 edges
8. `load_config()` - 23 edges
9. `CanonicalMeasurement` - 22 edges
10. `LegacyMeasurement` - 21 edges

## Surprising Connections (you probably didn't know these)
- `test_invalid_metadata_and_domain_are_rejected()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_relative_path()` --uses--> `Database`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → cloud_service/src/cloud_service/storage/database.py
- `test_concurrent_repository_access()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_database_uniqueness_is_a_conflict_not_idempotent_success()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_list_limit_filter_and_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py

## Import Cycles
- None detected.

## Communities (51 total, 23 thin omitted)

### Community 0 - "test_symmetric.py"
Cohesion: 0.06
Nodes (46): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number() (+38 more)

### Community 1 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "CanonicalMeasurement"
Cohesion: 0.07
Nodes (24): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), MeasurementValidationError, validate_measurement(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps() (+16 more)

### Community 3 - "LegacyMeasurement"
Cohesion: 0.09
Nodes (27): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values() (+19 more)

### Community 4 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 5 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 6 - "load_config"
Cohesion: 0.14
Nodes (18): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+10 more)

### Community 7 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _body(), cloud_server(), _public_key(), _Response, test_cloud_url_and_timeout_are_validated() (+8 more)

### Community 8 - "load_config"
Cohesion: 0.15
Nodes (20): Config, ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration() (+12 more)

### Community 9 - "test_session.py"
Cohesion: 0.11
Nodes (12): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+4 more)

### Community 10 - "create_app"
Cohesion: 0.11
Nodes (18): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+10 more)

### Community 11 - "GatewayErrorCode"
Cohesion: 0.11
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 12 - "load_config"
Cohesion: 0.19
Nodes (15): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+7 more)

### Community 13 - "test_cloud_storage.py"
Cohesion: 0.15
Nodes (18): MeasurementRepository, database(), measurement(), test_closed_database_errors_are_safe(), test_concurrent_repository_access(), test_corrupted_stored_row_is_translated(), test_database_uniqueness_is_a_conflict_not_idempotent_success(), test_invalid_repository_limits() (+10 more)

### Community 14 - "MlKemError"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 15 - "create_app"
Cohesion: 0.14
Nodes (16): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+8 more)

### Community 16 - "SessionManager"
Cohesion: 0.12
Nodes (3): SecureSession, SessionEstablishmentError, SessionManager

### Community 17 - "cloud_service/app.py"
Cohesion: 0.14
Nodes (3): Database, StorageConflictError, StorageError

### Community 18 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 19 - "json"
Cohesion: 0.13
Nodes (7): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clear_incremental_state_preserves_only_shared_artifacts(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 20 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 21 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 22 - "StoredMeasurement"
Cohesion: 0.20
Nodes (5): StoredMeasurement, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 23 - "test_kdf.py"
Cohesion: 0.22
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 24 - "edge_gateway/app.py"
Cohesion: 0.16
Nodes (5): get_config(), _logging_level(), main(), GatewayConfig, test_cli_uses_configured_server_settings_and_loads_once()

### Community 25 - "parse_legacy_measurement"
Cohesion: 0.18
Nodes (8): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 26 - "parse_public_key_response"
Cohesion: 0.26
Nodes (7): parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 29 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 259 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_public_key_client.py`, `test_session.py`, `MlKemError`, `session_client.py`, `parse_public_key_response`, `session.py`, `test_crypto_failure_is_classified_and_recorded`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `LegacyMeasurement`, `GatewayErrorCode`, `load_config`, `test_gateway_validation.py`, `edge_gateway/app.py`, `parse_legacy_measurement`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `cloud_service/app.py`, `create_app`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `FailureInjector` (e.g. with `FailureMode` and `test_duplicate_sequence_selection_varies_by_seed()`) actually correct?**
  _`FailureInjector` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._