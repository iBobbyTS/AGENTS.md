# Section-Aware Review Protocol

Use this protocol when `$code-review` is invoked by a sectioned large-feature workflow. It extends the ordinary review protocol without replacing its evidence, finding, repair, reset, or convergence rules.

## Contents

1. [Review modes](#1-review-modes)
2. [Section review boundary](#2-section-review-boundary)
3. [Reconstructing section intent](#3-reconstructing-section-intent)
4. [Section discovery algorithm](#4-section-discovery-algorithm)
5. [Section-specific finding classes](#5-section-specific-finding-classes)
6. [Section acceptance](#6-section-acceptance)
7. [Section reset triggers](#7-section-reset-triggers)
8. [Integration review focus](#8-integration-review-focus)
9. [Integration checkpoints](#9-integration-checkpoints)
10. [Review ledger additions](#10-review-ledger-additions)
11. [Orchestrator prompts](#11-orchestrator-prompts)

## 1. Review modes

Record exactly one primary mode before review.

### `STANDARD`

Review one ordinary PR, commit range, or working-tree diff. Use the existing skill workflow.

### `SECTION`

Review one implementation section against a frozen section contract and the feature-level invariants it may affect.

Required packet:

- Feature name and feature base.
- Section ID.
- Exact `section_base..section_head` or reproducible working-tree fingerprint.
- Feature contract or invariant source.
- Frozen section contract.
- Implementation handoff and verification evidence.
- Declared dependencies and deferred work.
- Review output path.

Verdict:

- `section-accepted`
- `section-blocked`
- `insufficient-evidence`

A `SECTION` review must not declare the whole feature mergeable.

### `DELTA`

Review one repair patch plus its invalidated impact cone. Freeze the finding IDs and acceptance criteria before repair. Use the existing delta-verification rules.

Verdict:

- `delta-verified` — all frozen findings in scope are closed and no new blocking defect was introduced inside the invalidated cone.
- `delta-blocked` — a frozen finding remains open or a new blocking defect exists inside the invalidated cone.
- `reset-required` — the repair materially changed the baseline or semantics and needs a new full discovery pass.
- `insufficient-evidence` — required closure evidence cannot be established.

### `INTEGRATION`

Review either a bounded mid-feature checkpoint or the final combination of accepted sections against the original feature contract. Record `integration_scope: CHECKPOINT | FINAL`.

Required packet:

- Feature base and current integrated head.
- Original goal, non-goals, global invariants, and applicable acceptance criteria.
- Requirement coverage matrix.
- Section status and accepted heads included in the scope.
- Cross-section contracts and integration checkpoints.
- Deferred-work ledger.
- Prior review index and available validation evidence.

Verdict for `CHECKPOINT`:

- `checkpoint-passed`
- `checkpoint-blocked`
- `checkpoint-insufficient-evidence`

Verdict for `FINAL`:

- `mergeable`
- `not mergeable`
- `insufficient evidence`

## 2. Section review boundary

The primary bounded change is `section_base..section_head`, not the entire feature branch.

Inspect outside the range only when needed to establish:

- Predecessor contract reality.
- Direct callers/callees and shared owners.
- Public API, schema, migration, permission, state, concurrency, release, or operations impact.
- Tests and documentation whose assumptions the section changes.
- Whether declared deferred work makes the current intermediate state invalid.

Do not reopen accepted predecessor implementation merely because it is nearby. Reopen it only when the current section invalidates its contract or evidence.

## 3. Reconstructing section intent

Write two separate cards.

### Feature card

- Full feature goal.
- Non-goals.
- Global invariants.
- Full-feature criteria relevant to the section.

### Section card

- Exact behavior increment or enabling seam.
- Section non-goals.
- Dependencies and predecessor heads.
- Acceptance criteria.
- Validation commands.
- Compatibility, rollout, recovery, and deferred work.

Treat the section contract as authoritative only when it agrees with repository/product authority. If it conflicts, report the conflict rather than silently reviewing to the weaker document.

## 4. Section discovery algorithm

1. Freeze review mode, base, head, contract revision, and diff fingerprint.
2. Confirm the section changes only declared scope or explain every expansion.
3. Trace the primary section behavior end to end.
4. Apply every triggered ordinary review lens.
5. Verify the section-level acceptance criteria.
6. Challenge the feature-level invariants touched by the section.
7. Inspect predecessor/consumer contracts at the seam.
8. Test at least one negative, boundary, or partial-failure path for `Medium` or `Large` risk.
9. Verify the intermediate repository/runtime state remains valid before future sections.
10. Confirm every deferred item is explicit, assigned, and safe to postpone.
11. Deduplicate symptoms under stable root-cause finding IDs.

Perform this full discovery exactly once for a stable section baseline.

## 5. Section-specific finding classes

Use the ordinary decision classes and severities. Add these common root-cause categories when relevant:

- `Contract mismatch`: implementation diverges from frozen section acceptance.
- `Feature-invariant violation`: locally correct behavior breaks a global invariant.
- `Hidden dependency`: section relies on unstated future or predecessor behavior.
- `Invalid intermediate state`: repository or runtime cannot remain safe before later sections.
- `Deferred-work leak`: required behavior is postponed without an owner or safe boundary.
- `Cross-section contract ambiguity`: producer and consumer semantics are not frozen.
- `Scope expansion`: implementation absorbs another section or unrelated cleanup.
- `Evidence gap`: claimed behavior lacks a reliable oracle in the current environment.

Do not file “the rest of the feature is not implemented” when it is explicitly and safely deferred to named sections.

## 6. Section acceptance

Return `section-accepted` only when:

- No unresolved `Must Fix` or unaccepted `Should Fix` remains.
- No blocking `Needs Decision` remains.
- Mandatory triggered coverage is complete or explicitly bounded.
- Required targeted checks pass or external blockers and residual risk are explicit.
- Accepted repair findings have independent closure evidence.
- The intermediate state is valid.
- Deferred work is explicit and assigned.
- The section preserves relevant feature-level invariants.

One clean, coverage-complete section review is sufficient when there was no repair. After repair, one successful `DELTA` verification is sufficient unless a reset trigger fires. Do not require two empty full-section reviews.

A separate `FINAL` pass is optional for an ordinary section. Use it for unusually high-risk sections or when reviewer independence materially adds evidence. The feature still requires one final `INTEGRATION` review.

## 7. Section reset triggers

Run a new full `SECTION` review when:

- Section acceptance criteria materially change.
- Public API, schema, migration, permission, tenancy, state owner, concurrency, destructive behavior, or rollout semantics change.
- The repair rewrites a substantial share of the section.
- Scope expands into another section or new feature behavior.
- The base/head changes outside the tracked implementation or repair patch.
- Predecessor integration changes the contract being reviewed.
- Evidence or ledger fingerprints are stale or contradictory.

Record the reset reason and preserve prior finding history.

## 8. Integration review focus

An `INTEGRATION` review uses the full feature range for orientation, but it should not replay every local section line by line.

Prioritize evidence that section reviews could not establish independently:

- Full behavior against the original goal.
- Requirement coverage gaps.
- Cross-section API/schema/state/permission/error contracts.
- Ordering, retries, deduplication, idempotency, and partial failure across sections.
- Combined UI/API/background-job flows.
- Migration order and mixed-version deployment states.
- Feature-flag on/off behavior, rollout, rollback, and removal.
- Security, privacy, observability, performance, cost, and operational readiness.
- Deferred items, temporary compatibility paths, debug scaffolding, and branch-scope integrity.

Read prior section ledgers after forming an independent view. Use them to verify closure and avoid duplicating already-supported local conclusions.

## 9. Integration checkpoints

For a mid-feature checkpoint, use `INTEGRATION` mode with a bounded cluster rather than whole-feature merge semantics.

Checkpoint verdicts:

- `checkpoint-passed`
- `checkpoint-blocked`
- `checkpoint-insufficient-evidence`

State exactly which sections and contracts were combined. A checkpoint may reopen an accepted section when combined evidence disproves its contract.

## 10. Review ledger additions

Add these fields to `STATE.md` or the equivalent review file:

```markdown
- Review mode: STANDARD | SECTION | DELTA | INTEGRATION
- Feature: <name>
- Feature base: <commit>
- Section/checkpoint: <ID or N/A>
- Section base/head: <commits or N/A>
- Contract path/revision: <path/version>
- Feature invariant source: <path>
- Declared dependencies: <IDs/heads>
- Declared deferred work: <items/owners>
```

For section reports, replace the final merge verdict with the section verdict and explicitly state:

```text
This verdict is provisional and does not establish whole-feature merge readiness.
```

## 11. Orchestrator prompts

### Independent section discovery

```text
Review mode: SECTION.
Review section {ID} in {working path} from {section_base} to {section_head}.
Read {feature_contract}, {section_contract}, and {handoff}.
Use [$code-review]({skill path}/SKILL.md).
Write the review to {output_path}.
Do not repair and do not review the whole feature except for the direct impact cone.
```

### Section delta verification

```text
Review mode: DELTA.
Verify findings {IDs} for section {ID} in {working path} from {repair_base} to {repair_head}.
Read the frozen findings at {ledger_path} and review only the repair delta plus its invalidated impact cone.
Use [$code-review]({skill path}/SKILL.md).
Write the result to {output_path}.
```

### Final feature integration review

```text
Review mode: INTEGRATION.
Review feature {name} in {working path} from {feature_base} to {feature_head}.
Read {feature_contract}, {feature_state}, section artifacts, and the review index.
Use [$code-review]({skill path}/SKILL.md).
Focus on full acceptance and cross-section interactions; do not mechanically replay every accepted local line.
Write the review to {output_path}.
```
