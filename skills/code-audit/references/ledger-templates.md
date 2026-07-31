# Code Audit Ledger Templates

Use these templates to preserve audit knowledge across cycles. Keep persistent agent-facing artifacts in English. Write each run’s `REPORT.md` in Chinese.

## Contents

1. [CURRENT.md](#currentmd)
2. [SYSTEM-MAP.md](#system-mapmd)
3. [COVERAGE.md](#coveragemd)
4. [FINDINGS.md](#findingsmd)
5. [Run SCOPE.md](#run-scopemd)
6. [Run EVIDENCE.md](#run-evidencemd)
7. [Run REPORT.md](#run-reportmd)
8. [State and Transition Rules](#state-and-transition-rules)

## CURRENT.md

```markdown
# Active Audit Run

Run directory: `.agent-work/audit/runs/{YYYYMMDD-HHMM}/`
Profile: `docs/audit-profile.md` | `AUDIT_PROFILE.md` | `.agent-work/audit/PROFILE.md`
System map: `.agent-work/audit/SYSTEM-MAP.md`
Coverage: `.agent-work/audit/COVERAGE.md`
Findings: `.agent-work/audit/FINDINGS.md`
Scope: `.agent-work/audit/runs/{YYYYMMDD-HHMM}/SCOPE.md`
Evidence: `.agent-work/audit/runs/{YYYYMMDD-HHMM}/EVIDENCE.md`
Report: `.agent-work/audit/runs/{YYYYMMDD-HHMM}/REPORT.md`

Mode: Baseline | Periodic | Targeted Re-audit | Reset Baseline
Repository head:
Last audited head:
Current phase: RECONCILE | MAP | SCOPE | DISCOVERY | DECISION | REMEDIATION | RE-AUDIT | REPORT | BLOCKED
Authorized remediation: Yes | No
Open Must Fix IDs:
Open Needs Decision IDs:
External blockers:
Current remediation wave:
Next action:
```

Delete only after the run report and persistent-ledger updates are complete.

## SYSTEM-MAP.md

```markdown
# Audit System Map

Last reconciled:
Repository head:
Profile status:
Map owner:

## 1. System Boundary

- Included workload/products:
- Excluded adjacent systems and rationale:
- Primary users:
- Operators/maintainers:
- Business/mission goals:
- Critical workflows:
- Crown-jewel data/assets/secrets:
- Privileged/irreversible actions:
- External systems/processors:
- Deployment environments:
- Legal/privacy/contractual constraints:

## 2. Component Inventory

| Component / domain | Purpose | Owner | Criticality | Entry points | Data/state | Dependencies | Runtime/deployment | Evidence/source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 3. Interfaces and Contracts

| ID | Producer/provider | Consumer | Contract/API/event/schema | Version/compatibility | Auth/trust boundary | Owner | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 4. Data and State Map

| Store/state/event | Classification | Readers | Writers | Source of truth | Retention/deletion | Backup/restore | Isolation boundary | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 5. Trust and Privilege Map

| Boundary/action | Actor/identity | Input/source | Required authorization | Secrets/data exposed | Effective permissions | Approval gate | Audit evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 6. Deployment and Operations Map

| Service/job/component | Environment | Build artifact | Deploy path | Config/flags | Dependencies | SLO/critical signal | Rollback/recovery | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 7. Agent and Tooling Map

| Agent/harness/tool | Model/version | Purpose | Identity/tokens | Filesystem/network/tools | Untrusted inputs | Durable state/memory | Approval boundary | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 8. Scenario Portfolio

| Scenario ID | Attribute | Workflow/assets | Components/contracts | Expected response | Evidence target | Criticality | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 9. Dependency and Invalidation Edges

| From node | To coverage/scenario | Why dependent | Change types that invalidate | Boundary/stop condition |
| --- | --- | --- | --- | --- |

## 10. Known Map Gaps

| Gap | Risk | Required evidence/owner | Status |
| --- | --- | --- | --- |
```

## COVERAGE.md

```markdown
# Audit Coverage Ledger

Last updated:
Repository head:

## Status Definitions

- `Fresh`: required scope and evidence reviewed against the recorded state.
- `Stale`: confidence decayed but no direct contradiction exists.
- `Invalidated`: a change/event directly breaks the prior proof assumptions.
- `Unknown`: no trustworthy evidence exists.

## Area Coverage

| Coverage ID | Area/control | Criticality | Required depth/cadence | Last reviewed commit/date/environment | Scope reviewed | Evidence refs | Gaps | Dependencies | Invalidation triggers | Status | Next rotation reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Scenario Coverage

| Scenario ID | Scenario | Required response/measure | Last exercised | Evidence/result | Gaps | Dependencies | Invalidation triggers | Status | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Control Baseline Coverage

| Control ID | Control/outcome | Source/profile requirement | Implementation scope | Verification evidence | Exceptions | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Coverage Change Log

| Date/run | Coverage ID | Previous status | New status | Reason/change | Evidence |
| --- | --- | --- | --- | --- | --- |

## Due Rotation Queue

| Priority | Coverage/scenario | Reason due | Criticality | Evidence needed | Suggested next run |
| --- | --- | --- | --- | --- | --- |
```

### Coverage rules

- Never mark an entire subsystem `Fresh` from one scanner result.
- Record the exact reviewed boundary and evidence.
- Use `Invalidated`, not `Stale`, when a proof assumption directly changed.
- Preserve prior evidence references when status changes.
- Do not collapse coverage into a single percentage.
- An area can be `Fresh` for one scenario and `Unknown` for another; use separate rows when necessary.

## FINDINGS.md

```markdown
# Persistent Audit Findings and Debt

Last updated:
Repository head:

## Open Findings

| ID | Severity | Decision class | Status | Root cause | Affected scenarios/areas | Owner/decision | Due/revisit trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Closed Findings

| ID | Closed in run/head | Closure evidence | Residual risk | Reopen trigger |
| --- | --- | --- | --- | --- |

## Accepted Debt and Risk

| ID | Owner | Why acceptable now | Safety ceiling | Mitigations/monitoring | Revisit trigger/date | Expected resolution |
| --- | --- | --- | --- | --- | --- | --- |

## Golden-Principle Candidates

| GP ID | Recurring issue/invariant | Evidence occurrences | Proposed enforcement | False-positive/maintenance risk | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Candidate Disposition

| Candidate | Run/area | Disposition | Evidence/reason |
| --- | --- | --- | --- |

---

## AUD-001 — <concise root-cause title>

- Severity: Must Fix | Should Plan | Track as Debt
- Decision class: Needs Decision | Agent-Fixable | External Blocker
- Status: Candidate | Open | Accepted | Remediating | Verification Failed | Closed | Risk Accepted | Deferred
- Confidence: High | Medium | Low
- First detected run:
- Last updated run:
- Owner:

### Quality attributes and profile requirements

- Affected attributes:
- Profile/control requirement:
- Violated invariant/outcome:

### Failure, abuse, or structural path

```text
Stimulus/trigger:
Environment/preconditions:
Path/components:
Expected response:
Observed or supported failure:
```

### Impact and risk basis

- User/business/mission impact:
- Security/privacy/data/reliability impact:
- Likelihood/exploitability:
- Blast radius:
- Reversibility/recovery:
- Systemic reach:

### Scope and occurrences

| Component/path/symbol/workflow | Evidence | Why affected |
| --- | --- | --- |

### Evidence

- Code/configuration evidence:
- Test/scanner evidence:
- Runtime/operations/incident evidence:
- Architecture/history evidence:
- Contradicting evidence considered:
- Gaps/assumptions:

### Recommended direction

- Smallest credible remediation/control:
- Rollout/migration/rollback implications:
- Suggested priority:

### Frozen acceptance criteria

- [ ] Root cause is removed or bounded at the correct control boundary.
- [ ] Original scenario now satisfies the required response.
- [ ] Sibling/parallel paths are covered.
- [ ] Verification uses a meaningful oracle.
- [ ] Release, rollback, recovery, permission, and observability implications are addressed.
- [ ] Persistent coverage is updated.

### Human decision or risk acceptance

- Decision required:
- Options/consequences:
- Decision:
- Authority/date:
- Residual-risk owner:

### Remediation history

| Wave/head | Changes | Verification | Result | Coverage invalidated |
| --- | --- | --- | --- | --- |

### Closure/reopen

- Closure evidence:
- Residual risk:
- Reopen trigger:
```

### Finding rules

- Keep stable IDs across audit cycles.
- Deduplicate by root cause; list occurrences.
- Never delete open history to make a run appear clean.
- Close only against the current head/environment with evidence.
- Record accountable human authority for `Risk Accepted`.
- Require owner, ceiling, and trigger for `Deferred`/debt.
- Reopen the same ID for the same root cause.

## Run SCOPE.md

```markdown
# Audit Run Scope

Run:
Mode: Baseline | Periodic | Targeted Re-audit | Reset Baseline
Repository range/head:
Profile and status:
Resource/budget constraints:
Authorized remediation: Yes | No

## 1. Scope Selection Summary

| Scope item | Reason | Criticality | Quality attributes | Scenarios | Expected evidence | Planned depth |
| --- | --- | --- | --- | --- | --- | --- |

Reason must be one or more: `always-on critical`, `changed/high-churn`, `invalidated`, `rotating`, `incident`, `finding/debt follow-up`, `profile gap`, `reset`.

## 2. Changed and Invalidated Surface

| Change/component | Semantic class | Dependent coverage/scenarios | Invalidation result | Rationale |
| --- | --- | --- | --- | --- |

## 3. Always-On Critical Scenarios

| Scenario | Why required now | Evidence target |
| --- | --- | --- |

## 4. Rotating Deep Slices

| Area | Last reviewed | Why selected | Planned boundary |
| --- | --- | --- | --- |

## 5. Incident, Finding, and Debt Follow-up

| Item | Trigger/evidence | Planned verification |
| --- | --- | --- |

## 6. Exclusions

| Area | Reason excluded | Residual risk | Next review trigger |
| --- | --- | --- | --- |

## 7. Material Assumptions and Decisions Needed

- 

## 8. Stop Criteria for This Run

- [ ] Every scoped item has evidence and outcome.
- [ ] Required scenarios are exercised or explicitly blocked.
- [ ] Persistent ledgers are updated.
- [ ] Report states gaps and next priorities.
```

## Run EVIDENCE.md

Append one section immediately after each reviewed area or scenario.

```markdown
# Audit Run Evidence

Run:
Repository head/environment:

## Evidence Index

| Unit | Status | Severity | Coverage IDs | Finding IDs | Evidence summary | Gaps |
| --- | --- | --- | --- | --- | --- | --- |

---

## UNIT-001 — <area or scenario>

- Scope reason:
- Status: Reviewed | Partial | Skipped | Needs Follow-up
- Outcome: Must Fix | Should Plan | Track as Debt | No Action | Evidence Gap
- Coverage IDs:
- Finding IDs:

### Scope and boundaries

- Components/files/interfaces/workflows:
- Quality attributes:
- Scenarios/controls:
- Excluded sub-scope:

### Hypotheses and disposition

| Candidate | Evidence sought | Disposition | Evidence/reason |
| --- | --- | --- | --- |

### Evidence inspected

- Code/configuration:
- Tests/scanners:
- Runtime/logs/metrics/traces:
- Build/release/provenance:
- Docs/profile/ADR/history:
- Human/operator evidence:

### Commands and results

| Command/check | Result | Environment/head | Limitation |
| --- | --- | --- | --- |

### Scenario result

```text
Stimulus:
Environment:
Expected response/measure:
Observed/supported response:
Result: Satisfied | Partially Satisfied | Not Satisfied | Unknown
```

### Findings or No Action rationale

- 

### Gaps and assumptions

- 

### Coverage update

- Previous status:
- New status:
- Evidence refs:
- Dependencies/invalidation triggers:
- Next rotation reason:
```

## Run REPORT.md

```markdown
# 代码审计报告

## 执行摘要

- 审计模式：`Baseline` | `Periodic` | `Targeted Re-audit` | `Reset Baseline`
- 仓库范围与当前 head：
- Audit Profile 状态：`Approved` | `Draft`
- 系统整体健康状况：
- 最稳固区域：
- 最高风险区域：
- 本轮未覆盖的重要风险：

## 需要用户敲定的业务/风险语义

### AUD-xxx — <标题>

- 需要决定：
- 选项与后果：
- 建议及证据：
- 阻塞的审计/修复范围：

没有时写“无”。

## 主要发现

按 `必须修复`、`需要规划`、`记录为技术债` 排序。

### AUD-xxx — <标题>

- 分类：必须修复 | 需要规划 | 记录为技术债
- 状态：
- 影响的质量属性/关键流程：
- 触发路径：
- 影响与风险排序依据：
- 证据：
- 建议方向：
- 修复与验证状态：
- 证据缺口/置信度：

## 本轮已修复

| Finding ID | 根因 | 修复范围 | 验证证据 | 覆盖状态更新 | 剩余风险 |
| --- | --- | --- | --- | --- | --- |

## 审计范围与抽样依据

- Always-on critical：
- Changed/high-churn：
- Invalidated dependency cones：
- Rotating deep slices：
- Incident/finding/debt follow-up：
- 排除范围及原因：

## 场景与质量属性验证

| 场景 | 属性 | 预期响应 | 证据/结果 | 缺口 |
| --- | --- | --- | --- | --- |

## 仓库、运行和发布证据

### 已检查

- 仓库状态和差异：
- 数据/迁移/恢复：
- 权限和信任边界：
- 发布/回滚/配置：
- 可观测性和事故恢复：
- 依赖/构建/供应链：
- Agent/harness/tooling：

### 已运行检查

| 命令/流程 | 结果 | 限制 |
| --- | --- | --- |

### 未运行或不可获得

| 证据 | 原因 | 剩余风险 | 所需负责人/动作 |
| --- | --- | --- | --- |

## 覆盖新鲜度更新

| Coverage/Scenario | 旧状态 | 新状态 | 证据 | 下次触发/轮换原因 |
| --- | --- | --- | --- | --- |

## 技术债和持久护栏

- 到期/触发的技术债：
- 新的 golden principle candidate：
- 建议新增的 lint/test/generator/CI/doc control：
- 可安全删除/收缩的复杂度：

## 假设、人工复核与下一轮重点

- 假设：
- 需要人工复核：
- 下一轮优先范围：
- Full-baseline reset 是否触发：

## 风险排序依据

说明业务/用户影响、安全/数据/资金/可用性风险、发生概率、爆炸半径、可逆性、证据强度、系统性程度和修复成本。不要只按代码行数、文件大小或扫描器 severity 排序。
```

## State and Transition Rules

Coverage transitions:

```text
Unknown -> Fresh | Stale | Invalidated
Fresh -> Stale                  through age/churn/evidence decay
Fresh -> Invalidated            through direct assumption break
Stale -> Fresh                  after required re-evidence
Stale -> Invalidated            after direct contradiction/change
Invalidated -> Fresh            after targeted re-audit
```

Finding transitions:

```text
Candidate -> Open
Open -> Accepted
Open -> Risk Accepted
Open -> Deferred
Accepted -> Remediating
Remediating -> Closed
Remediating -> Verification Failed
Verification Failed -> Remediating
Closed -> Open                  on reopen evidence
```

Golden-principle transitions:

```text
Candidate -> Approved for Design
Approved for Design -> Implementing
Implementing -> Enforced
Enforced -> Recalibration Needed
Recalibration Needed -> Enforced | Retired
```

Do not:

- Mark coverage `Fresh` because a report was generated.
- Close findings from agent summaries alone.
- Treat run completion as system risk elimination.
- Accept debt without owner/ceiling/trigger.
- Promote a rule from one low-impact stylistic occurrence.
- Delete historical evidence during a reset.
