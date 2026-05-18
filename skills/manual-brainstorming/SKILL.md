---
name: manual-brainstorming
description: Use only when the user explicitly asks to brainstorm, clarify, design, or spec a change before implementation, or explicitly names this skill. Do not use automatically for ordinary build, fix, implementation, or code-edit requests.
---

# Manual Brainstorming

## Overview

Use this skill as an explicit design conversation before implementation. Keep it lightweight enough for Codex: clarify intent, compare approaches, validate the design, then produce an implementation plan only after approval.

## Trigger Discipline

- Use this skill only because the user explicitly requested brainstorming, design/spec work, or this skill by name.
- Do not infer this skill from a normal request to build, fix, refactor, or edit code.
- Do not write code, scaffold files, commit, push, or open a PR during this skill unless the user explicitly changes the task.

## Workflow

1. **Explore project context.**
   - Read existing project instructions such as `AGENTS.md`, relevant docs, package/config files, and recent diffs when a repository exists.
   - Identify existing ownership boundaries, validation commands, documentation rules, and whether the request touches sensitive areas such as persistence, auth, routing, background jobs, or UI state.

2. **Scope the request.**
   - If the request includes multiple independent subsystems, recommend splitting it into separate design/plan cycles.
   - Keep the current cycle focused on one deliverable that can be implemented and verified independently.

3. **Ask clarifying questions one at a time.**
   - Focus on purpose, constraints, non-goals, success criteria, affected users, and acceptable tradeoffs.
   - Prefer concise multiple-choice questions when they reduce ambiguity.
   - Stop asking when there is enough information to propose credible approaches.

4. **Propose 2-3 approaches.**
   - Lead with the recommended approach and explain why.
   - Include tradeoffs: implementation risk, testability, maintainability, user impact, and scope.
   - Call out what should be deliberately excluded by YAGNI.

5. **Present the design in reviewable sections.**
   - Cover architecture, affected modules, data/control flow, edge cases, error handling, test strategy, and documentation impact.
   - Scale detail to risk: short for small changes, deeper for stateful or cross-module changes.
   - Ask the user to confirm or revise each meaningful section before proceeding.

6. **Use the user's `.agent-work/PLAN.md` plan flow instead of Superpowers docs.**
   - Do not create `docs/superpowers/specs/` or `docs/superpowers/plans/`.
   - Do not commit the design or plan unless the user explicitly asks for a commit.
   - Keep the design in chat until the user approves it.
   - When an implementation plan is requested and approved, write the complete Markdown plan to `.agent-work/PLAN.md` according to the user's global instructions.
   - If `.agent-work/PLAN.md` already exists, read it before continuing and avoid overwriting user work without explaining the replacement.

7. **Self-review before handoff.**
   - Check for placeholders, contradictions, vague requirements, missing error cases, untestable acceptance criteria, and scope creep.
   - Verify the plan maps each requirement to concrete tasks and validation steps.
   - Ensure the plan does not introduce unnecessary shared state, broad refactors, or duplicated logic.

8. **User review gate.**
   - Ask the user to review the final design or `.agent-work/PLAN.md` before implementation.
   - If the user requests changes, revise and repeat the self-review.
   - Do not implement until the user approves the design/plan or explicitly asks to proceed without a plan.

9. **Transition to implementation.**
   - After approval, follow repository instructions and the user's normal implementation workflow.
   - If context was compacted or plan memory may be incomplete, reread `.agent-work/PLAN.md` before continuing.
