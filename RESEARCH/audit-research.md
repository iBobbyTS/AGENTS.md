# Code Audit Skill Research

Research date: 2026-07-15  
AI-agent source window: 2025-07-15 through 2026-07-15  
Output target: `code-audit/SKILL.md` and its `references/` directory  
Source details: [source-register.md](source-register.md)

## Contents

1. [Executive Conclusion](#executive-conclusion)
2. [Audit Boundary and Difference from Review](#1-audit-boundary-and-difference-from-review)
3. [Research Questions](#2-research-questions)
4. [Research Method](#3-research-method)
5. [Project Audit Profile](#4-why-a-project-audit-profile-is-required)
6. [Traditional Audit Surface](#5-traditional-audit-surface)
7. [Current AI-Agent Systemic Risks](#6-current-ai-agent-systemic-risks)
8. [Making One Audit Agent Find More](#7-making-one-audit-agent-find-more-in-a-cycle)
9. [Persistent Audit Control Plane](#8-persistent-audit-control-plane)
10. [Coverage Freshness and Invalidation](#9-coverage-freshness-and-invalidation)
11. [Audit Modes](#10-baseline-periodic-targeted-and-reset-modes)
12. [Audit Remediation Loop](#11-audit-remediation-loop)
13. [Loop Engineering Applied to Audit](#12-loop-engineering-applied-to-audit)
14. [Preventing Technical-Debt Accumulation](#13-preventing-technical-debt-accumulation)
15. [Metrics](#14-metrics-for-evaluating-the-new-audit-loop)
16. [Skill Architecture Produced](#15-skill-architecture-produced)
17. [Alternatives Rejected](#16-alternatives-rejected)
18. [Limitations and Forward Validation](#17-limitations-and-forward-validation)
19. [References](#references)

## Executive Conclusion

A periodic code audit should not be implemented as “run the largest possible review over the entire repository every 30–50 commits.” Commit count is a useful reminder, but a poor measure of risk. One authorization redesign can invalidate more assurance than dozens of documentation or local UI commits.

The replacement audit skill treats audit as a persistent risk-control system:

1. Maintain an approved project audit profile.
2. Maintain a system map of workflows, assets, trust boundaries, contracts, state, deployment, and agent tooling.
3. Maintain a coverage ledger with freshness and explicit invalidation triggers.
4. Maintain a stable findings/debt ledger across audit runs.
5. Separate baseline audits, periodic audits, targeted re-audits, and full-baseline resets.
6. Select each periodic scope from always-critical areas, changed/high-churn areas, invalidated dependency cones, rotating deep slices, incidents, and open debt.
7. Perform broad discovery before remediation.
8. Re-audit only remediation deltas, affected scenarios, and invalidated conclusions unless a reset trigger fires.
9. Convert recurring failure classes into durable controls or “golden principle candidates.”
10. Report both what was reviewed and what remains unknown; never imply whole-system safety from sampling.

This design makes audit knowledge compound over time. The repository gradually becomes cheaper to audit because prior evidence, system relationships, and recurring controls remain usable instead of being discarded after every run.

## 1. Audit Boundary and Difference from Review

### 1.1 Audit use case

Use the audit skill for:

- A first full-system baseline audit.
- Periodic system-health, architecture, security, reliability, maintainability, or technical-debt audits.
- An audit after a major incident or architecture transition.
- A periodic audit of an AI-assisted or largely agent-generated repository.
- A de-bloat or over-engineering audit when explicitly requested.
- A targeted re-audit after systemic remediation.

### 1.2 Review versus audit

| Dimension | Bounded review | Periodic audit |
| --- | --- | --- |
| Primary object | One PR, commit range, or diff. | Current system and its accumulated risk. |
| Primary decision | Mergeable, not mergeable, or insufficient evidence. | Current risk posture, material findings, coverage gaps, and next control priorities. |
| Baseline | Exact base/head and change intent. | Audit profile, system map, prior coverage, incidents, current head/environment. |
| Typical scope | Changed code plus impact cone. | Critical, changed, invalidated, rotating, incident-driven, and debt-follow-up areas. |
| Persistence | Needed for large/multi-round review. | Required across audit cycles. |
| Repetition | Repair delta until merge criteria hold. | Periodic updates plus targeted deep slices; occasional full baseline reset. |
| Completion | No unresolved merge blocker and required evidence obtained. | In-scope coverage recorded, findings evidenced, gaps explicit, ledgers updated. |
| Unreviewed code | Outside the bounded change. | Remains `Stale`, `Invalidated`, or `Unknown`; never silently considered safe. |

Combining these workflows would either make review too broad or make audit too diff-centric. The final package therefore keeps separate skills and only shares conceptual patterns such as evidence, root-cause IDs, maker/checker separation, and scoped re-verification.

## 2. Research Questions

- What constitutes a traditional full-system software audit beyond code style and unit tests?
- How should an audit profile calibrate depth and severity to system risk?
- Which architecture, reliability, operations, supply-chain, and recovery areas are commonly omitted by code-centric review?
- Which systemic risks emerge in high-throughput agent-generated repositories?
- How can audit coverage remain trustworthy between runs?
- How should code changes invalidate prior conclusions without forcing a complete rescan?
- How should a periodic audit choose rotating scope?
- How should remediation be verified efficiently?
- How can repeated findings reduce future debt rather than create an endless audit/fix loop?
- Which loop-engineering practices help long-running audits, and which create false assurance or cost explosion?

## 3. Research Method

### 3.1 Input analysis

The existing audit skill was already broad and unusually strong. It covered:

- Audit framing, sampling, architecture, functional correctness, UI, state, concurrency, security, release, reliability, performance, supply chain, tests, maintainability, and AI-agent artifacts.
- Agent-first repository knowledge, agentic security/autonomy, evals, runtime/tooling, stale state, verification, and anti-bloat.
- A project audit profile, persistent `FULL.md`/`REPORT.md`, and a final repository reality check.

The main problems were operational:

- The skill body carried too much detailed knowledge at once.
- Persistent state was run-oriented rather than a complete longitudinal control plane.
- It did not fully separate baseline, periodic, targeted re-audit, and reset semantics.
- Commit cadence could still be interpreted as a full-rescan cadence.
- Coverage freshness and dependency-based invalidation were not first-class enough.
- Recurring findings were not consistently promoted into durable controls.
- Repair loops could still converge by repeated broad rescans rather than scoped evidence.

### 3.2 Search tracks

| Track | Purpose | Sources |
| --- | --- | --- |
| Traditional assurance | Define durable audit domains and control baselines. | NIST SSDF, OWASP ASVS/Top 10, SEI ATAM, Google SRE, AWS Well-Architected, SLSA. |
| Current agent-code evidence | Identify systemic degradation, persistent debt, security, review, and long-horizon risks. | 2025–2026 empirical work and benchmarks. |
| Current vendor harnesses | Identify practical repository, eval, validation, and cleanup controls. | OpenAI, Anthropic, Cursor, GitHub, Google/DORA. |
| Practitioner/community | Identify loop failure modes and field practices worth testing. | Current loop-engineering and community reports. |

### 3.3 Evidence policy

- Traditional sources establish control areas but must be tailored to the project's mission and impact.
- AI studies support audit hypotheses but do not automatically establish defects in a specific repository.
- Vendor experiences identify current control patterns but remain self-reported and context specific.
- Community reports are never treated as prevalence evidence.
- Audit findings require concrete repository, configuration, runtime, operational, or process evidence.

### 3.4 Date policy

All AI-agent-specific evidence is dated 2025-07-15 or later. Older materials are retained only for stable architecture, security, reliability, supply-chain, and software-development assurance.

## 4. Why a Project Audit Profile Is Required

A generic audit cannot prioritize correctly without knowing:

- What system is in scope.
- Who depends on it.
- Which workflows are business critical.
- Which data, secrets, money, or privileged actions are crown jewels.
- Which failures are expensive or irreversible.
- Which legal, privacy, regulatory, or contractual constraints apply.
- Which quality attributes take precedence.
- Which risk is acceptable.
- Which evidence is mandatory.

The retained `audit-profile-template.md` uses risk and assurance concepts from NIST, OWASP, ATAM, SRE, AWS, and SLSA. It is not a feature specification. It is the stable contract that tells the audit how to rank correctness, security, reliability, modifiability, performance, operability, and cost.

Without a profile, the auditor tends to:

- Overweight visible code smells.
- Underweight business workflows and data-loss paths.
- Treat all security findings as equally severe.
- Miss operational evidence that exists outside source files.
- Recommend architecture changes without understanding quality-attribute tradeoffs.
- Apply enterprise controls to a low-impact tool or under-audit a high-impact service.

The new skill therefore creates a draft profile when none exists, records assumptions, and asks for approval before relying on uncertain policy. If the user explicitly asks to continue, the audit proceeds but preserves the gaps in the final report.

## 5. Traditional Audit Surface

A full audit is a system assurance activity, not an enlarged style review. The coverage reference organizes the following control planes.

### 5.1 Governance, context, and risk

Inspect:

- System/workload boundary and owners.
- Business/mission goals and critical workflows.
- Crown-jewel assets, data, secrets, money, and privileged actions.
- Stakeholders, external systems, vendors, processors, and contractual boundaries.
- Risk/impact classification and explicit non-goals.
- Most expensive failure modes and realistic threat actors.
- Required control baseline, audit cadence, and evidence owners.

The NIST SSDF provides lifecycle-oriented practices across preparing the organization, protecting software, producing well-secured software, and responding to vulnerabilities (A-01). It supports auditing process and evidence, not only source code.

### 5.2 Architecture and quality-attribute tradeoffs

Inspect:

- Domain/component ownership and dependency direction.
- Public interfaces, event contracts, schemas, extension points, and versioning.
- State ownership and source of truth.
- Architectural decisions, known tradeoffs, and transition paths.
- Modifiability, reliability, security, performance, operability, and cost interactions.
- God modules, cycles, parallel abstractions, bypasses, and unclear ownership.

ATAM evaluates architecture against quality-attribute goals and exposes interactions/tradeoffs that can inhibit business objectives (A-04). The skill adopts scenario-based review rather than declaring an architecture “good” in the abstract.

A scenario records:

```text
stimulus + source + environment + affected artifact
    -> expected response and response measure
    -> architectural decisions and tradeoffs
    -> evidence and gaps
```

### 5.3 Functional correctness and domain integrity

Inspect:

- Critical workflows from entry point to persistence/output.
- Business rules, invariants, state transitions, and edge cases.
- Partial failure, retry, compensation, and irreversible side effects.
- Compatibility with existing data and clients.
- Consistency between UI, API, domain model, storage, jobs, and reporting.
- Money, units, dates, time zones, ordering, rounding, and identifiers.

A codebase can pass tests while implementing the wrong business semantics. The audit profile and scenario map provide the authority that line-level review lacks.

### 5.4 Identity, security, privacy, and abuse

Inspect:

- Authentication and session/token handling.
- Authorization on every object/action path.
- Tenant/data isolation and privileged operations.
- Input validation, output encoding, file/URL/command handling, deserialization, and dynamic execution.
- Secret management and leakage through logs, errors, telemetry, artifacts, caches, frontend bundles, or tools.
- Cryptographic use and key lifecycle.
- Threat models, abuse cases, least privilege, defense in depth, and security response.
- Privacy classification, minimization, consent, retention, deletion, and processor boundaries.

OWASP ASVS provides requirement-level verification depth; OWASP Top 10 is a risk index, not a complete audit (A-02, A-03). The skill preserves both code-level and system-level trust-boundary analysis.

### 5.5 Data lifecycle, persistence, and recovery

Inspect:

- Schemas, constraints, validation boundaries, migrations, backfills, and compatibility windows.
- Transactions, consistency, isolation, idempotency, and duplicate handling.
- Cache invalidation, derived state, and stale data.
- Retention, deletion, export, audit logging, and irreversible transforms.
- Backup integrity, restore testing, point-in-time recovery, disaster recovery, and ownership.
- Data corruption detection and reconciliation.

A backup configuration without tested restoration is not recovery evidence.

### 5.6 Concurrency, async work, and distributed state

Inspect:

- Races, re-entrancy, cancellation, stale response overwrite, duplicate submissions, and cleanup.
- Timers, subscriptions, workers, queues, locks, transactions, leases, and leader election.
- Retry limits, backoff, dead-letter handling, poison messages, idempotency keys, and compensation.
- State machines that accumulated flags instead of explicit transitions.
- Backpressure, overload, partition behavior, and degraded modes.

### 5.7 Reliability, operations, release, and incident response

Inspect:

- Deployment topology and environment separation.
- Configuration, feature flags, secrets, rollout sequencing, compatibility, and rollback.
- Emergency disable and degraded-mode behavior.
- SLOs/SLIs, error budgets or equivalent release-risk policy.
- Logs, metrics, traces, dashboards, alerts, and actionable runbooks.
- Latency, traffic, errors, saturation, queue depth, capacity, and correctness signals.
- Incident records, postmortems, recurrence controls, and recovery exercises.

Google SRE's monitoring guidance emphasizes user-relevant signals such as latency, traffic, errors, and saturation, while its reliability model treats acceptable unreliability as an explicit product decision (A-05, A-06). AWS Well-Architected broadens this into operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability (A-07).

### 5.8 Performance, capacity, and cost

Inspect:

- Query plans, N+1 behavior, pagination, batch sizes, payloads, memory/CPU growth, cold starts, and third-party latency.
- Capacity assumptions, quotas, limits, load tests, and scaling behavior.
- Cache correctness versus performance benefit.
- Cost drivers, runaway loops, retry storms, agent/tool token cost, and external API usage.
- Performance changes that sacrifice correctness, security, or operability.

### 5.9 Dependencies, build, provenance, and release integrity

Inspect:

- Direct/transitive dependencies, licenses, unsupported runtimes, vendored/generated code, and package scripts.
- Lockfiles, registry identity, dependency confusion, mutable references, and build-time network access.
- CI/CD identities, permissions, secrets, protected branches/tags, artifact promotion, and release signing.
- Reproducibility/traceability, SBOM or dependency inventory, provenance, and post-review artifact tampering.

SLSA build provenance models the builder, build definition, inputs, invocation, and resulting artifact so consumers can verify where an artifact came from (A-08).

### 5.10 Test, validation, and evaluation quality

Inspect:

- Unit/integration/end-to-end/system test balance.
- Negative, permission, migration, concurrency, recovery, rollback, and performance cases.
- Over-mocking, flaky tests, skipped checks, weakened thresholds, and implementation-detail assertions.
- Static analysis, type checks, linters, scanners, and browser/runtime validation.
- Whether a finding is backed by a real oracle.
- For agent systems: task evals, regression sets, model-upgrade gates, transcript/tool-call review, state checks, and production monitoring.

Anthropic's current eval guidance illustrates combining deterministic tests, rubric graders, static analysis, state checks, tool-call expectations, and cost/latency/transcript metrics (V-06). The audit skill uses this as a layered-evidence pattern rather than prescribing one universal eval stack.

### 5.11 Maintainability, ownership, and technical debt

Inspect:

- Change hotspots, churn, complexity concentration, coupling, cycles, and oversized ownership boundaries.
- Duplicate helpers/components/services/schemas/tests and parallel abstractions.
- Documentation, ADRs, runbooks, onboarding paths, and public contracts.
- Whether future maintainers can infer intent from repository-local sources.
- Debt entries with owner, ceiling, trigger, and repayment path.
- Whether current architecture makes the next likely change easier or harder.

The anti-bloat attachment adds a safe simplification ladder: delete unnecessary behavior first, prefer standard/native/existing capabilities, shrink local code before adding abstractions, and never remove safety or required controls merely to reduce line count.

## 6. Current AI-Agent Systemic Risks

The audit skill expands beyond individual suspicious patches to patterns that accumulate across a repository.

### 6.1 High-throughput local optimization

Agents often solve the immediate task using the nearest visible pattern. At repository scale this can create:

- Duplicate utilities and state owners.
- Multiple error, validation, formatting, or data-access paths.
- Compatibility layers without consumers.
- Verbose scaffolding and concentrated complexity.
- Architecture that passes each checkpoint but becomes harder to extend.

SlopCodeBench directly studies iterative extension and reports structural erosion and verbosity despite intermediate progress (E-03). OpenAI's agent-first engineering report similarly notes that agents replicate existing weak patterns, leading the team to replace weekly large cleanup with continuously enforced “golden principles” and targeted cleanup (V-01).

Audit response:

- Measure repeated patterns and public-surface growth, not only test pass/fail.
- Identify root ownership and enforce boundaries mechanically where justified.
- Rotate deep audits through high-churn areas before weak patterns spread.
- Treat cleanup as continuous control work, not a rare giant rewrite.

### 6.2 Persistent AI-introduced debt

The large-scale “Debt Behind the AI Boom” preprint reports a substantial dataset of verified AI-authored commits, frequent statically detected issue introduction, and persistence of some issues to later repository revisions (E-01).

Audit response:

- Keep a longitudinal findings/debt ledger.
- Track issue-class recurrence and survival.
- Require owner/ceiling/revisit trigger for accepted debt.
- Upgrade recurring root causes into tests, lints, shared boundaries, generators, or CI controls.
- Avoid assuming a later agent will incidentally clean up an earlier compromise.

### 6.3 Repository knowledge gaps

Current agent-review research indicates that project-specific knowledge transfer is a relative weakness for AI reviewers (E-04). Agents also start new contexts without implicit organizational memory (V-05).

Audit response:

- Audit `AGENTS.md`, skills, architecture docs, product specs, schemas, plans, and generated references as control-plane assets.
- Require a short navigational entry point and maintained deeper sources.
- Check freshness, ownership, cross-links, and mechanical refresh where possible.
- Separate authoritative documentation from generated reports and obsolete plans.
- Treat tacit or external-only policy as an audit gap.

### 6.4 Validation gaming and self-certification

An agent can make visible tests pass by changing tests, narrowing fixtures, swallowing errors, or weakening CI. A review or audit agent can also accept the implementation narrative it was given.

Audit response:

- Inspect validation posture as code.
- Preserve negative tests and required checks.
- Use independent evidence types.
- Separate maker, checker, and stop authority at high-risk points.
- Ensure agent-generated patches pass the same controls as human patches.
- Never allow an agent to mark itself complete solely through its own summary.

### 6.5 Adversarial context and prompt injection

Current review-agent research shows that deceptive PR narratives can influence review decisions even when the code reintroduces known vulnerability patterns (E-05). Agent workflows also ingest issue text, comments, docs, webpages, logs, emails, and tool output.

Audit response:

- Treat all external text as untrusted data, not policy.
- Separate claims from verification.
- Review prompt construction, tool output handling, shell execution, and secret exposure.
- Restrict egress, tool allowlists, and credential scope.
- Require approval for destructive, production, credential, deployment, or policy-changing actions.
- Audit local control planes and loopback services; `localhost` is not a trust boundary when an agent browses untrusted content or executes code.

OWASP's current agentic guidance adds risks around identity, tool use, memory, excessive autonomy, supply chain, and skills/plugins (A-09 through A-11).

### 6.6 Agent identity and self-modifying controls

Agents may operate with developer tokens, CI credentials, deployment access, connectors, or permission to modify their own prompts, hooks, scanners, and approval rules.

Audit response:

- Use separate, scoped, revocable, auditable agent identities.
- Map effective permissions, not only declared configuration.
- Prevent agents from independently widening their own scope or disabling gates.
- Require separate approval for security posture, CI permissions, deployment, production data, and destructive operations.
- Retain logs/traces long enough for investigation while scrubbing secrets and personal data.

### 6.7 Generated artifacts and provenance

Agent-generated code can include copied logic, generated schemas, vendored files, plans, reports, screenshots, datasets, binaries, and build artifacts.

Audit response:

- Identify authoritative versus derived/generated artifacts.
- Track source and generation method.
- Keep temporary or sensitive artifacts out of production bundles and git history where appropriate.
- Verify release provenance and ensure reviewed source corresponds to shipped artifacts.
- Audit license and supply-chain implications of generated or copied material.

### 6.8 Evaluation drift

Agent behavior changes with model, prompt, harness, tool, dependency, and environment upgrades.

Audit response:

- Version material model/harness changes.
- Maintain representative regression tasks and high-risk scenarios.
- Compare tool calls, state changes, cost, latency, and failure behavior—not only final task completion.
- Define rollback and monitoring signals before increasing autonomy.

## 7. Making One Audit Agent Find More in a Cycle

A single audit agent can cover more by structuring the audit around system relationships and scenarios rather than reading files in arbitrary order.

### 7.1 Reconcile reality first

Before reasoning about risk:

- Inspect current repository state, recent history, branches, generated changes, and release configuration.
- Read the current audit profile and persistent ledgers.
- Reconcile system map entries with code and runtime reality.
- Identify missing, stale, or contradicted evidence.
- Verify whether previously reported fixes are actually present.

This prevents the audit from amplifying stale summaries or old architecture assumptions.

### 7.2 Build or update the system map

Map:

- Critical workflows.
- Components and owners.
- Interfaces/contracts and dependency direction.
- Data stores, state owners, events, jobs, and queues.
- Trust boundaries and privileged actions.
- Deployment/release/operations topology.
- Agent/tooling control plane.
- Scenario dependencies and invalidation relationships.

The map is the mechanism that makes targeted future audits credible. Without it, every change appears to invalidate everything.

### 7.3 Allocate scope by risk, not file count

A periodic cycle should combine:

1. Always-on critical coverage.
2. Changed or high-churn areas since the last audited head.
3. Areas directly invalidated by changed dependencies/contracts/scenarios.
4. A rotating deep slice of stale or under-evidenced areas.
5. Incident, bug, support, and operational hotspots.
6. Open high-risk findings and debt triggers.

A 30–50 commit cadence can start this selection process, but does not determine scope or depth.

### 7.4 Run independent audit lenses before remediation

Use a discovery wave that covers:

1. Business correctness and critical invariants.
2. Architecture and quality-attribute tradeoffs.
3. Security, privacy, identity, trust, and abuse.
4. Data lifecycle, migrations, consistency, backup, restore, and deletion.
5. Concurrency, jobs, queues, retries, idempotency, and partial failure.
6. Reliability, release, rollback, degraded mode, observability, and incidents.
7. Performance, capacity, quotas, and cost.
8. Dependencies, build, CI/CD, provenance, and release artifacts.
9. Tests, evals, scanners, validation integrity, and evidence quality.
10. Maintainability, ownership, documentation, debt, and anti-bloat.
11. Agent repository/harness/autonomy/tool/memory risks where applicable.

Do not fix during candidate generation. Premature remediation narrows attention to the first visible defect and hides systemic patterns.

### 7.5 Use scenarios and properties

For each critical workflow, test concrete failure scenarios:

- Dependency unavailable during a write.
- Duplicate queue delivery.
- Old application version running during migration.
- Tenant/object identifier substituted by an attacker.
- Rollback after a partial schema deployment.
- Backup restore to a clean environment.
- Rate limit or capacity exhaustion.
- Feature flag changed during active work.
- Agent reads malicious issue/PR/tool content before executing a privileged action.

For deterministic invariants, use property/metamorphic/fuzz techniques where practical (V-07). The audit must still validate that the property reflects intended semantics.

### 7.6 Inspect runtime and operational evidence

Source code alone cannot prove:

- Alert actionability.
- Restore success.
- Deployment ordering.
- Real latency/capacity.
- Retry storms or queue recovery.
- Actual token/permission scope.
- Production-only configuration drift.

The audit should inspect logs, metrics, traces, dashboards, deployment records, incidents, restore exercises, or test-environment simulations when available. Missing production evidence is a gap or blocker, not a reason to guess.

### 7.7 Falsify and root-cause-deduplicate

For each candidate:

- State the failure scenario and violated profile requirement/invariant.
- Trace a reachable path.
- Attempt to disprove it.
- Distinguish code, configuration, process, environment, and evidence gaps.
- Group symptoms under a stable systemic root cause.
- Record affected components and scenarios.

This produces fewer but more useful findings and allows one remediation to invalidate or close all attached instances.

## 8. Persistent Audit Control Plane

The new skill maintains these artifacts:

```text
.agent-work/audit/
├── PROFILE.md
├── SYSTEM-MAP.md
├── COVERAGE.md
├── FINDINGS.md
├── CURRENT.md
└── runs/{YYYYMMDD-HHMM}/
    ├── SCOPE.md
    ├── EVIDENCE.md
    └── REPORT.md
```

A versioned project may store the profile in `docs/audit-profile.md` or `AUDIT_PROFILE.md`; the control semantics remain the same.

### 8.1 Profile

Stable risk and evidence contract. Change only when the system, mission, risk tolerance, or control baseline changes.

### 8.2 System map

Current model of components, workflows, data, trust, deployment, and agent tooling. Preserve transition history where it affects compatibility or risk.

### 8.3 Coverage ledger

For each area or scenario, record:

- Criticality and required depth.
- Last reviewed commit/date/environment.
- Evidence and gaps.
- Dependencies and invalidation triggers.
- Next rotation reason.
- `Fresh`, `Stale`, `Invalidated`, or `Unknown`.

Do not invent an aggregate “security percentage.” Concrete evidence and invalidation relationships are more actionable than fake precision.

### 8.4 Findings/debt ledger

Use stable IDs and record:

- Root cause and affected scenarios/components.
- Severity and decision class.
- Evidence, uncertainty, and status.
- Owner, accepted risk, ceiling, and revisit trigger.
- Remediation and closure evidence.
- Candidate durable control.

### 8.5 Run artifacts

Each run records selected scope and raw evidence separately from the user-facing Chinese report. This allows future audits to reuse facts without inheriting unsupported narrative conclusions.

## 9. Coverage Freshness and Invalidation

### 9.1 States

- `Fresh`: required scope and evidence were reviewed against the recorded head and environment.
- `Stale`: age, churn, dependency changes, or missing runtime evidence lowers confidence without a direct contradiction.
- `Invalidated`: a code/config/contract/incident/architecture change directly breaks the previous conclusion.
- `Unknown`: no trustworthy evidence exists.

### 9.2 Invalidation model

Invalidate a conclusion when its dependency or scenario assumption changes. Examples:

| Change | Likely invalidated coverage |
| --- | --- |
| Authorization service API changes | Object access, tenant isolation, privileged workflows, relevant tests and runbooks. |
| Schema/migration changes | Readers/writers, rollback, old/new version compatibility, backups, analytics/exports. |
| Queue retry policy changes | Idempotency, duplicate effects, backpressure, dead-letter recovery, alert thresholds. |
| Deployment topology changes | Network/trust boundaries, configuration, secrets, observability, rollback, capacity. |
| New agent MCP connector | Identity, permissions, egress, prompt injection, secret exposure, audit logging. |
| Shared formatter/validator replaced | All callers and stored/output compatibility, not unrelated modules. |

Do not invalidate the whole repository merely because a common dependency version changed. Trace which conclusions depended on the changed behavior.

### 9.3 Rotation

Rotate deep coverage based on:

- Criticality.
- Time since evidence.
- Churn and ownership changes.
- Prior gaps or accepted debt.
- Dependency exposure.
- Incident/support frequency.
- Model/harness/runtime upgrades.
- Lack of runtime validation.

A rotation ledger prevents “interesting” modules from receiving repeated attention while quiet but critical paths remain unaudited.

## 10. Baseline, Periodic, Targeted, and Reset Modes

### 10.1 Baseline audit

Use when no trustworthy persistent control plane exists. Establish:

- Approved/draft profile.
- System map.
- Initial critical scenario coverage.
- Known gaps and evidence owners.
- Findings/debt baseline.
- Rotation plan.

A baseline does not require reading every line. It requires defensible system coverage and explicit unknowns.

### 10.2 Periodic audit

Use at the normal cadence. Select changed, invalidated, critical, rotating, incident-driven, and debt-follow-up scope. Update persistent state.

### 10.3 Targeted re-audit

Use after remediation. Review:

- Repair delta.
- Affected dependencies and scenarios.
- Invalidated evidence.
- New regression/control evidence.

Do not automatically repeat the whole audit.

### 10.4 Full-baseline reset

Reset broad conclusions when:

- Architecture, runtime, language/framework, platform, or deployment topology materially changes.
- Data model, identity, authorization, tenant isolation, or privacy model is redesigned.
- New crown-jewel data, regulated scope, privileged action, or risk tolerance appears.
- Build/release system, critical dependency, agent platform, MCP/tooling, or autonomy model materially changes.
- A major incident or audit evidence disproves broad assumptions.
- Persistent ledgers are missing, corrupt, or refer to a materially different system.
- Remediation rewrites broad boundaries such that dependency-based invalidation is no longer credible.

A reset is expensive and should be evidence-triggered, not scheduled by an arbitrary round count.

## 11. Audit Remediation Loop

### 11.1 State machine

```text
RECONCILE
  -> MAP
  -> SCOPE
  -> DISCOVERY
  -> DECISION
  -> REMEDIATION (optional)
  -> TARGETED_REAUDIT
       -> REMEDIATION when accepted findings remain
       -> RESET_BASELINE when a reset trigger fires
       -> REPORT when closure conditions hold
  -> COMPLETE | BLOCKED
```

### 11.2 Discovery before repair

Complete the planned discovery wave before broad remediation. Otherwise the first repair can erase evidence, change scope, and prevent recognizing a systemic pattern.

Emergency `Must Fix` issues may be isolated and remediated early, but record the interruption and rebase the remaining audit evidence.

### 11.3 Decision classes

- `Needs Decision`: risk tolerance, business semantics, control baseline, architecture tradeoff, or operational behavior requires accountable authority.
- `Agent-Fixable`: intended outcome and constraints are sufficiently established.
- `External Blocker`: production/runtime evidence, owner input, environment, or third-party state is unavailable.

### 11.4 Remediation wave

- Freeze finding IDs, root causes, evidence, and acceptance criteria.
- Batch the smallest coherent systemic repair.
- Add the strongest affordable regression/control at the root boundary.
- Preserve unrelated repository work.
- Record code/config/process changes and verification per finding.

### 11.5 Targeted re-audit

Re-audit only:

- Changed code/configuration/process.
- Invalidated coverage entries.
- Affected critical scenarios.
- The new control's false-positive/false-negative behavior where relevant.

The audit skill shares the review skill's delta-and-impact-cone principle, but applies it to persistent system coverage.

### 11.6 Convergence and caps

Do not make “repeat until two empty whole audits” the stop condition. Complete when:

- Every in-scope area has a status, evidence, and gap record.
- Findings have concrete scenario or structural evidence.
- Mandatory critical scenarios were traced or explicitly blocked.
- Authorized remediations have current closure evidence.
- Persistent map, coverage, and findings ledgers match repository reality.
- Reported limitations prevent overclaiming.

Use a soft remediation-wave cap of three and a hard cap of five by default. At the hard cap, block with a specific diagnosis:

- Missing profile/risk decision.
- Weak or contradictory oracle.
- Inaccessible operational evidence.
- Unstable architecture/base.
- Scope expanding during remediation.
- Repeated systemic failure that needs redesign or a durable control.

## 12. Loop Engineering Applied to Audit

### 12.1 Benefits

- Persistent state survives context boundaries.
- Scope can be selected mechanically from changes and freshness.
- Independent roles can discover, repair, and verify.
- Repeated controls and cleanup can run continuously.
- Evidence and reports become reproducible.

### 12.2 Risks

| Risk | Audit-specific consequence |
| --- | --- |
| Repeated whole-repo loops | Severe cost with little new evidence. |
| Same model family as writer/reviewer/judge | Correlated blind spots become institutionalized. |
| Scanner/test optimization | Repository appears healthier while semantic or operational risk remains. |
| Stale persistent state | Old conclusions are treated as current assurance. |
| Unbounded autonomous remediation | Audit changes architecture or policy without authority. |
| Rule accumulation | “Golden principles” become a noisy, contradictory policy graveyard. |
| Audit theater | Large reports create confidence without runtime or recovery evidence. |
| Cognitive surrender | Humans accept the loop's risk ranking without owning the tradeoffs. |

Practitioner sources recommend separating maker and checker while warning that closed model loops can confidently agree on shared errors and that verification remains an accountable responsibility (C-01, C-02).

### 12.3 Design response

- Keep a human decision gate for risk, semantics, architecture, and irreversible action.
- Use fresh independent agents selectively for high-risk discovery or final verification.
- Preserve raw evidence and deterministic checks.
- Reconcile persistent state against repository/runtime reality each run.
- Version rules, assign owners, measure false positives, and retire stale controls.
- Track token/tool cost and audit yield.

## 13. Preventing Technical-Debt Accumulation

### 13.1 Recurring issue classes

A repeated issue is evidence that the system lacks a control. Mark it as a `golden principle candidate` when it has:

- A clear invariant.
- Multiple evidenced occurrences or a high-impact recurrence risk.
- A plausible enforcement mechanism.
- Acceptable false-positive cost.
- An owner and maintenance path.

Possible controls:

- Static architecture/dependency lint.
- Boundary validation/type/schema.
- Shared authorization or error-handling owner.
- Regression/property/integration/recovery test.
- Generator/template change.
- CI/release guardrail.
- Short repository rule linked to authoritative documentation.
- Scheduled targeted cleanup and quality grade.

OpenAI's current agent-first report describes replacing a weekly 20% cleanup burden with encoded principles and continuous targeted cleanup (V-01). Cursor describes converting feedback and human misses into candidate rules that can later be promoted or disabled (V-09). Both support a governed feedback-to-control path rather than permanent manual review.

### 13.2 Debt acceptance

A valid `Track as Debt` entry needs:

- Owner.
- Reason the compromise is acceptable now.
- Scope/ceiling that must not expand.
- Observable revisit trigger.
- Target control or repayment direction.
- Expiry/review date when appropriate.

Do not use “technical debt” as a label for an unowned defect.

### 13.3 Anti-bloat

When requested, apply the retained ladder:

1. Does it need to exist?
2. Does the standard library solve it?
3. Does the native platform solve it?
4. Does an installed dependency already solve it?
5. Can the behavior be expressed locally with fewer files/branches/states?
6. Only then add the smallest new abstraction.

Never remove validation at trust boundaries, security controls, data-loss prevention, migration safeguards, accessibility basics, meaningful tests, or real operational calibration solely to reduce size.

## 14. Metrics for Evaluating the New Audit Loop

Track trends rather than optimizing one number:

### Coverage

- Critical scenarios with `Fresh` evidence.
- Stale/invalidated/unknown high-risk areas.
- Rotation age by criticality.
- Runtime/recovery evidence gaps.

### Findings

- Accepted findings by severity and root-cause class.
- Duplicate/superseded findings.
- False positives or disproved candidates.
- Recurrence after remediation.
- Debt survival past trigger/ceiling.

### Convergence

- Remediation waves per finding class.
- Full-baseline resets and causes.
- Oscillation/no-progress events.
- Time/token/tool cost by discovery, remediation, and re-audit.

### Control improvement

- Recurring findings promoted to durable controls.
- Control false-positive rate and maintenance burden.
- Reduction in repeated issue classes.
- Documentation/architecture freshness violations.

### Operational outcome

- Escaped incidents linked to previously audited areas.
- Restore/recovery exercise results.
- SLO/error-budget or equivalent reliability trend.
- Release rollback and emergency-disable effectiveness.

Do not optimize “number of findings.” An audit that disproves weak hypotheses, closes unknowns, and improves durable controls can be more valuable than one that emits many low-confidence comments.

## 15. Skill Architecture Produced

| File | Responsibility |
| --- | --- |
| `code-audit/SKILL.md` | Compact executable baseline/periodic workflow, persistent state, scope selection, remediation, reset, and stop rules. |
| `code-audit/references/audit-coverage.md` | Traditional full-system control planes, scenario and evidence guidance, risk routing. |
| `code-audit/references/ai-agent-risk-catalog.md` | Systemic AI-generated repository, harness, autonomy, prompt, tool, eval, and provenance risks. |
| `code-audit/references/audit-loop-protocol.md` | Persistent-state model, baseline/periodic/targeted/reset modes, invalidation, rotation, remediation convergence, and orchestration. |
| `code-audit/references/ledger-templates.md` | Profile/system-map/coverage/findings/run templates and Chinese report structure. |
| `code-audit/references/audit-profile-template.md` | Project risk, impact, quality-attribute, control, evidence, and sampling baseline. |
| `code-audit/references/anti-bloat.md` | Safe deletion/shrink/reuse ladder and anti-bloat tags. |

The detailed references are loaded only when their audit stage or risk focus requires them. The core `SKILL.md` remains below 500 lines.

## 16. Alternatives Rejected

### Full repository rescan every 30–50 commits

Rejected because commit count does not measure risk and because it discards prior trustworthy evidence. Commit count remains a scheduling signal.

### Audit only changed files

Rejected because systemic risk lives in unchanged dependencies, operations, data, trust boundaries, recovery, and accumulated architecture. Periodic scope includes changed cones plus critical and rotating slices.

### Read every file in a baseline

Rejected as a universal requirement. A defensible baseline maps the system, critical scenarios, control evidence, and unknowns; line-by-line exhaustiveness can still be selected for high-risk modules.

### Keep one run-local report and start over next time

Rejected because audit value should compound. Persistent system, coverage, and findings ledgers are required.

### Assign one aggregate health or security score

Rejected because it hides unknowns, mixes incomparable evidence, and creates false precision. Use concrete freshness and scenario coverage.

### Let the audit agent automatically remediate everything

Rejected because risk tolerance, product semantics, architecture, data behavior, and operational tradeoffs require accountable authority. Repair is opt-in and gated.

### Treat AI-specific smells as findings

Rejected because authorship and style are not impacts. The AI catalog is a hypothesis generator; evidence remains mandatory.

### Add every lesson as a permanent rule

Rejected because rule bloat can become another stale instruction system. Promote only evidenced recurring invariants with owners and retirement paths.

### Use a giant annual cleanup

Rejected because agent-generated weak patterns can replicate quickly and giant rewrites carry high regression risk. Prefer continuous small controls and targeted cleanup.

## 17. Limitations and Forward Validation

- Many current AI-agent sources are preprints or vendor reports.
- Persistent coverage is only as accurate as the system map and invalidation relationships.
- Operational evidence may be inaccessible in local audit environments.
- A fresh verifier can share correlated model blind spots.
- Rotation policies need calibration to repository risk and change velocity.
- Long-lived ledgers themselves can become stale and must be audited.
- More controls can reduce autonomy or create false positives; measure their cost.
- The skill should be forward-tested on:
  - A new baseline audit with no profile.
  - A periodic audit after mixed low/high-risk commits.
  - A migration/auth/deployment change that invalidates several scenarios.
  - A recurring AI-generated duplication/complexity pattern promoted to a control.
  - A remediation that crosses a full-baseline reset boundary.

Measure accepted findings, evidence gaps, stale/invalidated coverage, duplicate work avoided, repair waves, reset accuracy, and token/tool cost. Update the loop protocol based on observed failure modes rather than increasing the default number of complete passes.

## References

See [source-register.md](source-register.md). The principal audit sources are A-01 through A-11, V-01, V-05 through V-14, E-01 through E-10, and C-01 through C-08.
