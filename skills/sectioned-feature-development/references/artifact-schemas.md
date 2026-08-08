# Artifact Schemas and Lifecycle

This reference defines the durable artifacts used by the workflow and the deterministic helper script.

## Contents

1. [`PLAN-FULL.md`](#1-plan-fullmd)
2. [`PLAN.md`](#2-planmd)
3. [`FEATURE-STATE.md`](#3-feature-statemd)
4. [`{ID}-CONTRACT.md`](#4-id-contractmd)
5. [`{ID}-HANDOFF.md`](#5-id-handoffmd)
6. [Review files](#6-review-files)
7. [Hard-cap replan files](#7-hard-cap-replan-files)
8. [Archive lifecycle](#8-archive-lifecycle)
9. [Helper script commands](#9-helper-script-commands)

## 1. `PLAN-FULL.md`

Purpose: authoritative feature contract, requirement coverage, section lineage/dependency graph, integration gates, and all active section specifications.

Required top-level content:

- Feature metadata and exact base.
- Goal, user/operator behavior, non-goals, and global invariants.
- Authoritative sources and hard constraints.
- Full acceptance criteria and validation commands.
- Ownership/state-boundary map.
- Requirement coverage matrix.
- Section index, lineage, and dependency graph.
- Integration checkpoint plan.
- Rollout, rollback, migration, flag, observability, and cleanup plan.
- Decision and deferred-work ledgers.

Use exact markers so `scripts/section_plan.py` can extract stable context:

```markdown
<!-- FEATURE-CONTEXT:START -->
...feature context required by every section...
<!-- FEATURE-CONTEXT:END -->

<!-- SECTION:S01:START -->
## S01 — Title
...
<!-- SECTION:S01:END -->
```

After hard-cap re-decomposition, hierarchical IDs are valid:

```markdown
<!-- SECTION:S03.1:START -->
## S03.1 — Smaller descendant
...
<!-- SECTION:S03.1:END -->
```

If `S03.1` later requires another hard-cap split, use descendants such as `S03.1.1` and `S03.1.2`. Treat the original section as depth `0` and continue autonomously through depth `3` (for example `S03.1.1.1`). If the next descendants would be depth `4+`, record `BLOCKED_RECURSION_DEPTH` in `FEATURE-STATE.md` and the hard-cap record, then request Human approval for deeper recursion or a re-plan.

Each active section block must contain:

```markdown
### 目标
### 行为增量
### 依赖
### 预计范围
### 非目标
### 全局不变量
### 验收标准
### 验证命令
### 发布与恢复
### 延后项
```

For a hard-cap descendant, add lineage in `预计范围` or metadata, for example:

```markdown
- Lineage: `S03 -> S03.1`
- Replan generation: `1`
- Replaces parent behavior slice: `S03` (parent state: `SPLIT_AFTER_HARD_CAP`)
```

The retired parent can remain in the top-level section index/history but must not remain an active executable section block if doing so would leave contradictory dependencies. Requirement/dependency tables must point at active descendants.

## 2. `PLAN.md`

Purpose: transient execution packet for exactly one active leaf section.

Generated content includes:

- Source plan path and SHA-256 fingerprint.
- Extraction time.
- Feature context block.
- Exactly one active section block.

Do not append unrelated scratch notes. Put durable decisions in `FEATURE-STATE.md`, the section contract, or hard-cap replan record.

Delete `PLAN.md` only after the active section is accepted, split, or explicitly abandoned and durable artifacts exist.

## 3. `FEATURE-STATE.md`

Purpose: externalized state across agents, context resets, review rounds, and hard-cap retries.

Required records:

- Feature base/current head and execution mode.
- Active branch/worktree and retry branch/worktree.
- Current state and next action.
- Section status with lineage, base/head, review round, clean streak, and replan generation.
- Requirement coverage status.
- Decisions and authority.
- Open findings and review locations.
- Checks run/not run.
- Integration checkpoints.
- Hard-cap events, backup branches, failed tips, and descendant mapping.
- Reset/evidence invalidation events.
- Deferred items and residual risk.

Update it before every context handoff.

## 4. `{ID}-CONTRACT.md`

Purpose: immutable agreement for one active section attempt.

Required records:

- Section ID and lineage.
- Replan generation.
- Feature identifier.
- Frozen `section_base` and dependency heads.
- Goal, behavior, non-goals, and global invariants.
- Scope and semantic boundaries.
- Acceptance criteria and verification commands.
- Compatibility, migration, rollout, rollback, and observability.
- Allowed deferred work.
- Replan/reset triggers.
- Open user-owned decisions; must be empty before implementation.

A hard-cap split retires the parent attempt. Descendants receive new contracts rooted at the appropriate base rather than mutating the old contract in place.

## 5. `{ID}-HANDOFF.md`

Purpose: implementation or repair evidence for the next context.

Required records:

- Section ID/lineage and review round context.
- Base/head or diff fingerprint.
- Files and behavior changed.
- Decisions made and source.
- Commands run with exact outcome.
- Manual/runtime evidence.
- Known limitations and deferred work.
- Suggested impact-cone edges.
- Commit ID when authorized.

A handoff is a claim to verify, not proof by itself.

## 6. Review files

Counting section review names:

```text
{ID}-SECTION-r01.md
{ID}-SECTION-r02.md
{ID}-SECTION-r03.md
{ID}-SECTION-r04.md
{ID}-SECTION-r05.md
```

Optional non-counting repair evidence may use:

```text
{ID}-DELTA-r02-fix01.md
```

Final/integration files may use:

```text
FEATURE-INTEGRATION-r01.md
FEATURE-INTEGRATION-DELTA-r01-fix01.md
```

Every counting review file should record:

- Review mode `SECTION`.
- Exact base/head.
- Contract and feature-invariant paths.
- Coverage and critical paths.
- New material findings with stable IDs.
- Checks/evidence.
- Reviewer's local verdict.

The main orchestrator separately records `review_round` and `clean_streak`; an individual reviewer does not decide the two-clean workflow condition.

## 7. Hard-cap replan files

Naming:

```text
.agent-work/replans/{ID}-g{generation}-HARD-CAP.md
```

Required records:

- Failed parent section ID/title and lineage.
- Original `section_base`.
- Failed tip.
- `codex/backup/***` branch.
- Five review files and reviewed heads.
- Round-by-round new material findings/root causes.
- Repair commits/checks.
- Recurring failure pattern.
- `@sol_max` prompt/context summary.
- Descendant IDs and dependency/requirement changes.
- Retry branch/worktree and new active section.

Use `assets/HARD-CAP-REPLAN.template.md`.

## 8. Archive lifecycle

After final reporting:

1. Ensure `FEATURE-STATE.md` points to actual final head and final verdict.
2. Ensure active sections no longer depend on transient `PLAN.md` content.
3. Preserve parent/descendant lineage for every hard-cap split.
4. Remove transient `PLAN.md`.
5. Move `PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md`.
6. Preserve contracts, handoffs, review files, replan files, and backup branch names unless repository policy specifies otherwise.

## 9. Helper script commands

```bash
# Validate feature/section headings, markers, hierarchical IDs, references, and dependency DAG
python scripts/section_plan.py validate .agent-work/PLAN-FULL.md

# List sections and titles
python scripts/section_plan.py list .agent-work/PLAN-FULL.md

# Extract an original section
python scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S03 --output .agent-work/PLAN.md

# Extract a hard-cap descendant
python scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S03.1 --output .agent-work/PLAN.md

# Print SHA-256 fingerprint
python scripts/section_plan.py fingerprint .agent-work/PLAN-FULL.md

# Copy to timestamped archive
python scripts/section_plan.py archive \
  .agent-work/PLAN-FULL.md --dest-dir .agent-work/plans

# Move only after finalization
python scripts/section_plan.py archive \
  .agent-work/PLAN-FULL.md --dest-dir .agent-work/plans --move
```

The script refuses duplicate IDs, invalid markers/headings, self/unknown dependencies, dependency cycles, and output/archive overwrite.
