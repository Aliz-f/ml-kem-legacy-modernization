# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 646 nodes · 1487 edges · 34 communities (19 shown, 15 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 159 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `86f6e18e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_symmetric.py
- load_config
- test_cloud_storage.py
- CanonicalMeasurement
- cli.py
- test_sensor.py
- test_session.py
- load_config
- edge_gateway/config.py
- MlKemError
- session_client.py
- encoding.py
- test_kdf.py
- public_key.py
- test_public_key_client.py
- session.py
- fetch_public_key
- test_cli.py
- test_public_key.py
- SessionManager
- test_crypto_failure_is_classified_and_recorded
- SessionMetrics
- _Handler
- _RejectRedirect
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 33 edges
2. `MeasurementRepository` - 25 edges
3. `create_app()` - 23 edges
4. `load_config()` - 23 edges
5. `CanonicalMeasurement` - 22 edges
6. `SessionManager` - 19 edges
7. `StorageError` - 18 edges
8. `fetch_public_key()` - 18 edges
9. `Database` - 17 edges
10. `validate_measurement()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `test_full_acceptance_lifecycle()` --calls--> `load_state()`  [EXTRACTED]
  tests/ai_history/test_cli.py → src/ai_history/storage.py
- `test_full_acceptance_lifecycle()` --calls--> `validate()`  [EXTRACTED]
  tests/ai_history/test_cli.py → src/ai_history/storage.py
- `test_validation_rejects_duplicate_metadata_and_mismatched_filename()` --calls--> `validate()`  [EXTRACTED]
  tests/ai_history/test_cli.py → src/ai_history/storage.py
- `test_validation_rejects_unresolved_conflict_markers()` --calls--> `validate()`  [EXTRACTED]
  tests/ai_history/test_cli.py → src/ai_history/storage.py
- `test_concurrent_repository_access()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py

## Import Cycles
- None detected.

## Communities (34 total, 15 thin omitted)

### Community 0 - "test_symmetric.py"
Cohesion: 0.06
Nodes (46): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number() (+38 more)

### Community 1 - "load_config"
Cohesion: 0.07
Nodes (36): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), Config (+28 more)

### Community 2 - "test_cloud_storage.py"
Cohesion: 0.07
Nodes (25): Database, StorageConflictError, StorageError, StoredMeasurement, MeasurementRepository, _stored(), database(), test_closed_database_errors_are_safe() (+17 more)

### Community 3 - "CanonicalMeasurement"
Cohesion: 0.08
Nodes (25): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), MeasurementValidationError, validate_measurement(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps() (+17 more)

### Community 4 - "cli.py"
Cohesion: 0.14
Nodes (31): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+23 more)

### Community 5 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 6 - "test_session.py"
Cohesion: 0.08
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _Handler, _manager(), _stamp(), test_close_wipes_the_session_key() (+6 more)

### Community 7 - "load_config"
Cohesion: 0.12
Nodes (21): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+13 more)

### Community 8 - "edge_gateway/config.py"
Cohesion: 0.17
Nodes (16): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), GatewayConfig, _integer(), load_config(), _non_negative_int() (+8 more)

### Community 9 - "MlKemError"
Cohesion: 0.16
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 10 - "session_client.py"
Cohesion: 0.18
Nodes (9): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+1 more)

### Community 11 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 12 - "test_kdf.py"
Cohesion: 0.22
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 13 - "public_key.py"
Cohesion: 0.19
Nodes (4): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, test_missing_fields_and_non_object_are_rejected()

### Community 14 - "test_public_key_client.py"
Cohesion: 0.18
Nodes (8): _body(), cloud_server(), _public_key(), _Response, test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key(), test_invalid_json_is_not_a_transport_retry(), test_oversized_body_is_rejected()

### Community 16 - "fetch_public_key"
Cohesion: 0.23
Nodes (8): _endpoint(), fetch_public_key(), PublicKeyTransportError, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable(), test_http_status_is_classified(), test_redirect_is_not_followed(), test_timeout_is_retryable()

### Community 17 - "test_cli.py"
Cohesion: 0.42
Nodes (9): run(), start(), test_cannot_start_while_active_or_corrupt_state(), test_first_id_slug_and_multiline_prompt(), test_full_acceptance_lifecycle(), test_modified_requires_changes_and_revision_preserves_rounds(), test_rejection_and_second_task(), test_validation_rejects_duplicate_metadata_and_mismatched_filename() (+1 more)

### Community 18 - "test_public_key.py"
Cohesion: 0.33
Nodes (4): _payload(), _public_key(), test_contract_violations_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 20 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 204 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_session.py`, `MlKemError`, `session_client.py`, `public_key.py`, `session.py`, `fetch_public_key`, `test_crypto_failure_is_classified_and_recorded`, `SessionMetrics`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `test_cloud_storage.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `CanonicalMeasurement` connect `CanonicalMeasurement` to `test_cloud_storage.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `MeasurementRepository` (e.g. with `CanonicalMeasurement` and `Database`) actually correct?**
  _`MeasurementRepository` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `CanonicalMeasurement` (e.g. with `StoredMeasurement` and `MeasurementRepository`) actually correct?**
  _`CanonicalMeasurement` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._