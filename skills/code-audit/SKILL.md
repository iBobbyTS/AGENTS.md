---
name: code-audit
description: "Use when Codex is asked to perform or finish a full codebase audit, architecture audit, technical-debt audit, maintainability audit, security audit, over-engineering/de-bloat audit, or audit of an AI-assisted or AI-generated codebase. Focus on traditional engineering risks plus AI-agent failure modes such as local-optimum patches, duplicated abstractions, over-mocked tests, fragile fallbacks, unnecessary dependencies, and unreviewed generated logic. After an audit is complete, any commit that records the audit result must include the commit-message trailer `Maintenance-Audit: true`."
---

# Code Audit

Perform a full-system audit. Do not treat this as a pre-change refactoring gate; this skill is for periodic or requested audits of the current codebase state.

For AI-agent-specific risks, ground the audit in current official product behavior, current repository configuration, and observed code. Do not rely on stale folklore about older model limitations unless the repository still shows that failure mode.

## Language And Formatting

- `FULL.md` must be written in English and is the agent-facing audit ledger.
- `REPORT.md` must be written in Chinese and is the user-facing audit report.
- 保留文件路径、代码符号、命令名、错误信息和证据原文，不要翻译它们。
- `Maintenance-Audit: true` 这个 commit trailer 必须保持英文原样，不要翻译。

## Persistent Audit Artifacts

For non-trivial audits, persist progress under `.agent-work/audit/` so the audit can survive context compression and be resumed without rereading already-reviewed code.

### Artifact Setup

After a quick repository survey, create one timestamped audit directory:

```text
.agent-work/audit/{YYYYMMDD-HHMM}/
├── FULL.md
└── REPORT.md
```

Also create `.agent-work/audit/CURRENT.md` while the audit is in progress.

- `CURRENT.md` must point to the active timestamped audit directory and report file.
- At the beginning, `CURRENT.md` only needs a coarse module/component outline from the initial survey.
- As larger modules are audited, expand `CURRENT.md` with smaller submodules and update progress.
- Delete `CURRENT.md` after `REPORT.md` is complete.
- If continuing an interrupted audit, read `CURRENT.md` first, then read the referenced `FULL.md` before reviewing more code or reporting completion.

### FULL.md Ledger

Use `FULL.md` as the complete audit ledger. After each module, component, workflow, or similarly reasonable review unit, append the result immediately before moving on.

Start `FULL.md` with a compact progress index:

```markdown
| Area | Status | Severity | Files | Notes |
| --- | --- | --- | --- | --- |
| Auth middleware | Reviewed | Must Fix | src/auth/* | Object-level permission gap |
| Settings UI | Reviewed | No Action | app/settings/* | State and layout reviewed |
```

For every reviewed area, record:

- Module, component, workflow, or subsystem name.
- Status: `Reviewed`, `Partial`, `Skipped`, or `Needs Follow-up`.
- Severity: `Must Fix`, `Should Plan`, `Track as Debt`, or `No Action`.
- Scope: relevant file paths, symbols, API routes, commands, workflows, and line ranges where useful.
- Focus: audit concerns inspected, such as permissions, state flow, concurrency, reliability, release safety, tests, architecture, tooling, agent harnesses, MCP/connectors, agent memory/state, or UI states.
- Evidence: concrete code references, command outputs, test results, or observed behavior.
- Verification: tests/checks run or manual verification still needed.
- Gaps / Assumptions: unreviewed paths, missing evidence, or unsupported assumptions.

Only areas with real findings need repair-oriented details:

- Finding description.
- Trigger or failure path.
- Impact.
- Recommended priority.
- Suggested fix direction.

For `No Action` areas, do not invent findings, triggers, impact, or fix recommendations. Record the reviewed scope, focus, evidence, verification, and any remaining gaps.

### REPORT.md

Generate `REPORT.md` only after rereading `FULL.md`. The final report must be written in Chinese. It should extract and prioritize actionable findings, preserve audit coverage and limitations, and include assumptions, human-review needs, and verification gaps. Do not rely on conversation memory as the source of the final report.

## Project Audit Profile

Before a non-trivial audit, look for a project-specific audit profile in this order:

1. `docs/audit-profile.md`
2. `AUDIT_PROFILE.md`
3. `.agent-work/audit/PROFILE.md`

If a profile exists, read it before creating the timestamped audit directory and use it as the stable baseline for scope, sampling, risk ranking, and required coverage. The profile sets minimum coverage, not a ceiling: still follow evidence, user instructions, and newly discovered risks.

If no profile exists, read `references/audit-profile-template.md`, copy its template into `docs/audit-profile.md` when project docs are versioned and repo rules allow it; otherwise copy it into `.agent-work/audit/PROFILE.md` as a draft. Then ask the user to define or approve the unknown fields before proceeding beyond the initial survey. If the user asks to continue immediately, mark the profile `Draft`, proceed with explicit assumptions, and list the missing profile decisions in `REPORT.md`.

Do not put feature requirements or implementation plans in the profile. It should define audit direction: system class, risk tolerance, quality attributes, control baselines, required evidence, and sampling rules.

Read `references/audit-profile-template.md` only when creating, updating, or explaining an audit profile. Do not load the template for every audit when a project profile already exists.

## General Audit Areas

### Audit Framing and Sampling

- Start from the project audit profile, then identify any missing business-critical workflows, crown-jewel data, external trust boundaries, expensive failure modes, owners, operational history, and recent high-churn areas.
- Define quality attributes before judging architecture: correctness, security, reliability, modifiability, performance, operability, portability, and cost. Record which attributes matter most for this system.
- Use scenario-based architecture review for important systems: for each high-risk scenario, describe the stimulus, environment, expected response, architectural decisions involved, tradeoffs, and evidence.
- Sample beyond files that look complex. Include public entry points, auth/permission gates, persistence boundaries, migrations, integration points, background jobs, release paths, observability, and rollback paths.
- Rank findings by user/business impact, exploitability or likelihood, blast radius, reversibility, evidence strength, and whether the issue is systemic or isolated.

### Structure and Module Boundaries

- Identify god objects, oversized files, long functions, deeply nested branching, and modules with unclear ownership.
- Check whether dependency direction, layering, and boundaries match the existing architecture.
- Look for duplicate helpers, parallel abstractions, and bypasses around established service, component, or utility layers.
- Check for consistency drift: three or more same-purpose implementations, undocumented reusable entry points, or code that bypasses documented project conventions for shared behavior.
- Check ownership, extension points, API stability, dependency cycles, and whether architecture decisions are captured in code, ADRs, docs, or tests.
- Flag AI-generated patterns that solve a local problem by adding more in-place logic instead of reusing or extending the architecture.

### Functional Correctness

- Review core user workflows, business rules, edge cases, error paths, retries, and empty states.
- Check whether recent features regress older behavior.
- Look for implementations that run successfully but encode the wrong product or domain semantics.
- Trace critical invariants from input validation through domain logic, persistence, side effects, and user-visible output.
- Check backward compatibility, versioned contracts, import/export behavior, and how partial failure affects user or data state.

### UI and UX

- Review layout, responsiveness, accessibility, loading states, empty states, error states, and disabled/submitting/selected interaction states.
- Check for visual or interaction-style drift introduced by incremental AI changes.
- Flag pages where new controls or panels were stacked onto the UI without preserving information architecture.

### Data and State Management

- Review schemas, migrations, default values, validation boundaries, cache invalidation, persistence, and derived state.
- Check whether there is a single source of truth for important state.
- Flag duplicated state, stale cached data, inconsistent normalization, and validation that only happens in the UI or caller.
- Check data classification, retention, deletion, audit logs, backup/restore assumptions, privacy boundaries, and irreversible data transformations.

### Concurrency, Async, and Thread Safety

- Review race conditions, cancellation, re-entrancy, stale responses overwriting newer state, duplicate submissions, and task cleanup.
- Check timers, subscriptions, streams, workers, background jobs, locks, transactions, and idempotency boundaries.
- Flag state machines that became less predictable because fixes added more flags instead of clarifying transitions.

### Data Security and Permissions

- Review authentication, authorization, tenant isolation, object-level permissions, input validation, output encoding, file paths, external URLs, and command execution.
- Check whether secrets, tokens, personal data, or sensitive business data can leak through logs, errors, caches, telemetry, generated files, frontend bundles, or agent/tool output.
- Check secure-by-default behavior, threat models, abuse cases, attack surface reduction, least privilege, defense in depth, vulnerability disclosure/response, and whether security requirements are traced into implementation and tests.
- Review dependency, script, network, and supply-chain risks introduced by agentic development.

### Release, Operations, and Reliability

- Review deployment topology, environment separation, configuration, feature flags, database migration sequencing, backward/forward compatibility, rollback, and emergency-disable paths.
- Check whether critical services define SLOs or equivalent reliability targets, error budgets or release risk policies, and user-facing indicators for availability and correctness.
- Audit observability for the highest-risk workflows: logs, metrics, traces, dashboards, alert quality, latency, traffic, errors, saturation, and whether alerts map to actionable runbooks.
- Review backups, restores, disaster recovery, idempotency, retry policies, queue recovery, rate limits, backpressure, graceful degradation, and incident-response evidence.

### Performance, Capacity, and Cost

- Review bottlenecks, query plans, N+1 patterns, pagination, batch sizes, cache behavior, payload sizes, cold starts, memory/CPU growth, and third-party latency.
- Check whether load assumptions, benchmarks, limits, budgets, and capacity plans match observed or expected usage.
- Flag performance fixes that trade away correctness, security, maintainability, or operability without explicit evidence.

### Software Supply Chain and Build Integrity

- Review direct and transitive dependencies, lockfiles, unsupported runtimes, licenses, vendored code, generated code, package scripts, and build-time network access.
- Check whether releases have reproducible or traceable build provenance, artifact integrity, SBOM or dependency inventory where appropriate, and a process for dependency vulnerability response.
- Audit CI/CD permissions, artifact signing, release promotion, environment secrets, protected branches/tags, and whether build outputs can be tampered with after review.

### Test and Validation Quality

- Check whether tests verify real behavior rather than implementation details or smoke execution.
- Flag over-mocking that hides integration failures.
- Review coverage of happy paths, failure paths, edge cases, permissions, migrations, concurrency, integration boundaries, rollback/recovery, performance-critical paths, and UI states.
- Check the test portfolio balance: fast unit tests for local logic, integration tests for contracts and persistence, and end-to-end or system tests for critical user workflows.
- Check CI, linting, type checks, browser/UI validation, and flaky-test risks.
- Check whether agent-authored or auto-fix changes weakened validation by deleting negative tests, narrowing fixtures, disabling scanners, skipping flaky-but-important checks, or moving high-risk checks outside required CI.
- Treat a clean AI review, scanner result, or agent self-review as one signal in a layered verification system, not as proof that the codebase is safe.

### Maintainability and Evolution Risk

- Identify hotspots where future changes require understanding too many unrelated modules.
- Review naming, comments, documentation, and domain intent.
- Review ownership, onboarding path, ADRs, runbooks, architectural diagrams, public contracts, and whether comments explain durable intent rather than stale implementation details.
- Assess whether current boundaries can support the next likely features without concentrated risk.
- Separate acceptable local complexity from structural debt that will compound.
- Check whether high-velocity agent work has left areas that no maintainer can explain from repo-local docs, tests, and code history. Classify this as maintainability risk when future humans or agents cannot safely extend the area.

### AI-Assisted Development Artifacts

- Look for duplicated patterns, duplicated components, repeated utility functions, and near-identical tests created by local prompting.
- Flag local patch drift where a feature adds a second formatter, chart layer, state owner, request/error handler, or similar shared concern instead of extending an existing or documented path.
- Flag brittle logic that appears optimized to pass current tests rather than express the intended behavior.
- Review plausible but unverified fallbacks, compatibility layers, swallowed errors, invented configuration keys, environment variables, or conventions.
- Check whether generated code introduced broad permissions, hidden data movement, or unreviewed external assumptions.
- Measure quality beyond pass/fail: code reuse, redundant files, dependency count, public API growth, complexity/churn hotspots, and whether repeated agent changes make the next change easier or harder.
- Check whether agents repeatedly copied a weak pattern because it already existed. If so, recommend codifying the intended rule in docs, tests, linting, generators, or cleanup tasks rather than fixing only one instance.
- Flag agent-friendly but system-hostile code: verbose scaffolding that improves local legibility while obscuring ownership, compatibility branches that are never exercised, and generated docs or plans that no longer match executable behavior.

### Agent-First Repository Knowledge

- Audit `AGENTS.md`, skills, rules, prompts, planning docs, architecture docs, and generated reference files as part of the system when agents use them to make changes.
- Prefer a short agent entry point that routes to maintained sources of truth over a large instruction file that mixes stale rules, product intent, and task-specific history.
- Check whether repository knowledge is versioned, discoverable, cross-linked, and mechanically refreshed when code changes.
- Flag stale agent instructions, obsolete plans, undocumented conventions, and external knowledge that agents rely on but cannot inspect from the repository.
- Check whether generated reports, plans, diagrams, and summaries are clearly separated from authoritative docs and excluded from production artifacts when appropriate.

### Agentic Security and Autonomy

- Build or verify a project-specific threat model before prioritizing security findings: assets, trust boundaries, untrusted inputs, privileged actions, data flows, and realistic attacker paths.
- Audit AI-agent identities, service accounts, CI tokens, workflow permissions, approval modes, sandbox profiles, network allowlists, and human-in-the-loop gates. Agent identities should be separate from developer identities, scoped, revocable, and auditable.
- Treat sandboxing, model-based approval classifiers, AI reviewers, and secret scanners as defense-in-depth layers. Flag configurations where any one layer is treated as sufficient for destructive commands, production data, deployments, or secrets.
- Check for prompt-injection and cross-domain instruction risks wherever agents read untrusted content: issue bodies, PR comments, docs, webpages, tool output, logs, emails, support tickets, generated files, or third-party MCP responses.
- Review MCP servers, plugins, skills, hooks, browser tools, local control planes, and remote connectors for source trust, version pinning, least privilege, egress controls, tool allowlists, command execution, and secret exposure.
- Check whether local control planes, loopback services, browser extensions, sockets, and webhooks require authentication and authorization before executing file, process, network, or deployment actions.
- Do not trust `localhost`, same-origin, or developer-machine access as a security boundary when an agent can browse untrusted content or execute code on the same host.
- Flag agent workflows that can modify their own permissions, rules, hooks, CI gates, review requirements, or security scanners without separate human review.

### Agent Evaluation and Observability

Use this section when the repository builds, configures, or operates agents, agent hooks, security bots, code-review bots, or automation templates.

- Check whether the project defines success criteria for agent behavior beyond task completion: "does not break existing behavior", "does what was asked", "keeps security invariants", and "keeps maintainability within budget".
- Audit evals, regression suites, model-upgrade gates, transcript review, production monitoring, and human calibration for agent workflows. Flag agent changes that ship without a baseline or rollback signal.
- Check whether agent logs, traces, transcripts, memory, and stored findings are retained long enough for debugging but scrubbed of secrets and personal data.
- Review deduplication, suppression, snooze, and memory mechanisms for security or quality findings. Flag systems where an agent can permanently hide a finding without accountable human review.
- Verify that agent-generated PRs, patches, or remediation tasks pass the same required checks as human changes and cannot mark themselves complete solely through their own summary.

### Ponytail-Derived Anti-Bloat Focus

Use this focus when the audit request mentions over-engineering, bloat, de-bloat, unnecessary complexity, unnecessary dependencies, "what can we delete", YAGNI, or a repo/module getting too large.

When this focus applies, read `references/anti-bloat.md` before the simplification pass and use its ladder, tags, source discipline, and safety boundaries in `FULL.md` and `REPORT.md`.

## Agent Verification

### Repository Reality Check

Before reporting audit completion, the agent must verify the current repository state directly.

- Run or inspect the equivalent of `git status`.
- Review relevant staged, unstaged, and recent committed diffs.
- Confirm which files were actually changed, added, deleted, or left untouched.
- Do not rely on previous task summaries, implementation-agent claims, or stale conversation context as proof.
- If the repository state contradicts the previous plan or agent summary, treat the repository state as authoritative.

### Evidence Discipline

Every finding must include concrete evidence where possible.

- Prefer file paths, function names, class names, API routes, migrations, tests, commands, and observed outputs.
- Mark unsupported claims as assumptions.
- Mark missing evidence as an audit gap.
- Do not claim that a workflow, test, migration, or UI state works unless it was inspected or run.
- Do not claim that a previous agent completed work unless the result is visible in code, tests, logs, or git history.

### Stale State and Context Drift

Check for signs that previous AI-agent work was based on stale assumptions.

- Reports mention files that no longer exist.
- Completion summaries do not match the current diff.
- Tests were described as passing but no command output or CI result is available.
- Old architectural assumptions remain in comments, docs, prompts, or generated reports.
- The code contains compatibility layers, fallbacks, or flags added to preserve behavior that no longer exists.

Classify stale-state findings as:
- `Must Fix` if they affect runtime behavior, security, migrations, data correctness, or deployment.
- `Should Plan` if they mainly affect maintainability, documentation, or developer understanding.
- `Track as Debt` if they are harmless but should be removed later.

### Agent-Generated Code Smell Detection

Look specifically for patterns commonly introduced by AI coding agents.

- Near-duplicate helpers, components, services, schemas, or tests.
- Parallel abstractions that solve the same problem in different places.
- Generic fallback logic that hides real errors.
- Broad `try/catch` blocks that swallow failures.
- Configuration keys, environment variables, or conventions that are invented but undocumented.
- Comments that explain intent but do not match the implementation.
- Tests that validate mocks rather than real behavior.
- Code that appears optimized to satisfy current tests rather than express domain logic.
- Large rewrites that replace working architecture without clear justification.

### Independent Verification Pass

The agent must perform an independent verification pass after reviewing implementation details.

- Re-run available tests when feasible.
- Inspect failing, skipped, or newly added tests.
- Check whether tests cover real integration boundaries, not only mocked behavior.
- Review the highest-risk workflows end to end from entry point to persistence or output.
- Verify migrations, background jobs, permissions, and destructive operations with extra scrutiny.
- If tests cannot be run, state why and list the manual or CI checks still required.

### Subagent Audit Prompting

When the main agent asks a subagent to perform an independent audit pass, pass only:

```text
Audit {working path}, [$code-audit]({user home dir}/.codex/skills/code-audit/SKILL.md)
```

Do not pass extra instructions, summaries, suspected issues, expected focus areas, prior conclusions, or main-agent analysis unless the user explicitly specifies them. Keep the subagent prompt minimal to maximize independent variation and increase the chance of finding different latent issues.

### Simplification Pass

After identifying findings, the agent must check whether complexity can be reduced.

- Identify code that can be deleted.
- Identify duplicated logic that can be merged.
- Identify new abstractions that should instead reuse existing layers.
- Check for premature abstraction as well as duplication: when similar logic appears fewer than three times and does not affect high-risk semantics such as permissions, APIs, time/date, money, units, persistence, or error handling, avoid recommending a shared helper solely for tidiness.
- Identify fallback or compatibility code that should be removed rather than preserved.
- Prefer smaller, reversible fixes over broad rewrites.

### Agent Runtime and Tooling Audit

When the repository includes agent configuration, automation scripts, MCP setup, CI scripts, or development tooling, audit them as part of the system.

- Apply the agentic security checks above to tooling as shipped infrastructure, not merely developer convenience.
- Check whether scripts, generated reports, plans, and temporary files can leak secrets or enter production bundles.
- Check whether tool configuration is documented enough for another developer to reproduce the workflow.


## Output Format for `REPORT.md`

### 审计验证
- 仓库状态已检查：是/否，附证据。
- 差异已审阅：是/否，附范围。
- 审计范围与抽样依据：覆盖的模块、入口、数据流、运行/发布路径，以及未覆盖原因。
- 关键质量属性：本次按哪些属性排序风险，例如正确性、安全、可靠性、可维护性、性能、运维性、成本。
- 已运行测试：命令、结果与限制。
- 未运行测试：原因。
- 已检查高风险流程。
- 已检查发布/回滚/观测/恢复路径。
- 假设。
- 需要人工复核。
- 已知过时上下文或冲突证据。
除非修复在代码中可见且有验证证据支持，否则不要把某个发现标记为已解决。

### 主要发现
先列出发现，按严重性排序。能给出具体文件引用时就给出。将每个发现归类为以下之一：

- `必须修复`：安全问题、数据丢失/损坏风险、严重功能错误，或已经阻碍可靠开发的结构性问题。
- `需要规划`：有意义的技术债、测试缺口、可维护性热点，或不紧急但应排期处理的设计风险。
- `记录为技术债`：可接受的短期折中，但需要负责人、触发条件或后续标记。
- `无需处理`：就当前项目规模和风险画像而言，已审阅区域是合理的。

补充一段简短总结，说明系统整体健康状况、最稳固的部分、最高风险区域，以及下一轮建议审计的重点。

### 风险排序依据
简要说明本报告如何按业务影响、用户影响、数据/资金/安全风险、发生概率、爆炸半径、可逆性、证据强度、系统性程度和修复成本排序。不要只按代码行数、文件大小或主观代码味道排序。

When committing completed audit work, include this trailer exactly once in the commit message:

```text
Maintenance-Audit: true
```
