# Codex Custom Instructions

## Language

- Reply in Chinese by default, unless I explicitly ask for English or another language.
- Write Implementation Plans in Chinese by default, unless I explicitly ask for English or another language.
- When asked `Please review my uncommitted changes`, reply also in Chinese. 

## Scope And Project Setup

- Do not create `.agents/skills/` dir. If it doesn't exist, ask me to run `$init-codex-project` first.
- If an existing repository already has project-specific rules, follow them.
- When a reusable project-specific method emerges, update the relevant repo skill in `.agents/skills/`.

## Docker

- Use Colima to start Docker on my local machine when the Docker daemon is needed.
- Prefer `docker-compose` command spelling over `docker compose`.

## Implementation Quality

- When changing functionality, add or update meaningful unit tests unless the change is purely mechanical or documentation-only.
- Cover real behavior and meaningful edge cases; do not add assertions that only execute code without verifying outcomes.
- Run the relevant checks before finishing when the environment permits it. If checks cannot run, explain the blocker clearly.
- For browser or UI work, use the repository's existing validation workflow when it exists.
- Before adding behavior that may span multiple pages, modules, or workflows, inspect project docs and existing implementations for a documented shared convention or reusable entry point. Prefer extending that path and avoid creating parallel implementations.

## Safety

- Preserve user work. Do not remove, reset, or revert changes I did not ask you to remove.
- Before destructive operations such as `git clean`, `git reset`, or equivalent commands, run the appropriate dry run and inspect the output.
- Do not commit, push, or create pull requests unless I explicitly ask for that action.

## Plans

- When I ask for an Implementation Plan, write it in Chinese by default.
- After I approve an Implementation Plan, write the complete Markdown plan to `.agent-work/PLAN.md`.
- When the implementation is complete, rename `.agent-work/PLAN.md` to `.agent-work/PLANS/{YYYYMMDD-HHMM}.md`.
- If context is compacted or plan memory may be incomplete, reread `.agent-work/PLAN.md` before continuing.
- For long debugging sessions, repeated experiments, second-pass fixes, or debugging likely to survive context compaction, proactively use `$second-pass-debugging` skill.

## Subagents

- I authorize proactive subagent use when it materially reduces main-thread work without lowering correctness.
- Prefer `gpt-5.4-mini` for low-risk, bounded, independently verifiable subtasks such as code search, call-chain inspection, test-failure triage, documentation or localization consistency checks, repetitive refactors, and independent verification.
- Use stronger models such as `gpt-5.5` for complex delegated work that is worth splitting out of the main thread.
- The main agent owns final judgment, integration, diff review, and acceptance of subagent output.
- Do not fully delegate high-risk work such as architecture decisions, core security behavior, data deletion or migration, complex concurrency/state-machine changes, or release decisions.

## Maintainability Guardrails

- Small, local, mechanical, or documentation-only changes should proceed normally. In the final response, include only a one-line maintainability judgment.
- For non-trivial implementations, include a concise `维护性判断` covering affected modules, ownership boundaries, complexity introduced, test coverage, and whether follow-up cleanup is recommended.
- Before editing, do a brief maintainability preflight only when the change touches persistence, security, routing, background jobs, concurrency, shared UI state, core services, more than 3 modules, roughly more than 150 lines, or an already-large coordinator/controller/view model.
- If the preflight finds that a direct change would materially worsen a god object, unclear state owner, fragile state machine, circular dependency, duplicated logic, or under-tested core path, pause before editing. Explain the specific risk and recommend the smallest enabling refactor plus protective tests.
- Apply the rule of three before introducing new shared helpers, components, or services: when the same or closely similar goal appears in three or more places, prefer a shared abstraction and document its use in the project docs. For one-off or two-place duplication, keep the change local unless it affects a high-risk semantic boundary.
- High-risk semantic boundaries, such as security, permissions, API clients, time/date, money, units, persistence, and error handling, should be checked for an existing single source of truth even before three repetitions.
- Prefer this sequence for large or risky changes: identify ownership/state boundary, add or verify regression coverage, make the smallest needed refactor, implement the behavior, then report maintainability impact.
