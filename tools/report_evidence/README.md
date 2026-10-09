# Report-evidence collector

Run `UV_CACHE_DIR=/tmp/mlkem-uv-cache uv run python tools/report_evidence/run_evaluation.py` from the repository root. It creates sanitized, reproducible performance evidence in `docs/report-evidence/` using only temporary loopback services and SQLite databases. It does not run Docker or alter development data.

The collector records raw latency observations and descriptive statistics. It intentionally does not claim unmeasured resource use, WAN performance, public-key/session wire sizes, or the requested 20 cold-session observations.
