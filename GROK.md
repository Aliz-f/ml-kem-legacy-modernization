# Grok Build Instructions

Before making any repository change, read and follow [AGENTS.md](AGENTS.md).
It is the canonical AI-agent policy for this project; if these instructions
conflict with it, `AGENTS.md` wins. Read the architecture, protocol, roadmap,
and member-task documents that AGENTS.md requires, identify frozen contracts
and the current phase, and inspect related code/tests before coding.
Architecture and protocol documents are implementation constraints, not
optional background reading.

## Required operating rules

- Before a new significant task, read `Group-Explanation 01.pdf` and
  `Group-Explanation 02.pdf`, inspect relevant existing work, and run
  `uv run ai-history status`.
- Do not start work when another AI-history task awaits human review, revision,
  or final verification, unless a human explicitly resumes the relevant task.
- Start exactly one task with `uv run ai-history start` before implementation.
  Record the human request faithfully and identify the agent as `Grok Build`.
- Treat generated code and advice as untrusted. Inspect it continuously and
  complete the requested implementation, documentation, tests, and relevant
  checks before asking for human review.
- Use the repository's `uv` workflow. Do not add `requirements.txt`.
- Never put secrets, credentials, tokens, private keys, shared secrets, or
  `.env` contents in prompts, AI-history records, logs, commits, or reviews.
- Never write a student's personal reflection, experiences, or feelings.
- Do not change a frozen endpoint, schema, status code, crypto/KDF/AAD/nonce,
  retry/session/fallback rule, or storage mapping because current code differs.
  Report the mismatch and use AGENTS.md's required architecture-change order.
- Preserve the frozen protocol, exact Legacy `400`/`422` mapping, same-envelope
  ordinary retry, fail-closed secure mode, and no-counter/no-replay-window v1
  constraints summarized in AGENTS.md.

## Mandatory review gate

After all work and checks are complete, run `uv run ai-history output` with
only factual, sanitized results, then stop. Ask a human to provide:

```text
Problems Found: ...
Decision: Accepted | Modified | Rejected
Requested Modifications: ... (required when Modified)
```

Only record the human's actual review. For `Modified`, implement the requested
changes, rerun relevant checks, run `uv run ai-history revision`, and stop for
another review. After `Accepted`, obtain explicit final human verification and
run `uv run ai-history verify`. Automated checks and AI review do not replace
human review or verification.

## Task startup template

Use this sequence after receiving a task:

```bash
uv run ai-history status
uv run ai-history start \
  --title "Short human-readable title" \
  --task "Required change and boundaries." \
  --prompt "Exact instruction supplied to Grok Build." \
  --agent "Grok Build"
```

For the complete commands, branch workflow, checks, review protocol, and
parallel-task guidance, read [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md).
