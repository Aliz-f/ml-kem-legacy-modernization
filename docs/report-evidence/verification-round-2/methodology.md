# Verification round 2 methodology

Command: `UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python tools/report_evidence/run_round_2.py`.

The primary comparison excludes exactly one first observation from every independent 30-message run in both modes (3 × 29 = 87 each); raw first-message observations remain in `measurements.csv`. Cold-session metrics use 30 independent two-message service/session lifecycles. No observations were deleted as outliers.

Timing, payload, lifecycle, and scope limitations are machine-readable in `benchmark_summary.json`.
