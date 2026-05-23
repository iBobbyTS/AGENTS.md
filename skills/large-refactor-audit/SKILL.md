---
name: large-refactor-audit
description: Use when reviewing substantial refactors, migrations, or architecture transitions, especially when the main risks are transitional abstraction balance, business-logic drift, state-model correctness, boundary coverage, manual verification, or UX/operator workflow fit.
---

# Large Refactor Review

## Overview

Use this skill to review large code changes that reshape architecture, state flow, or domain modeling. Focus on whether the refactor preserves business semantics, keeps the transitional design understandable, and remains usable for operators.

## Persistent Review Notes

For non-trivial refactor reviews, persist notes under `.agent-work/refactor-review/` so the review can survive context compression and be resumed without losing already-inspected areas.

Create one timestamped review directory after a quick diff survey:

```text
.agent-work/refactor-review/{YYYYMMDD-HHMM}/
├── NOTES.md
└── REPORT.md
```

Also create `.agent-work/refactor-review/CURRENT.md` while the review is in progress.

- Base the review outline on `git diff`, staged changes, and relevant recent commits, not a full-codebase audit.
- Use `CURRENT.md` to track the active review directory, the diff range or commands inspected, and a compact checklist of changed modules or workflows.
- Use `NOTES.md` as the running ledger. After each changed module, workflow, state boundary, test group, or manual-test area is reviewed, append the result immediately before moving on.
- Delete `CURRENT.md` only after `REPORT.md` is complete.
- If continuing an interrupted review, read `CURRENT.md` first, then `NOTES.md`, then inspect only the remaining or newly changed diff areas.

For each reviewed unit, record:

- Area or workflow name.
- Status: `Reviewed`, `Partial`, `Skipped`, or `Needs Follow-up`.
- Severity: `Must Fix`, `Should Plan`, `Track as Debt`, or `No Action`.
- Scope: changed files, symbols, routes, tests, docs, or manual flows inspected.
- Focus: abstraction, state flow, business semantics, tests, UX, docs, or failure paths.
- Evidence: code references, diff hunks, command output, or observed browser behavior.
- Gaps / Assumptions: unreviewed paths, missing environment, or follow-up verification.

Generate `REPORT.md` only after rereading `NOTES.md`. The report should prioritize actionable risks, preserve coverage and limitations, and avoid relying on conversation memory.

## Review Flow

1. Reconstruct the change intent and the invariants it must preserve.
2. Map the affected surface area across modules, state owners, and data flow.
3. Check transitional abstractions for balance:
   - too much indirection for the current scope
   - too little abstraction for repeated logic or duplicated state
   - temporary compatibility layers that should already be removable
4. Review correctness:
   - business-rule drift
   - state-machine consistency
   - stale data, race conditions, or invalid reuse of prior results
   - boundary conditions, empty states, and failure paths
5. Review validation quality:
   - real edge-case coverage, not just smoke tests
   - regression tests for changed behavior
   - manual verification for the highest-risk flows
6. Review UX and operator fit:
   - does the interaction match industrial or operational expectations
   - are labels, defaults, errors, and state transitions legible
   - does the workflow avoid surprising or irreversible behavior
7. Summarize the outcome as engineering risk, not merge readiness.

## What to Call Out

- Over-abstracted transition layers that obscure the actual behavior
- Under-abstracted rewrites that duplicate logic or state in multiple places
- Incorrect or incomplete business semantics
- Missing boundary tests or unverified failure paths
- Manual-test gaps on the highest-risk workflows
- UX that conflicts with operator intuition, especially in workflow tools
- Mechanically assembled patches that duplicate logic, add parallel paths, or bypass established layers
- Fragile compatibility branches, fallback logic, or default values that preserve obsolete behavior without a clear exit plan
- Tests that mirror implementation details instead of validating the real user-visible behavior
- Comments, names, or config choices that look plausible but are not grounded in the domain model or repository patterns
- Documentation drift: user-facing docs, operator notes, migration guidance, or inline comments that no longer match the refactor's behavior

## Output Expectations

Report findings with concrete code references when possible. Classify them as:

- `Must Fix`
- `Should Plan`
- `Track as Debt`
- `No Action`

For each nontrivial finding, include the trigger, impact, and smallest credible fix direction. Prefer a concise engineering review over a merge decision or PR-response template.
