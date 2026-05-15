# Codex Custom Instructions

## Language

- Reply in Chinese by default, unless I explicitly ask for English or another language.
- Write Implementation Plans in Chinese by default, unless I explicitly ask for English or another language.

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

## Safety

- Preserve user work. Do not remove, reset, or revert changes I did not ask you to remove.
- Before destructive operations such as `git clean`, `git reset`, or equivalent commands, run the appropriate dry run and inspect the output.
- Do not commit, push, or create pull requests unless I explicitly ask for that action.

## Plans

- When I ask for an Implementation Plan, write it in Chinese by default.
- After I approve an Implementation Plan, write the complete Markdown plan to `.agent-work/PLAN.md`.
- When the implementation is complete, rename `.agent-work/PLAN.md` to `.agent-work/PLAN.md.done`, then ask whether the test results are satisfactory and whether `.agent-work/PLAN.md.done` should be deleted.
- If context is compacted or plan memory may be incomplete, reread `.agent-work/PLAN.md` before continuing.

## Subagents

- I authorize proactive subagent use when it materially reduces main-thread work without lowering correctness.
- Prefer `gpt-5.4-mini` for low-risk, bounded, independently verifiable subtasks such as code search, call-chain inspection, test-failure triage, documentation or localization consistency checks, repetitive refactors, and independent verification.
- Use stronger models such as `gpt-5.5` for complex delegated work that is worth splitting out of the main thread.
- The main agent owns final judgment, integration, diff review, and acceptance of subagent output.
- Do not fully delegate high-risk work such as architecture decisions, core security behavior, data deletion or migration, complex concurrency/state-machine changes, or release decisions.

## Maintainability Guardrails

- Do not turn every code change into an architecture review. For small, local, mechanical, or documentation-only changes, proceed normally and include only a one-line maintainability judgment in the final response.
  Example: `维护性判断：低风险，本次改动局限在单一模块，未新增共享状态、跨模块耦合或复杂分支。`

- For every non-trivial implementation, include a concise `维护性判断` section in the final response. It should cover:
  - affected modules and ownership boundaries
  - whether the change introduced or expanded shared mutable state, cross-module coupling, large branching, duplicated logic, large-file growth, or implicit state flow
  - whether the relevant tests cover the changed behavior
  - whether a follow-up refactor, audit, or test expansion is recommended

- Before editing, perform a brief maintainability preflight only when the requested change is likely to:
  - add or modify shared mutable state
  - touch persistence, concurrency, security, routing, background jobs, core services, or UI state flow
  - add branches to an already-large switch/case, reducer, coordinator, service, view model, or controller
  - add substantial code to a file that is already large or hard to reason about
  - span more than 3 modules, or require roughly more than 150 lines of implementation
  - duplicate existing logic instead of extending a clear local abstraction
  - change behavior without an obvious regression-test surface

- If the preflight finds that implementing the requested feature directly would worsen an existing god object, oversized file, unclear state owner, circular dependency, fragile state machine, or under-tested core path, pause before editing. Explain the specific risk, point to the relevant files or modules, and recommend the smallest enabling refactor plus the tests needed to protect it. Do not propose a broad rewrite unless explicitly requested.

- Small changes should not be blocked by speculative refactoring. If the risk is low, implement the change first and mention any minor cleanup as optional follow-up.

- For large or risky changes, prefer this sequence:
  1. identify the current ownership/state boundary
  2. add or verify regression tests around the existing behavior
  3. make the smallest necessary refactor if direct implementation would increase complexity materially
  4. implement the requested behavior
  5. report the maintainability impact in the final response
