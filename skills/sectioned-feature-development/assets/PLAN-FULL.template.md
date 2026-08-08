# 完整实施计划：<Feature Name>

- 创建时间：<YYYY-MM-DD HH:MM TZ>
- 工作模式：`PLAN_ONLY | EXECUTE_NO_COMMIT | EXECUTE_WITH_COMMITS`
- 仓库：`<path>`
- Feature branch/worktree：`<branch or N/A>`
- Feature base：`<commit>`
- 计划版本：`v1`
- 当前状态：`PLANNING`

<!-- FEATURE-CONTEXT:START -->
## Feature Contract

### 一句话目标

<明确说明完成后系统新增或改变的结果。>

### 用户/操作者可观察行为

- <行为 1>
- <行为 2>

### 非目标

- <明确不做什么>

### 全局不变量

- `INV-01`：<每个 section 和最终结果都必须保持的事实>
- `INV-02`：<安全、数据、状态或兼容性不变量>

### 硬约束与权威来源

| ID | 约束 | 权威来源 |
|---|---|---|
| C-01 | <约束> | `<repo path / issue / decision>` |

### 完整功能验收标准

- `R-01`：<行为级标准>
- `R-02`：<行为级标准>

### 完整功能验证命令

```bash
<command>
```

### Ownership / State Boundary

| Boundary | Authoritative owner | Consumers | Risk |
|---|---|---|---|
| <state or decision> | `<module>` | `<modules>` | `<risk>` |

### Compatibility / Migration / Rollout / Rollback

- 兼容策略：<...>
- 迁移策略：<...>
- 发布/开关：<...>
- 回滚/恢复：<...>
- 可观测性：<...>
- 临时机制清理条件：<...>
<!-- FEATURE-CONTEXT:END -->

## Requirement Coverage Matrix

| Requirement | Primary section(s) | Section oracle | Integration oracle | Status |
|---|---|---|---|---|
| R-01 | S01 | <test/check> | CP1 / FINAL | planned |
| R-02 | S02 | <test/check> | FINAL | planned |

## Section Index and Dependency Graph

| ID | Parent | Replan gen | Title | Type | Depends on | Integrates with | Risk | Status |
|---|---|---:|---|---|---|---|---|---|
| S01 | — | 0 | <title> | vertical | — | CP1 | medium | planned |
| S02 | — | 0 | <title> | enabling/expand/migrate/contract | S01 | CP1 | high | planned |

```text
S01 -> S02 -> CP1 -> FINAL
```

## Integration Checkpoints

### CP1 — <name>

- Included sections: `S01`, `S02`
- Contracts proved: <...>
- Critical paths: <...>
- Commands/evidence: <...>
- Rollback/disable path: <...>

## Plan Gate

- [ ] Every requirement maps to section and integration evidence.
- [ ] Dependency graph is acyclic.
- [ ] Every high-risk boundary has an owner and oracle.
- [ ] Every section is independently implementable, testable, and reviewable.
- [ ] Cross-section contracts and checkpoints are explicit.
- [ ] Refactor and behavior are separated or inseparability is justified.
- [ ] Parallel sections do not share a semantic owner.
- [ ] Rollout, rollback, migration, observability, and cleanup are covered.
- [ ] No final “integrate everything” dump remains.

## Sections

<!-- SECTION:S01:START -->
## S01 — <Section Title>

### 目标

<本 section 唯一主要目标。>

### 行为增量

- <完成后可观察、可验证的行为>

### 依赖

- Requires: `none`
- Integrates with: `CPx | none`
- Expected predecessor head: `<filled when contract freezes>`

### 预计范围

- Lineage: `original`
- Replan generation: `0`
- Files/symbols/workflows: `<expected scope>`
- Semantic boundaries: `<persistence/security/API/etc.>`
- Estimated behavioral size: `<range>`
- Risk: `low | medium | high`
- Split trigger: <when to stop and split again>

### 非目标

- <本 section 明确不处理的内容>

### 全局不变量

- `INV-01`
- <section-specific invariant>

### 验收标准

- `S01-AC-01`：<具体、可证伪的标准>
- `S01-AC-02`：<边界/失败标准>

### 验证命令

```bash
<targeted test/lint/typecheck/runtime command>
```

保留证据：<log, screenshot, response, migration result, etc.>

### 发布与恢复

- Intermediate state validity: <...>
- Compatibility/migration: <...>
- Flag/rollout: <...>
- Rollback/recovery: <...>
- Observability: <...>

### 延后项

- <none or assign to a named existing section>
<!-- SECTION:S01:END -->

<!-- SECTION:S02:START -->
## S02 — <Section Title>

### 目标

<...>

### 行为增量

- <...>

### 依赖

- Requires: `S01`
- Integrates with: `CP1`
- Expected predecessor head: `<filled when contract freezes>`

### 预计范围

- Lineage: `original`
- Replan generation: `0`
- Files/symbols/workflows: `<...>`
- Semantic boundaries: `<...>`
- Estimated behavioral size: `<...>`
- Risk: `high`
- Split trigger: <...>

### 非目标

- <...>

### 全局不变量

- `INV-01`

### 验收标准

- `S02-AC-01`：<...>

### 验证命令

```bash
<command>
```

### 发布与恢复

- Intermediate state validity: <...>
- Compatibility/migration: <...>
- Flag/rollout: <...>
- Rollback/recovery: <...>
- Observability: <...>

### 延后项

- <none or assigned section>
<!-- SECTION:S02:END -->

## Decision Ledger

| ID | Question | Decision/authority | Affected sections | Status |
|---|---|---|---|---|
| D-01 | <question> | <decision or pending> | S02 | open |

## Deferred Work Ledger

| ID | Item | Required for feature contract? | Owner section/follow-up | Status |
|---|---|---|---|---|
| DW-01 | <item> | yes/no | S02 / follow-up issue | planned |

## Replan History

| Version | Date | Trigger | Sections/evidence invalidated | Decision |
|---|---|---|---|---|
| v1 | <date> | initial | — | — |
