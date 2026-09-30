# Shared Graphify code graph

Graphify provides a shared code graph that helps contributors and agents narrow
repository exploration before reading implementation details. It is a developer
tool only: it is not part of any service runtime, Docker image, protocol, or
cryptographic path.

## Use

`uv sync` installs the pinned Graphify development dependency. Query the shared
graph from the repository root:

```bash
uv run graphify query "Which modules implement the Gateway-to-Cloud secure path?"
uv run graphify path "SessionManager" "SecureEnvelope"
uv run graphify explain "Measurement"
```

The committed artifacts are:

```text
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
graphify-out/manifest.json
```

## Automation

The `Graphify shared code graph` GitHub Actions workflow refreshes these
artifacts when a same-repository pull request changes graph-relevant code or
Python package manifests. It runs local code extraction followed by local
clustering, commits only changed graph artifacts to the pull request branch,
then verifies a second refresh produces no diff.

Do not run Graphify installers, Graphify hook installers, or hand-edit generated
artifacts. If CI reports that an artifact is stale, rerun the workflow by pushing
the applicable branch; do not repair generated JSON manually.

## Safety and authority

Extraction always uses `--code-only --no-viz`, so it is local AST analysis and
does not invoke a model or send source files to an API. `.graphifyignore` adds
defence-in-depth exclusions for secrets and machine-local data.

Graph relationships can be inferred and are not a source of truth. Follow
`AGENTS.md`: read the required frozen architecture documents, inspect direct
source and tests, and complete the normal AI-history and human-review workflow.
