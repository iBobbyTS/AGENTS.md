# AGENTS.md
个人使用的Coding Agent约束，作为备份和分享。

本README纯手打，无AI，仓库内其余文件基本 100%AI。

## 目录

- [AGENTS.md](#agentsmd文件)
- [Git Hook](#git-hook)
- [Skills](#Skills)
    - [init-codex-project (初始化项目)](#init-codex-project)
    - [ai-aware-code-audit (面向 AI
    主导编程的审计)](#ai-aware-code-audit)

### AGENTS.md文件
这是 Codex 默认读取的约束名，所以把它作为本仓库的名字。
Codex 设计总共有2层 `AGENTS.md`，一个在 `~/.codex/AGENTS.md`，另一个在项目的根目录里。
注：GUI 里 Settings - Personalization - Custom instructions 指向的就是 `~/.codex/AGENTS.md`

主要职责：
- 语言：回复、Implementation Plan都用中文。
- Skills：通过 `.agents/skills/` 判断用户是否初始化过这个项目，没有的话通过 [$init-codex-project](skills/init-codex-project) 进行初始化。
    - `.agents/skills/` 是当前项目运行时常用的最佳实践，如果发现有更好的方法，Agent应该主动更新
- 测试：除了修改文档、修改UI字符串之类的，其他逻辑修改都需要做单元测试；测试必须执行；测试不得用无意义断言。
- 代码安全：未经要求的不回滚Agent不了解的修改；破坏性操作前先 dry run；不主动commit, push
- Implementation Plan：批准后写入 `.agent-work/PLAN.md`，执行完成后重命名为 `PLAN.md.done`，上下文压缩后重新读取。目前Codex没有显式的逻辑证明它会保存Implementation Plan，上下文压缩后会重新读取，所以需要有这条规则。
- Sub-agent 调度：拆分原则是 context-aware，而不是类似人工软件开发的 role-aware 分工；小任务给 `gpt-5.4-mini`，大人物给 `gpt-5.5`。高风险任务不外包。
- 可维护性（重要）：主要是用来避免上帝对象、超大文件等问题。小功能执行完后汇报可维护性，是否增加了复杂度；大公牛执行前先判断是否需要进行Class, Function的职责拆分。
- Docker：主要是我本地用的是colima而非 Docker Desktop，agent经常去尝试docker compose浪费token。colima比较清量，不会像 Dokcer Desktop那样一下占1-2G的内存

### Git Hook

> 还没实战测试
- 每次审计完成时提交消息带上 `Maintenance-Audit: true` （用 [ai-aware-code-audit](skills/ai-aware-code-audit/) 时会自动带上）。
- 在用户层面配置一个计算上次什么时候审计的脚本。
- 使用 [init-codex-project](skills/init-codex-project/) 初始化项目时定好这个项目多久审计一次。
- 每次提交时Git会提醒下次审计什么时候或已经超过了设定间隔。

### Skills

#### [init-codex-project](skills/init-codex-project/)

初始化项目，根据项目采用的技术栈，定下：
- 运行时的命令，防止每次都试。
- git提交语言、UI语言
- ...... (它按我的要求自动创建完我还没审查)

#### [ai-aware-code-audit](skills/ai-aware-code-audit/)

用 `Codex` 和 `ChatGPT-5.5 Extended Thinking` vibe出来的审计规则，除了传统审计的覆盖面，还包含了gpt-5.4, gpt-5.5时代AI编程可能造成的各类技术债（更早的没有参考，模型和Agent能力进化速度都很快）。
