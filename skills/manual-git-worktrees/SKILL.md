---
name: manual-git-worktrees
description: Use only when the user explicitly asks to create or use an isolated git worktree. Set up a `.worktrees/` workspace, verify existing isolation first, ensure `.worktrees/` is ignored before creation, and report whether the ignore rule was committed. Do not use automatically for ordinary implementation, debugging, or planning.
---

# Manual Git Worktrees

Use this skill only when explicitly invoked.

## Workflow

1. Detect existing isolation first.
   - Run `git rev-parse --git-dir`, `git rev-parse --git-common-dir`, `git rev-parse --show-superproject-working-tree`, and `git branch --show-current`.
   - If already in a linked worktree, report the current path and branch and stop.
   - If inside a submodule, treat it as a normal checkout.

2. Choose the worktree location.
   - Use `.worktrees/` at the repository root.
   - Create one branch per task with a short, task-specific branch name.

3. Ensure `.worktrees/` is ignored before creating anything.
   - Check whether `.gitignore` already ignores `.worktrees/`.
   - If not, add `.worktrees/` to `.gitignore` first.
   - If the repo has no other dirty paths, stage and commit that single ignore change.
   - If the repo already has other modified files, keep the `.gitignore` change uncommitted and report it.
   - Do not create the worktree until the ignore rule exists in the repo checkout you are using.

4. Create the worktree.
   - Prefer any native worktree helper exposed by the environment.
   - Otherwise use `git worktree add` under `.worktrees/`.

5. Verify the new workspace.
   - Run the repo's normal setup or baseline checks only as needed to confirm the isolated workspace is usable.
   - If the baseline is already failing, report that before continuing with feature work.

6. Report the result.
   - Include the full worktree path, branch name, ignore-rule status, and baseline status.
   - Do not switch into implementation mode unless the user asked for it in the same request.
