---
name: code-audit
description: "Perform or continue a periodic full-system codebase audit covering architecture, correctness, security, reliability, operations, supply chain, maintainability, technical debt, anti-bloat, and AI-agent-specific risks. Use for scheduled audits after sustained development, risk reassessment, architecture or security audits, and remediation-enabled audit loops that must preserve coverage state across runs instead of rescanning the entire repository after every fix."
---

# Code Audit

Audit the current system as a maintained product, not merely a diff. Use durable risk and coverage state so periodic audits deepen over time instead of restarting from zero.

## Boundary

- Use this skill for periodic or explicitly requested codebase/system audits.
- Do not use it as the default merge gate for one bounded pull request; use `$code-review` for that.
- Audit actual repository, runtime, delivery, and agent-tooling behavior. Do not equate a static scan or clean test run with a complete audit.
- Treat an audit as risk sampling unless a defined baseline proves exhaustive coverage.
- Repair only when the user explicitly authorizes remediation.
- Preserve user work and repository history. Do not reset, merge, push, deploy, or change production systems unless explicitly asked.

## Load References Progressively

- Read [references/audit-profile-template.md](references/audit-profile-template.md) only when creating, revising, or explaining a project audit profile.
- Read [references/audit-coverage.md](references/audit-coverage.md) when selecting audit domains and scenarios.
- Read [references/ai-agent-risk-catalog.md](references/ai-agent-risk-catalog.md) when agents materially create, review, deploy, or operate the repository, or when the repository ships agent functionality.
- Read [references/audit-loop-protocol.md](references/audit-loop-protocol.md) for periodic scope selection, remediation loops, freshness, invalidation, and reset rules.
- Read [references/anti-bloat.md](references/anti-bloat.md) when simplification, deletion, over-engineering, unnecessary dependencies, or YAGNI is in scope.
- Read [references/ledger-templates.md](references/ledger-templates.md) before creating or updating persistent audit artifacts.

## Persistent Audit System

Use this structure for non-trivial audits:

```text
.agent-work/audit/
├── PROFILE.md                 # when docs/audit-profile.md is not appropriate
├── SYSTEM-MAP.md
├── COVERAGE.md
├── FINDINGS.md
├── CURRENT.md                 # active run only
└── runs/
    └── {YYYYMMDD-HHMM}/
        ├── SCOPE.md
        ├── EVIDENCE.md
        └── REPORT.md
```

Prefer `docs/audit-profile.md` when project documentation is versioned and repository rules allow it. Do not create duplicate profiles.

Keep `SYSTEM-MAP.md`, `COVERAGE.md`, and `FINDINGS.md` durable across audit cycles. Store run-specific evidence under `runs/`. Delete `CURRENT.md` only after the run report is complete.

## Establish the Audit Profile

Look for the profile in this order:

1. `docs/audit-profile.md`
2. `AUDIT_PROFILE.md`
3. `.agent-work/audit/PROFILE.md`

If none exists:

1. Read `references/audit-profile-template.md`.
2. Create a draft in the first repository-appropriate location.
3. Record explicit assumptions for unknown fields.
4. Ask the user to approve material risk, business, regulatory, or scope choices before deep auditing when those choices change prioritization.
5. If instructed to proceed immediately, continue under `Draft` status and surface every material assumption in `REPORT.md`.

The profile defines minimum coverage, risk tolerance, quality attributes, critical workflows, control baselines, evidence expectations, and sampling rules. It does not define feature requirements or implementation plans.

## Choose Baseline or Periodic Mode

Use `Baseline` when:

- No trustworthy system map or coverage state exists.
- The project has never received this audit.
- A reset trigger invalidated broad prior conclusions.
- The user explicitly requests a comprehensive new baseline.

Use `Periodic` when durable audit state is trustworthy. Do not perform a whole-repository rescan merely because 30–50 commits accumulated.

In periodic mode, derive scope from:

1. Always-on critical surfaces from the profile.
2. Changed/high-churn areas since the last audit.
3. Areas invalidated by dependencies, contracts, incidents, or prior repairs.
4. Rotating deep slices whose freshness is due.
5. Open findings, accepted debt, prior gaps, and production/test failures.
6. End-to-end scenarios crossing multiple components.

Commit count is a trigger to reassess risk, not the unit of audit coverage.

## Phase 0: Reconcile Repository Reality

- Inspect `git status`, current branch/head, relevant recent commits, tags/releases, and deployment/configuration state available in the repository.
- Read `CURRENT.md` before continuing an interrupted run.
- Reconcile persistent ledgers with files, symbols, architecture, and workflows that still exist.
- Mark stale evidence and invalidated coverage explicitly.
- Identify generated/vendor directories and exclusions with rationale.
- Record which runtime environments, tests, scanners, logs, metrics, incidents, and external systems are accessible.

Never rely on a previous audit report, agent summary, or commit message as proof of current behavior.

## Phase 1: Build or Refresh the System Map

Map the system at a level useful for risk decisions:

- Users, operators, business workflows, crown-jewel data, secrets, money, and privileged actions.
- External interfaces and trust boundaries.
- Domains/modules, ownership, dependency direction, and public contracts.
- Data stores, schemas, migrations, caches, queues, jobs, and state machines.
- Deployment topology, environments, configuration, feature flags, observability, backups, and recovery.
- CI/CD, dependencies, build provenance, release artifacts, and third-party services.
- Agent identities, prompts, skills, MCP/connectors/plugins, memory, sandboxes, tool/network permissions, evals, and autonomous actions.

Update only what changed or was previously unknown. Preserve history when architecture transitions matter.

## Phase 2: Plan Risk-Based Coverage

Read `references/audit-coverage.md` and create `SCOPE.md`.

For every selected area, record:

- Why it is in scope: critical, changed, invalidated, rotating, incident-driven, debt follow-up, or scenario dependency.
- Quality attributes and failure scenarios under review.
- Files, interfaces, workflows, runtime evidence, and expected tests.
- Coverage depth and exclusions.
- Evidence needed to mark the area `Fresh`.

Use scenario-based review for critical workflows. State the stimulus, environment, expected response, architectural decisions, tradeoffs, and evidence.

Do not sample only complex-looking files. Include entry points, auth/permission gates, persistence, migrations, background work, integrations, release/rollback, observability, and recovery.

## Phase 3: Perform Broad Discovery Before Remediation

Audit selected areas through independent lenses before changing code:

1. Business correctness and critical workflow invariants.
2. Architecture and quality-attribute tradeoffs.
3. Identity, authorization, privacy, trust boundaries, and abuse paths.
4. Data lifecycle, migrations, consistency, backup, restore, retention, and deletion.
5. Concurrency, jobs, queues, retries, idempotency, and partial failure.
6. Reliability, deployment, rollback, degraded mode, observability, and incident recovery.
7. Performance, capacity, quotas, and cost.
8. Dependencies, build integrity, CI/CD permissions, provenance, and release artifacts.
9. Tests, evals, scanners, validation integrity, and evidence quality.
10. Maintainability, ownership, documentation, technical debt, and anti-bloat.
11. AI-agent repository, harness, autonomy, prompt-injection, memory, and tool risks when applicable.

For each area:

- Generate failure hypotheses.
- Validate or falsify them from code, configuration, history, tests, runtime evidence, or authoritative documentation.
- Append evidence immediately to `EVIDENCE.md` and update persistent coverage.
- Deduplicate findings by root cause and assign stable IDs such as `AUD-001`.
- Record `No Action` coverage without inventing findings.

## Finding Classification

Use one severity:

- `Must Fix`: security, privacy, data loss/corruption, serious correctness, unsafe deployment/recovery, or structural risk that already prevents reliable development.
- `Should Plan`: meaningful architecture, reliability, test, operational, ownership, or maintainability risk requiring scheduled work.
- `Track as Debt`: acceptable bounded compromise with owner, ceiling, and revisit trigger.
- `No Action`: reviewed area is reasonable for the approved profile and current evidence.

Use one decision class:

- `Needs Decision`: business semantics, risk tolerance, control baseline, architecture tradeoff, or acceptable operational behavior requires human authority.
- `Agent-Fixable`: intended outcome and constraints are sufficiently established.
- `External Blocker`: required environment, production evidence, owner input, or third-party state is unavailable.

Rank findings by business/user impact, exploitability or likelihood, blast radius, reversibility, evidence strength, systemic reach, and remediation cost—not by code size or scanner severity alone.

## Remediation-Enabled Mode

Repair only when authorized.

1. Freeze accepted finding IDs, root cause, evidence, and acceptance criteria.
2. Resolve blocking `Needs Decision` items before selecting a repair direction.
3. Batch the smallest coherent remediation wave.
4. Preserve unrelated repository state.
5. Add the strongest affordable regression or control at the root-cause boundary.
6. Re-audit only the remediation delta, invalidated dependency cones, and affected scenarios.
7. Run a full reset only when a reset trigger fires.

A repair agent cannot close its own finding by explanation. Closure requires current code/configuration plus independent or phase-separated verification evidence.

## Coverage Freshness and Invalidation

Use these states in `COVERAGE.md`:

- `Fresh`: required scope and evidence were reviewed against the recorded head/environment.
- `Stale`: time, churn, dependency age, or missing runtime evidence reduces confidence but no direct contradiction exists.
- `Invalidated`: a change, incident, contract, architecture, or finding directly breaks the previous conclusion.
- `Unknown`: no trustworthy evidence exists.

Do not assign fake precision such as “82% secure.” Record concrete surfaces, evidence, dates/commits, and invalidation triggers.

When an audited component changes, invalidate only dependent conclusions that can actually be affected. Use the dependency and scenario relationships in `SYSTEM-MAP.md`.

## Full-Baseline Reset Triggers

Start a new baseline when one or more holds:

- Major architecture, runtime, language, framework, platform, or deployment-topology shift.
- Data model, identity, authorization, tenant-isolation, or privacy model redesign.
- New crown-jewel data, regulated scope, privileged action, or materially different risk tolerance.
- Critical dependency, build/release system, agent platform, MCP/tooling, or autonomy model changes.
- Major incident, data loss, security event, or audit evidence disproves broad assumptions.
- Persistent ledgers are missing, corrupt, irreconcilably stale, or refer to a materially different system.
- Remediation rewrites broad boundaries such that targeted invalidation cannot credibly bound the impact.

Record why the baseline reset was necessary and which historical findings remain relevant.

## Prevent Technical-Debt Recurrence

When the same issue class recurs, do not schedule another identical scan as the primary response.

Promote an evidence-backed recurring rule into a durable control when appropriate:

- Structural/static lint.
- Boundary schema/type validation.
- Regression, property, integration, chaos, or recovery test.
- Shared policy/authorization/error-handling entry point.
- Generator/template correction.
- CI/release guardrail.
- Short repository rule linked to an authoritative source.
- Quality grade or recurring targeted cleanup task.

Call this a `golden principle candidate` in `FINDINGS.md`. Require an invariant, owner, enforcement mechanism, false-positive assessment, and retirement/update path.

Prefer continuous small cleanup over rare giant de-bloat rewrites. Apply `references/anti-bloat.md` when requested, but never delete security controls, migration safeguards, data-loss prevention, accessibility basics, meaningful tests, or real operational knobs merely to reduce line count.

## Verification and Stop Conditions

Complete an audit run only when:

- Every in-scope area has a coverage status, evidence, and gap record.
- Every reported finding has a reachable failure path or concrete structural/operational evidence.
- Mandatory critical scenarios have been traced or explicitly blocked.
- Authorized remediations have code-visible/config-visible closure evidence.
- Relevant tests, scanners, runtime checks, or manual validations were run, or missing evidence is explicit.
- Persistent `SYSTEM-MAP.md`, `COVERAGE.md`, and `FINDINGS.md` reflect current repository reality.
- The final report states sampling limits and never implies unaudited areas are safe.

Use the remediation convergence rules in `references/audit-loop-protocol.md`. At the hard cap, block with a diagnosis—missing profile decision, weak oracle, inaccessible production evidence, architecture conflict, unstable base, or repeated systemic failure—not a generic request to keep looping.

## Delegation Boundary

For an independent audit executor, an orchestrator may pass only:

```text
Audit {working path}, [$code-audit]({user home dir}/.codex/skills/code-audit/SKILL.md)
```

Do not leak prior suspected findings into an independent discovery pass unless the user explicitly requests a targeted audit.

A subagent receiving that minimal prompt is already the audit executor and must not delegate the same audit again.

For remediation, pass exact authorized finding IDs and frozen acceptance criteria. For final verification, provide current system scope and authoritative profile, but delay prior rationalizations until after independent inspection.

## Report

Write agent-facing persistent artifacts in English. Write each run’s `REPORT.md` in Chinese. Preserve file paths, symbols, commands, errors, evidence text, and finding IDs verbatim.

The report must include:

- Audit mode: `Baseline` or `Periodic`.
- Profile status and material assumptions.
- Repository state and audit range.
- Scope-selection rationale: critical, changed, invalidated, rotating, incident-driven, and debt follow-up.
- Quality attributes and end-to-end scenarios reviewed.
- Tests, scanners, runtime/operational evidence, and gaps.
- Findings ordered by severity and risk basis.
- Authorized repairs and verification by finding ID.
- Coverage freshness updates and next rotation priorities.
- System health summary, strongest areas, highest risks, and human decisions.

Do not mark a finding resolved unless closure is visible in the current repository/configuration and supported by verification evidence.

When committing completed audit work, include this trailer exactly once:

```text
Maintenance-Audit: true
```
