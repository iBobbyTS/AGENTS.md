---
name: sectioned-feature-development
description: "Plan and execute non-trivial software changes as reviewable sections with durable feature state, per-section contracts, independent implementation/review agents, two-clean-review section acceptance, automatic hard-cap re-decomposition, integration checkpoints, and a final cross-section gate. Use when any trigger applies: expected behavioral edits may exceed roughly 300 lines; more than three modules, packages, services, pages, or workflows are affected; the change crosses a high-risk semantic boundary; architecture or state ownership changes; the impact cone is difficult to bound; or a previous whole-change implementation/review failed to converge."
---

# Sectioned Feature Development

Develop one large feature as a sequence of bounded sections. Each section must be independently implementable, testable, reviewable, and reversible enough to diagnose. A section is provisionally accepted only after two consecutive fresh full `SECTION` reviews find no new material actionable issue. If five full review rounds fail to reach that condition, automatically preserve the failed attempt, escalate decomposition to [@sol_max](subagent://sol_max), split only the current section in `PLAN-FULL.md`, and reimplement the smaller descendants from the original section base through recursion depth `3`. Pause only before a split that would create depth `4+`, requesting Human approval for deeper recursion or a re-plan.

## Boundary and authority

- Follow repository-local instructions before this skill.
- Use this skill for one feature, refactor, migration, or architectural transition, not for periodic repository audits.
- Determine execution authority before changing product code:
  - `PLAN_ONLY`: write/validate planning artifacts only.
  - `EXECUTE_NO_COMMIT`: implement and validate without branch/commit operations.
  - `EXECUTE_WITH_COMMITS`: create/switch bounded feature or retry branches/worktrees and make section implementation/repair commits.
- A planning or review request alone does not authorize commits.
- If governing Custom Instructions explicitly delegate branch/commit authority to `$sectioned-feature-development`, that scoped delegation takes precedence over their general no-commit rule only for this workflow's bounded feature/retry branches and implementation/repair/snapshot commits.
- Never push, merge, create a pull request, rewrite published history, clean, delete user work, or discard unrelated changes unless separately authorized.
- A five-round review hard cap is **not** a user-decision point while the next split stays at recursion depth `1`–`3`. Do not ask whether to continue; run the automatic re-decomposition protocol and resume implementation.
- Count recursive split depth from the original section: `S03` is depth `0`, `S03.1` is depth `1`, `S03.1.1` is depth `2`, and `S03.1.1.1` is depth `3`. Only pause when the next required split would create depth `4` or deeper; ask Human whether to authorize deeper recursion or re-plan the affected feature boundary.
- Still stop when a real user-owned decision is required: product semantics, compatibility policy, migration meaning, acceptable risk, rollout behavior, or another non-inferable business choice.

## Trigger

Use this workflow when any condition holds:

- Expected behavioral edits are roughly more than 300 lines.
- More than three modules, packages, services, pages, or workflows are affected.
- The change crosses persistence, schema, money, time, units, security, permissions, tenancy, routing, concurrency, background jobs, public API, deployment, or shared-state boundaries.
- Architecture or state ownership changes.
- The impact cone is difficult to bound.
- A previous whole-change implementation or review loop failed to converge.

The line threshold is only a routing trigger. Semantic risk and reviewability dominate raw line count.

## Required artifacts

Use these paths unless repository rules define equivalent ones:

```text
.agent-work/
├── PLAN-FULL.md
├── PLAN.md
├── FEATURE-STATE.md
├── sections/
│   ├── S01-CONTRACT.md
│   ├── S01-HANDOFF.md
│   └── ...
├── reviews/
│   ├── S01-SECTION-r01.md
│   ├── S01-SECTION-r02.md
│   └── ...
├── replans/
│   ├── S01-g01-HARD-CAP.md
│   └── ...
└── plans/
    └── {YYYYMMDD-HHMM}_FULL.md
```

Keep `PLAN-FULL.md` and `FEATURE-STATE.md` authoritative. Chat history is not durable project state.

## Load references progressively

- Read [references/section-planning.md](references/section-planning.md) before dividing or re-dividing a feature.
- Read [references/orchestration-protocol.md](references/orchestration-protocol.md) before delegating implementation, review, repair, or hard-cap recovery.
- Read [references/integration-and-convergence.md](references/integration-and-convergence.md) before accepting a section or running integration gates.
- Read [references/artifact-schemas.md](references/artifact-schemas.md) when creating, extracting, validating, carrying forward, or archiving artifacts.

## State machine

```text
PREFLIGHT
  -> FEATURE_CONTRACT
  -> SECTION_PLAN
  -> PLAN_GATE
  -> SECTION_CONTRACT
  -> IMPLEMENT
  -> LOCAL_VALIDATE
  -> COMMIT_IF_AUTHORIZED
  -> FULL_SECTION_REVIEW
       -> CLEAN -> FULL_SECTION_REVIEW
       -> FINDINGS -> REPAIR -> COMMIT -> FULL_SECTION_REVIEW
       -> USER_DECISION -> BLOCK
       -> ROUND_5_WITHOUT_2_CLEAN -> HARD_CAP_REPLAN
  -> SECTION_ACCEPTED
  -> INTEGRATION_CHECKPOINT when triggered
  -> next SECTION_CONTRACT
  -> FEATURE_INTEGRATION_REVIEW
  -> FINAL_VALIDATE
  -> ARCHIVE_AND_REPORT

HARD_CAP_REPLAN
  -> BACKUP_FAILED_TIP
  -> CHECK_RECURSION_DEPTH
       -> DEPTH_1_TO_3 -> SOL_MAX_SPLIT_CURRENT_SECTION
       -> DEPTH_4_PLUS -> HUMAN_APPROVAL_OR_REPLAN
  -> VALIDATE_REVISED_PLAN
  -> RETRY_FROM_ORIGINAL_SECTION_BASE
  -> EXTRACT_FIRST_READY_CHILD
  -> IMPLEMENT
```

Do not advance because an agent says it is done. Advance only when the corresponding artifact and evidence gate is satisfied.

## Phase 0: Preflight and feature contract

1. Inspect repository rules, architecture sources, current branch, `git status`, relevant recent commits, build/test entry points, and validation environment.
2. Freeze the exact `feature_base` commit.
3. Use the repository's code graph/index first when governing instructions require it.
4. Create `.agent-work/PLAN-FULL.md` and record:
   - one-sentence outcome;
   - observable behavior;
   - explicit non-goals;
   - feature-level invariants;
   - authoritative constraints;
   - full acceptance criteria and validation commands;
   - ownership/state boundaries;
   - compatibility, migration, rollout, rollback, flag, observability, and cleanup requirements.
5. Identify the smallest enabling refactor if direct work would materially worsen an unsafe ownership boundary or under-tested core path.
6. In `EXECUTE_WITH_COMMITS`, create the feature branch before product-code implementation.

## Phase 1: Divide the feature

Create all initial sections in `PLAN-FULL.md` before implementation.

Prefer:

1. walking skeleton / contract proof when integration is uncertain;
2. vertical behavior slices;
3. explicit expand-migrate-contract or branch-by-abstraction stages when compatibility requires them;
4. cleanup/contraction only after consumers have moved and evidence proves the old path is unused.

Every section needs:

- stable ID such as `S01`;
- goal and observable behavior increment;
- dependency/predecessor relationship;
- expected files/symbols/workflows and semantic boundaries;
- non-goals and named deferred work;
- touched feature invariants;
- falsifiable acceptance criteria;
- exact validation commands/evidence;
- compatibility/rollout/recovery implications;
- estimated size/risk and split trigger.

A valid section can be understood by one reviewer without loading the entire feature implementation and can be verified without undocumented future work.

Use the helper when practical:

```bash
python {skill-dir}/scripts/section_plan.py validate .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py list .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S01 --output .agent-work/PLAN.md
```

Hierarchical descendant IDs are valid after a hard-cap split, for example `S03 -> S03.1, S03.2` and later `S03.1 -> S03.1.1, S03.1.2`.

## Phase 2: Plan gate

Before implementation, verify:

- every full-feature requirement maps to section evidence and final integration evidence;
- dependencies are explicit and acyclic;
- high-risk boundaries have one authoritative owner and an oracle;
- cross-section contracts/checkpoints are named;
- refactor and behavior are separated unless inseparable;
- no section is a vague “finish/integrate everything” bucket;
- each section is small enough to plausibly converge under the five-review-round rule.

Use one clean plan reviewer for ambiguous/high-risk plans. It challenges decomposition and contracts; it does not implement.

## Phase 3: Freeze one current section

For the next dependency-ready section:

1. Record `section_base` as the exact accepted predecessor head.
2. Extract exactly that section into `.agent-work/PLAN.md`.
3. Create `.agent-work/sections/{ID}-CONTRACT.md`.
4. Resolve genuine open business decisions before code.
5. Set `replan_generation` to `0` for an original section, or inherit/increment lineage for descendants.
6. Update `FEATURE-STATE.md` with section ID, lineage, base, execution path, expected checks, review round `0`, and clean streak `0`.

Ordinary implementation must not silently redefine the frozen section contract.

## Phase 4: Implement and locally validate

Delegate exactly one current section.

Default routing when these configured profiles exist:

- ordinary implementation: [@sol_medium](subagent://sol_medium);
- high-risk implementation or repair: [@sol_high](subagent://sol_high);
- section review: fresh [@sol_xhigh](subagent://sol_xhigh);
- hard-cap section re-decomposition: [@sol_max](subagent://sol_max).

The implementer receives repository rules, feature goal/invariants, current `PLAN.md`, section contract, exact `section_base`, and required checks. It must not implement future sections.

Require:

- smallest code change satisfying the section contract;
- meaningful behavior/edge/error regression coverage;
- targeted checks before broad checks;
- `.agent-work/sections/{ID}-HANDOFF.md` with files, decisions, commands/results, limitations, and head.

In `EXECUTE_WITH_COMMITS`, commit the coherent section implementation before review.

## Phase 5: Full section review loop

Each **review round** is one fresh, independent, full `$code-review` invocation in `SECTION` mode over the current `section_base..section_head` plus the direct semantic impact cone.

Use a clean [@sol_xhigh](subagent://sol_xhigh)  subagent for every counting round. Do not tell it whether previous rounds were clean and do not preload prior reviewer conclusions. Give it only the current section packet and output path:

```text
Review mode: SECTION
Section: {ID}
Range: {section_base}..{section_head}
Feature contract: .agent-work/PLAN-FULL.md
Section contract: .agent-work/sections/{ID}-CONTRACT.md
Implementation handoff: .agent-work/sections/{ID}-HANDOFF.md
Output: .agent-work/reviews/{ID}-SECTION-r{NN}.md
Use: $code-review
```

Maintain:

```text
review_round = 0
clean_streak = 0
```

For at most five full review rounds:

1. Increment `review_round` and run a fresh full `SECTION` review.
2. Main agent inspects the report and current repository state.
3. If a finding requires a genuine user-owned decision, record it and block immediately.
4. If there is **no new material actionable finding**:
   - increment `clean_streak`;
   - if `clean_streak == 2`, mark the section `section-accepted`;
   - otherwise run the next fresh full review.
5. If there is any new `Must Fix`, `Should Fix`, or blocking `Needs Decision` finding:
   - set `clean_streak = 0`;
   - deduplicate symptoms under stable root-cause IDs;
   - send only agent-fixable findings from that round to a [@sol_high](subagent://sol_high)  repair agent;
   - run the relevant deterministic checks;
   - in `EXECUTE_WITH_COMMITS`, commit the repair;
   - update the handoff and `section_head`;
   - run the next **fresh full `SECTION` review**, not a counting DELTA review.

The following do not break a clean streak unless they imply a material defect in the frozen section: repeated wording of an already-closed root cause, explicitly deferred future-section work, unsupported hypotheses, style preference, `Should Plan`, or bounded debt.

A repair validation may use targeted tests or a non-counting DELTA check internally, but only a fresh full `SECTION` review increments `review_round` or `clean_streak`.

There is **no soft cap**.

### Five-round hard cap

After review round 5, if the section has not reached two consecutive clean full reviews, do **not** ask the user whether to continue and do **not** start review round 6. Enter `HARD_CAP_REPLAN` automatically.

## Phase 6: Automatic hard-cap re-decomposition

Treat five-round non-convergence as evidence that the current section boundary is still too broad, too coupled, or insufficiently isolated for reliable agent implementation/review. Preserve the failed attempt, then retry from the original section base with smaller descendants.

### 6.1 Preserve the failed attempt

1. Record `failed_tip = HEAD`, `section_base`, current section ID, replan generation, all five review files, repair commits, and check results.
2. Ensure current-section-owned code changes are committed when commits are authorized. Never absorb unrelated user changes into the snapshot.
3. Create a backup branch **without prompting for authorization**:

```text
codex/backup/{feature-slug}-{section-id}-g{generation}-{YYYYMMDD-HHMMSS}
```

Point it at `failed_tip`. Prefer creating the ref without switching branches.
4. Write `.agent-work/replans/{section-id}-g{generation}-HARD-CAP.md` using the bundled template. Summarize, round by round, what each of the five reviews found, which root causes were repaired, what recurred, and why the section did not achieve two clean rounds.

The backup is evidence and a recovery point. Do not continue implementing on that failed code state.

### 6.2 Escalate decomposition to `@sol_max`

Before spawning `@sol_max`, calculate the depth of the descendants that the split would create.

- If the next descendants are depth `1`, `2`, or `3`, continue autonomously: invoke `@sol_max`, validate the split, create the retry branch/worktree, extract the first ready descendant, and resume implementation. Do not pause for approval or merely report progress.
- If the next descendants would be depth `4` or deeper, preserve the failed attempt as usual, record state `BLOCKED_RECURSION_DEPTH`, and pause. Ask Human to choose whether to authorize deeper recursion or re-plan the affected parent/feature boundary. Do not ask for approval at depth `0`–`3`.

Spawn a clean [@sol_max](subagent://sol_max). Explicitly tell it:

- the currently failing section ID/title and its `section_base`;
- the feature goal, invariants, and current `PLAN-FULL.md`;
- the backup branch and failed tip;
- the five review files plus a concise round-by-round issue summary;
- that the hard cap was reached;
- that it must **split only the current section in `PLAN-FULL.md` into smaller independently implementable/reviewable descendant sections**;
- that accepted predecessor sections and user-owned feature semantics are frozen;
- that it must update requirement coverage, dependency edges, downstream `Requires`, checkpoints, and deferred-work ownership affected by the split;
- that it must not implement product code;
- that descendants should use hierarchical lineage IDs such as `S03.1`, `S03.2`; if a descendant later fails, continue the hierarchy.
- the current depth and maximum autonomous depth `3`; it must not propose depth `4+` descendants without recorded Human approval.

The [@sol_max](subagent://sol_max) replan must use the five review histories as decomposition evidence: repeated bug classes should become explicit boundaries, invariants, oracles, or separate descendant sections rather than being copied as prose into one smaller-looking but semantically identical section.

### 6.3 Main-agent plan rewrite and validation

After `@sol_max` returns:

1. Main agent inspects and, if necessary, normalizes the `PLAN-FULL.md` split. `@sol_max` proposes the decomposition; the main agent owns final artifact integrity.
2. Preserve the parent section as historical lineage with state `SPLIT_AFTER_HARD_CAP`; do not schedule it again.
3. Validate the revised `PLAN-FULL.md` with `section_plan.py` and verify the dependency graph remains acyclic and every full-feature requirement remains covered.
4. If the proposed split requires a new user-owned product decision, block only for that decision. Also block with `BLOCKED_RECURSION_DEPTH` when the next descendants would be depth `4+`. Otherwise, through depth `3`, do not ask for permission merely to continue after the hard cap.
5. Update `FEATURE-STATE.md` with backup branch, failed tip, hard-cap summary, descendant IDs, and next ready descendant.

### 6.4 Retry from the original section base

Do **not** cherry-pick the failed section implementation or repair commits into the retry.

Start the descendant sequence from the failed parent section's original `section_base`:

- In `EXECUTE_WITH_COMMITS`, create a new retry branch/worktree from `section_base`. Prefer a new branch/worktree rather than resetting the failed branch.
- Carry forward only orchestration artifacts required for the revised plan/state; do not carry failed product-code diffs.
- If unrelated user changes make branch switching unsafe, leave the failed worktree untouched and create an isolated retry worktree from `section_base`.
- Record the new retry path/branch in `FEATURE-STATE.md`.

Then the **main agent** extracts the first dependency-ready descendant from revised `PLAN-FULL.md` into `.agent-work/PLAN.md` and resumes Phase 3 → Phase 5 with the normal implementer/reviewer agents.

Hard-cap recovery is recursive through depth `3` without pausing. If `S03.1` itself reaches five rounds without two consecutive clean reviews, preserve that failed attempt, call [@sol_max](subagent://sol_max), split it into `S03.1.1`, `S03.1.2`, and retry those from `S03.1`'s own `section_base`. Apply the same autonomous process for depth-`3` descendants such as `S03.1.1.1`. If another failure would require depth `4`, preserve evidence and request Human approval for deeper recursion or a re-plan instead of splitting automatically.

## Phase 7: Integration checkpoints

Run a targeted checkpoint when a public contract, schema, permission model, state owner, queue, deployment path, feature flag, or dependency cluster becomes consumable by later sections.

Verify cross-section contracts and representative end-to-end paths without reopening every accepted local line. A checkpoint may invalidate an accepted section only when actual combined behavior disproves its frozen contract evidence.

Parallelize only sections with accepted dependencies, distinct semantic owners/contracts, isolated worktrees, and deterministic integration order.

## Phase 8: Final feature integration gate

After all active leaf sections are accepted and all deferred items are resolved or explicitly approved, use a clean `$code-review` `INTEGRATION` review over `feature_base..feature_head`.

Focus on what section reviews cannot prove alone:

- original full-feature behavior and non-goals;
- cross-section API/schema/state/permission/ordering/error contracts;
- end-to-end critical paths and combined edge cases;
- migration, compatibility, rollout, rollback, flags, cleanup;
- observability, performance, security, privacy, operational readiness, documentation;
- requirement coverage and branch-scope integrity.

Repair integration findings in bounded scope and rerun the necessary integration evidence. Do not mechanically replay all accepted section reviews.

Then run the deterministic full-feature validation suite and state final readiness as `mergeable`, `not-mergeable`, or `insufficient-evidence`.

## Phase 9: Archive and report

1. Update `FEATURE-STATE.md` with every active/retired section lineage, base/head, verdict, review rounds, clean streak, backup branch, hard-cap replan, checks, decisions, and residual risk.
2. Delete transient `.agent-work/PLAN.md` only after its section is accepted, split, or explicitly abandoned and durable artifacts exist.
3. Move `.agent-work/PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md` after final reporting.
4. Keep contracts, handoffs, review evidence, and hard-cap summaries unless repository policy says otherwise.
5. Report in Chinese by default: feature result, section lineage/status, hard-cap splits, findings repaired, checks, decisions, integration result, residual risk, and maintainability judgment.

## Non-negotiable rules

- One implementer works on one extracted section/descendant at a time.
- Every counting review is a fresh full `SECTION` review from a clean reviewer context.
- Two consecutive clean full reviews are required for section acceptance.
- Any material actionable finding resets the clean streak to zero.
- Five full review rounds is a hard cap; there is no soft cap and no round 6.
- Hard-cap recovery automatically backs up the failed tip and invokes [@sol_max](subagent://sol_max) for descendant depths `1`–`3`; it does not request continuation approval at those depths.
- Only a split that would create recursion depth `4` or deeper pauses for Human approval to recurse further or re-plan. Depth `0`–`3` technical decomposition is never a pause point.
- Reimplementation after a split starts from the failed parent section's original base, not from its repeatedly repaired code.
- Failed-attempt commits are preserved on `codex/backup/***` and are not cherry-picked by default.
- A repair agent does not declare its own work accepted.
- New user-owned semantics require a real decision; ordinary technical decomposition does not.
- Section acceptance is provisional and cannot replace the final integration gate.
