# Verification round 2 evidence index

| Area | Result | Primary evidence |
| --- | --- | --- |
| Matched performance | 3 × 30 messages/mode; first observation excluded symmetrically (n=87/mode); 30 cold lifecycles | `benchmark_summary.json`, `measurements.csv`, `methodology.md` |
| Security/failure tests | AAD, sessions, storage, outage, logging, retry and Compose restart tests passed | `security_results.json`, `metrics_snapshot.txt`, `test_suite_results.json` |
| Required checks | frozen sync, Ruff, AI-history check and Compose configuration passed | `test_suite_results.json` and task history |
| Full regression | 1,726 collected; monolithic completion blocked by external command window; 666 distinct bounded tests passed | `test_suite_results.json` |
| Scope | local loopback/temporary SQLite performance; Compose only for restart verification; no Docker/WAN aggregate | `methodology.md`, `benchmark_summary.json` |
