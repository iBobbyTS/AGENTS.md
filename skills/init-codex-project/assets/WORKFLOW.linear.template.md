# WORKFLOW.md

This repository uses a Linear-backed Symphony-style workflow for task orchestration.

## Task Source

- Primary task system: Linear.
- Treat the Linear issue as the source of task intent, acceptance criteria, priority, and discussion context.
- Before implementation, read the issue description, comments, attachments, and linked documents that are relevant to the task.

## Agent Workflow

1. Select one Linear issue or user-approved task at a time.
2. Gather repository context from `AGENTS.md`, `.codex/config.toml`, `.agents/skills/`, and relevant docs.
3. Create or reuse an isolated work branch/worktree when the task requires code changes.
4. Make scoped changes that satisfy the issue acceptance criteria.
5. Run the relevant checks named in repository guidance.
6. Summarize changed files, test results, residual risks, and any follow-up tasks.
7. Do not close or transition the Linear issue unless the user explicitly asks.

## Subagents

- Use low-cost subagents for bounded exploration, consistency checks, and independent verification.
- Keep final integration, risk judgment, and release decisions in the main thread.
- Do not delegate sensitive operations such as data deletion, migrations, production changes, or security decisions without explicit approval.

## Linear Notes

- Add a Linear comment only when the user asks or when the workflow explicitly requires status reporting.
- Keep comments concise and factual: summary, verification, blockers, and next step.
- Do not expose secrets, local paths with sensitive data, or irrelevant implementation logs in Linear.
