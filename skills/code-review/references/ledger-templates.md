# Code Review Ledger Templates

Use these templates for `Large` reviews, repair-enabled loops, or work that must survive context compression. Keep agent-facing ledgers in English. Write the final `REPORT.md` in Chinese.

## Contents

1. [CURRENT.md](#currentmd)
2. [STATE.md](#statemd)
3. [FINDINGS.md](#findingsmd)
4. [REPORT.md](#reportmd)
5. [Status Transition Rules](#status-transition-rules)

## CURRENT.md

```markdown
# Active Change Review

Review directory: `.agent-work/change-review/{YYYYMMDD-HHMM}/`
State: `.agent-work/change-review/{YYYYMMDD-HHMM}/STATE.md`
Findings: `.agent-work/change-review/{YYYYMMDD-HHMM}/FINDINGS.md`
Report: `.agent-work/change-review/{YYYYMMDD-HHMM}/REPORT.md`

Baseline:
- Repository:
- Base:
- Head:
- Diff command:
- Patch fingerprint:

Current phase: INITIALIZE | FULL_DISCOVERY | DECISION_GATE | REPAIR_WAVE | DELTA_VERIFY | FINAL_FRESH_VERIFY | BLOCKED
Current repair wave:
Open Must Fix IDs:
Open Needs Decision IDs:
External blockers:
Next action:
```

Delete `CURRENT.md` only after the final report is complete.

## STATE.md

```markdown
# Review State

## 1. Baseline

- Repository:
- Review target: PR | commit range | staged diff | unstaged diff
- Base branch/commit:
- Head branch/commit:
- Diff commands:
- Patch fingerprint:
- Worktree status inspected at:
- Review depth: Small | Medium | Large
- Repair authorized: Yes | No
- Soft repair-wave cap: 3
- Hard repair-wave cap: 5

## 2. Intent and Authority

- One-sentence intent:
- Explicit non-goals:
- Authoritative requirements:
- Accepted human decisions:
- Unverified author/PR claims:

## 3. Invariants

| ID | Invariant | Source | Risk if violated | Verification method |
| --- | --- | --- | --- | --- |
| INV-001 |  |  |  |  |

## 4. Change Map

### Entry points and workflows
- 

### Public contracts, schemas, and migrations
- 

### State, persistence, queues, and side effects
- 

### Auth, permissions, tenants, and trust boundaries
- 

### Config, CI, deployment, rollback, and observability
- 

### Tests and documentation
- 

## 5. Coverage Matrix

| Lens | Trigger | Scope reviewed | Status | Evidence | Gap / invalidation trigger |
| --- | --- | --- | --- | --- | --- |
| Intent/domain | Always |  | Reviewed |  |  |
| Correctness | Always |  | Reviewed |  |  |
| Data/persistence |  |  | Skipped |  |  |
| State/concurrency |  |  | Skipped |  |  |
| Security/privacy |  |  | Reviewed |  |  |
| Reliability/release |  |  | Partial |  |  |
| Performance/cost |  |  | Skipped |  |  |
| Architecture/debt | Always |  | Reviewed |  |  |
| Dependencies/supply chain |  |  | Skipped |  |  |
| Tests/CI | Always |  | Reviewed |  |  |
| UI/accessibility |  |  | Skipped |  |  |
| AI-agent/harness |  |  | Reviewed |  |  |

Allowed status: `Reviewed`, `Partial`, `Skipped`, `Needs Follow-up`, `Invalidated`.

## 6. Critical-Path Traces

### PATH-001: <name>

```text
Input/stimulus:
Environment/state:
Entry point:
Transformations:
Persistence/side effects:
Output:
Required invariants:
Failure paths inspected:
Evidence:
Gaps:
```

## 7. Round Log

| Round | Mode | Baseline / repair range | Scope and impact cone | New root causes | Closed | Reopened | Checks | Progress | Reset reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | FULL |  |  |  |  |  |  |  |  |

Progress must be one or more of: finding closed, candidate falsified, new root cause proven, coverage gap closed, durable guardrail added.

## 8. Verification

### Commands run

| Command | Result | Head/fingerprint | Notes |
| --- | --- | --- | --- |

### Checks not run

| Check | Reason | Residual risk | Required owner/action |
| --- | --- | --- | --- |

### Manual/runtime evidence
- 

## 9. Reset Events

| Event | Previous baseline | New baseline | Trigger | Findings/coverage invalidated |
| --- | --- | --- | --- | --- |

## 10. Convergence

- Repair waves used:
- Repeated failure classes:
- Non-convergence diagnosis:
- Final fresh verifier identity/framing:
- Final fresh verification result:
- Stop conditions satisfied: Yes | No
- Merge decision: mergeable | not mergeable | insufficient evidence
```

## FINDINGS.md

Start with compact indexes, then keep one stable section per root-cause finding.

```markdown
# Review Findings

## Open Findings

| ID | Severity | Decision class | Status | Root cause | Scope | Owner / decision needed |
| --- | --- | --- | --- | --- | --- | --- |

## Closed Findings

| ID | Severity | Closed in | Verification | Reopen trigger |
| --- | --- | --- | --- | --- |

## Candidate Disposition

| Candidate | Lens | Disposition | Evidence / reason |
| --- | --- | --- | --- |
| CAND-001 | Security | Disproved |  |

---

## REV-001 — <concise root-cause title>

- Severity: Must Fix | Should Fix | Should Plan | Track as Debt
- Decision class: Needs Decision | Agent-Fixable | External Blocker
- Status: Candidate | Open | Accepted | Repairing | Verification Failed | Closed | Risk Accepted | Deferred
- Confidence: High | Medium | Low
- First detected in round:
- Last updated in round:

### Invariant

- Violated invariant:
- Authority/source:

### Trigger and proof path

1. 
2. 
3. 

### Impact

- User/business impact:
- Security/privacy/data/operations impact:
- Blast radius:
- Reversibility:

### Scope and occurrences

| Path / symbol / route | Lines or hunk | Why affected |
| --- | --- | --- |

### Evidence

- Code evidence:
- Test/runtime evidence:
- Configuration/documentation evidence:
- Contradicting evidence considered:
- Remaining uncertainty:

### Smallest credible fix direction

- 

### Frozen acceptance criteria

- [ ] Original trigger is no longer reachable or is handled correctly.
- [ ] Root cause is fixed across listed sibling paths.
- [ ] Required invariant is enforced at the correct boundary.
- [ ] Regression oracle fails before and passes after when feasible.
- [ ] No required validation, permission, or release control is weakened.

### Human decision

- Question:
- Options and consequences:
- Decision:
- Decision authority/date:

### Repair record

- Authorized IDs/wave:
- Previous head:
- Current head:
- Files/symbols changed:
- Repair explanation:
- Unrelated changes: None | <list>
- Contract or scope expansion: No | <details>

### Verification record

- Repair delta reviewed:
- Impact cone reviewed:
- Commands/results:
- Manual/runtime evidence:
- Acceptance criteria result:
- Closure rationale:
- Reopen trigger:

### History

| Round | Transition | Evidence / reason |
| --- | --- | --- |
| 0 | Candidate -> Open |  |
```

### Finding rules

- Never renumber an ID.
- Never delete a finding to make the open list clean.
- Add occurrences to the root cause rather than duplicating findings.
- Close only with current-head evidence.
- Mark `Risk Accepted` only with accountable human authority and bounded residual risk.
- Mark `Deferred` only with owner, ceiling, and revisit trigger.
- Reopen under the same ID when the same root cause remains or recurs.
- Create a new ID when the root cause is materially different.

## REPORT.md

```markdown
# 代码审查报告

## 合并结论

`mergeable` | `not mergeable` | `insufficient evidence`

一句话说明当前结论及最高风险。

## 需要用户敲定的业务语义

### REV-xxx — <标题>

- 需要决定：
- 选项与后果：
- 仓库证据支持的建议：
- 阻塞范围：

没有此类事项时写“无”。

## 主要发现

按 `Must Fix`、`Should Fix`、`Should Plan`、`Track as Debt` 排序。

### REV-xxx — <标题>

- 严重性：
- 状态：
- 触发条件：
- 影响：
- 证据：
- 最小修复方向：
- 验证情况：
- 置信度：

## 本次已修复

| Finding ID | 根因 | 修复范围 | 验证证据 | 剩余风险 |
| --- | --- | --- | --- | --- |

仅列出当前代码和验证证据支持已关闭的 finding。

## 审查覆盖

- 审查范围与基线：
- 变更意图与关键不变量：
- 已检查风险镜头：
- 已追踪关键流程：
- repair delta 与影响锥：
- reset 事件：
- final fresh verification：

## 验证

### 已运行

| 命令/流程 | 结果 | 限制 |
| --- | --- | --- |

### 未运行

| 检查 | 原因 | 剩余风险 |
| --- | --- | --- |

## 假设、证据缺口与人工复核

- 

## 收敛情况

- 完整发现轮次：
- 修复波次：
- 新增根因数：
- 重开 finding：
- 重复失效类别及建议的持久护栏：
- 停止条件是否满足：
```

## Status Transition Rules

Allowed finding transitions:

```text
Candidate -> Open
Open -> Accepted
Open -> Risk Accepted
Open -> Deferred
Accepted -> Repairing
Repairing -> Closed
Repairing -> Verification Failed
Verification Failed -> Repairing
Closed -> Open                 when reopen evidence appears
```

Do not transition:

- `Open -> Closed` without a repair or proof that the candidate was false. A false candidate belongs in `Candidate Disposition`, not as a closed defect.
- `Repairing -> Closed` from the repair agent’s summary alone.
- `Needs Decision -> Agent-Fixable` without recording the authoritative decision or repository evidence.
- `Deferred -> Closed` merely because the review ended.

Coverage transitions:

```text
Unknown -> Reviewed | Partial | Skipped | Needs Follow-up
Reviewed -> Invalidated        when its evidence or assumptions change
Invalidated -> Reviewed        after targeted re-verification
```
