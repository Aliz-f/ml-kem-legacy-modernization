# Using Grok Build in this repository

This guide is for the teammate operating Grok Build. The authoritative rules
are in [AGENTS.md](../AGENTS.md); [GROK.md](../GROK.md) is the repository-root
entry point to give Grok Build alongside each task.

## Give Grok Build this context

Attach or direct it to these files before it changes the repository:

1. `GROK.md`
2. `AGENTS.md`
3. `Group-Explanation 01.pdf`
4. `Group-Explanation 02.pdf`
5. Any task-specific files, acceptance criteria, and existing tests

Use a concrete task prompt that names the goal, constraints, affected areas,
required checks, and exclusions. Never include secrets or a student's personal
reflection material.

## Recommended prompt wrapper

```text
Work on this repository task: <task>.

Read GROK.md and AGENTS.md first. Follow AGENTS.md as the canonical policy.
Before implementation, read both Group-Explanation PDFs, inspect relevant
existing files, run `uv run ai-history status`, and start one AI-history task
with my exact prompt and agent `Grok Build`. Do not make changes if another
task is awaiting human review, revision, or final verification.

Implement only the requested scope. Treat all generated output as untrusted;
inspect it, run relevant checks, and fix your own findings. Use `uv`; do not
add requirements.txt. Do not expose secrets or write personal reflections.

When work is ready, record factual sanitized results with `ai-history output`
and stop for my human review. Do not invent review decisions or verification.
```

## Human responsibilities

The teammate must reserve a history task ID before parallel work, inspect the
diff and the AI-history entry, and provide the actual review decision. After an
accepted review, the teammate must explicitly confirm final verification before
Grok Build runs `ai-history verify`. See
[DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) for the full branch,
review, revision, and merge process.
