---
name: code-review
description: Review one pull request, commit range, or uncommitted diff, especially AI- or agent-authored code changes. Use for requested code reviews, merge-readiness checks, external PR review feedback, and small/medium/large change reviews where Codex should evaluate correctness, maintainability, tests, security, CI integrity, and AI-aware risks; not for full periodic codebase audits.
---

# Code Review

## Overview

Use this skill to review a bounded change set with senior-engineer judgment. Optimize for real defects, merge risk, maintainability, and useful feedback, not exhaustive audit theater or style-only commentary.

Treat AI- and agent-authored code as plausible but untrusted: verify the intent, trace the behavior, and check for quiet technical debt that may not break tests.

## Review Contract

- Review; do not implement fixes while using this skill unless the user explicitly changes the task from review to repair.
- Base the review on the actual diff, PR, commit range, or uncommitted changes. Do not drift into a full-codebase audit.
- Lead with findings. If there are no actionable findings, say that clearly and include residual risk or test gaps.
- Distinguish verified facts from assumptions. Do not claim CI, tests, or local checks pass unless inspected.
- Prefer technical facts, repository conventions, documented requirements, and observed behavior over personal preference.
- Optimize for high-signal findings. If a concern is low-confidence and not severe, investigate more or report it as residual risk instead of creating a speculative blocker.
- Treat automated or agent review output as one defense-in-depth signal, not proof that the change is safe.
- Do not block on nits. Mark optional polish as non-blocking.
- Preserve user work. Do not reset, clean, merge, approve, request changes, push, or post PR comments unless explicitly asked.

## Review Mode

Use this skill as a composition of baseline review work, one depth classification, and any applicable overlays:

- Baseline review: always apply `Review Contract`, `First Pass`, `Universal Checks`, `AI-Aware Checks`, `Evidence And Validation`, and `Comment And Report Format`.
- Depth classification: choose exactly one of `Small`, `Medium`, or `Large` based on the change surface and risk.
- PR/external overlay: add `PR And External Review Mode` when the review involves a pull request, merge readiness, CI status, unresolved review threads, or external reviewer feedback.
- Subagent overlay: add `Subagent Review Prompting` when the main agent delegates an independent review pass to a subagent.

## First Pass

1. Collect the review surface:
   - PR URL or ID, base branch, head branch, changed files, commits, unresolved review threads, and CI/check status when available.
   - For local review, inspect `git status`, staged and unstaged diffs, and the relevant commit range.
   - Read inline review comments in code context, not as isolated text.
   - For agent-authored changes, inspect any available plan, task summary, terminal logs, test output, citations, or generated PR description, then verify them against the diff and repository.
2. Reconstruct the change intent:
   - What requirement, bug, user workflow, migration, or cleanup is this meant to address?
   - What invariants must remain true?
   - Can the purpose be described in one sentence?
3. Classify review depth:
   - `Small`: narrow diff, local behavior, few files, no high-risk boundary.
   - `Medium`: several modules or workflows, shared helpers, API shape, persistence-adjacent logic, or meaningful UI behavior.
   - `Large`: refactor, migration, architecture transition, state-model rewrite, security/permission change, concurrency/background job, data deletion, or broad test/config change.
   - `PR / external feedback` is an overlay, not a depth classification.
4. Check reviewability before deep review:
   - If the change is too large, mixes unrelated work, lacks intent, has failing CI with test-only edits, or has no plan for a broad agent change, request a breakdown or summary before spending deep review effort.

## Universal Checks

Check these for every non-trivial review:

- Correctness: requirement fidelity, critical path behavior, edge cases, empty/max/invalid inputs, stale data, error paths, and surprising conditionals.
- Code health: complexity added, readability, naming, comments, local cohesion, dead code, duplicated logic, and consistency with existing patterns.
- Tests: meaningful regression coverage, edge cases, failure paths, correct assertions, and whether tests validate behavior rather than implementation details.
- Security: authn/authz, permission checks on every branch, input validation, output encoding, secret handling, logging of sensitive data, SSRF/injection/deserialization risks, and least privilege.
- Data and persistence: migrations, compatibility, rollback, idempotency, transactional behavior, data loss, ordering, time zones, units, money, and schema/API contracts.
- Operations: CI changes, config/env changes, observability, rate limits, performance, resource cleanup, and failure recovery.
- User/operator workflow: labels, defaults, irreversible actions, loading/error states, accessibility, localization, and whether the interaction matches the product's normal workflow.
- Documentation: public APIs, operator docs, migration notes, changelog-style notes, and inline comments that must change with behavior.

## AI-Aware Checks

Include these in the baseline review:

- CI integrity:
  - Treat weakened CI as blocking unless explicitly justified.
  - Check for removed tests, skipped tests, lowered thresholds, changed workflow triggers, conditionalized checks, `|| true`, softened lint/typecheck/build steps, or deleted failure assertions.
- Reuse blindness:
  - Search for new utilities, validators, adapters, hooks, services, middleware, or "almost the same" helpers.
  - Require consolidation when equivalent functionality already exists, especially under shared semantic boundaries.
- Hallucinated correctness:
  - Verify new APIs, framework calls, config keys, environment variables, database columns, package names, and CLI flags against local code or authoritative docs.
  - Do not trust clean syntax or passing tests as proof that behavior is right.
- Dependency risk:
  - Verify any new dependency exists in the intended registry, is spelled correctly, is actively maintained enough for the project, has an acceptable license, and is necessary.
  - Watch for phantom or suspicious packages, lockfile churn, broad transitive additions, and generated code copied from unknown sources.
- Dependency remediation risk:
  - For agent-authored vulnerability fixes, verify the advisory, affected usage, reachability, chosen patched or downgraded version, breaking API changes, and tests.
  - Check that the patch removes the vulnerability rather than merely restoring the build, silencing the scanner, or changing tests around the warning.
- Over-mocked tests:
  - Flag tests that only assert implementation details, freeze generated structure, overuse mocks, or were changed to match the new behavior without proving the old bug.
- Local-optimum patches:
  - Look for narrow fixes that silence a symptom while bypassing the documented shared path, permissions model, validation layer, or error-handling convention.
- Agent runtime and permission boundaries:
  - Treat changes to sandboxes, approval modes, allowlists, workflow permissions, credentials, MCP servers, connectors, automation runners, or agent memory/state as high-risk.
  - Block scope escalation, data exfiltration, destructive or shared-infrastructure actions, review bypass, security-posture degradation, and modifications to an agent's own permission configuration unless explicitly justified.
  - For new or changed remote tools, MCP servers, and connectors, review both supply-chain risk and prompt-injection risk: version/source trust, mutable remote behavior, egress, secret exposure, and whether tool output is treated as untrusted.
  - Do not treat subagent, automation, or model-produced summaries as inherently more trustworthy than the external content they read.
- Prompt/LLM workflow security:
  - For workflows that call an LLM, block untrusted PR/issue/commit content flowing into prompts without sanitization, model output being executed as shell commands, secrets exposed to model steps, or write-scoped tokens without need.
  - Require a human approval gate for model output that can affect production, credentials, deployment, or destructive actions.

## Small Change Review

For a small change, keep the review lightweight and precise:

- Confirm the change does exactly what it claims and no more.
- Check nearby context in the whole file when the hunk alone is insufficient.
- Resist new abstractions, new dependencies, broad rewrites, or unrelated cleanup unless the change touches a high-risk semantic boundary.
- Ask for tests only when behavior changed, a bug was fixed, or the path is easy to regress. For purely mechanical/docs-only changes, note why tests are not needed.
- Prefer "can merge with non-blocking nits" over delaying for optional polish.

## Medium Change Review

For a medium change, map the affected surface before commenting:

- Trace at least one critical path end to end from input through transforms to output.
- Check shared state owners, public APIs, validation, error handling, routing, localization, and persistence-adjacent behavior.
- Compare new helpers or components against existing patterns before accepting another layer.
- Require regression coverage for changed behavior and edge cases that matter to users or operators.
- Identify which risks can be follow-up debt and which must be fixed before merge.

## Large Refactor Review

For a large change, run a quick diff survey first, then create a structured review ledger so the review survives interruption:

```text
.agent-work/change-review/{YYYYMMDD-HHMM}/
├── NOTES.md
└── REPORT.md
```

Also create `.agent-work/change-review/CURRENT.md` while the review is active. Record the active review directory, diff range or commands inspected, checklist, reviewed areas, evidence, gaps, and assumptions. Delete `CURRENT.md` only after `REPORT.md` is complete.

If continuing an interrupted large review, read `CURRENT.md` first, then `NOTES.md`, then inspect only the remaining or newly changed diff areas.

Use `NOTES.md` as the running ledger. After each module, workflow, state boundary, test group, or manual-test area is reviewed, append the result immediately before moving on. For each reviewed unit, record:

- Area: module, workflow, state boundary, test group, documentation area, or manual flow.
- Status: `Reviewed`, `Partial`, `Skipped`, or `Needs Follow-up`.
- Scope: changed files, symbols, routes, tests, docs, or manual flows inspected.
- Focus: design, functionality, complexity, tests, UX, docs, security, data, state flow, or failure paths.
- Outcome: `Must Fix`, `Should Fix`, `Should Plan`, `Track as Debt`, or `No Action`.
- Finding / Action: concise issue, rationale, impact, and smallest credible next step; use `None` for `No Action`.
- Evidence / Validation: code references, diff hunks, command output, CI/test output, or observed browser behavior.
- Gaps / Assumptions: unreviewed paths, missing environment, changed files not inspected, or follow-up verification.

Generate `REPORT.md` only after rereading `NOTES.md`. The report should prioritize actionable risks, preserve coverage and limitations, and avoid relying on conversation memory.

Review large changes by area:

- Intent and invariants preserved.
- Ownership boundaries: modules, state owners, data flow, APIs, persistence, and UI workflows.
- Transitional abstractions: too much indirection, duplicated state, parallel implementations, obsolete compatibility layers, and abstractions created before the rule of three without a high-risk semantic reason.
- Business semantics: permission behavior, state machines, migration compatibility, failure modes, and operator workflows.
- Validation: unit/integration/e2e/manual coverage for highest-risk flows, plus rollback or backout plan when needed.
- Documentation drift: public docs, migration docs, operator notes, and comments.

If the PR is too broad to review credibly, say so and request smaller scoped units, a plan, or reviewer ownership split before issuing low-confidence findings.

## Subagent Review Prompting

When the main agent asks a subagent to perform an independent review pass, pass only:

```text
Review {working path}, [$code-review]({user home dir}/.codex/skills/code-review/SKILL.md)
```

Do not pass extra instructions, summaries, suspected issues, expected focus areas, prior conclusions, or main-agent analysis unless the user explicitly specifies them. Keep the subagent prompt minimal to maximize independent variation and increase the chance of finding different latent issues.

## PR And External Review Mode

When reviewing a pull request or external reviewer feedback:

- Always collect unresolved requested-change threads, review comments, approvals, CI/check status, target/base branch, and changed files.
- Verify each external comment against repository reality before agreeing with it.
- Separate blockers, suggestions, questions, style nits, and reviewer misunderstandings.
- Treat unresolved correctness, security, data loss, permission, migration, build/test failure, or requested-change issues as not mergeable.
- Treat maintainability and test gaps as blocking when they affect changed behavior or create meaningful future risk.
- Do not approve, merge, request changes, or post comments unless explicitly asked.
- Include one clear decision: `mergeable`, `not mergeable`, or `insufficient evidence`.
- If responding to reviewers, draft respectful technical replies with evidence and the smallest acceptable resolution.

## Evidence And Validation

- Run or inspect relevant checks when feasible. Prefer existing project validation workflows over inventing new ones.
- For bug fixes and non-trivial logic changes, look for a test that would fail before the change.
- For UI changes, inspect screenshots or run existing browser checks when the repository supports them.
- For risky unattended or agent-authored diffs, use a fresh-context or adversarial second pass when feasible to generate hypotheses, then validate each candidate finding yourself before reporting it.
- For security-sensitive changes, anchor findings to the project's assets, trust boundaries, and realistic impact. Use OWASP-style focus areas: input validation, output encoding, authn/authz, session handling, access control, cryptography, secrets, logging, database access, file handling, and dynamic execution.
- Validate security findings in a sandbox or test environment when practical; avoid speculative vulnerability reports that create triage burden without a concrete exploit path or affected trust boundary.
- If checks cannot run, report the blocker and avoid overstating confidence.

## Comment And Report Format

Use severity labels that reflect actionability:

- `Must Fix`: blocks merge or acceptance.
- `Should Fix`: important before merge unless the user accepts the risk.
- `Should Plan`: valid risk or cleanup that can be scheduled.
- `Track as Debt`: acceptable now, but record the future cost.
- `No Action`: inspected area with no issue found.

For each actionable finding, include:

- File and line reference when possible.
- Trigger: what in the diff creates the concern.
- Impact: why it matters for users, operators, security, data, or maintainability.
- Smallest credible fix direction.
- Evidence inspected.
- Confidence when the issue is subtle, security-sensitive, or based on partial evidence.

Deduplicate findings by root cause. Do not report compiler/linter-only errors, repeated instances, documentation wording, or generated-output churn unless they create distinct merge risk that automated checks will not handle.

When drafting inline comments, prefer a conventional shape:

```text
issue (blocking): <specific problem>

<why this matters and the smallest fix direction>
```

Use `suggestion (non-blocking):`, `question:`, `nit:`, or `praise:` only when those labels match the actual action required.

## No-Finding Outcome

If no actionable issues are found, say so directly. Include:

- The diff/PR range reviewed.
- The checks, CI, tests, docs, or manual flows inspected.
- Remaining assumptions or unreviewed areas.
- A concise merge-readiness or risk statement when applicable.
