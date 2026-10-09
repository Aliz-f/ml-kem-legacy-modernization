# Reproducible report-evidence methodology

Run identity: `e634db327c04b6e03ee1f319f040a0a6a990ecb2` at `2026-10-09T09:07:49.896906+00:00`.

The collector makes three independent runs per explicit mode, each with 30 sequential valid Legacy measurements. It calls the existing production-client harnesses: Legacy client → disposable loopback Gateway → disposable loopback Cloud → temporary file-backed SQLite. No Compose service, persistent database, or sensor five-second interval is used. Timing begins immediately before the Legacy client sends and ends after its response; `perf_counter()` is used.

A cold secure first message includes public-key retrieval, encapsulation, session request/decapsulation/HKDF/session creation, and secure delivery. Steady-state secure delivery excludes it. The harness has no warm-up, no concurrent load, no injected failures, and zero Legacy/Gateway Cloud retries. Values are local-host observations, not production capacity or network measurements.

Classical successful messages: 90; ML-KEM successful messages: 90. Raw observations and descriptive statistics are in `measurements.csv` and `benchmark_summary.json`.
