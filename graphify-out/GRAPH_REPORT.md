# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 769 nodes · 1755 edges · 39 communities (22 shown, 17 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 203 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_symmetric.py
- cli.py
- edge_gateway/config.py
- CanonicalMeasurement
- SessionManager
- FailureInjector
- test_sensor.py
- test_session.py
- load_config
- test_cloud_storage.py
- test_gateway_models.py
- test_public_key_client.py
- load_config
- StorageError
- session_client.py
- cloud_service/app.py
- test_kdf.py
- session.py
- ConfigurationError
- encoding.py
- refresh_graphify.py
- test_public_key.py
- cloud_server
- _RejectRedirect
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 33 edges
2. `FailureInjector` - 30 edges
3. `MeasurementRepository` - 25 edges
4. `create_app()` - 23 edges
5. `load_config()` - 23 edges
6. `CanonicalMeasurement` - 22 edges
7. `SessionManager` - 19 edges
8. `create_app()` - 19 edges
9. `make_payload()` - 19 edges
10. `StorageError` - 18 edges

## Surprising Connections (you probably didn't know these)
- `test_invalid_metadata_and_domain_are_rejected()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_concurrent_repository_access()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_database_uniqueness_is_a_conflict_not_idempotent_success()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_list_limit_filter_and_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_parameterized_identifiers()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py

## Import Cycles
- None detected.

## Communities (39 total, 17 thin omitted)

### Community 0 - "test_symmetric.py"
Cohesion: 0.05
Nodes (47): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number() (+39 more)

### Community 1 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "edge_gateway/config.py"
Cohesion: 0.06
Nodes (32): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+24 more)

### Community 3 - "CanonicalMeasurement"
Cohesion: 0.07
Nodes (25): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), MeasurementValidationError, validate_measurement(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps() (+17 more)

### Community 4 - "SessionManager"
Cohesion: 0.06
Nodes (16): encapsulate(), MlKemError, validate_public_key(), SecureSession, SessionEstablishmentError, SessionManager, SessionMetrics, _raw_public_key() (+8 more)

### Community 5 - "FailureInjector"
Cohesion: 0.10
Nodes (25): FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects(), test_failure_rate_zero_never_injects() (+17 more)

### Community 6 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 7 - "test_session.py"
Cohesion: 0.09
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _Handler, _manager(), _stamp(), test_close_wipes_the_session_key() (+6 more)

### Community 8 - "load_config"
Cohesion: 0.13
Nodes (21): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+13 more)

### Community 9 - "test_cloud_storage.py"
Cohesion: 0.12
Nodes (19): StoredMeasurement, MeasurementRepository, _stored(), test_closed_database_errors_are_safe(), test_concurrent_repository_access(), test_corrupted_stored_row_is_translated(), test_database_uniqueness_is_a_conflict_not_idempotent_success(), test_exact_stored_model_mapping() (+11 more)

### Community 10 - "test_gateway_models.py"
Cohesion: 0.16
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 11 - "test_public_key_client.py"
Cohesion: 0.11
Nodes (15): _endpoint(), fetch_public_key(), PublicKeyTransportError, _body(), _Handler, _public_key(), test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+7 more)

### Community 12 - "load_config"
Cohesion: 0.16
Nodes (16): create_app(), lifespan(), main(), StartupError, load_config(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+8 more)

### Community 13 - "StorageError"
Cohesion: 0.14
Nodes (6): Database, StorageConflictError, StorageError, database(), test_missing_parent_and_invalid_file_errors_are_safe(), test_relative_path()

### Community 14 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 15 - "cloud_service/app.py"
Cohesion: 0.15
Nodes (8): health(), ready(), _unavailable(), Config, FailureMode, SecurityMode, test_custom_environment(), test_defaults_do_not_create_database()

### Community 16 - "test_kdf.py"
Cohesion: 0.17
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 17 - "session.py"
Cohesion: 0.17
Nodes (4): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, test_missing_fields_and_non_object_are_rejected()

### Community 18 - "ConfigurationError"
Cohesion: 0.18
Nodes (12): ConfigurationError, integer(), number(), text(), value(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries(), test_invalid_configuration() (+4 more)

### Community 19 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 20 - "refresh_graphify.py"
Cohesion: 0.31
Nodes (3): normalize_artifacts(), refresh_graph(), _without_section()

### Community 21 - "test_public_key.py"
Cohesion: 0.39
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 236 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_session.py`, `test_public_key_client.py`, `session_client.py`, `test_kdf.py`, `session.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `ConfigurationError`, `StorageError`, `cloud_service/app.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `FailureInjector` (e.g. with `test_duplicate_sequence_selection_varies_by_seed()` and `test_duplicate_sequence_uses_previous_sequence_without_rewinding_input()`) actually correct?**
  _`FailureInjector` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `MeasurementRepository` (e.g. with `CanonicalMeasurement` and `Database`) actually correct?**
  _`MeasurementRepository` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_symmetric.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05276907001044932 - nodes in this community are weakly interconnected._