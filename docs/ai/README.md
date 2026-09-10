# AI development history

AI-generated code is untrusted until students review it. This directory records
significant AI-assisted work using one Markdown file per task in `history/` and
machine-readable active state in `.state.json`. It records summaries, paths, and
sanitized results only: never secrets, keys, tokens, credentials, `.env` values,
source copies, or Git diffs.

Lifecycle: `In Progress` → `Awaiting Human Review`; human `Accepted` decisions
move to `Awaiting Final Verification` and then `Complete`, `Modified` decisions
lead to a recorded revision and another review, and `Rejected` closes the task.
Automated checks never replace human review or final human-confirmed verification.

Use `uv run ai-history --help` for commands including `start`, `output`,
`review`, `revision`, `verify`, `status`, `show`, `list`, and `check`. Compatible
agents follow `AGENTS.md`; the CLI and CI validate the process but cannot force
every external AI product to comply.
