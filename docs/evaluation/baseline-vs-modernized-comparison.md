# Baseline versus Modernized Mode comparison

M5-70 uses one matched, live workload for both explicit modes. Generate the
comparison table with real observations instead of copying fixed numbers:

```bash
uv run python scripts/measure_mode_comparison.py --samples 10
```

The JSON `comparison` object supplies this table from that invocation:

| Metric | Classical | ML-KEM |
| --- | --- | --- |
| First-message latency | `first_message_latency_ms.classical` | `first_message_latency_ms.mlkem` |
| Steady-state latency | `steady_state_latency_ms.classical` | `steady_state_latency_ms.mlkem` |
| Gateway→Cloud payload size | `gateway_to_cloud_payload_bytes.classical` | `gateway_to_cloud_payload_bytes.mlkem` |
| Session setup | not applicable | `session_setup.mlkem` |
| Successful messages | `successful_messages.classical` | `successful_messages.mlkem` |
| Failed messages | `failed_messages.classical` | `failed_messages.mlkem` |
| Storage success | `storage_success.classical` | `storage_success.mlkem` |

Both runs use the identical Legacy payload sequence, message count, local
loopback HTTP deployment, temporary SQLite reset, no injected faults, and
zero retries. The ML-KEM first message must remain separate because it includes
session establishment. The output is an observation for its recorded host and
versions, not a ranking or production capacity estimate.
