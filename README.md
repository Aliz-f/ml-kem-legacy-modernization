# ML-KEM Legacy Modernization

Course project repository containing three components: a simulated legacy system,
an edge gateway, and a cloud service.

The implemented system supports both explicit Classical Baseline Mode and
Modernized ML-KEM Mode across the Legacy Device, Edge Gateway, Cloud Service,
and SQLite storage. The Gateway--Cloud secure path uses ML-KEM-768,
HKDF-SHA-256, and AES-256-GCM under the frozen protocol contract.

Run the three-service test deployment with `docker compose up`; the Legacy
Device sends to the Gateway, which forwards accepted measurements to the Cloud.

## AI-assisted work

[AGENTS.md](AGENTS.md) is the mandatory policy for every AI agent and requires
architecture/roadmap reading before changes. Teammates using Grok Build should
start with [GROK.md](GROK.md) and follow the companion [Grok Build
workflow](docs/GROK_BUILD_WORKFLOW.md).
