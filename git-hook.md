# Git Hook 审计提醒方案

这套方案的目标很简单：让所有由 Git 管理、由 Codex 参与开发的项目，在提交时自动提醒是否需要做一次可维护性审计。

## 设计思想

1. 提醒逻辑放在 Git hook，不放在 Codex 自己的判断里。
2. 可执行脚本随仓库版本控制；安装脚本只写入仓库本地 Git 配置。
3. 提醒必须是非阻塞的，只负责输出提示，不影响 commit 成功。
4. 明确的审计标记优先于猜测。最近一次带 `Maintenance-Audit: true` 的提交，是最新审计点。

## 复现流程

### 1. 安装仓库自带的 Git hook

在仓库根目录执行：

```sh
./scripts/install-git-hooks.sh
```

该脚本设置当前仓库的 `core.hooksPath=.githooks`；不会修改全局 Git 配置，也不会影响其他项目。

### 2. 仓库内的提醒脚本

`.githooks/codex-maintainability-audit-reminder` 已随仓库提供，职责只有三个：

1. 读取当前仓库的本地配置。
2. 计算距离上次审计还有多少次提交，或者已经超出多少次提交。
3. 打印提醒后退出 0。

仓库本地 Git 配置只保存两项状态：

```sh
git config --local codex.maintainabilityAuditInterval <N>
git config --local codex.maintainabilityAuditBaseline <HEAD_SHA>
```

其中：

- `codex.maintainabilityAuditInterval` 是审计间隔，必须是数字。
- `codex.maintainabilityAuditBaseline` 是可选基线，通常初始化时写入当前 `HEAD`。
- 如果仓库里已经有 `Maintenance-Audit: true` 标记提交，脚本会优先用它。

### 3. 用 hook 触发提醒

已提供以下 Git hook 入口：

- `post-commit`
- `post-merge`
- `post-rewrite`
- `post-applypatch`
- `post-checkout`

其中 `commit` 是主要场景；其它 hook 用来避免合并、重写历史、切换分支后计数失真。

提示文案统一成两种：

```text
建议<N>次后进行项目审计。
上次审计是<N>次前，建议尽快安排审计。
```

### 4. 通过初始化 skill 连接新项目

专门的 [$init-codex-project](skills/init-codex-project) 初始化 skill 负责把新仓库接进这套机制；仓库需提交 `.githooks/` 与安装脚本，随后执行安装脚本。

它应该：

1. 检查仓库是否已经接入 Git 版本管理。
2. 询问用户审计间隔是多少次提交，不要问按天或按周。
3. 写入仓库本地的 `codex.maintainabilityAuditInterval`。
4. 如果仓库已经有提交，且用户没有要求“必须等到显式审计标记后才开始计数”，就把当前 `HEAD` 写成基线。
5. 保留 `Maintenance-Audit: true` 作为显式审计标记。

这样，新项目初始化并安装 hook 后，只要用户继续提交，Git 就会在合适的 hook 点提醒是否该审计了。

### 5. 在 Codex 的 commit instruction 里补一句

用户需要自己在 Codex 的 Settings - Git - Commit instruction 里加入这句：

```text
After committing, report audit reminder shown by git hooks.
```

这句的作用是让 Codex 在提交完成后把 Git hook 的提醒也带出来，避免用户只看到提交结果却漏掉审计提示。

## 维护约定

- 不要把每个仓库的状态写进 `.githooks/`；状态仍保存在仓库本地 Git 配置和 Git 历史中。
- 不要让提醒阻塞正常提交。
- 不要把“多久提醒一次”做成按天或按周的定时任务，这个问题本质上是 Git 历史长度问题。
- 不要猜测审计点，优先读取显式 `Maintenance-Audit: true` 标记。
- 新 clone 或新 worktree 必须各自执行一次 `./scripts/install-git-hooks.sh`，因为 `core.hooksPath` 是本地 Git 配置，不会由 Git 版本控制。

## 最小检查

复现后，至少确认这三件事：

1. `git commit` 后能看到提醒。
2. 审计标记提交后，后续计数会重置。
3. 取消或修改仓库本地阈值后，提示内容会跟着变化。
