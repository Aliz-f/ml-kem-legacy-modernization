# Final evidence methodology

Generated at `2026-10-09T10:07:14.360160+00:00` from preserved round-two raw observations. The original exact benchmark collection start/end time was **NOT RECORDED**; its generated timestamp and source commit are retained in the source artifact.

## Environment and architecture

The experiment used one local Linux machine, Python 3.12, Cryptography ML-KEM-768, FastAPI/Uvicorn, disposable loopback Legacy client → Gateway ASGI app → Cloud ASGI app → temporary SQLite. It is not a WAN, Docker-network, load, or production benchmark.

## Workload and timing

Three independent runs per mode sent 30 valid sequential logical measurements with no concurrent load or intentionally injected failure. Timing began immediately before the Legacy HTTP request and ended when the Legacy client received its final response. The first observation of every run was excluded only from the primary steady-state comparison; all raw observations remain in round-two CSV.

## Cold sessions and statistics

Thirty independent service/session lifecycles measured cold secure establishment; they are not independent physical machines. Statistics are mean, median, sample standard deviation, minimum, maximum, count, and nearest-rank p95 (`ceil(0.95*n)`). No significance test is claimed.

## Limits

Single-machine loopback, sequential delivery, only three independent steady-state runs, no WAN/load/CPU/RAM study, finite security tests, and no universal production claim limit interpretation. The pooled overhead is an observation, not a stable universal penalty.
