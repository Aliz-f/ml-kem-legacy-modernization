# AI-agent policy

This policy applies to Codex, Claude Code, GitHub Copilot, Cursor, Gemini, and
all other AI coding agents. Read it before significant repository-changing work.

## Required course-guideline check for new features

Before planning, designing, or implementing a new feature, agents must read
`Group-Explanation 01.pdf` and `Group-Explanation 02.pdf`. Treat these course
documents and the current repository as the source of truth. Keep scope small;
record significant AI prompts, outputs, decisions, changes, risks, and
verification; manually and continuously evaluate AI code; use a maintained
library for future ML-KEM work; and never use AI for a student’s personal
reflection, experiences, or feelings.

1. Inspect existing work and the two course documents, then run `uv run ai-history status` before a new significant AI task. Do not silently open another task when one is awaiting human review, awaiting final verification, or revision is not explicitly resumed.
2. Start a task before implementation and record the human prompt faithfully. Use the repository uv workflow; never add `requirements.txt`.
3. Complete all requested code, documentation, refactoring, tests, and relevant checks before the review gate. Record only actual, sanitized results.
4. Run `ai-history output`, then stop development. Never populate human fields. Ask for Problems Found; Decision: Accepted, Modified, or Rejected; and Requested Modifications if Modified.
5. For `Modified`, record the review, complete the full revision, run checks, record it with `ai-history revision`, and stop for another review. Preserve all rounds, negative findings, and rejected entries; never rewrite history.
6. After `Accepted`, request explicit final human verification and use `ai-history verify`. AI checks never substitute for human review.
7. Never store secrets in history: private/shared keys, credentials, passwords, tokens, `.env` contents, or secret configuration. Do not claim a test or human verification happened unless it actually did.

The CLI validates state and documentation but process compliance ultimately depends on compatible agents and human review.
