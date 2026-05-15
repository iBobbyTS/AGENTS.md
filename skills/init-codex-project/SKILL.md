---
name: init-codex-project
description: Initialize or retrofit a repository with Codex-native workflow files. Use when the user asks to set up, migrate, bootstrap, or dry-run project-level Codex configuration, including AGENTS.md, .codex/config.toml, repo skills in .agents/skills, and optional Linear/Symphony WORKFLOW.md task orchestration.
---

# Init Codex Project

## Overview

Initialize a repository with Codex-native project guidance while keeping global instructions lean. Generate repository guidance at runtime from inspected project facts and user decisions; only optional Linear/Symphony `WORKFLOW.md` is copied from a template by script.

## Workflow

1. Inspect the repository before proposing files.
   - Read `package.json`, existing `AGENTS.md`, `.codex/config.toml`, `.agents/skills/**/SKILL.md`, `.skill/index.md`, `.agent/**`, and `docs/README.md` when they exist.
   - Do not inspect `.skill/legacy/` unless the user explicitly asks.
2. Ask only for missing decisions that affect generated files.
   - The repository's technology stack and execution model: frameworks, package manager, runtime, and whether project work runs in Docker or locally.
   - Whether the project should use Linear/Symphony task orchestration.
   - Documentation preference when the repository has no docs structure: no docs for now, initialize docs, or propose a docs outline. If the user says docs are needed, create `docs/README.md` first and use that document as the source of truth for future documentation-update rules. If the user says docs are not needed, do not create a placeholder docs record.
   - Whether existing non-Codex conventions such as `.skill/index.md` should be migrated, preserved, or ignored.
   - Explicit language and style policies for code, UI copy, code comments, documentation, and Git commit messages. Do not record generic "match existing" guidance; inspect enough to propose concrete policies or ask the user.
   - The UI localization policy during initialization: source/default locale, supported locales, localization framework, message file locations, generation commands, and whether all locales must be updated together. If the project has no UI localization, record that policy instead of deferring the decision.
   - Whether the repository should opt into git-hook-based maintainability audit reminders, and if so how many commits should elapse between audits before the hook reminds the user. Ask for the interval as a number, not as a daily or weekly schedule.
   - Whether the repository will use the explicit audit marker trailer `Maintenance-Audit: true`, so the hook can treat that commit as the latest audit point. If the repository opts in and already has commits, set the initial baseline to the current `HEAD` unless the user says the first reminder should wait for a real audit marker.
3. Generate project guidance directly as the agent.
   - Build proposed `AGENTS.md`, `.codex/config.toml`, and `.agents/skills/<project-skill>/SKILL.md` content from inspected repository facts and the decisions gathered above.
   - Show or explain proposed changes before writing when overwriting existing guidance.
   - Use normal file-editing tools such as `apply_patch` after the user approves generated content.
   - Do not pass commit, localization, documentation, validation, or project-shape decisions through `scripts/init_codex_project.py`.
   - When a repository opts into git-based maintainability reminders, record the local audit cadence in repo config with `git config --local codex.maintainabilityAuditInterval <N>`. If `HEAD` exists and the user did not request an audit-marker-only baseline, also run `git config --local codex.maintainabilityAuditBaseline <current-head-sha>`.
   - Keep the executable hook implementation in the shared user-level hooks directory configured by global `core.hooksPath`. Repository state must stay repository-local through git config and git history; do not store per-repository audit counters in the shared hook directory.
   - The shared hook should be non-blocking and should print a reminder on relevant hookable git state changes. Before the interval is reached, it prints `建议<N>次后进行项目审计。` where `<N>` is the remaining commit count. Once the interval is reached or exceeded, it prints `上次审计是<N>次前，建议尽快安排审计。` where `<N>` is the number of commits since the latest audit marker or baseline.
   - When `docs/README.md` exists or has just been created, place any documentation-update requirement in the repository-level `AGENTS.md`, not in the user-level `~/.codex/AGENTS.md`.
   - If the repository is developed inside Docker, use the appropriate container for project work and do not use local `bun`, `npx`, `python`, or similar runtime commands.
4. Use the bundled script only for optional Linear/Symphony workflow files.
   - Run `scripts/init_codex_project.py --repo <path> --linear --dry-run` only when the user wants Linear/Symphony workflow files.
   - Run `scripts/init_codex_project.py --repo <path> --linear --write` only after the user approves that `WORKFLOW.md` diff.
5. Keep responsibilities separated.
   - Put long-lived repo rules in `AGENTS.md`.
   - Put executable/default configuration in `.codex/config.toml`.
   - Put project-specific reusable workflow detail in `.agents/skills/<project-skill>/SKILL.md`.
   - Put Linear/Symphony task orchestration in `WORKFLOW.md` only when requested.
6. Preserve existing user work.
   - Never overwrite existing files without showing the diff first.
   - When writing, merge with existing project guidance where practical and leave legacy files in place unless the user asks for migration cleanup.

## Generated Files

Generate most files directly at runtime from repository context:

- `AGENTS.md`: long-lived repository rules synthesized from repo facts and user decisions.
- `.codex/config.toml`: stable executable/default configuration only when needed.
- Repository git hook policy: repository-local audit cadence stored in `codex.maintainabilityAuditInterval`, optional repository-local baseline stored in `codex.maintainabilityAuditBaseline`, and no executable hook code inside the repository unless the user explicitly asks for repo-local hooks.
- `.agents/skills/<project-skill>/SKILL.md`: project-specific reusable workflow detail; frontmatter must contain only `name` and `description`.

Use the bundled script only for optional workflow orchestration:

- `scripts/init_codex_project.py`: preview or copy `WORKFLOW.md` when the user explicitly wants Linear/Symphony.
- `assets/WORKFLOW.linear.template.md`: optional Linear/Symphony workflow template.
- `references/codex-official-locations.md`: official file-location map to avoid inventing parallel conventions.

## Project Information To Capture

Capture only facts that are stable and useful across future Codex sessions:

- Languages, frameworks, package manager, runtime, Docker or local-first workflow.
- Explicit language and style policies for code, UI copy, code comments, documentation, and Git commit messages, including Conventional Commits or repository-specific prefixes when applicable.
- Maintainability audit policy for git-hook-based reminders: whether the repository uses reminders, the commit-count interval, and whether the initial baseline is current `HEAD` or the first explicit audit marker.
- Maintainability audit markers, including whether the repo uses `Maintenance-Audit: true` as the explicit latest-audit marker trailer. A newer valid marker supersedes the stored baseline.
- Required test, lint, typecheck, build, browser, and migration verification commands.
- Documentation preference and update rules, especially when `docs/README.md` exists.
- UI localization policy, localization framework, supported languages, message source paths, and generation commands.
- Deployment/runtime providers and local emulation commands.
- Safety-sensitive areas such as data migration, permissions, authentication, and destructive operations.

Do not duplicate Codex platform capabilities such as generic browser automation instructions, built-in subagent descriptions, or skill mechanics. Reference official locations instead.

## Validation

After editing this skill, run:

```bash
python3 /Users/ibobby/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/ibobby/.codex/skills/init-codex-project
python3 /Users/ibobby/.codex/skills/init-codex-project/scripts/init_codex_project.py --repo /path/to/repo --linear --dry-run
```
