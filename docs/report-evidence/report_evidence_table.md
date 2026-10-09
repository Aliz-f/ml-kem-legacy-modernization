# Evidence index

| Category | Collected evidence | Qualification |
| --- | --- | --- |
| Reproducible performance | `benchmark_summary.json`, `measurements.csv`, `methodology.md` | 3 × 30 local loopback messages per mode; 3 cold sessions only |
| Environment | `environment.json` | Docker/CPU/RAM are additionally recorded in task output, not automatically sampled by collector |
| Implementation state | `implementation_inventory.md` | Static inspection plus selected integration tests |
| Security/fault tests | `security_results.json` | 19 selected tests passed; not all scenarios rerun |
| Metrics | `metrics_snapshot.txt` | Actual values asserted by live integration tests; no external monitoring stack |
| Risks/governance | `technical_debt.md`, `docs/technical-debt.md`, `docs/risk-register.md` | Course prototype limitations remain |
