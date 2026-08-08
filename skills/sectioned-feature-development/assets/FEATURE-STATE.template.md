# Feature State：<Feature Name>

## 1. Current State

- Mode: `PLAN_ONLY | EXECUTE_NO_COMMIT | EXECUTE_WITH_COMMITS`
- Working path: `<path>`
- Active feature/retry branch: `<branch/path or N/A>`
- Feature base: `<commit>`
- Current head: `<commit or diff fingerprint>`
- Current state: `<state>`
- Active section: `<Sxx / Sxx.n or none>`
- Parent lineage: `<none or Sxx -> Sxx.n>`
- Replan generation: `<0+>`
- Review round: `<0..5>`
- Clean streak: `<0..2>`
- Next action: `<exact next gate>`
- Last updated: `<timestamp>`

## 2. Feature Contract Summary

- Goal: <...>
- Non-goals: <...>
- Global invariants: `INV-01`, `INV-02`
- Plan: `.agent-work/PLAN-FULL.md`

## 3. Section Status and Lineage

| ID | Parent | State | Base | Head | Review round | Clean streak | Replan gen | Contract | Review/Handoff |
|---|---|---|---|---|---:|---:|---:|---|---|
| S01 | — | PLANNED | — | — | 0 | 0 | 0 | — | — |

Valid states include `PLANNED`, `CONTRACT_FROZEN`, `IMPLEMENTED`, `UNDER_REVIEW`, `REPAIRING`, `SECTION_ACCEPTED`, `SPLIT_AFTER_HARD_CAP`, `BLOCKED`.

## 4. Requirement Coverage

| Requirement | Active section evidence | Integration evidence | Status |
|---|---|---|---|
| R-01 | — | — | planned |

## 5. Open Findings

| Finding | Severity/class | Section/round | Frozen acceptance | Review file | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | none |

## 6. Decisions

| ID | Decision | Authority/source | Affected scope | Status |
|---|---|---|---|---|
| D-01 | <...> | <...> | Sxx | accepted/open |

## 7. Checks and Evidence

| Time | Scope | Command/evidence | Result | Artifact |
|---|---|---|---|---|
| <...> | S01 | `<command>` | pass/fail/blocked | `<path>` |

## 8. Hard-Cap Replans

| Parent | Generation | Original base | Failed tip | Backup branch | Summary | Descendants | Retry branch/worktree |
|---|---:|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — |

## 9. Integration Checkpoints

| ID | Included active sections/head | Contracts/paths | Result | Evidence |
|---|---|---|---|---|
| CP1 | — | — | planned | — |

## 10. Reset / Evidence Invalidation Events

| ID | Time | Trigger | Old baseline | New baseline | Evidence invalidated |
|---|---|---|---|---|---|
| — | — | — | — | — | none |

## 11. Deferred Work and Residual Risk

| ID | Item/risk | Required before merge? | Owner | Status/acceptance |
|---|---|---|---|---|
| — | — | — | — | none |
