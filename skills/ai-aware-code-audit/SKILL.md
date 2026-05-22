---
name: ai-aware-code-audit
description: "Use when Codex is asked to perform or finish a full codebase audit, architecture audit, technical-debt audit, maintainability audit, security audit, or audit of an AI-assisted or AI-generated codebase. Focus on traditional engineering risks plus AI-agent development failure modes such as local-optimum patches, duplicated abstractions, over-mocked tests, fragile fallbacks, and unreviewed generated logic. After an audit is complete, any commit that records the audit result must include the commit-message trailer `Maintenance-Audit: true`."
---

# AI-Aware Code Audit

Perform a full-system audit. Do not treat this as a pre-change refactoring gate; this skill is for periodic or requested audits of the current codebase state.

## Persistent Audit Artifacts

For non-trivial audits, persist progress under `.agent-work/audit/` so the audit can survive context compression and be resumed without rereading already-reviewed code.

### Artifact Setup

After a quick repository survey, create one timestamped audit directory:

```text
.agent-work/audit/{YYYYMMDD-HHMM}/
├── FULL.md
└── REPORT.md
```

Also create `.agent-work/audit/CURRENT.md` while the audit is in progress.

- `CURRENT.md` must point to the active timestamped audit directory and report file.
- At the beginning, `CURRENT.md` only needs a coarse module/component outline from the initial survey.
- As larger modules are audited, expand `CURRENT.md` with smaller submodules and update progress.
- Delete `CURRENT.md` after `REPORT.md` is complete.
- If continuing an interrupted audit, read `CURRENT.md` first, then read the referenced `FULL.md` before reviewing more code or reporting completion.

### FULL.md Ledger

Use `FULL.md` as the complete audit ledger. After each module, component, workflow, or similarly reasonable review unit, append the result immediately before moving on.

Start `FULL.md` with a compact progress index:

```markdown
| Area | Status | Severity | Files | Notes |
| --- | --- | --- | --- | --- |
| Auth middleware | Reviewed | Must Fix | src/auth/* | Object-level permission gap |
| Settings UI | Reviewed | No Action | app/settings/* | State and layout reviewed |
```

For every reviewed area, record:

- Module, component, workflow, or subsystem name.
- Status: `Reviewed`, `Partial`, `Skipped`, or `Needs Follow-up`.
- Severity: `Must Fix`, `Should Plan`, `Track as Debt`, or `No Action`.
- Scope: relevant file paths, symbols, API routes, commands, workflows, and line ranges where useful.
- Focus: audit concerns inspected, such as permissions, state flow, concurrency, tests, architecture, tooling, or UI states.
- Evidence: concrete code references, command outputs, test results, or observed behavior.
- Verification: tests/checks run or manual verification still needed.
- Gaps / Assumptions: unreviewed paths, missing evidence, or unsupported assumptions.

Only areas with real findings need repair-oriented details:

- Finding description.
- Trigger or failure path.
- Impact.
- Recommended priority.
- Suggested fix direction.

For `No Action` areas, do not invent findings, triggers, impact, or fix recommendations. Record the reviewed scope, focus, evidence, verification, and any remaining gaps.

### REPORT.md

Generate `REPORT.md` only after rereading `FULL.md`. The final report should extract and prioritize actionable findings, preserve audit coverage and limitations, and include assumptions, human-review needs, and verification gaps. Do not rely on conversation memory as the source of the final report.

## General Audit Areas

### Structure and Module Boundaries

- Identify god objects, oversized files, long functions, deeply nested branching, and modules with unclear ownership.
- Check whether dependency direction, layering, and boundaries match the existing architecture.
- Look for duplicate helpers, parallel abstractions, and bypasses around established service, component, or utility layers.
- Flag AI-generated patterns that solve a local problem by adding more in-place logic instead of reusing or extending the architecture.

### Functional Correctness

- Review core user workflows, business rules, edge cases, error paths, retries, and empty states.
- Check whether recent features regress older behavior.
- Look for implementations that run successfully but encode the wrong product or domain semantics.

### UI and UX

- Review layout, responsiveness, accessibility, loading states, empty states, error states, and disabled/submitting/selected interaction states.
- Check for visual or interaction-style drift introduced by incremental AI changes.
- Flag pages where new controls or panels were stacked onto the UI without preserving information architecture.

### Data and State Management

- Review schemas, migrations, default values, validation boundaries, cache invalidation, persistence, and derived state.
- Check whether there is a single source of truth for important state.
- Flag duplicated state, stale cached data, inconsistent normalization, and validation that only happens in the UI or caller.

### Concurrency, Async, and Thread Safety

- Review race conditions, cancellation, re-entrancy, stale responses overwriting newer state, duplicate submissions, and task cleanup.
- Check timers, subscriptions, streams, workers, background jobs, locks, transactions, and idempotency boundaries.
- Flag state machines that became less predictable because fixes added more flags instead of clarifying transitions.

### Data Security and Permissions

- Review authentication, authorization, tenant isolation, object-level permissions, input validation, output encoding, file paths, external URLs, and command execution.
- Check whether secrets, tokens, personal data, or sensitive business data can leak through logs, errors, caches, telemetry, generated files, frontend bundles, or agent/tool output.
- Review dependency, script, network, and supply-chain risks introduced by agentic development.

### Test and Validation Quality

- Check whether tests verify real behavior rather than implementation details or smoke execution.
- Flag over-mocking that hides integration failures.
- Review coverage of happy paths, failure paths, edge cases, permissions, migrations, concurrency, and UI states.
- Check CI, linting, type checks, browser/UI validation, and flaky-test risks.

### Maintainability and Evolution Risk

- Identify hotspots where future changes require understanding too many unrelated modules.
- Review naming, comments, documentation, and domain intent.
- Assess whether current boundaries can support the next likely features without concentrated risk.
- Separate acceptable local complexity from structural debt that will compound.

### AI-Assisted Development Artifacts

- Look for duplicated patterns, duplicated components, repeated utility functions, and near-identical tests created by local prompting.
- Flag brittle logic that appears optimized to pass current tests rather than express the intended behavior.
- Review plausible but unverified fallbacks, compatibility layers, swallowed errors, invented configuration keys, environment variables, or conventions.
- Check whether generated code introduced broad permissions, hidden data movement, or unreviewed external assumptions.

## Agent Verification

### Repository Reality Check

Before reporting audit completion, the agent must verify the current repository state directly.

- Run or inspect the equivalent of `git status`.
- Review relevant staged, unstaged, and recent committed diffs.
- Confirm which files were actually changed, added, deleted, or left untouched.
- Do not rely on previous task summaries, implementation-agent claims, or stale conversation context as proof.
- If the repository state contradicts the previous plan or agent summary, treat the repository state as authoritative.

### Evidence Discipline

Every finding must include concrete evidence where possible.

- Prefer file paths, function names, class names, API routes, migrations, tests, commands, and observed outputs.
- Mark unsupported claims as assumptions.
- Mark missing evidence as an audit gap.
- Do not claim that a workflow, test, migration, or UI state works unless it was inspected or run.
- Do not claim that a previous agent completed work unless the result is visible in code, tests, logs, or git history.

### Stale State and Context Drift

Check for signs that previous AI-agent work was based on stale assumptions.

- Reports mention files that no longer exist.
- Completion summaries do not match the current diff.
- Tests were described as passing but no command output or CI result is available.
- Old architectural assumptions remain in comments, docs, prompts, or generated reports.
- The code contains compatibility layers, fallbacks, or flags added to preserve behavior that no longer exists.

Classify stale-state findings as:
- `Must Fix` if they affect runtime behavior, security, migrations, data correctness, or deployment.
- `Should Plan` if they mainly affect maintainability, documentation, or developer understanding.
- `Track as Debt` if they are harmless but should be removed later.

### Agent-Generated Code Smell Detection

Look specifically for patterns commonly introduced by AI coding agents.

- Near-duplicate helpers, components, services, schemas, or tests.
- Parallel abstractions that solve the same problem in different places.
- Generic fallback logic that hides real errors.
- Broad `try/catch` blocks that swallow failures.
- Configuration keys, environment variables, or conventions that are invented but undocumented.
- Comments that explain intent but do not match the implementation.
- Tests that validate mocks rather than real behavior.
- Code that appears optimized to satisfy current tests rather than express domain logic.
- Large rewrites that replace working architecture without clear justification.

### Independent Verification Pass

The agent must perform an independent verification pass after reviewing implementation details.

- Re-run available tests when feasible.
- Inspect failing, skipped, or newly added tests.
- Check whether tests cover real integration boundaries, not only mocked behavior.
- Review the highest-risk workflows end to end from entry point to persistence or output.
- Verify migrations, background jobs, permissions, and destructive operations with extra scrutiny.
- If tests cannot be run, state why and list the manual or CI checks still required.

### Simplification Pass

After identifying findings, the agent must check whether complexity can be reduced.

- Identify code that can be deleted.
- Identify duplicated logic that can be merged.
- Identify new abstractions that should instead reuse existing layers.
- Identify fallback or compatibility code that should be removed rather than preserved.
- Prefer smaller, reversible fixes over broad rewrites.

### Agent Runtime and Tooling Audit

When the repository includes agent configuration, automation scripts, MCP setup, CI scripts, or development tooling, audit them as part of the system.

- Check whether agents have unnecessary filesystem, network, deployment, or secret access.
- Check whether scripts can expose secrets through logs, generated files, telemetry, or command output.
- Check whether dangerous commands require approval or are isolated from production data.
- Check whether agent-generated reports, plans, or temporary files are excluded from production bundles.
- Check whether tool configuration is documented well enough for another developer to reproduce the workflow.


## Output Format

### Agent Verification
- Repository state checked: yes/no, with evidence.
- Diffs reviewed: yes/no, with scope.
- Tests run: command, result, and limitations.
- Tests not run: reason.
- High-risk workflows inspected.
- Assumptions.
- Human review required.
- Known stale context or conflicting evidence.
The agent must not mark a finding as resolved unless the fix is visible in code and supported by verification evidence.

### General Findings
Lead with findings, ordered by severity. Use concrete file references when available. Classify each finding as one of:

- `Must Fix`: security issues, data loss/corruption risks, severe functional errors, or structural problems that already block reliable development.
- `Should Plan`: meaningful debt, test gaps, maintainability hotspots, or design risks that are not urgent but should be scheduled.
- `Track as Debt`: acceptable short-term tradeoffs that need an owner, trigger condition, or follow-up marker.
- `No Action`: reviewed areas that are reasonable for the current project size and risk profile.

Include a brief summary of overall system health, strongest areas, highest-risk areas, and recommended next audit focus.

When committing completed audit work, include this trailer exactly once in the commit message:

```text
Maintenance-Audit: true
```
