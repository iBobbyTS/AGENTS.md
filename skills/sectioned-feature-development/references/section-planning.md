# Section Planning Guide

Use this guide to turn one large feature into reviewable sections without losing feature-level coherence.

## Contents

1. [Plan around behavior and invariants](#1-plan-around-behavior-and-invariants)
2. [Preferred section types](#2-preferred-section-types)
3. [Section quality test](#3-section-quality-test)
4. [Size heuristics](#4-size-heuristics)
5. [Dependency graph](#5-dependency-graph)
6. [Requirement coverage matrix](#6-requirement-coverage-matrix)
7. [Planning cross-section contracts](#7-planning-cross-section-contracts)
8. [Parallelization decision](#8-parallelization-decision)
9. [Hard-cap re-decomposition](#9-hard-cap-re-decomposition)
10. [Common anti-patterns](#10-common-anti-patterns)
11. [Example decomposition](#11-example-decomposition)

## 1. Plan around behavior and invariants

A useful section is not merely a group of files. It is a bounded change in system behavior with a known owner, explicit dependencies, and a testable completion condition.

Start from four maps:

1. **Outcome map** — user, operator, API consumer, or background-system outcomes.
2. **Invariant map** — truths that must hold across every intermediate and final state.
3. **ownership map** — modules or services that own state, decisions, and side effects.
4. **dependency map** — contracts that must exist before another section can proceed.

Do not begin by assigning one section to frontend, one to backend, and one to tests. That creates horizontal partial work whose correctness cannot be observed until late integration.

## 2. Preferred section types

### 2.1 Walking skeleton

Use a walking skeleton when the architecture, deployment route, data flow, or integration path is uncertain. Implement the thinnest end-to-end path that proves the major components can communicate and that the validation environment can observe the result.

A walking skeleton should:

- Exercise real entry and exit points.
- Use the intended ownership and dependency direction.
- Include a minimal test or demo path.
- Avoid premature breadth and polish.
- Produce information that can change later section design.

It is not a throwaway prototype unless the plan explicitly says so.

### 2.2 Vertical behavior slice

This is the default. A vertical section implements one coherent outcome across only the layers required to make it real and testable.

Examples:

- Register one account type end to end, including validation, persistence, API, UI state, and tests.
- Support one new export format from request through generated artifact and download behavior.
- Add one permission-controlled action, including policy evaluation, UI affordance, audit record, and denial tests.

A vertical section may touch several modules. Reviewability comes from one behavior and one contract, not from a low file count alone.

### 2.3 Enabling refactor

Use only when later behavior cannot be added safely without a seam, stable owner, or characterization coverage.

An enabling refactor must:

- Preserve observable behavior.
- Have protective tests before or within the same section.
- Establish a specific boundary required by named later sections.
- Avoid broad cleanup, renaming, or abstraction unrelated to the feature.
- Be independently reversible.

Separate large moves/renames from semantic changes so reviewers can distinguish structure from behavior.

### 2.4 Expand–migrate–contract

Use for incompatible APIs, schemas, event formats, state representations, or shared interfaces.

- **Expand:** add a backward-compatible new path while retaining the old path.
- **Migrate:** move consumers, data, or traffic incrementally; observe both paths.
- **Contract:** remove the old path only after evidence proves migration is complete.

Give each phase its own section or small cluster. Record the exit condition for the contract phase before starting expansion, or the temporary dual-path state may become permanent.

### 2.5 Branch by abstraction

Use when replacing a large implementation behind a stable seam.

Typical section sequence:

1. Introduce or verify an abstraction with no behavioral change.
2. Route the current implementation through it.
3. Add the new implementation behind the same contract.
4. Migrate selected callers or traffic.
5. Make the new implementation authoritative.
6. Remove the old implementation and temporary seam when appropriate.

Do not introduce an abstraction merely to make the plan look incremental. It must narrow a real semantic boundary.

### 2.6 Feature-flagged slice

Use a release flag when incomplete behavior must coexist with a deployable branch or when rollout needs controlled exposure.

Every flag needs:

- Owner.
- Default state and safe legacy behavior.
- Scope or cohort semantics.
- Test matrix for relevant on/off states.
- Rollout and rollback method.
- Expiry or removal section.

Do not use flags to hide broken intermediate states from tests.

## 3. Section quality test

A proposed section is acceptable only when all applicable questions have good answers.

### Coherence

- Does the section change one related behavior or establish one necessary seam?
- Can its purpose be stated without “and then also” clauses?
- Are refactor, generated churn, formatting, and behavior disentangled?

### Independence

- Are all predecessors explicit?
- Can the section be implemented without guessing future contracts?
- Can it be reverted without reverting unrelated sections?

### Testability

- Is there a deterministic oracle for completion?
- Can the critical path be exercised before future sections exist?
- Are negative, boundary, and failure cases named?

### Reviewability

- Can a reviewer understand the intent from the contract and diff?
- Is the impact cone bounded enough for one review session?
- Are generated files, lockfiles, migrations, or mechanical edits separated or clearly labeled?

### Integrability

- Does the repository remain buildable and operational after the section?
- Are temporary compatibility states explicit and safe?
- Is the next consumer of this section named?

### Feature coherence

- Which feature-level acceptance criteria does the section advance?
- Which global invariants does it touch?
- What remains deliberately deferred?

## 4. Size heuristics

Do not use line count as the sole splitter. Use it as a warning signal together with semantic breadth.

A normal section should usually satisfy these heuristics:

- One primary behavior or seam.
- One implementer session and one reviewer session.
- A small number of semantic owners.
- Roughly 100–400 behavioral lines when practical, excluding generated files, snapshots, lockfiles, and pure moves.
- No more than one high-risk semantic boundary unless the boundaries are inseparable.

Split again when:

- The section needs multiple independent acceptance oracles.
- Its contract contains several unrelated outcomes.
- It changes both a provider contract and many consumers without a compatibility phase.
- It mixes data migration, runtime cutover, and old-path removal.
- Review requires repeatedly switching between unrelated workflows.
- The implementation cannot be left in a valid intermediate state.
- The repair impact cone would approximate the whole feature.

Do not split so finely that a new API or abstraction has no real usage. A section must remain understandable as a working increment.

## 5. Dependency graph

Represent dependencies explicitly in `PLAN-FULL.md`.

Use these edge types:

- `requires`: implementation cannot begin until predecessor is accepted.
- `integrates-with`: sections can be built independently but need a checkpoint together.
- `migrates-from`: consumer or data migration depends on an expanded compatible path.
- `contracts`: cleanup removes a temporary path after all migrations prove complete.
- `conflicts-with`: sections cannot run in parallel because they modify the same semantic owner.

The graph must be acyclic. If two sections require each other, the boundary is wrong or a walking skeleton/common contract section is missing.

## 6. Requirement coverage matrix

Map every full-feature criterion to implementation and verification.

```markdown
| Requirement | Primary section(s) | Section oracle | Integration oracle | Status |
|---|---|---|---|---|
| R-01 | S01, S03 | targeted test | end-to-end flow | planned |
| R-02 | S02 | schema test | migration rehearsal | planned |
```

No requirement may be covered only by “final testing.” That usually means the section design has no local oracle.

Also map non-functional requirements:

- Security and authorization.
- Privacy and data retention.
- Concurrency and ordering.
- Reliability, retry, and idempotency.
- Performance and cost ceilings.
- Observability and operational control.
- Accessibility and UX states.
- Migration, rollout, rollback, and recovery.

## 7. Planning cross-section contracts

For every producer-consumer relationship, record:

- Authoritative owner.
- Data or control contract.
- Version or compatibility state.
- Error and fallback semantics.
- Ordering and idempotency assumptions.
- Security/permission context propagated.
- Test that proves the contract at the producer.
- Test that proves it at the consumer.
- Integration checkpoint that proves the combined path.

Do not rely on “both sections use the same type” as proof when runtime serialization, persistence, permissions, or deployment boundaries exist.

## 8. Parallelization decision

Parallel work is an optimization, not the default.

A pair of sections may run in parallel only when all are true:

- Neither depends on the other's code or accepted behavior.
- They do not modify the same state owner, schema, public contract, migration, or central coordinator.
- Their test fixtures and generated artifacts do not conflict.
- Their branches/worktrees are isolated.
- The integration order and checkpoint are predetermined.
- A conflict can be resolved without inventing new semantics.

When uncertain, run sequentially. Parallel agents can increase throughput while also multiplying integration states and reviewer load.

## 9. Hard-cap re-decomposition

When one active section reaches five fresh full `SECTION` review rounds without two consecutive clean rounds, do not increase the review budget. Treat the five reports as empirical evidence that the section boundary is still wrong for agentic implementation/review.

The `@sol_max` decomposer should split only the failed section and preserve accepted predecessors plus the original feature contract. Use hierarchical IDs such as `S03.1`, `S03.2`; if `S03.1` later fails, use `S03.1.1`, `S03.1.2`.

Count dots in the lineage ID as recursive split depth: `S03` is depth `0`, `S03.1` depth `1`, `S03.1.1` depth `2`, and `S03.1.1.1` depth `3`. Complete hard-cap backup, decomposition, plan validation, retry setup, and descendant execution autonomously through depth `3`. Only when the next split would create depth `4+` should orchestration pause and ask Human whether to authorize deeper recursion or re-plan the affected boundary.

Good split axes include:

- one observable behavior per descendant;
- one authoritative state/ownership boundary per descendant where practical;
- contract introduction separated from consumer migration;
- schema expand, data migrate, and contract/remove separated;
- enabling refactor separated from behavior;
- policy definition separated from enforcement integration;
- producer separated from worker/retry/dead-letter behavior;
- root-cause classes repeatedly exposed by different review rounds separated into independent oracles.

A valid re-decomposition must update:

- requirement coverage matrix;
- dependency graph and downstream `Requires`;
- integration checkpoints;
- deferred-work ownership;
- section lineage and replan generation.

Do not preserve failed implementation structure merely because code already exists. The retry starts from the failed parent section's original `section_base`; the backup branch exists for forensic comparison and recovery, not as the new implementation base.

## 10. Common anti-patterns

### Horizontal layer plan

```text
S01 database
S02 backend
S03 frontend
S04 tests
```

Problem: no section has an observable outcome, tests arrive after design errors have compounded, and the final section becomes the first real integration.

Better: slice by outcome, with contract or migration sections only where necessary.

### One section per directory or file type

Problem: file layout is not a semantic boundary. Reviewers still need the whole feature to know whether a section is correct.

### “Foundation” section with speculative abstractions

Problem: the agent designs APIs without actual usage evidence, and later sections inherit wrong assumptions.

Better: pair a new seam with at least one real use or walking skeleton.

### Final “wire everything together” section

Problem: all cross-section risk is delayed to the largest, least reviewable step.

Better: define integration checkpoints after each dependency cluster.

### Mixed refactor and behavior

Problem: movement and semantics obscure each other, making defects and rollback harder.

Better: enabling refactor first with characterization tests, then behavior.

### Parallel dependent agents

Problem: both agents invent the shared contract, resulting in incompatible implementations or a large reconciliation patch.

Better: freeze the shared contract in an accepted predecessor section.

### “Done” defined by files changed

Problem: agents optimize for output rather than behavior.

Better: define observable acceptance criteria and commands.

## 11. Example decomposition

Feature: add resumable bulk upload with per-tenant quotas.

```text
S00  Walking skeleton: one small upload travels through UI, API, storage, and status readback.
S01  Quota policy owner and denial behavior with unit/contract tests.
S02  Expand upload session schema/API for resumable offsets; old single-shot path remains valid.
S03  Implement server-side chunk validation, idempotency, and recovery.
S04  Implement client resume flow and user-visible states behind a release flag.
CP1  Integrate S01–S04: quota + interrupted upload + resume end to end.
S05  Migrate eligible callers and telemetry dashboards.
S06  Rollout controls, cleanup, documentation, and remove obsolete path after evidence.
FINAL Cross-section acceptance, migration rehearsal, rollback, security, performance, and flag-lifecycle review.
```

This plan has vertical outcomes, explicit high-risk boundaries, an intermediate integration checkpoint, and a defined contraction phase.
