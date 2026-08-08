# Integration and Convergence Guide

Use this guide to distinguish section acceptance from feature readiness and to interpret the two-clean-review / five-round hard-cap policy.

## Contents

1. [Review roles](#1-review-roles)
2. [Two-clean section acceptance](#2-two-clean-section-acceptance)
3. [Five-round hard cap](#3-five-round-hard-cap)
4. [Why hard-cap recovery splits instead of asking to continue](#4-why-hard-cap-recovery-splits-instead-of-asking-to-continue)
5. [Integration checkpoints](#5-integration-checkpoints)
6. [Final integration review](#6-final-integration-review)
7. [Reset and evidence invalidation](#7-reset-and-evidence-invalidation)
8. [Human decision points](#8-human-decision-points)
9. [Final readiness gate](#9-final-readiness-gate)

## 1. Review roles

### SECTION

A full review of one frozen section range plus its direct impact cone. Each counting round uses a fresh reviewer context.

Possible local result:

- material actionable findings;
- no new material actionable finding;
- blocked by a genuine decision/evidence gap.

The parent workflow, not the individual reviewer, decides whether two consecutive clean rounds have been achieved.

### Optional DELTA

A targeted repair check may prove that one fix closes its finding and does not break its immediate impact cone. It is useful evidence but does not count toward the five full review rounds or two-clean streak.

### INTEGRATION

A cross-section review of the assembled feature after accepted active leaf sections compose on the actual feature head. It focuses on emergent behavior rather than replaying every section line.

## 2. Two-clean section acceptance

A section is provisionally accepted only when all are true:

- section contract and base/head are stable and recorded;
- required checks pass or an external evidence blocker is explicit;
- no unresolved `Must Fix`, unaccepted `Should Fix`, or blocking `Needs Decision` remains;
- deferred work has an explicit later owner and does not make the current intermediate state invalid;
- two consecutive fresh full `SECTION` reviews discover no new material actionable root cause.

### Clean streak rules

Initialize `clean_streak = 0`.

- Clean full review -> `clean_streak += 1`.
- New material actionable finding -> `clean_streak = 0`.
- Repair -> streak remains `0` until a later full review is clean.
- Optional DELTA verification -> no effect on streak.
- Repeated wording of an already-closed root cause -> does not reset by itself.
- Unsupported hypothesis/style preference/non-blocking debt -> does not reset by itself.

The second counting reviewer must not be primed with “the previous round was clean” or prior persuasive conclusions.

## 3. Five-round hard cap

Per active section attempt:

- Maximum counting full `SECTION` reviews: **5**.
- Soft cap: **none**.
- Acceptance condition: two consecutive clean counting reviews within those five.
- Round 6 is forbidden for the same section attempt.

Examples:

```text
R1 findings -> repair
R2 clean
R3 clean
=> accepted in 3 rounds
```

```text
R1 findings -> repair
R2 findings -> repair
R3 clean
R4 findings -> repair
R5 clean
=> not accepted; hard-cap split, because clean streak is only 1
```

```text
R1 findings -> repair
R2 findings -> repair
R3 findings -> repair
R4 clean
R5 clean
=> accepted at the hard boundary
```

## 4. Why hard-cap recovery splits instead of asking to continue

Five non-convergent full reviews are treated as evidence about the decomposition, not as a request for a larger review budget.

Common evidence patterns:

- multiple independent behaviors were placed in one section;
- one section spans several state/ownership boundaries;
- repairs repeatedly disturb adjacent contracts;
- the test oracle is too broad or indirect;
- expand/migrate/contract phases were collapsed together;
- an enabling refactor and feature behavior are entangled;
- hidden cross-section dependencies were left inside the section.

Recovery therefore:

1. preserves the failed code state on `codex/backup/***`;
2. summarizes all five review rounds;
3. asks `@sol_max` to re-decompose only that section;
4. validates the new descendant plan;
5. restarts implementation from the failed parent's original `section_base`.

Do not ask the user “continue?” just because the hard cap was reached or because a technical split at recursion depth `1`–`3` is needed. Complete those splits and resume execution autonomously. A Human question is appropriate when decomposition exposes a genuine user-owned semantic decision or when the next split would create recursion depth `4+`; in the latter case ask whether to authorize deeper recursion or re-plan the affected boundary.

## 5. Integration checkpoints

Use a checkpoint when later sections begin consuming a newly established cross-section contract, including:

- API producer + first real consumer;
- schema expansion + read/write migration;
- permission policy + enforcement path;
- producer + queue/worker + retry behavior;
- new state owner + downstream consumers;
- feature flag + old/new path parity;
- independently developed branches after combination.

Checkpoint evidence should include combined head, included sections, contracts under test, happy/negative/partial-failure paths, commands/results, rollback/disable path, and known not-yet-included sections.

Checkpoint outcomes:

- `checkpoint-passed`;
- `checkpoint-blocked`;
- `checkpoint-insufficient-evidence`.

A checkpoint can invalidate prior local evidence when actual composition disproves a section assumption. Preserve the original review/replan lineage rather than rewriting history.

## 6. Final integration review

After all active leaf sections are accepted, review the assembled feature against the original contract.

### Original intent

- Does behavior satisfy the original user/operator outcome?
- Are non-goals still respected?
- Is every requirement mapped to implementation and evidence?

### Cross-section contracts

- API request/response and error semantics;
- schema/data ownership and migration order;
- state ownership and synchronization;
- authorization/tenancy consistency;
- event ordering, retry, idempotency, cancellation;
- shared UI state and loading/error/empty states;
- cleanup and feature-flag lifecycle.

### End-to-end and operations

- representative happy path;
- negative permission/input path;
- partial-failure/retry path;
- rollback/disable behavior;
- logs/metrics/traces/audit signals;
- performance/resource bounds where relevant;
- security/privacy/secret handling;
- documentation/config/runbook completeness.

### Branch integrity

- only feature-related changes are present;
- generated artifacts are reproducible;
- tests were not weakened to force green;
- temporary scaffolding is removed or explicitly owned;
- active descendant heads and review evidence correspond to the actual feature head.

## 7. Reset and evidence invalidation

A section review attempt should be treated as a new baseline when a material change alters:

- section goal or acceptance criteria;
- public API/serialized contract;
- schema/data ownership/migration order;
- auth/authorization/tenancy/privacy semantics;
- concurrency/order/retry/idempotency/destructive behavior;
- architecture/state owner/dependency direction;
- rollout/rollback/feature-flag semantics;
- scope beyond the frozen contract;
- base/head outside tracked implementation/repair operations.

Hard-cap re-decomposition is stronger than an ordinary reset: the parent attempt is retired and descendants start from the parent's original base.

## 8. Human decision points

Require the user/accountable owner for:

- ambiguous business/product behavior;
- compatibility policy choices;
- migration/backfill meaning;
- acceptable data/security/operational risk;
- rollout cohort/timing policy when not already specified;
- conflicting authoritative requirements.

Do not require user approval merely to:

- create the hard-cap backup branch;
- invoke `@sol_max`;
- split a technical section;
- create the retry branch/worktree;
- extract the first descendant and resume implementation.

All of the above remain autonomous through recursive split depth `3`. Require Human approval only before creating depth-`4+` descendants, unless another genuine user-owned decision already requires a pause.

## 9. Final readiness gate

State `mergeable` only when:

- all active leaf sections are provisionally accepted;
- parent sections retired by hard-cap splits have complete lineage/evidence;
- all full-feature requirements are covered;
- required integration checkpoints pass;
- final integration review has no unresolved material merge blocker;
- full-feature deterministic checks pass or explicit external blockers/residual risk are reported;
- rollout, rollback, migration, observability, and cleanup obligations are resolved or explicitly accepted.

Otherwise use `not-mergeable` or `insufficient-evidence`.
