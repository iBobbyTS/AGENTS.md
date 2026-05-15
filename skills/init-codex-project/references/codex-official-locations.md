# Codex Official Locations

Use these locations when initializing repositories. Do not invent parallel index files.

## User Scope

- User instructions: `~/.codex/AGENTS.md` or `$CODEX_HOME/AGENTS.md`.
- User override instructions: `~/.codex/AGENTS.override.md` when intentionally replacing normal personal instructions.
- User config: `~/.codex/config.toml` or `$CODEX_HOME/config.toml`.
- User subagents: `~/.codex/agents/*.toml` only for cross-project roles that are stable and worth keeping globally.
- User skills: `~/.codex/skills/<skill>/SKILL.md` in the Codex app environment; official docs may also refer to `$HOME/.agents/skills` for app-level skills.

## Repository Scope

- Repository instructions: `<repo>/AGENTS.md`.
- Nested repository instructions: `<subdir>/AGENTS.md` or `<subdir>/AGENTS.override.md` when a subtree needs tighter rules.
- Repository config: `<repo>/.codex/config.toml`.
- Repository subagents: `<repo>/.codex/agents/*.toml` only when built-in agents are insufficient.
- Repository skills: `<repo>/.agents/skills/<skill>/SKILL.md`.
- Optional orchestration workflow: `<repo>/WORKFLOW.md` when using Symphony-style task orchestration.

## Placement Rules

- Keep personal preferences global.
- Keep project facts in repo files.
- Keep long procedures in skills or references, not in global instructions.
- Keep Symphony/Linear task orchestration optional; do not create `WORKFLOW.md` unless requested.
