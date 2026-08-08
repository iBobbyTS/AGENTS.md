# Hard-Cap Replan：<Section ID — Title>

## Failed Attempt

- Feature: `<name>`
- Parent section: `<Sxx / Sxx.n>`
- Parent lineage: `<...>`
- Replan generation: `<n>`
- Original section base: `<commit>`
- Failed tip: `<commit>`
- Backup branch: `codex/backup/<...>`
- Failed working path: `<path>`
- Hard cap: `5 full SECTION reviews`
- Required acceptance: `2 consecutive clean full SECTION reviews`

## Five Review Rounds

| Round | Reviewed head | New material findings | Root cause / boundary | Repair commit | Result |
|---:|---|---|---|---|---|
| 1 | `<sha>` | `<REV ids / none>` | `<...>` | `<sha / —>` | `findings / clean` |
| 2 | `<sha>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 3 | `<sha>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 4 | `<sha>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 5 | `<sha>` | `<...>` | `<...>` | `<...>` | `hard-cap / clean` |

## Review Artifacts

- `.agent-work/reviews/<ID>-SECTION-r01.md`
- `.agent-work/reviews/<ID>-SECTION-r02.md`
- `.agent-work/reviews/<ID>-SECTION-r03.md`
- `.agent-work/reviews/<ID>-SECTION-r04.md`
- `.agent-work/reviews/<ID>-SECTION-r05.md`

## Convergence Diagnosis

- Recurring root-cause classes: <...>
- Coupled ownership/contracts: <...>
- Weak or over-broad oracle: <...>
- Repair-induced interactions: <...>
- Evidence that motivates the split: <...>

## @sol_max Re-decomposition Request

- Split only this parent section.
- Preserve accepted predecessors and user-owned feature semantics.
- Use hierarchical descendant IDs.
- Update requirement coverage, dependency edges, downstream `Requires`, checkpoints, and deferred-work ownership.
- Do not implement product code.
- Do not copy failed implementation structure without re-deriving the boundary from the review evidence.

## Resulting Descendants

| ID | Goal | Depends on | Independent oracle | Review-risk reduction |
|---|---|---|---|---|
| `<Sxx.1>` | <...> | <...> | <...> | <...> |
| `<Sxx.2>` | <...> | <...> | <...> | <...> |

## Retry

- Parent state: `SPLIT_AFTER_HARD_CAP`
- Retry starts from: `<original section base>`
- Retry branch/worktree: `<codex/retry/...>`
- First ready descendant: `<Sxx.1>`
- Failed implementation commits cherry-picked: `no`
