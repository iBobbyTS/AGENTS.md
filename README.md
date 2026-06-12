# AGENTS.md
个人使用的Coding Agent约束，作为备份和分享。<br>
本README纯手打，无AI，仓库内其余文件基本 100%AI。

## 目录

- [AGENTS.md](#agentsmd文件)
- [Git Hook](#git-hook)
- [Skills](#skills)
    - [ai-aware-code-audit](#ai-aware-code-audit): 面向 AI 主导编程的审计
    - [debug-notes-to-engineering-notes](#debug-notes-to-engineering-notes): 仅在官方文档不全/有误时才使用，结合[second-pass-debugging](#second-pass-debugging)，燃烧自己的token，为后人照亮debug之路
    - [feishu-message-sender](#feishu-message-sender): 飞书自定义机器人在长任务里定时汇报
    - [init-codex-project](#init-codex-project): 初始化项目
    - [large-refactor-audit](#large-refactor-audit): 大规模重构代码的review
    - [manual-brainstorming](#manual-brainstorming): 手动触发的brainstorming
    - [manual-git-worktrees](#manual-git-worktrees): 手动分出git worktree实现功能
    - [second-pass-debugging](#second-pass-debugging): 第一次修复失败后走这个流程
    - [receiving-code-review](#receiving-code-review): Review PR 触发

### AGENTS.md文件
[AGENTS.md](AGENTS.md) 是 Codex 默认读取的约束名，所以把它作为本仓库的名字。Codex 设计总共有2层 `AGENTS.md`，一个在 `~/.codex/AGENTS.md`，另一个在项目的根目录里。

> 注：GUI 里 Settings - Personalization - Custom instructions 指向的就是 `~/.codex/AGENTS.md`

主要职责：
- 语言：回复、Implementation Plan都用中文。
- Skills：通过 `.agents/skills/` 判断用户是否初始化过这个项目，没有的话通过 [$init-codex-project](skills/init-codex-project) 进行初始化。
    - `.agents/skills/` 是当前项目运行时常用的最佳实践，如果发现有更好的方法，Agent应该主动更新。
- 测试：除了修改文档、修改UI字符串之类的，其他逻辑修改都需要做单元测试；测试必须执行；测试不得用无意义断言。
- 代码安全：未经要求不回滚Agent不了解的修改；破坏性操作前先 dry run；不主动commit, push。
- Implementation Plan：批准后写入 `.agent-work/PLAN.md`，执行完成后重命名为 `PLAN.md.done`，上下文压缩后重新读取。目前Codex没有显式的逻辑证明它会保存Implementation Plan，上下文压缩后会重新读取，所以需要有这条规则。
- Sub-agent 调度：拆分原则是 context-aware，而不是类似人工软件开发的 role-aware 分工；小任务给 `gpt-5.4-mini`，大任务给 `gpt-5.5`。高风险任务不外包。
- 可维护性（重要）：主要是用来避免上帝对象、超大文件等问题。小功能执行完后汇报可维护性，是否增加了复杂度；大功能执行前先判断是否需要进行Class, Function的职责拆分。
- Docker：主要是我本地用的是`colima`而非 Docker Desktop，agent经常去尝试`docker compose`浪费token。colima比较轻量，不会像 Dokcer Desktop 那样一下占1-2G的内存。

### Git Hook

> 还没实战测试

[git-hook.md](git-hoot.md)：操作指引
- 每次审计完成时提交消息带上 `Maintenance-Audit: true` （用 [ai-aware-code-audit](skills/ai-aware-code-audit/) 时会自动带上）。
- 在用户层面配置一个计算上次什么时候审计的脚本。
- 使用 [init-codex-project](skills/init-codex-project/) 初始化项目时定好这个项目多久审计一次。
- 每次提交时Git会提醒下次审计什么时候或已经超过了设定间隔。

### Skills

#### [ai-aware-code-audit](skills/ai-aware-code-audit/)

用 `Codex` 和 `ChatGPT-5.5 Extended Thinking` vibe出来的审计规则，除了传统审计的覆盖面，还包含了gpt-5.4, gpt-5.5时代AI编程可能造成的各类技术债（更早的没有参考，模型和Agent能力进化速度都很快）。
> 没有下面这一条约束，大项目会陷入死循环。Agent倾向于读完所有代码，分析完所有模块再写报告，一旦超出上下文就会触发软件自动压缩，之前的分析结果会丢失，必须重新读代码。

审计过程：先阅读项目，了解大致结构，然后创建 `.agent-work/audit/{YYYYMMDD-HHMM}` 文件夹，在这里面放 `FULL.md`，实时保存审计结果，审计进度保存在 `.agent-work/audit/CURRENT.md` 里，审计结束后再根据 `FULL.md` 生成 `REPORT.md`。

#### [debug-notes-to-engineering-notes](skills/debug-notes-to-engineering-notes)

使用[second-pass-debugging](#second-pass-debugging)修完问题后把 `.agent-work/debug` 里的记录沉淀到 `docs/engineering-notes`，方便后续开发和其他人阅读。会记录正确做法、错误尝试记录、和官方文档不符的部分、版本记录。不包含项目/实现约定。

#### [feishu-message-sender](skills/feishu-message-sender)

建议长任务时使用，不要让agent在前台轮询。使用这个skill它会复制一份模板脚本，然后编辑脚本并后台启动，用你的飞书机器人发送一条任务开始通知、每小时的进度汇报、任务结束总结。<br>
机器人配置放在 `~/.config/feishu-message-sender/secret.json`，格式为`{"webhook":"https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxx","secret":"签名秘钥","name":"本电脑的名字"}`。<br>
飞书官方：[自定义机器人使用指南](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN)（给agent看的话用[md版本](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot.md)）

#### [init-codex-project](skills/init-codex-project/)

初始化项目，根据项目采用的技术栈，创建项目级 AGENTS.md 文件，定下：
- 运行时的命令，防止每次都试。
- git提交语言、UI语言
- ...... (它按我的要求自动创建完我还没审查)

#### [large-refactor-audit](skills/large-refactor-audit/)

底层重构、大面积代码改动提交前使用这个skill进行review。
已包含对传统的review面和ai代码纰漏的检查。<br>
审计过程会实时保存，原因和流程见 [ai-aware-code-audit](#ai-aware-code-audit)。

> 注：下面4个skill都是根据[Superpowers](https://github.com/obra/superpowers) [v5.1.0](https://github.com/obra/superpowers/releases/tag/v5.1.0)  做的 “Codex-native” 版本。没有照搬 Superpowers 是因为它的约束过重，对于Codex这样的高级智能体会浪费过多token，所以修改后的都是手动/条件触发，不是默认触发。

#### [manual-brainstorming](skills/manual-brainstorming/)

根据 `brainstorming` 修改而来，只有用户主动触发才会走这套完整的流程，避免小改动也浪费时间和token。<br>
删除了plan保存要求和plan文件的commit，继续按照 [AGENTS.md](#agentsmd文件) 就行。

#### [manual-git-worktree](skills/manual-git-worktree/)

根据 `using-git-worktrees` 修改而来，只有用户主动触发才会走git worktree开发。

#### [second-pass-debugging](skills/second-pass-debugging/)
根据 `systematic-debugging` 修改而来。只有bug第一次修复失败才会触发。<br>
先做“证据盘点”，包括上一轮改了什么、为什么没解决、现在的失败现象是什么、有没有可运行复现。然后再进原 `systematic-debugging` 的流程。<br>
新增流程：把试错过程记录在`.agent-work/debug`下，避免疑难杂症经历过多次上下文压缩后忘记之前试过的错误路径。

#### [receiving-code-review](skills/receiving-code-review/)

根据 `receiving-code-review` 修改而来。只有外部的修改，比如PR，才会走这套流程，去除了针对 subagent 的 code review，因为当前 Codex 还不支持 Orchestrator，我不想手动实现，效益可能不高，等官方即可。[AGENTS.md](#agentsmd文件) 里的subagent逻辑不需要完整的code review。<br>
判断是否可以合并：如果可以合并，先汇报给用户，写好message供用户阅读；如果不能合并，提出哪里有问题，需要怎么改，并询问用户是comment让PR提交者改还是直接改。
