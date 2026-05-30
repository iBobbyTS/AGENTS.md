---
name: manual-git-worktrees
description: Use only when the user explicitly asks to create or use an isolated git worktree. Coordinate active-agent scope files under `.worktrees/current-agents/`, set up a `.worktrees/` workspace, verify existing isolation first, ensure `.worktrees/` is ignored before creation, and report whether the ignore rule was committed. Do not use automatically for ordinary implementation, debugging, or planning.
---

# Manual Git Worktrees

Use this skill only when explicitly invoked.

## Workflow

1. Detect existing isolation first.
   - Run `git rev-parse --show-toplevel`, `git rev-parse --git-dir`, `git rev-parse --git-common-dir`, `git rev-parse --show-superproject-working-tree`, and `git branch --show-current`.
   - If already in a linked worktree, report the current path and branch and stop.
   - If inside a submodule, treat it as a normal checkout.

2. Check active-agent scope conflicts before writing any new scope file.
   - Use `.worktrees/current-agents/` at the repository root as the active-agent registry.
   - Before creating or modifying any registry file, read every existing `*.md` file under `.worktrees/current-agents/`.
   - If `.worktrees/current-agents/` does not exist, treat it as no active-agent registry entries.
   - Estimate the current task scope before registration: intended goal, likely modules/components/workflows, and expected files or path patterns that may be modified.
   - Compare the estimated scope against every existing registry entry.
   - Treat overlapping files, overlapping path patterns, shared ownership boundaries, migrations/schema changes, shared state, routing, build/config files, or unclear ownership as a conflict.
   - If a conflict is found before starting, stop immediately. Tell the user which registry file/task conflicts, what scope overlaps, and recommend starting this task after the conflicting task finishes.
   - If a conflict appears later because the task scope changes, stop immediately with the same conflict report.
   - Ignore only the extreme race where two agents read the registry at the same time before either writes.

3. Choose the worktree location.
   - Use `.worktrees/` at the repository root.
   - Create one branch per task with a short, task-specific branch name.

4. Ensure `.worktrees/` is ignored before creating anything under `.worktrees/`.
   - Check whether `.gitignore` already ignores `.worktrees/`.
   - If not, add `.worktrees/` to `.gitignore` first.
   - If the repo has no other dirty paths, stage and commit that single ignore change.
   - If the repo already has other modified files, keep the `.gitignore` change uncommitted and report it.
   - Do not create the worktree until the ignore rule exists in the repo checkout you are using.

5. Register this task after the conflict check passes.
   - Create `.worktrees/current-agents/` if needed.
   - Create one Markdown file named after the task goal, for example `.worktrees/current-agents/fix-login-timeout.md`.
   - If the natural filename already exists, add a short unique suffix rather than overwriting it.
   - Record enough detail for another agent to detect conflicts:
     - Task goal.
     - Expected scope and non-goals.
     - Expected files, directories, modules, routes, schemas, config files, or workflows that may be modified.
     - Current branch and planned worktree path.
     - Start time.
   - If the task goal or implementation scope changes materially, update this file before continuing work.

6. Create the worktree.
   - Prefer any native worktree helper exposed by the environment.
   - Otherwise use `git worktree add` under `.worktrees/`.

7. Verify the new workspace.
   - Run the repo's normal setup or baseline checks only as needed to confirm the isolated workspace is usable.
   - If the baseline is already failing, report that before continuing with feature work.

8. Report the result.
   - Include the full worktree path, branch name, ignore-rule status, and baseline status.
   - Do not switch into implementation mode unless the user asked for it in the same request.

9. Clean up the active-agent registry entry during wrap-up.
   - Delete only the registry Markdown file created for this task.
   - Do this when the task is complete, abandoned, or blocked before handing control back to the user.
   - If waiting for another active agent is required, report the conflict and end the response instead of keeping the task open.
