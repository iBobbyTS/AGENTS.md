# Review Loop Protocol

Use this protocol for a review that may repair findings and iterate. Its purpose is to maximize first-pass discovery while making later rounds incremental, evidence-driven, and convergent.

## Contents

1. [Core Rule](#core-rule)
2. [State Machine](#state-machine)
3. [Roles](#roles)
4. [Full Discovery Algorithm](#full-discovery-algorithm)
5. [Decision Gate](#decision-gate)
6. [Repair Wave](#repair-wave)
7. [Delta Verification](#delta-verification)
8. [Impact-Cone Expansion](#impact-cone-expansion)
9. [Full-Reset Triggers](#full-reset-triggers)
10. [Fresh Final Verification](#fresh-final-verification)
11. [Convergence and Budgets](#convergence-and-budgets)
12. [Same-Agent Fallback](#same-agent-fallback)
13. [Orchestrator Prompts](#orchestrator-prompts)
14. [Reference Pseudocode](#reference-pseudocode)

## Core Rule

Perform exactly one full discovery pass per stable baseline. A stable baseline may be an ordinary change, one frozen implementation section, or a final integrated feature range. After repair, review only:

- The repair delta.
- The semantic and operational impact cone invalidated by that delta.
- Previously reviewed conclusions whose evidence changed.

Start another full discovery pass only after an explicit reset trigger. Never use “run the same full review again” as the normal iteration primitive.

Separate four activities:

1. Generate failure hypotheses.
2. Validate or falsify hypotheses.
3. Repair accepted findings.
4. Verify the repaired state.

Combining them in one undifferentiated conversation encourages anchoring, self-justification, forgotten findings, and repeated scanning.

## State Machine

```text
INITIALIZE
  -> FULL_DISCOVERY
  -> DECISION_GATE
       -> BLOCKED_DECISION       when business semantics are unresolved
       -> REPAIR_WAVE            when authorized fixable findings exist
       -> FINAL_FRESH_VERIFY      when no repair is required
  -> DELTA_VERIFY
       -> REPAIR_WAVE            when accepted findings remain
       -> FULL_DISCOVERY          only after RESET
       -> FINAL_FRESH_VERIFY      when closure criteria are met
  -> COMPLETE | BLOCKED
```

Persist the state in `STATE.md` and `FINDINGS.md` for large or multi-round reviews.

Use these round modes:

- `FULL`: full discovery against a stable ordinary base/head.
- `SECTION`: full discovery for one frozen section base/head and contract.
- `DELTA`: repair delta plus invalidated impact cone.
- `RESET`: new full discovery because the baseline or semantics materially changed.
- `INTEGRATION`: cross-section or full-feature composition review.
- `FINAL`: fresh-context adversarial verification when it adds independent evidence.

## Roles

Prefer distinct roles, not necessarily distinct models:

### Discovery reviewer

- Receives the raw repository, bounded change, and ordinary skill prompt.
- Reconstructs intent and generates candidates across independent lenses.
- Does not fix code during discovery.
- Freezes evidence-backed findings with stable IDs.

### Decision owner

- Resolves product semantics, compatibility policy, risk acceptance, UX intent, and other authority-bound choices.
- Does not need to adjudicate deterministic implementation details.

### Repair agent

- Receives only accepted `Agent-Fixable` IDs, acceptance criteria, and relevant evidence.
- Makes the smallest coherent repair.
- Records exactly what changed and which checks ran.
- Cannot close findings by assertion.

### Verification reviewer

- Reviews the repair delta and impact cone.
- Reopens findings when acceptance criteria are not met.
- Creates a new stable ID only for a genuinely different root cause.

### Final fresh verifier

- Begins from current code, intent, invariants, and raw diff.
- Avoids prior reviewer rationalizations until after independent inspection.
- Checks the highest-risk workflows and closure evidence.

## Full Discovery Algorithm

### 1. Freeze the baseline

Record:

- Repository path.
- Base and head commit or exact local diff commands.
- Diff fingerprint, such as commit IDs plus a hash of the patch.
- Worktree status.
- Review depth and triggered risk lenses.

Do not begin a multi-round loop against an unspecified or moving baseline.

### 2. Build intent and invariant cards

Write:

- One-sentence goal.
- Explicit non-goals.
- User/business invariants.
- Security/data/reliability invariants.
- Compatibility and rollout assumptions.
- Claims that require verification.

An unresolved invariant becomes `Needs Decision` or an explicit evidence gap, not an invented assumption.

### 3. Map the change graph

Map changed nodes and relevant edges:

- Entry points and external interfaces.
- Callers and callees.
- State owners and event flows.
- Schemas, migrations, caches, queues, and files.
- Auth and permission gates.
- Configuration, feature flags, CI, deployment, and rollback.
- Tests, docs, logs, metrics, and alerts.

### 4. Generate candidates by lens

For each triggered lens from `review-coverage.md`:

- Enter that review mindset explicitly.
- Generate concrete failure hypotheses.
- Record candidates without editing.
- Use different scenario families: boundary values, invalid transitions, partial failure, retry, concurrency, hostile input, mixed versions, operator error, and rollback.

Do not let an early plausible finding consume the rest of the review. Finish candidate generation for all mandatory lenses first.

### 5. Validate and falsify

For every candidate:

- Trace reachability.
- Identify the violated invariant.
- Search for guards or contracts that disprove it.
- Run targeted checks where feasible.
- Record supporting and contradicting evidence.
- Drop speculative low-severity candidates that cannot be substantiated.

### 6. Root-cause deduplicate

Group findings by the smallest shared cause whose repair would close the instances. Attach locations as occurrences rather than filing one comment per line.

Examples:

- Missing object-level authorization across four routes -> one root cause with four occurrences.
- Shared serializer emits an incorrect timestamp in six APIs -> one root cause.
- Three unrelated error paths each leak different secrets -> separate findings unless one logging abstraction causes all three.

### 7. Freeze findings

Assign stable IDs. Freeze:

- Root cause.
- Trigger.
- Impact.
- Evidence.
- Severity.
- Decision class.
- Acceptance criteria.
- Initial affected scope.

Repairs may add evidence or affected occurrences, but must not quietly weaken the original acceptance criteria.

## Decision Gate

Partition open findings into:

- `Needs Decision`.
- `Agent-Fixable`.
- `External Blocker`.

Block before repair when a decision changes the safe implementation direction. Ask a compact question containing:

- Finding IDs.
- Competing semantics or risk choices.
- Consequences of each choice.
- Recommended default, if repository evidence supports one.

Do not ask the user to approve ordinary implementation details that can be derived from the existing contract.

A decision is durable evidence. Record it in the ledger and, when appropriate, in repository-local product/architecture documentation so later agents do not reopen the same ambiguity.

## Repair Wave

Group accepted findings into a wave only when they share a coherent change boundary and can be validated together.

### Repair constraints

- Fix frozen IDs only.
- Avoid opportunistic refactoring.
- Preserve the original base for comparison.
- Add or strengthen the smallest useful regression oracle.
- Prefer one root-cause fix over repeated local patches.
- Remove obsolete fallback or compatibility code when the accepted semantics make it unnecessary.
- Do not weaken tests, CI, scanners, types, permissions, or logging to obtain a green result.

### Repair output

For every ID, record:

- Files and symbols changed.
- Repair explanation.
- New or changed tests.
- Commands and outputs.
- Known gaps.
- Whether the repair changes any contract or expands scope.

A repair that changes the contract must be evaluated against the reset rules before delta verification.

## Delta Verification

Create a repair patch from the previous verified head to the new head. Review that patch rather than the whole original PR.

### Verify each repaired finding

- Reproduce or reason through the original trigger.
- Confirm the acceptance criterion.
- Confirm the root cause, not only one occurrence, is addressed.
- Check for bypasses and sibling paths.
- Run the targeted regression oracle.
- Check that the repair did not weaken another invariant.

### Search for new defects only inside the invalidated cone

- Review new branches, fallback paths, states, dependencies, permissions, and error behavior introduced by the repair.
- Inspect adjacent unchanged code only when the repair invalidates its assumptions.
- Do not reopen previously validated unaffected areas just to seek stochastic variation.

### Round result

Record:

- Findings closed, reopened, or still open.
- New root-cause findings.
- Coverage conclusions invalidated and revalidated.
- Checks run.
- Whether a reset trigger fired.

## Impact-Cone Expansion

Start with every changed file, hunk, symbol, schema, configuration key, and workflow in the repair delta. Expand only through semantically relevant edges.

### Code edges

- Direct callers and callees.
- Implementations of changed interfaces.
- Overrides and dispatch registrations.
- Shared validators, serializers, error mappers, and policy gates.
- Importers of changed constants, types, and exported APIs.

### Data edges

- Readers and writers of changed fields/tables/files/cache keys/events.
- Migrations and mixed-version compatibility.
- Indexes, constraints, retention, and restore paths.

### State/concurrency edges

- Producers/consumers of changed events.
- Locks, transactions, queues, retries, timers, cancellation, and deduplication.
- State transitions whose predicates or side effects changed.

### Security edges

- Authentication and authorization gates before and after the changed operation.
- Tenant/user scope propagation.
- Trust-boundary validation and output handling.
- Token, secret, network, filesystem, command, or tool permissions.

### Operations edges

- Config/env/feature flags.
- Deployment and rollback ordering.
- Observability and alerts.
- Capacity, quotas, and third-party failure handling.

### Evidence edges

- Tests and fixtures that encode the old behavior.
- Docs, plans, generated schemas, and runbooks used as sources of truth.
- Previous finding conclusions whose proof references changed code.

Stop expansion when an edge cannot change the observed behavior or invalidate prior evidence. Record the boundary so a later reviewer can challenge it.

## Full-Reset Triggers

Reset the baseline and run a new full discovery when any condition holds:

1. A public API, persisted schema, migration, event contract, or compatibility promise materially changes.
2. Authentication, authorization, tenant isolation, data classification, secret handling, or privileged tooling changes direction.
3. Concurrency, transaction, idempotency, destructive action, queue, or retry semantics materially change.
4. Deployment topology, release ordering, rollback, environment, CI permissions, or feature-flag strategy materially changes.
5. Ownership or architectural direction changes, such as introducing a new state owner or replacing a shared layer.
6. The repair wave expands outside the original goal or rewrites a substantial share of the behavior.
7. The base branch or head changed outside the tracked repair patch.
8. The ledger cannot be reconciled with repository reality.
9. New evidence disproves the original intent or invariant model.
10. A final verifier finds a new systemic root-cause class that could affect broad previously reviewed scope.

A configurable churn threshold, such as 20–30% of the behavioral diff being rewritten, may be used as a warning signal, not as an automatic proof. Semantic change overrides numeric thresholds.

## Fresh Final Verification

Use a fresh context when possible.

### Input order

1. Current repository and raw bounded diff.
2. Authoritative intent, invariants, and accepted decisions.
3. Required checks and high-risk workflows.
4. Prior ledger only after independent inspection.

### Required questions

- Does the current code do the requested thing and preserve the invariants?
- Is there a reachable high-impact failure the prior review missed?
- Did repairs introduce a different root cause?
- Are security/data/release claims supported by evidence?
- Does the closure evidence actually correspond to the current head?
- Is residual risk honestly bounded?

The final verifier should not redo every low-risk line. It should challenge the highest-risk conclusions, repair cones, and places where prior agents had incentives to declare completion.

## Convergence and Budgets

### Normal budget

- One `FULL` discovery round.
- Up to three repair waves under normal conditions.
- One `FINAL` fresh verification for a large ordinary review or final integration gate. It is optional for a section with no repair; after section repair, a successful independent `DELTA` verification normally suffices unless risk or a reset trigger justifies more.

### Hard cap

Use five repair waves as the default hard cap. At the cap, block and diagnose the convergence failure rather than asking a generic “continue?”

Classify the blocker:

- `Specification gap`: intended behavior is not authoritative.
- `Weak oracle`: tests/checks cannot distinguish correct from plausible.
- `Architecture conflict`: local fixes repeatedly violate another boundary.
- `Oscillation`: repairs alternate between incompatible behaviors.
- `Scope explosion`: every fix expands the impact cone.
- `Unstable base`: unrelated changes invalidate evidence.
- `Environment gap`: required behavior cannot be exercised.
- `Model/harness limitation`: the same agent repeatedly repeats a known pattern despite explicit evidence.

Offer bounded choices: decide semantics, add an oracle, split the change, redesign the boundary, restore a stable baseline, involve a specialist, accept documented residual risk, or explicitly extend the budget.

### Progress test

A round makes progress only when it does at least one:

- Closes an accepted finding with evidence.
- Proves a candidate false and removes uncertainty.
- Adds a genuinely new evidence-backed root cause.
- Closes a mandatory coverage gap.
- Converts a recurring failure into a durable test, lint, rule, or documented invariant.

Repeatedly restating a symptom, reformatting the report, or rerunning the same scan is not progress.

### Repeated failure classes

When the same issue class appears twice in one change or recurs across changes, propose a harness improvement:

- Regression test or property.
- Static or structural lint.
- Shared validator or policy gate.
- Generator/template change.
- Repository rule or architecture documentation.
- CI enforcement.

Do not turn every preference into a rule. Promote only rules with repeated evidence, a clear invariant, low false-positive cost, and an accountable owner.

## Same-Agent Fallback

When only one agent is available, simulate role separation:

1. Complete discovery without edits.
2. Persist frozen findings and coverage.
3. End the discovery phase and reread only accepted IDs.
4. Repair the smallest wave.
5. Generate a clean repair diff from the frozen head.
6. Reconstruct the impact cone from the diff rather than memory.
7. Attempt to falsify closure for each ID.
8. Perform a final pass with a different review framing and input order.

The agent must not close a finding because “I fixed it.” It must close it because the original trigger is no longer reachable or the invariant is now enforced and verified.

## Orchestrator Prompts

### Independent discovery

For `SECTION` and `INTEGRATION` review packets, also follow `section-review-protocol.md`.

```text
Review {working path}, [$code-review]({skill path}/SKILL.md)
```

Keep this prompt minimal to preserve independent variation. The reviewer gathers the repository context itself.

### Authorized repair

```text
Repair only the accepted Agent-Fixable findings {IDs} in {working path}.
Read {ledger path}. Preserve every frozen acceptance criterion.
Do not commit, push, update the PR, or perform unrelated cleanup.
Record the repair diff and verification evidence for each ID.
```

### Delta verifier

```text
Verify the repair wave from {previous head} to {current head} in {working path}.
Read the frozen findings {IDs} and review only the repair delta plus its invalidated impact cone.
Reopen any finding whose acceptance criterion is not proven. Create new IDs only for distinct root causes.
```

### Fresh final verifier

```text
Perform a fresh merge-readiness verification of {bounded change} in {working path} using [$code-review]({skill path}/SKILL.md).
Start from the current repository, authoritative intent, and invariants. Independently inspect the highest-risk paths before reading prior review rationalizations. Verify current closure evidence and report any new material root-cause class.
```

## Reference Pseudocode

```text
state = initialize_baseline_and_ledger()
mode = FULL
repair_waves = 0

while true:
    if mode in {FULL, RESET}:
        candidates = generate_candidates_across_triggered_lenses(state)
        findings = validate_falsify_and_deduplicate(candidates)
        freeze_findings(findings, state)

    decisions, fixable, blockers = partition_open_findings(state)

    if decisions block a safe repair:
        mark_goal(BLOCKED, reason="business semantics")
        ask_only_required_decisions(decisions)
        break

    if blockers prevent required evidence:
        mark_goal(BLOCKED, reason="external evidence")
        report_blockers_and_residual_risk(blockers)
        break

    if fixable is empty:
        final_result = fresh_final_verify(state)
        if final_result.has_new_material_root_cause:
            add_findings(final_result.findings, state)
            mode = RESET if final_result.is_systemic else DELTA
            continue
        if stop_conditions_hold(state):
            mark_goal(COMPLETED)
        else:
            mark_goal(BLOCKED, reason="insufficient evidence")
        break

    if repair_waves >= 5:
        mark_goal(BLOCKED, reason=diagnose_non_convergence(state))
        ask_for_bounded_resolution_choice()
        break

    wave = select_smallest_coherent_repair_wave(fixable)
    frozen_head = current_head()
    repair(wave)
    repair_waves += 1

    delta = diff(frozen_head, current_head())
    if reset_triggered(delta, state):
        record_reset_reason(state)
        state = rebaseline_preserving_finding_history(state)
        mode = RESET
        continue

    cone = expand_invalidated_impact_cone(delta, state)
    delta_result = verify_repairs_and_cone(wave, delta, cone)
    update_findings_coverage_and_evidence(delta_result, state)
    mode = DELTA
```
