# Audit Loop Protocol

Use this protocol to run periodic audits that accumulate trustworthy coverage, target changing risk, and converge after remediation. It replaces repeated whole-repository rescans with durable state, explicit invalidation, rotating depth, and scenario verification.

## Contents

1. [Core Model](#core-model)
2. [Persistent State](#persistent-state)
3. [Baseline Audit](#baseline-audit)
4. [Periodic Audit](#periodic-audit)
5. [Scope Allocation](#scope-allocation)
6. [Coverage Freshness and Invalidation](#coverage-freshness-and-invalidation)
7. [Discovery and Evidence](#discovery-and-evidence)
8. [Decision and Remediation](#decision-and-remediation)
9. [Targeted Re-Audit](#targeted-re-audit)
10. [Full-Baseline Reset](#full-baseline-reset)
11. [Convergence and Budget](#convergence-and-budget)
12. [Golden Principles and Debt Control](#golden-principles-and-debt-control)
13. [Orchestrator Prompts](#orchestrator-prompts)
14. [Reference Pseudocode](#reference-pseudocode)

## Core Model

A periodic audit is not “review every file again.” It is a risk-control process over time:

```text
profile + system map + change history + incidents + coverage freshness + open debt
    -> scope selection
    -> evidence-backed discovery
    -> findings and gaps
    -> decisions/remediation
    -> targeted re-audit
    -> durable coverage and guardrails
```

Keep the distinction clear:

- `Baseline audit`: establish trustworthy system/risk/coverage state.
- `Periodic audit`: update changed, invalidated, critical, and rotating areas.
- `Targeted re-audit`: verify a remediation delta and its dependent scenarios.
- `Reset baseline`: rebuild broad conclusions after a material system/risk transition.

Commit count can trigger a periodic audit, but it must not determine the scope by itself. Thirty small documentation commits and one authorization redesign do not carry the same risk.

## Persistent State

Maintain four durable control artifacts.

### Audit profile

Defines:

- System boundary and owners.
- Critical workflows and crown-jewel assets.
- Risk/impact classification and tolerance.
- Quality-attribute priorities.
- Required coverage and evidence.
- Security, reliability, supply-chain, and agent baselines.
- Sampling and severity calibration.

The profile changes only when the system or risk policy changes, not for every run.

### System map

Maps:

- Components/domains and owners.
- Interfaces/contracts and dependency direction.
- Data stores/events/queues and state ownership.
- Trust boundaries and privileged actions.
- Deployment/release/operations topology.
- Agent/tooling control plane.
- Scenario paths and dependency relationships.

The map enables bounded invalidation. Without it, every change appears to require a whole-repo rescan.

### Coverage ledger

For each area/scenario records:

- Criticality and required depth.
- Last reviewed commit/date/environment.
- Evidence and known gaps.
- Dependencies and invalidation triggers.
- `Fresh`, `Stale`, `Invalidated`, or `Unknown` status.
- Next rotation reason.

### Findings/debt ledger

Persists:

- Open and closed root-cause findings.
- Accepted risk and debt with owners, ceilings, and triggers.
- Recurrent issue classes.
- Golden-principle candidates and enforcement status.
- Reopen evidence.

Do not let per-run reports replace these durable ledgers.

## Baseline Audit

Use a baseline audit to create a credible starting point.

### Step 1: approve or draft the profile

Resolve or explicitly assume:

- Critical workflows and assets.
- Risk tolerance and impact class.
- Security/reliability/control baseline.
- Required evidence.
- Exclusions and sampling limits.

Block only when an unresolved decision materially changes priority or acceptable behavior. Otherwise proceed with clearly labeled assumptions.

### Step 2: build the system map

Survey repository structure, entry points, data flows, trust boundaries, deployment, CI/CD, operations, and agent tooling. Do not deeply audit every file during mapping.

### Step 3: classify areas

Assign:

- Criticality: `Critical`, `High`, `Medium`, `Low`.
- Change/churn level.
- Evidence availability.
- Required audit depth.
- Dependency fan-in/fan-out.
- Initial freshness: usually `Unknown`.

### Step 4: define scenario portfolio

Select critical scenarios such as:

- Authentication and authorization.
- Tenant/data isolation.
- Core transaction/workflow correctness.
- Migration and rolling-deploy compatibility.
- Background job retry/idempotency.
- Dependency outage and degraded mode.
- Backup/restore and incident recovery.
- Release/rollback.
- Agent prompt-injection/tool abuse when applicable.

### Step 5: audit by risk slices

Audit critical scenarios and representative subsystem slices. Update coverage immediately after each unit. A baseline may span multiple runs; mark unreviewed areas `Unknown`, never silently complete.

### Step 6: publish baseline limits

State what is fresh, partial, unknown, excluded, or blocked. Do not call the repository “fully audited” unless the profile defines and evidence demonstrates that level of coverage.

## Periodic Audit

Use the previous ledgers as the starting point.

### Step 1: reconcile reality

- Inspect current head, tags/releases, status, and change range since the last run.
- Confirm persistent artifacts refer to current files, components, workflows, and owners.
- Read incident/bug/operational evidence since the last run.
- Identify major dependency, platform, model, harness, or tooling changes.

### Step 2: compute changed and invalidated areas

Classify changes by semantics, not file count:

- Behavior/domain.
- Data/schema/migration.
- Auth/permission/privacy.
- Concurrency/jobs/events.
- Release/config/CI/operations.
- Dependencies/build/supply chain.
- Architecture/ownership.
- Agent/harness/tooling.
- Tests/evals/validation.
- Documentation/source-of-truth.

Follow system-map edges to invalidate only conclusions whose assumptions can change.

### Step 3: add always-on critical areas

Include profile-mandated critical surfaces even without direct code changes when:

- Their evidence is stale.
- They depend on changed infrastructure or contracts.
- They carry severe impact requiring periodic confirmation.
- Incidents or telemetry indicate drift.

### Step 4: add rotating deep slices

Select areas not recently audited, prioritizing:

- High criticality.
- High churn or complexity.
- Weak tests/observability.
- Broad fan-in/fan-out.
- Accepted debt approaching its trigger.
- Ownership changes.
- Agent-generated growth or repeated patterns.

Rotation prevents stable-looking, untouched risk from remaining unaudited indefinitely.

### Step 5: add incident and finding follow-up

Include:

- Escaped defects.
- Security alerts and abuse reports.
- Flaky or suppressed checks.
- Operational toil and manual repair.
- Reopened findings.
- Risk-accepted items at review date/threshold.
- Golden-principle candidates needing evidence.

### Step 6: write explicit scope

Record selected areas, reasons, scenarios, evidence goals, exclusions, and resource limits in the run’s `SCOPE.md` before deep discovery.

## Scope Allocation

A useful starting heuristic for a normal periodic audit is:

- **35%** changed/high-churn areas and invalidated dependency cones.
- **25%** always-on critical scenarios.
- **25%** rotating deep slices.
- **15%** incidents, open findings, debt, and evidence gaps.

This is a planning heuristic, not a standard or score. Override it when risk dictates. Examples:

- An authorization redesign may consume nearly the entire cycle.
- A quiet but critical restore path may deserve more than rotating-share allocation.
- A major incident may convert the run into a targeted forensic audit.

Allocate budget by risk and evidence needed, not equal file counts.

## Coverage Freshness and Invalidation

### Fresh

Mark `Fresh` only when:

- Required scope was inspected against the recorded repository/environment.
- Required scenario or control evidence exists.
- Known gaps are below the profile’s threshold.
- No active invalidation trigger applies.

### Stale

Mark `Stale` when confidence decays without direct contradiction:

- Review age exceeds profile cadence.
- Significant churn occurred near but not inside the area.
- Dependencies/runtime versions changed without proven semantic impact.
- Runtime/operational evidence is too old.
- Ownership or documentation changed.

### Invalidated

Mark `Invalidated` when a change or event directly breaks a previous proof assumption:

- Contract/schema/interface changed.
- Caller/callee or dependency behavior changed.
- Auth/data/trust boundary changed.
- Deployment topology or configuration changed.
- A new incident disproved expected behavior.
- Remediation rewrote the reviewed path.
- Source of truth or generated artifact became inconsistent.

### Unknown

Use `Unknown` when evidence does not exist or cannot be reconciled.

### Invalidation graph

For each coverage item, store explicit dependencies and triggers. Expand invalidation through:

- API/event/schema consumers and producers.
- Data readers/writers, caches, and migrations.
- State transitions, jobs, queues, retries, and locks.
- Permission/policy/tenant boundaries.
- Config, feature flags, deployments, rollback, and observability.
- Tests/evals/docs that encode assumptions.
- Agent prompts/tools/permissions that operate on the area.

Stop when the changed node cannot affect the scenario’s required response or evidence. Record the boundary and rationale.

Avoid false precision. Do not convert statuses into a single percentage that hides critical unknowns.

## Discovery and Evidence

### Separate candidate generation from remediation

Within each scoped area:

1. State quality attributes and scenarios.
2. Generate candidate failure modes through independent lenses.
3. Trace reachability and affected invariants.
4. Attempt to falsify each candidate.
5. Run targeted tests, scans, runtime checks, or experiments.
6. Deduplicate by root cause.
7. Update evidence and coverage before moving on.

Do not repair while broad discovery is still underway for the same area; early fixes can erase evidence, bias the reviewer, and expand scope without tracking.

### Evidence portfolio

Use the strongest feasible combination:

- Current code/configuration and data-flow traces.
- Unit/integration/e2e tests.
- Property, state-machine, differential, fuzz, load, chaos, migration, rollback, or restore checks.
- Static/type/security/dependency/secret/policy scans.
- Runtime logs, metrics, traces, dashboards, alerts, and incident records.
- Deployment/build/provenance evidence.
- Manual operator/user workflow verification.
- Authoritative profile, contracts, ADRs, and generated sources.

A clean automated scan is one layer, not an audit conclusion.

### Area outcome

Each scoped area ends with:

- Coverage status and evidence.
- Findings or `No Action`.
- Gaps/assumptions.
- Invalidation triggers.
- Next rotation reason.

## Decision and Remediation

Partition findings:

- `Needs Decision`: risk tolerance, business semantics, control baseline, architecture tradeoff, compatibility, or operational behavior requires authority.
- `Agent-Fixable`: intended control and outcome are clear.
- `External Blocker`: evidence/environment/owner is unavailable.

Ask only decisions that affect remediation or risk ranking. Record the answer durably.

### Remediation wave selection

Batch findings when they share:

- One root cause or policy boundary.
- One deployment/migration sequence.
- One validation strategy.
- A bounded dependency cone.

Avoid giant “cleanup all debt” waves. They erase attribution and create new unaudited architecture.

### Repair constraints

- Freeze finding IDs and acceptance criteria.
- Preserve evidence of the original failure when safe.
- Prefer root-cause controls over local patches.
- Add an executable guardrail where recurrence is likely.
- Do not weaken tests, scans, permissions, observability, or rollback to obtain closure.
- Record changes, checks, gaps, and contract expansion.

## Targeted Re-Audit

After a remediation wave:

1. Diff from the previous audited head to the repaired head.
2. Map changed components, contracts, data, permissions, operations, and controls.
3. Expand through the invalidation graph.
4. Re-run original failure/recovery/abuse scenarios.
5. Verify each frozen acceptance criterion.
6. Inspect new branches, dependencies, states, fallbacks, and operational paths.
7. Update only affected coverage items.
8. Reopen the same finding ID if the root cause remains.
9. Create a new ID only for a distinct root cause.

Do not repeat all unaffected modules or rotate new slices inside a remediation verification round. Keep remediation verification attributable.

## Full-Baseline Reset

Reset when targeted invalidation cannot credibly bound the change.

Triggers include:

- Major architecture/runtime/platform/language/framework transition.
- Identity, authorization, tenant, privacy, or data-model redesign.
- New regulated scope, crown-jewel asset, privileged workflow, or risk appetite.
- New deployment topology, build/release chain, critical dependency, or artifact model.
- New agent platform, autonomy level, MCP/tooling trust boundary, or model/harness control plane.
- Major security/data/reliability incident.
- Broad remediation or migration changing multiple system invariants.
- Missing/corrupt ledgers or a system map that no longer describes reality.

### Reset procedure

- Archive but do not erase historical findings/evidence.
- Reapprove or update the profile.
- Rebuild the system map.
- Mark broad coverage `Unknown` or `Invalidated` as appropriate.
- Carry forward still-relevant open findings and accepted risk.
- Define a new baseline plan and scenario portfolio.

## Convergence and Budget

### Audit-run completion

Complete the run when:

- Every scoped area has a recorded outcome.
- Every finding is evidence-backed or explicitly an assumption/gap.
- Required scenarios are run or blocked with residual risk.
- Persistent ledgers are current.
- Remediation authorized in this run is verified or remains openly blocked.
- The report states coverage limits and next priorities.

An audit run may complete with open findings. `Completed` means the planned audit work is complete, not that the system is risk-free.

### Remediation loop budget

Default:

- One discovery wave for the selected audit scope.
- Up to three remediation waves in the same run.
- One independent or phase-separated final verification of remediated critical findings.
- Hard cap of five remediation waves.

At the hard cap, block remediation and diagnose:

- Missing profile/business decision.
- Weak or absent oracle.
- Architecture conflict.
- Oscillating repair.
- Scope explosion.
- Unstable repository/environment.
- Inaccessible production/third-party evidence.
- Repeated agent/harness failure.

Do not respond with only “continue?” Present bounded choices and consequences.

### Progress test

A wave progresses only if it:

- Closes a finding with evidence.
- Falsifies a candidate and closes uncertainty.
- Adds a new root cause with evidence.
- Makes coverage fresh.
- Converts recurrence into a durable control.
- Resolves an accepted-debt trigger.

Repeated scans, restated summaries, and duplicate findings are not progress.

## Golden Principles and Debt Control

### Golden-principle candidate

Promote a recurring issue when it has:

- Repeated evidence or one severe systemic occurrence.
- A clear, durable invariant.
- A mechanically enforceable or unambiguously teachable rule.
- Acceptable false-positive/maintenance cost.
- An owner and update/retirement path.

Record:

- Issue class and occurrences.
- Invariant.
- Enforcement option.
- Expected prevented failures.
- False-positive/escape risk.
- Owner.
- Rollout and validation.

Possible enforcement:

- Static/structural/policy lint.
- Schema/type validator.
- Shared boundary abstraction.
- Regression/property/integration/recovery test.
- Generator/template update.
- CI/release control.
- Short repository instruction linked to authoritative docs.

### Technical-debt record

Every accepted debt item must include:

- Owner.
- Why acceptable now.
- Safety ceiling or bounded scope.
- Observable trigger for revisit.
- Deadline/cadence when appropriate.
- Mitigations and monitoring.
- Expected removal/fix path.

“Later” is not a debt plan.

### Continuous cleanup

Prefer narrow recurring cleanup tasks over rare massive refactors. Use audit evidence to choose targeted work:

- Repeated duplicate pattern.
- Stale compatibility path.
- Dead config/flag.
- Documentation/source-of-truth drift.
- Dependency and permission creep.
- Architecture fitness violation.
- Agent-generated bloat hotspot.

Keep each cleanup reviewable, reversible, and independently verified.

## Orchestrator Prompts

### Independent audit discovery

```text
Audit {working path}, [$code-audit]({skill path}/SKILL.md)
```

Keep prior suspected findings out of an independent discovery prompt unless the user requests a targeted audit.

### Remediation agent

```text
Remediate only accepted Agent-Fixable audit findings {IDs} in {working path}.
Read {FINDINGS.md} and the current run scope/evidence.
Preserve frozen acceptance criteria. Do not commit, push, deploy, or perform unrelated cleanup.
Record the exact remediation delta and verification evidence for every ID.
```

### Targeted re-auditor

```text
Re-audit the remediation from {previous head} to {current head} for findings {IDs}.
Review the remediation delta, invalidated system-map cones, and original scenarios only.
Reopen findings whose acceptance criteria are not proven. Update persistent coverage with current evidence.
```

### Fresh final verifier

```text
Perform a fresh verification of the remediated critical audit findings in {working path} using the approved audit profile.
Start from current code/configuration, system scenarios, and raw remediation diff. Inspect independently before reading prior rationalizations, then verify ledger closure evidence.
```

## Reference Pseudocode

```text
profile = load_or_draft_profile()
map = load_or_build_system_map()
coverage = load_or_initialize_coverage()
findings = load_or_initialize_findings()
repo = reconcile_current_repository()

if broad_reset_trigger(profile, map, coverage, repo):
    mode = BASELINE
    archive_history_without_erasing_findings()
    profile = reapprove_profile(profile, repo)
    map = rebuild_system_map(repo)
    coverage = invalidate_broad_coverage(coverage)
else:
    mode = PERIODIC
    map = refresh_changed_system_map_edges(map, repo)

scope = select_scope(
    always_on=profile.required_critical_coverage,
    changed=changes_since_last_run(repo),
    invalidated=propagate_invalidation(map, coverage, repo),
    rotating=due_rotating_slices(coverage),
    incidents=recent_incidents_and_failures(),
    debt=open_findings_and_due_debt(findings)
)
write_SCOPE(scope)

for area in scope:
    scenarios = define_scenarios(area, profile, map)
    candidates = generate_hypotheses(area, scenarios)
    results = validate_falsify_and_deduplicate(candidates)
    append_EVIDENCE(area, results)
    update_coverage(area, results, repo)
    update_findings(results)

partition findings into decisions, fixable, blockers

if decisions block remediation:
    mark_remediation(BLOCKED, "authority decision required")
    ask_required_decisions(decisions)

if remediation_authorized:
    repair_waves = 0
    while accepted_fixable_findings_exist():
        if repair_waves >= 5:
            block_with_convergence_diagnosis()
            break

        wave = choose_smallest_coherent_wave()
        previous_head = current_head()
        remediate(wave)
        repair_waves += 1
        delta = diff(previous_head, current_head())

        if broad_reset_triggered_by(delta):
            record_reset()
            mode = BASELINE
            break

        invalidated = propagate_delta_invalidation(map, coverage, delta)
        verification = targeted_reaudit(wave, delta, invalidated)
        update_findings_and_coverage(verification)

        if not round_made_progress(verification):
            diagnose_and_block_or_change_control_strategy()

finalize_persistent_ledgers()
write_chinese_REPORT(
    mode, profile, scope, evidence, findings,
    coverage_updates, gaps, repairs, next_priorities
)
delete_CURRENT()
mark_audit_run(COMPLETED)
```
