# Legacy Device

Run the Legacy Device from the repository root with:

```text
uv run python -m legacy_system.main
```

The process reads its validated settings from the environment, constructs the
device controller, and runs until it receives `SIGINT` (Ctrl+C) or `SIGTERM`.
Both signals stop new work, log shutdown, and let the process exit normally.
The controller closes injected clients during shutdown. The current urllib
client releases each request's resources through its response context manager
and does not expose a separate `close()` operation.

The installed `legacy-device` console script uses the same `main.py`
composition root. The Docker image likewise runs `python -m
legacy_system.main`; its `SIGTERM` follows the same shutdown path.

## Documentation Index

The following component documents record the design, operational procedures, verification evidence, and technical debt for the Legacy Device:

- **[Architecture & Operations Guide](docs/architecture-operations.md)** (Task M1-23): Canonical reference covering module architecture, JSON wire contract, configuration, retry algorithms, failure simulation, and runtime lifecycle.
- **[AI Decisions Register](docs/ai-decisions.md)** (Task M1-24): Representative case examples from Member 1 development, human review modifications, and engineering reflection.
- **[Technical Debt Register](docs/technical-debt.md)** (Task M1-25): Known component limitations, operational trade-offs, retained risks, and future modernization improvements.
- **[Baseline Measurements](docs/baseline-measurements.md)** (Task M1-16): Pre-modernization benchmark data (100-sample latency, payload size distribution, and sequence behavior).
- **[Failure Simulation Validation](docs/failure-simulation.md)** (Task M1-17): System-level validation of all fault injection modes against real HTTP endpoints.
- **[Network Failure Behavior](docs/network-failures.md)** (Task M1-18): Verification of connection refusal, socket timeouts, disconnects, and transient gateway faults.
- **[Failure Injection Safety Safeguards](docs/failure-injection-safety.md)** (Task M1-19): Verification of wire purity, domain model immutability, sequence integrity, and PRNG isolation.
- **[Static Quality Review](docs/static-quality-review.md)** (Task M1-20): Automated AST checks enforcing zero debug calls, no secret exposure, and clean component boundaries.
