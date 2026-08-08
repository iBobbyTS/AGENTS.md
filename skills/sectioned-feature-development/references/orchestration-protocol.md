# Orchestration Protocol

Use this reference when the main agent delegates planning, section implementation, full section review, repair, automatic hard-cap re-decomposition, and final integration to separate agent contexts.

## Contents

1. [Roles](#1-roles)
2. [Context packets](#2-context-packets)
3. [Profile routing](#3-profile-routing)
4. [Section orchestration algorithm](#4-section-orchestration-algorithm)
5. [Five-round hard-cap recovery](#5-five-round-hard-cap-recovery)
6. [Commit and branch discipline](#6-commit-and-branch-discipline)
7. [Worktrees and retry isolation](#7-worktrees-and-retry-isolation)
8. [Decision handling](#8-decision-handling)
9. [State integrity](#9-state-integrity)

## 1. Roles

### Main orchestrator

Owns the feature contract, `PLAN-FULL.md`, dependency graph, execution state, subagent prompts, review-round accounting, backup/retry branch selection, and final acceptance gates. It must inspect repository state rather than trusting agent prose.

### Plan reviewer

Challenges initial section boundaries, dependencies, ownership, invariants, test oracles, compatibility, rollout, rollback, and integration checkpoints. It does not implement.

### Section implementer

Receives one extracted section and frozen contract. It implements only that section, runs requested checks, and records handoff evidence.

### Section reviewer

A fresh `sol_xhigh` context running `$code-review` in `SECTION` mode. Every counting review is a new full review of the current section range and direct semantic impact cone. It does not receive previous review conclusions before forming its own view.

### Repair agent

A `sol_high` context receiving the current round's frozen agent-fixable findings. It makes the smallest coherent repair, runs relevant checks, and records what changed. It does not decide whether the section is accepted.

### Hard-cap decomposer

A clean `@sol_max` context (profile `sol_max`) used only after five full review rounds fail to produce two consecutive clean rounds. It receives the failed section, original section base, current `PLAN-FULL.md`, and the five review histories. It splits only that section into smaller descendants and updates affected plan edges; it does not implement product code.

### Integration reviewer

A clean reviewer focused on cross-section composition and full-feature acceptance after active leaf sections are accepted.

### Decision owner

The user or accountable maintainer. Only genuine product semantics, compatibility policy, migration meaning, acceptable risk, rollout behavior, or other non-inferable business choices require this authority.

## 2. Context packets

Keep packets explicit. Do not preload persuasive history where independence matters.

### Implementer packet

```text
Working path: {path}
Feature plan: .agent-work/PLAN-FULL.md
Current execution plan: .agent-work/PLAN.md
Section: {ID}
Section contract: .agent-work/sections/{ID}-CONTRACT.md
Section base: {section_base}
Feature invariants: {IDs}
Required checks: {commands}
Commit authority: {mode}
Do not implement future sections.
```

### Full section review packet

```text
Review mode: SECTION
Working path: {path}
Section: {ID}
Range: {section_base}..{section_head}
Feature contract: .agent-work/PLAN-FULL.md
Section contract: .agent-work/sections/{ID}-CONTRACT.md
Implementation handoff: .agent-work/sections/{ID}-HANDOFF.md
Output: .agent-work/reviews/{ID}-SECTION-r{NN}.md
Use: $code-review
```

Do not include previous review findings, whether the last round was clean, or language such as “final confirmation”. The main orchestrator, not the reviewer, owns the two-clean-round rule.

### Repair packet

```text
Working path: {path}
Section: {ID}
Current reviewed head: {head}
Authorized findings from round {NN}: {IDs}
Review file: .agent-work/reviews/{ID}-SECTION-r{NN}.md
Frozen acceptance criteria: {criteria}
Section contract: .agent-work/sections/{ID}-CONTRACT.md
Required checks: {commands}
Do not broaden scope or fix unlisted speculative issues.
```

### Hard-cap `@sol_max` packet

```text
Task: Re-decompose one non-converging section. Do not implement product code.
Working path: {failed_working_path}
Feature plan: .agent-work/PLAN-FULL.md
Feature state: .agent-work/FEATURE-STATE.md
Current failed section: {ID} — {title}
Original section base: {section_base}
Failed tip: {failed_tip}
Backup branch: {backup_branch}
Hard-cap summary: .agent-work/replans/{ID}-g{generation}-HARD-CAP.md
Review files:
  - .agent-work/reviews/{ID}-SECTION-r01.md
  - .agent-work/reviews/{ID}-SECTION-r02.md
  - .agent-work/reviews/{ID}-SECTION-r03.md
  - .agent-work/reviews/{ID}-SECTION-r04.md
  - .agent-work/reviews/{ID}-SECTION-r05.md

The section failed to reach two consecutive clean full SECTION reviews within five rounds.
Split only this section into smaller independently implementable, testable, and reviewable descendants.
Preserve accepted predecessor sections and user-owned feature semantics.
Use hierarchical lineage IDs such as {ID}.1, {ID}.2; recursively extend through depth 3 without pausing.
Treat the original section as depth 0. If the proposed descendants would be depth 4+, do not split yet: return a Human-decision packet for deeper-recursion approval or boundary re-planning.
Use the five review histories as decomposition evidence: repeated root causes must become explicit boundaries, invariants, oracles, or separate descendants.
Update requirement coverage, dependency edges, downstream Requires, checkpoints, and deferred-work ownership affected by the split.
Do not carry failed implementation choices forward merely because they already exist.
```

### Integration review packet

```text
Review mode: INTEGRATION
Working path: {path}
Feature range: {feature_base}..{feature_head}
Feature contract and requirement matrix: .agent-work/PLAN-FULL.md
Feature state: .agent-work/FEATURE-STATE.md
Section contracts/handoffs: .agent-work/sections/
Review/replan evidence: .agent-work/reviews/, .agent-work/replans/
Focus: full acceptance, cross-section contracts, migration, rollout/rollback,
security, reliability, operations, cleanup, and deferred-work closure.
Output: .agent-work/reviews/FEATURE-INTEGRATION-r01.md
Use: $code-review
```

## 3. Profile routing

When the configured aliases exist, use:

- ordinary section implementation: `sol-medium`;
- high-risk section implementation and repairs: `sol_high`;
- every counting full `SECTION` review: clean `sol_xhigh`;
- five-round hard-cap re-decomposition: clean `@sol_max` (profile `sol_max`);
- final integration review: clean `sol_xhigh` unless governing instructions specify otherwise.

`@sol_max` is not a generic sixth reviewer. Its task is to change the decomposition, not to continue the same search process.

## 4. Section orchestration algorithm

```text
for section in dependency_order(active_leaf_sections):
    section_base = accepted_predecessor_head(section)
    extract_to_PLAN(section)
    freeze_contract(section, section_base)

    run_implementer(section)
    inspect_repo_and_handoff()
    run_required_checks()
    commit_if_authorized("implementation")

    review_round = 0
    clean_streak = 0

    while review_round < 5:
        review_round += 1
        section_head = current_head()
        report = run_clean_sol_xhigh_full_SECTION_review(
            section_base,
            section_head,
            output=f"{section}-SECTION-r{review_round:02d}.md"
        )

        findings = main_agent_validate_and_deduplicate(report)

        if findings.require_user_decision():
            persist_state_and_block_for_decision()

        if findings.has_no_new_material_actionable_issue():
            clean_streak += 1
            persist_round_state()
            if clean_streak == 2:
                accept_section_provisionally()
                break
            continue

        clean_streak = 0
        fixable = findings.agent_fixable_material_items()
        run_sol_high_repair(fixable)
        inspect_repo_and_handoff()
        run_relevant_checks()
        commit_if_authorized("repair")
        persist_round_state()

    if not section_is_accepted():
        hard_cap_replan(section)
        replace_parent_with_active_descendants()
        continue_from_original_section_base()
```

### What counts as material

A new `Must Fix`, `Should Fix`, or blocking `Needs Decision` root cause is material.

These normally do not reset a clean streak:

- repeated wording of an already-closed root cause;
- explicit work assigned to a later section when the current intermediate state is valid;
- unsupported hypotheses;
- style-only preferences;
- non-blocking `Should Plan` or bounded debt.

The main orchestrator makes this accounting decision from the review report and current evidence.

### DELTA checks

Targeted DELTA verification may be useful inside a repair wave, especially for risky fixes. It does not increment `review_round` and cannot increment `clean_streak`. Only a fresh full `SECTION` review counts.

## 5. Five-round hard-cap recovery

There is no soft cap. The only review-round budget is five full `SECTION` reviews per active section attempt.

If round 5 ends without `clean_streak == 2`:

1. **Do not run round 6.**
2. Determine the next descendant depth. If it is `1`–`3`, **do not ask whether to continue**. If it is `4+`, preserve evidence and request Human approval for deeper recursion or a re-plan.
3. Persist the failed attempt and review history.
4. Create `codex/backup/{feature-slug}-{section-id}-g{generation}-{timestamp}` at the failed tip.
5. Compile a round-by-round hard-cap summary.
6. For depth `1`–`3`, invoke clean `@sol_max` with the packet above. For depth `4+`, stop before invocation unless Human authorizes deeper recursion.
7. Validate the revised `PLAN-FULL.md`.
8. Mark the failed parent `SPLIT_AFTER_HARD_CAP` and activate its descendants.
9. Retry descendants from the failed parent's original `section_base`, not from the failed tip; continue directly through depth `3` without a progress pause.

### Round-by-round summary

The summary must preserve evidence, not vague “review still found issues” language:

| Round | Reviewed head | New material findings | Root cause / boundary | Repair commit | Result |
|---|---|---|---|---|---|
| 1 | `<sha>` | `REV-...` | `<...>` | `<sha>` | findings |
| 2 | `<sha>` | `...` | `...` | `<sha>` | findings/clean |
| 3 | `<sha>` | `...` | `...` | `<sha>` | ... |
| 4 | `<sha>` | `...` | `...` | `<sha>` | ... |
| 5 | `<sha>` | `...` | `...` | `—` | hard cap |

Also state recurring patterns: contract coupling, ownership ambiguity, too many behaviors, weak oracle, repair-induced interaction, or another evidence-backed cause.

### Decomposition requirements for `@sol_max`

A valid split must do more than reduce line count. Descendants should separate one or more of:

- behavior outcomes;
- ownership/state boundaries;
- contract introduction vs consumer migration;
- happy path vs risky side-effect path when independently shippable/testable;
- schema expansion vs migration vs contraction;
- policy evaluation vs enforcement integration;
- background production vs consumption/retry behavior;
- enabling refactor vs observable behavior;
- bug-prone interaction classes identified by the five reviews.

Each descendant needs an independent oracle and a stable intermediate repository state.

## 6. Commit and branch discipline

In `EXECUTE_WITH_COMMITS`:

- commit the initial coherent section implementation before its first review;
- after a review with agent-fixable material findings, make one coherent repair commit before the next full review;
- keep unrelated cleanup/user work out of section commits;
- at hard cap, ensure the failed attempt's section-owned work is committed before making the backup ref;
- the backup branch is created automatically under the skill's delegated authority;
- never push/merge the backup branch automatically.

Recommended messages:

```text
feat(section-S03): implement <behavior>
fix(section-S03): address review round 2 findings
chore(agent): snapshot S03 before hard-cap replan
```

The snapshot commit is only needed when section-owned tracked changes remain. Do not manufacture an empty snapshot commit.

## 7. Worktrees and retry isolation

After hard-cap backup, prefer a new retry branch/worktree rooted at `section_base` instead of resetting the failed branch.

Recommended retry branch:

```text
codex/retry/{feature-slug}-{section-id}-g{next-generation}-{YYYYMMDD-HHMMSS}
```

Rules:

- failed product-code commits remain only in the failed/backup lineage;
- do not cherry-pick them by default;
- carry forward the revised planning/state artifacts, not failed product-code diffs;
- if unrelated dirty user work exists, leave its worktree untouched and create an isolated retry worktree;
- update `FEATURE-STATE.md` with the new active path/branch.

## 8. Decision handling

### Must block

- required product semantics are undefined;
- two authoritative sources conflict;
- compatibility/migration behavior requires owner choice;
- acceptable risk or rollout policy cannot be inferred;
- the `@sol_max` split would require changing a frozen user-owned requirement.

### Must not block merely for permission

- review round 5 was reached;
- a backup branch must be created;
- `@sol_max` must be invoked;
- the current section must be split;
- a retry branch/worktree must be created under already delegated execution authority;
- the main agent must extract the first ready descendant and continue.

## 9. State integrity

Before every handoff, update `FEATURE-STATE.md` with:

- feature branch/worktree and active retry path;
- section ID and lineage;
- section base/current head;
- review round and clean streak;
- review report path and material finding IDs;
- repair commit/check result;
- replan generation;
- hard-cap backup branch/failed tip when applicable;
- active descendants and retired parent;
- exact next action.

After context compression, reread `PLAN-FULL.md`, `FEATURE-STATE.md`, and the current `PLAN.md` before continuing.
