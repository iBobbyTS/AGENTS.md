# 大功能分段开发与审查 Skill：研究过程、结论与参考资料

- 研究日期：2026-08-06
- AI Agent 资料时间下限：2025-08-06（不采用早于该日期的 Agent 工作流资料）
- 输入材料：`Codex Custom Instructions.md`、`code-review.zip`、`skill-creator.zip`
- 产出：`sectioned-feature-development` skill、section-aware `code-review` 修订版、可直接替换的 Custom Instructions 片段

## 1. 结论摘要

你的核心判断是正确的：**当一次变更足够大时，不应先完成整个功能再对整个 diff 反复 review；应先把完整目标固定为 feature contract，再按可验证的 section 逐段实现、逐段审查，并在最后单独做跨 section integration review。**

但“拆分”本身还不够。要真正解决“每轮 review 都能发现新问题，十几轮无法收尾”，流程必须同时满足以下条件：

1. **Section 按行为与不变量切分，而不是机械按目录、前后端或文件类型切分。** 默认采用可独立验证的纵向 slice；只有为后续行为建立必要 seam 时，才允许单独的 enabling refactor。
2. **每个 section 有冻结的 contract、base、acceptance criteria 和验证命令。** 否则 reviewer 每轮都可能重新定义“正确”。
3. **稳定 baseline 只做一次完整发现。** 修复后只 review repair delta 与被其失效的 impact cone；只有 contract、架构或高风险语义发生实质变化时才 reset 为新一轮完整审查。
4. **Section acceptance 与 feature merge readiness 分离。** Section 通过只说明该段局部成立；完整功能必须再经过跨 section 的 integration gate。
5. **用覆盖闭合代替“连续两轮没发现问题”。** 两次空审不是可靠统计证据，因为 reviewer 的搜索范围、上下文、基线和缺陷暴露并不独立；它还会把低信号意见不断引入循环。
6. **将状态外置到仓库文件。** `PLAN-FULL.md`、当前 `PLAN.md`、`FEATURE-STATE.md`、section contract、handoff 和 review ledger 是跨上下文的系统记录，聊天不是。
7. **设置 repair budget 和失败诊断。** 正常最多 3 个 repair wave，硬上限 5；达到上限时必须判断是 specification gap、weak oracle、architecture conflict、scope explosion、unstable base、environment gap，还是 reviewer noise，而不是继续泛化 review。

因此，现有 `code-review` skill **不需要重写**。它已经具备最重要的收敛机制：一次 full discovery、repair delta 复核、reset trigger、稳定 finding ID、决策分类、软/硬轮次上限，以及明确禁止“两轮全量空审”。需要的是增加 `SECTION`、`DELTA`、`INTEGRATION` 三种模式及其输入包、结论语义和 integration focus。

## 2. 对当前 Custom Instructions 的审查

### 2.1 已经做对的部分

新加入的规则包含几个高价值方向：

- 大变更使用独立 branch。
- 先生成完整计划，再逐 section 提取当前计划。
- 实现、review、repair 使用不同 profile/上下文。
- 每段完成后 commit，形成可恢复的检查点。
- review 结果持久化到 `.agent-work/reviews`。
- 完整计划最终归档。

这些做法与近一年厂商实践中反复出现的“durable project memory”“one feature at a time”“planner / generator / evaluator”“milestone verification”基本一致。

### 2.2 需要修改的部分

#### 问题 A：`300 lines` 被写成唯一近似门槛

风险并不与行数单调对应。一个 40 行的授权绕过、schema default 或并发状态转换，可能比 500 行的机械生成代码更需要完整流程。

建议把触发条件改为：

- 预计超过约 300 行**行为性修改**；或
- 超过 3 个模块、package、service、page 或 workflow；或
- 跨越 persistence、schema、security、permissions、tenancy、routing、money、time、units、concurrency、background job、public API、shared state、deployment 等高风险边界；或
- architecture 或 state ownership 发生变化；或
- impact cone 难以界定；或
- 之前 whole-change implementation/review 不收敛。

#### 问题 B：计划或 review 请求会意外获得 branch/commit 权限

你的全局规则写着“除非明确要求，否则不得 commit”，原新增段落却在触发阈值后无条件要求 branch 和 commit。这会让“帮我写计划”或“帮我判断方案”也可能被解释成执行授权。

最终设计保留通用 no-commit 规则，但在 Custom Instructions 中增加只针对 `$sectioned-feature-development` **implementation task** 的 scoped exception。这样权限来自上层指令的显式委托，而不是 skill 自己宣称可以覆盖上层规则。Skill 中仍区分：

- `PLAN_ONLY`
- `EXECUTE_NO_COMMIT`
- `EXECUTE_WITH_COMMITS`

只有用户直接授权，或 governing Custom Instructions 明确把 bounded branch/implementation/repair commit 权限委托给本 skill 时，才进入第三种模式。

#### 问题 C：每轮都用 clean reviewer 做完整 `$code-review`

“clean context”本身有价值，但**clean context 不等于重新扫描整个稳定 section**。如果每次修复后都让新 reviewer 从零审完整范围，reviewer 会以不同顺序采样大型搜索空间，产生更多新意见，也会重复已经有充分证据的区域。

正确结构是：

- 首轮：clean `SECTION` full discovery。
- 修复：冻结 finding IDs 和 acceptance criteria。
- 复核：独立 reviewer 只检查 repair delta + invalidated impact cone。
- reset：仅当公共 contract、schema、权限、状态所有权、并发、破坏性行为、部署语义、架构方向或范围发生实质变化时，才重新 full review。

#### 问题 D：连续两轮空审作为停止条件

现有 `code-review` skill 已经明确写出“不要求连续两轮空的 whole-change review”，这与新规则直接冲突。

这个停止条件有四个问题：

1. 两轮 review 并不独立；模型、提示、工具、代码路径和测试环境高度相关。
2. “没有发现”无法证明 reviewer 覆盖了什么，除非 coverage ledger 已闭合。
3. 修复改变 baseline 后，第二轮可能在检查不同对象。
4. 自动 review 的低信号意见会随着重复轮次累积，造成无止境 polish 或架构摇摆。

更可靠的停止条件是：

- 冻结 scope 的必需 lens 已 reviewed 或明确标记 evidence gap；
- 没有未解决 `Must Fix` 或未被接受的 `Should Fix`；
- 所有修复 finding 都有当前代码和独立验证证据；
- 必需测试通过或 blocker/residual risk 明确；
- verdict 与模式匹配。

没有修复时，一次覆盖完整的 section review 即可；有修复时，一次成功的 `DELTA` 验证即可，除非 reset trigger 触发。

#### 问题 E：只逐 section review，没有完整功能 integration gate

局部 section 可以全部正确，但组合后仍可能失败：

- producer/consumer 对 error semantics 理解不同；
- schema 与部署顺序不兼容；
- 两段分别正确的权限检查在组合路径上丢失 tenant context；
- 并行 agent 各自定义了不同的 shared state owner；
- feature flag 的 on/off 路径、migration 与 rollback 没有共同验证；
- deferred work 在 section 层面都“合理”，最终却没有人完成。

因此最后必须有一次 `INTEGRATION` review。它使用 feature base 到 final head 的完整范围定位，但重点不是逐行重审，而是原始需求、跨 section contract、端到端流程、迁移/发布/回滚、可观测性、性能、安全和 deferred-work closure。

#### 问题 F：`PLAN.md` 只含当前 section 可能丢失全局约束

当前 section 的实现 agent 不应读取整个历史噪声，但至少必须同时获得：

- feature 一句话目标；
- 非目标；
- global invariants；
- 与当前 section 相关的完整功能 acceptance criteria；
- 当前 section contract。

因此提供的提取脚本会从 `PLAN-FULL.md` 同时提取稳定 `FEATURE-CONTEXT` 和一个 section，而不是只复制 section body。

### 2.3 对原规则的建议替代结构

完整替代片段已单独放在 `CUSTOM_INSTRUCTIONS_REPLACEMENT.md`。核心变化是：让 Custom Instructions 只负责**触发、路由和 scoped 权限委托**，把易变、复杂的具体 state machine 放入 skill，避免全局指令持续膨胀。

触发条件应有意同时存在于 Custom Instructions 和 `$sectioned-feature-development` 的 YAML `description`：前者是全局硬路由，后者是 skill 自身的匹配/召回入口。两处保持同一判定语义；真正的流程细节只在 skill 中维护，因此不会形成两套 workflow。

## 3. 对现有 `code-review` skill 的判断

### 3.1 应保留的能力

现有 skill 的以下设计是本流程的基础，不应删除：

- 审查一个 bounded change set，而不是周期性扫描整个仓库。
- 将 agent 生成的代码、总结和测试声明视为待验证 claim。
- 区分 `Needs Decision`、`Agent-Fixable`、`External Blocker`。
- 使用稳定 finding ID，冻结 finding 语义和 acceptance criteria。
- 先完成一次 broad discovery，再进入 repair。
- 修复后只复核 repair delta 和 impact cone。
- 明确的 full-reset triggers。
- final fresh verification 的独立性原则。
- 正常 3 个 repair wave、硬上限 5。
- 明确禁止连续两次空的 whole-change review。

这些内容已经针对你先前“review 越做越长”的问题进行了正确优化。

### 3.2 必须增加的能力

修订版增加了：

| 能力 | 目的 |
|---|---|
| `STANDARD / SECTION / DELTA / INTEGRATION` 模式 | 避免同一种 merge-review 语义套在所有层级上 |
| Section review packet | 冻结 ID、base/head、contract、feature invariants、dependencies、deferred work |
| Section intent card + feature intent card | 防止局部优化破坏全局要求 |
| Intermediate-state validity | 防止“等后续 section 才能运行”的半成品被误判为通过 |
| Section verdict | `section-accepted` 不再被误写为 `mergeable` |
| Integration review focus | 专门检查跨 section 交互与完整功能接受标准 |
| Section-specific reset rules | 确定何时需要重新 full review |
| Section-aware ledger fields 和 prompts | 让 orchestrator 可重复、可审计地调用 review |

### 3.3 不需要修改的部分

`review-coverage.md` 和 `ai-agent-risk-catalog.md` 的基本 lens 仍然适用；它们不需要因 section 化而重写。Section 化改变的是**边界、输入包、结论层级和迭代方式**，不是正确性、安全、数据、并发、运维等风险类别本身。

## 4. 传统软件工程中的大功能开发流程

传统工程没有唯一标准流程，但在 code review、Agile/XP、Continuous Delivery 和演进式架构实践中，有一组高度一致的原则。

### 4.1 先定义目标、约束与完成条件

在编码之前明确：

- 用户或业务结果；
- 非目标；
- 关键不变量；
- 架构和兼容约束；
- 验收条件；
- 发布、迁移、回滚和运维要求。

这不是要求提前固定所有实现细节。相反，应冻结结果与约束，把局部技术路径留给后续 section 依据代码现实决定。

### 4.2 把大功能切成一个个自洽 change

Google Engineering Practices 将理想 CL 定义为“只处理一件事的最小自洽变更”，通常只是完整功能的一部分，并要求相关测试与 reviewer 理解所需的信息一起提供。其理由包括：小变更更容易快速、深入地审查，更少引入 bug，更容易回滚，也更容易在方向错误时减少浪费。

“自洽”比具体行数更重要：一个新 API 最好与至少一个真实 usage 一起出现，否则 reviewer 无法判断接口是否合理；另一方面，混合大规模 refactor 与功能语义会显著降低可审查性。

### 4.3 纵向 slice 优先

Agile 的 vertical slice 从用户/系统行为出发，跨越完成该行为所需的 UI、业务逻辑、API、持久化等层，而不是先做完整数据库层、再做完整后端、最后才连接 UI。

纵向 slice 的工程收益是：

- 每段都能产生真实反馈；
- 每段都有行为级 oracle；
- 架构错误更早暴露；
- 不把第一次真正集成推迟到最后；
- reviewer 能围绕一个结果而不是一组文件判断正确性。

对于基础设施或架构不确定的功能，可以先做 walking skeleton：用最薄的端到端路径证明主要组件、部署和测试链路是可行的，再逐步增加深度。

### 4.4 对不兼容变化使用演进模式

跨 API、schema、数据表示或共享实现的大改，不应一次性同时改所有 producer 和 consumer。

常用模式包括：

- **Parallel Change / Expand–Migrate–Contract**：先扩展兼容能力，再逐步迁移 consumer，最后删除旧路径。
- **Branch by Abstraction**：在稳定 seam 后逐步替换实现，避免长期分支最终产生巨大合并风险。
- **Feature Toggle**：让未完全开放的新路径与可部署主干共存，分离 code deployment 与 feature release；同时必须有 owner、默认状态、测试矩阵、回滚和删除期限。

### 4.5 每段独立实现、测试、review、集成

典型循环是：

```text
确定 slice contract
-> 实现最小行为
-> targeted tests / static checks
-> small review
-> 修复并验证
-> 合入共同集成状态
-> 运行跨 slice checkpoint
-> 下一 slice
```

Code review 的目标不是追求“完美代码”，而是在不降低代码健康度的前提下保持工程进展。非阻塞 polish 应明确标记，而不是无限阻塞一个已经改善系统的自洽 change。

### 4.6 最终做系统级接受与发布门禁

即使每个小 change 都已经 review，完整 feature 仍需要：

- 需求覆盖核对；
- 端到端和负路径；
- 跨模块 contract；
- migration/rollback rehearsal；
- 性能、安全、可观测性和运维；
- 临时 flag、兼容层和旧路径清理；
- release decision。

这就是新 skill 中 section gate 与 final integration gate 分离的传统工程依据。

## 5. 近一年 AI Agent 大功能开发资料的共同结论

### 5.1 Anthropic：长任务依赖增量工作和持久化 handoff

Anthropic 在 2025-11-26 的长任务 harness 文章中指出，多上下文任务的核心问题是新 session 没有先前记忆；其方案使用 initializer 建立环境和任务状态，coding agent 每轮只推进一个 feature，并留下 git commit 与 progress artifact。文章明确把“one feature at a time”描述为抑制 agent 一次做太多的关键手段。

这直接支持：

- `PLAN-FULL.md` + `FEATURE-STATE.md`；
- 每次只给一个 section；
- 每段 commit/handoff；
- 不把聊天上下文当作唯一记忆。

### 5.2 Anthropic 2026：planner / generator / evaluator 与 sprint contract

2026-03-24 的后续文章把长应用构建拆成 planner、generator、evaluator。每个 sprint 前，generator 与 evaluator 先约定“done”及验证方式；evaluator 通过 UI、API 和数据库状态执行具体标准。

文章同时给出两个重要限制：

- 默认 evaluator 可能测试得过浅，甚至会发现真实问题后自我说服为“不重要”；因此必须给出细粒度 criteria 和 hard threshold。
- 随模型能力提高，过重的 harness 组件可能过时；应寻找最简单、真正 load-bearing 的结构。

因此本 skill 没有对所有小任务强制 planner/generator/evaluator 多代理结构，只在大、风险高或曾经不收敛的任务触发；也没有为每个普通 section 强制额外两轮空审。

### 5.3 OpenAI：长任务的关键是 agent loop 和 durable project memory

OpenAI 2026-02-23 的 Codex 长任务文章将循环概括为 plan → edit → tools → observe → repair → update status → repeat，并强调 spec、plan、constraints、status 均写入可重复读取的 Markdown。Milestone 要足够小，具有 acceptance criteria、validation commands、stop-and-fix 规则和 decision notes；每个 milestone 都运行 tests/lint/typecheck/build 等验证。

这支持本 skill 的：

- feature contract；
- section milestone；
- validation command；
- failed validation 不进入下一段；
- decision ledger；
- current state/audit log。

### 5.4 OpenAI：Agent-first 工程的核心是 scaffolding、repository legibility 和小步 debt control

OpenAI 2026-02-11 的 harness engineering 文章描述：大目标被 depth-first 拆为 design、code、review、test 等较小 building blocks；plans 是版本化的一等 artifact，仓库文档与结构通过 lint/CI 机械执行；技术债通过持续的小 refactor PR 清理，而不是累积为大型修复。

这支持：

- 计划和决策进入仓库；
- section 不夹带随意 cleanup；
- 重复错误应转化为 test、lint、结构规则或 repo skill；
- 修复循环失败时改 harness/边界，而不是要求 agent “再努力一次”。

### 5.5 Cursor：先计划、错误时回到计划、用 fresh context 和可验证目标

Cursor 2026-01-09 的实践文章建议：先研究 codebase，生成含路径与代码参考的可编辑计划；如果实现方向错误，回到计划而不是不断用 follow-up prompt 修补。文章也建议在完成一个 logical unit 或 agent 开始混乱时开启新对话，并强调 typed language、lint、tests 和 verifiable goals。

这支持：

- plan gate；
- section contract material change 时 replan/reset；
- implementer/reviewer 上下文隔离；
- 不把无限 follow-up patch 当作正常流程。

### 5.6 GitHub：Spec → Plan → Tasks → Implement

GitHub 2025-09-02 的 Spec Kit 文章将流程明确为 Specify、Plan、Tasks、Implement；task 应是可单独实现、测试和 review 的小块，并在各阶段设置人工校正 checkpoint。

新 skill 保留这一主干，但补上了大型现有代码库最容易缺失的内容：global invariants、state ownership、compatibility/migration、repair delta 和 final integration review。

## 6. 学术资料对长任务与自动 review 的约束

以下均为 2025-08-06 之后发布的资料；其中多篇仍是预印本，因此用于判断方向和风险，不把单一数值视为永久能力上限。

### 6.1 长任务仍显著难于单 issue

- SWE-Bench Pro 收集需要专业工程师数小时到数天、跨多个文件和大量修改的任务。
- SWE-EVO 的 release-sized 任务平均涉及约 21 个文件和大规模测试集；论文报告当前最强结果仍远低于单 issue benchmark。
- RoadmapBench 的任务中位修改规模约 3,700 行、51 个文件，最强模型解决率仍不足一半。

三者共同说明：即使 2026 年模型的单任务能力明显提高，把一个 release-sized feature 当作单一 prompt、单一 diff 和单一最终 review，仍会暴露持续规划、跨文件协调、需求解释与回归保持方面的明显能力差距。

### 6.2 自动 code review 会产生大量低信号输出

2026 年一项对 code review agents 的经验研究报告，在其样本中 CRA-only PR 的 merge rate 较低，且大量自动评论落在低 signal-to-noise 区间。该研究不能证明“AI review 导致 PR 失败”，因为存在任务选择、项目和 reviewer composition 等混杂因素；但它足以反驳“多跑几轮自动 review 必然单调提高质量”的假设。

流程上的应对不是停止 Agent review，而是：

- 冻结 scope 和 contract；
- 只接受可复现、可达路径、明确影响和修复方向的 finding；
- 稳定 ID、root-cause dedup；
- 将 polish 与 blocker 分开；
- 人类保留业务语义和风险接受权；
- 用 deterministic tests/linters 替代重复出现的主观检查。

## 7. 社区经验及其证据权重

社区资料只作为实践信号，不与厂商实验或学术评估同权。

### 7.1 Jesse Vincent：brainstorm → plan → implement，task 后立即 code review

2025-10 的 Superpowers 工作流会先 brainstorm 与 plan，自动建立 worktree，再把任务逐个分配给 subagent，并在每个 task 后 code review；同时强调 TDD 和 realistic scenario 测试 skill，而不是通过问答测验宣布 skill 有效。

与本 skill 一致的部分：

- worktree isolation；
- task-by-task implementation and review；
- fresh agent roles；
- realistic validation；
- skill 本身也需要压力测试。

### 7.2 Simon Willison：并行 agent、architect plan 与 scout

2025-10 的实践记录提到让 architect 迭代计划，再由 fresh instances review/implement；对困难代码库可先派 scout，只为识别 sticky points，不准备直接合并其代码。

本 skill 将这一经验转化为：高不确定性时允许 walking skeleton 或 plan reviewer；并行只限 dependency-independent sections，而不是默认把所有 section 同时发出。

### 7.3 大规模 swarm 的反例：代码量不等于可交付质量

2026-01 对 Cursor 大规模 browser experiment 的社区复核指出：百万行产出和大量 agent 并不能替代通过 CI、build instructions 和实际运行证明可用。后续能构建并展示结果后，证据才显著增强。

这支持“agent summary 是 claim，不是 proof”，也支持 final integration gate 必须检查实际运行、构建、端到端行为和可复现性。

### 7.4 外置计划比把整个仓库塞进 context 更重要

相关 Hacker News 讨论中，实践者指出 coding agent 通过 grep、计划文件和外置状态处理远大于 context window 的代码库；同时也提醒超大 context 会降低局部相关性。这是社区观察，不是严格实验，但与厂商关于 durable memory 和 progressive disclosure 的结论一致。

## 8. 从资料到 Skill 的设计映射

| 研究结论 | Skill 设计 |
|---|---|
| Small CL 应是一个自洽 change | 一个 section 只承担一个行为增量或必要 seam |
| Vertical slice 产生更早反馈 | 默认按端到端行为切分，而非目录/层 |
| Refactor 与行为应尽量分开 | enabling refactor 需要保护测试和明确后继 section |
| Expand–migrate–contract | 为 schema/API/共享表示提供独立迁移阶段 |
| Feature flag 保持可部署 | section contract 必须写 flag 默认值、回滚和清理条件 |
| One feature at a time | implementer 每次只获得一个 section |
| Durable project memory | `PLAN-FULL.md`、`FEATURE-STATE.md`、handoff、review ledger |
| Sprint contract / hard criteria | `Sxx-CONTRACT.md` + acceptance criteria + commands |
| Planner/generator/evaluator | plan reviewer、implementer、section reviewer、repair、integration reviewer |
| Evaluator 可能表面化 | 强制负路径、边界、partial failure 和 runtime evidence |
| 新模型可能减少 scaffolding 需求 | 仅对大/高风险/不收敛任务触发，不把复杂流程施加给小改动 |
| 长任务 benchmark 能力仍不足 | 依赖图、section、checkpoint、final integration |
| 自动 review 可能低信号 | finding quality gate、dedup、severity、human decision、repair budget |
| Parallel agents 需隔离 | worktree + independent dependency + predetermined integration order |

## 9. 新 Skill 的关键设计决策

### 9.1 Skill 名称

选择 `sectioned-feature-development`，而不是 `large-feature-review`：

- 它覆盖 plan、implement、validate、review、repair、integrate、archive，而不只是 review。
- “sectioned” 强调执行单元；“feature” 表明仍需全局 contract；“development” 包含完整生命周期。

### 9.2 Section 是行为单元，不等于模块

保留你已有的 “section” 术语，但在规范中给出严格含义：

> 一个 section 是一个可独立实现、验证、review 和回滚的行为增量，或一个由后续明确使用、具有保护测试的 enabling seam。

这避免“小模块 review”退化成“按文件夹切 diff”，后者常常无法独立判断正确性。

### 9.3 三层门禁

1. **Plan gate**：需求覆盖、依赖 DAG、ownership、oracle、rollback。
2. **Section gate**：局部 contract 与 relevant global invariants。
3. **Feature integration gate**：完整需求与跨 section composition。

这三层分别防止错误计划、局部实现缺陷和组合缺陷。

### 9.4 Review 收敛模型

```text
稳定 section baseline
-> 一次 SECTION full discovery
-> 冻结 finding
-> 最小 repair wave
-> DELTA verification
-> 必要时再 repair
-> 仅 reset trigger 才重新 full discovery
```

这与现有 `code-review` skill 的核心一致，并消除新自定义规则中的冲突。

### 9.5 模型 routing

保留你当前偏好作为默认 alias：

- ordinary implementation：`sol-medium`
- high-risk implementation / repair：`sol_high`
- clean discovery review / integration review：`sol_xhigh`

但 skill 要求以项目实际 profile 名称和语义风险为准，不能因 20 行权限变更很短就使用低审查深度，也不能用最高模型做机械 plan extraction。

### 9.6 可执行辅助脚本

`section_plan.py` 负责：

- 验证 `FEATURE-CONTEXT` 和 section marker；
- 检查 section ID 唯一性；
- 检查所需 headings；
- 检查 self/unknown dependency ID 与 dependency cycle；
- 列出 sections；
- 将 feature context + 一个 section 提取到 `PLAN.md`；
- 生成 SHA-256 fingerprint；
- 安全复制或显式 move 到 timestamp archive。

把这部分做成脚本而不是每次让 Agent 手写，可以减少提取错段、遗漏全局约束和归档覆盖等机械错误。

## 10. 被拒绝的替代方案

### 10.1 完成全功能后反复 whole-change review

拒绝原因：范围过大、覆盖不可见、修复不断改变 baseline、reviewer 每轮重新采样，正是当前失败模式。

### 10.2 每个 section 连续两轮 clean review

拒绝原因：没有定义独立性与覆盖增益；成本近似翻倍，还会增加低信号意见。高风险 section 可选额外 fresh verification，但不是机械必需。

### 10.3 纯按层/目录拆分

拒绝原因：section 没有可观察行为，真正 integration 延迟到最后。

### 10.4 所有 section 并行

拒绝原因：共享 contract、state owner、schema、migration 和 generated source 会被不同 Agent 分别发明；整合 patch 可能比原始 feature 更大。

### 10.5 每个 section 都由 planner、implementer、reviewer、judge 多轮协商

拒绝原因：Anthropic 2026 的经验表明 harness 假设会随模型进化而过时；对普通 section 过度编排会增加成本和状态面。新 skill 只在高风险/模糊计划使用独立 plan reviewer，并保留最小必要角色分离。

### 10.6 通过增加 reviewer 数量代替测试 oracle

拒绝原因：没有 authoritative semantics 或可证伪验证时，更多 reviewer 只会产生更多互相冲突的合理猜测。

## 11. 使用建议

### 11.1 首次落地

建议先在一个 500–1500 行、跨 4–8 个模块、但业务语义已经明确的功能上使用。观察：

- section 首轮 finding 数；
- repair waves；
- reset 次数；
- integration gate 新发现的问题类型；
- plan 与实际 section 范围偏差；
- 哪些错误可转化为项目 test/lint/rule。

### 11.2 不要把流程效果只用“review 轮数”衡量

更好的指标包括：

- 首轮发现的 root-cause coverage；
- repair 后重新 full review 的比例；
- section scope expansion 率；
- integration gate 才发现的缺陷比例；
- 未定义业务语义导致的 block 次数；
- failed checks 在下一 section 前被关闭的比例；
- merge 后回归与 rollback 难度；
- technical debt 是否有 owner 和清理 section。

### 11.3 迭代 skill 的方式

只有当同类失败重复出现时，才把它提升为持久 guardrail：

- regression/property test；
- static/structural lint；
- shared validator；
- generator/template 修改；
- repo architecture docs；
- CI gate；
- project-specific skill。

避免把单次 reviewer 偏好写成永久规则。

## 12. 参考资料

### 12.1 AI Agent 厂商与官方工程资料（全部不早于 2025-08-06）

1. Anthropic, **Effective harnesses for long-running agents**, 2025-11-26. 增量推进、一个 feature 一次、git commit、progress artifact 和跨 context handoff。  
   <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
2. Anthropic, **Harness design for long-running application development**, 2026-03-24. Planner/generator/evaluator、sprint contract、具体 QA criteria、evaluator 局限与 harness 简化。  
   <https://www.anthropic.com/engineering/harness-design-long-running-apps>
3. OpenAI, **Harness engineering: leveraging Codex in an agent-first world**, 2026-02-11. Depth-first building blocks、repository knowledge、first-class plans、机械 guardrails、小步 debt cleanup。  
   <https://openai.com/index/harness-engineering/>
4. OpenAI Developers, **Run long horizon tasks with Codex**, 2026-02-23. Agent loop、durable project memory、milestones、acceptance criteria、validation commands、status/audit log。  
   <https://developers.openai.com/blog/run-long-horizon-tasks-with-codex>
5. Cursor, **Best practices for coding with agents**, 2026-01-09. Plan mode、从计划重启、context 管理、branches、careful review 和 verifiable goals。  
   <https://cursor.com/blog/agent-best-practices>
6. GitHub, **Spec-driven development with AI: Get started with a new open source toolkit**, 2025-09-02. Specify → Plan → Tasks → Implement，小而可 review/独立测试的 task 与人工 checkpoint。  
   <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/>

### 12.2 近期学术资料（全部不早于 2025-08-06）

1. Deng et al., **SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?**, first submitted 2025-09-21.  
   <https://arxiv.org/abs/2509.16941>
2. Le et al., **SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios**, first submitted 2025-12; accessed current 2026 revision.  
   <https://arxiv.org/html/2512.18470>
3. Xu et al., **RoadmapBench: Evaluating Long-Horizon Agentic Software Development Across Version Upgrades**, 2026-05-15.  
   <https://arxiv.org/abs/2605.15846>
4. Chowdhury et al., **From Industry Claims to Empirical Reality: An Empirical Study of Code Review Agents in Pull Requests**, 2026-04-03, accepted MSR 2026.  
   <https://arxiv.org/abs/2604.03196>

### 12.3 社区实践（经验性证据，全部不早于 2025-08-06）

1. Jesse Vincent, **Superpowers: How I'm using coding agents in October 2025**, 2025-10-09.  
   <https://blog.fsck.com/2025/10/09/superpowers/>
2. Simon Willison, **Embracing the parallel coding agent lifestyle**, 2025-10-05.  
   <https://simonwillison.net/2025/Oct/5/parallel-coding-agents/>
3. Simon Willison, **Scaling long-running autonomous coding**, 2026-01-19.  
   <https://simonwillison.net/2026/Jan/19/scaling-long-running-autonomous-coding/>
4. Hacker News discussion, **Scaling long-running autonomous coding**, accessed 2026-08-06. 用于补充外置计划、grep/context 与多 agent 集成的实践观察。  
   <https://news.ycombinator.com/item?id=46624541>

### 12.4 传统软件工程资料

1. Google Engineering Practices, **Small CLs**. 一个自洽 change、相关测试、stacked changes、refactor 分离与 reviewability。  
   <https://google.github.io/eng-practices/review/developer/small-cls.html>
2. Google Engineering Practices, **The Standard of Code Review**. 以持续改善 code health 为批准标准，而非追求完美。  
   <https://google.github.io/eng-practices/review/reviewer/standard.html>
3. Martin Fowler, **Parallel Change**, 2014-05-13. Expand–migrate–contract。  
   <https://martinfowler.com/bliki/ParallelChange.html>
4. Pete Hodgson / Martin Fowler, **Feature Toggles**, 2017. Release toggle、部署与发布分离、flag 生命周期与测试。  
   <https://martinfowler.com/articles/feature-toggles.html>
5. Jez Humble, **Make Large Scale Changes Incrementally with Branch By Abstraction**, 2011-05-05. 大规模替换的增量 seam 与退出策略。  
   <https://continuousdelivery.com/2011/05/make-large-scale-changes-incrementally-with-branch-by-abstraction/>
6. Agile Alliance, **A Tale of Slicing and Imagination**. User Story 作为跨层的 vertical slice，而非 horizontal layer backlog。  
   <https://agilealliance.org/resources/experience-reports/a-tale-of-slicing-and-imagination/>
7. Agile Alliance, **INVEST**. 独立、可测试、适当大小等 story 质量标准。  
   <https://agilealliance.org/glossary/invest/>

## 13. 研究方法与限制

### 13.1 搜索与筛选过程

1. 审阅输入的 Custom Instructions，提取大变更触发、分段、subagent、commit、review loop 和归档语义。
2. 解包 `code-review.zip`，检查主 skill、review-loop protocol、coverage、ledger 和 AI risk catalog。
3. 解包 `skill-creator.zip`，依据其目录、frontmatter、progressive disclosure、`agents/openai.yaml`、scripts/references/assets 和 validation 规范设计产物。
4. 对 AI Agent 资料设置 2025-08-06 的硬时间下限；优先顺序为厂商工程文章/官方文档、近期学术 benchmark/实证研究、最后才是社区实践。
5. 对传统工程资料不设一年限制，因为 small changes、vertical slicing、parallel change、feature flags 等原则属于稳定的软件工程基础。
6. 将每个候选流程规则映射到至少一个问题：scope、memory、oracle、review independence、repair convergence、integration、migration 或 operational readiness。
7. 对可能随模型提升而过时的复杂 harness 规则进行删减，只保留对当前问题有直接负载的结构。

### 13.2 明确排除的资料

- 2025-08-06 之前发布的 AI coding-agent 工作流文章，即使其历史影响较大。
- 原始 Ralph Wiggum 早期资料；它早于用户指定窗口。仅采用 2026 Anthropic 对社区同类模式的当代总结，不用旧文作为规则依据。
- 没有日期、没有可核对流程细节或只展示产出规模的营销内容。
- 将单次成功 demo 直接外推为生产可靠性的文章。
- 无法区分功能正确性与代码量/运行时长的评价。

### 13.3 限制

- 厂商文章通常来自受控实验或特定 repository，不能保证直接迁移到所有项目。
- 近期 benchmark 仍快速变化，绝对分数会随模型和 harness 更新；本研究只使用其“long-horizon 显著更难”的稳健方向。
- code review agent 实证研究存在选择偏差和混杂变量，不能证明因果；本研究只用它支持低信号风险与 human oversight。
- 社区经验是 anecdotal evidence，只在与官方/学术结论一致时用于补充操作细节。
- 未在真实用户仓库上运行完整 skill eval；本次完成了结构验证、脚本单元测试、模板提取/归档测试和修订 skill 的静态检查。实际最佳 section 大小和 profile routing 应通过几次真实项目运行校准。
