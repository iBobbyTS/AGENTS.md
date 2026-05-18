---
name: receiving-code-review
description: Use when reviewing a pull request, GitHub/GitLab code review, or external reviewer feedback to decide whether it can merge or how to respond. Do not use for subagent review results. This skill evaluates and reports; it does not directly implement fixes.
---

# Receiving Code Review

## Overview

Use this skill to evaluate PR feedback and external review comments with technical rigor. The goal is to decide whether the PR can merge, what must change if it cannot, and what message the user should send.

## Trigger Discipline

- Use this skill for pull requests, GitHub/GitLab review comments, external reviewer feedback, requested-changes reviews, approval decisions, and merge-readiness checks.
- Do not use this skill for subagent review results; those are handled by the main agent's normal verification and integration workflow.
- Do not implement fixes while using this skill. Report, draft messages, and ask the user how to proceed.
- Do not commit, push, merge, approve, request changes, or post comments unless the user explicitly asks.

## Workflow

1. **Collect the review surface.**
   - Identify the PR, branch, base branch, review comments, requested changes, CI/check status, and changed files.
   - Prefer official connector or `gh` data when available. If using local git, inspect `git status`, `git diff`, and relevant commit range.
   - Read unresolved inline comments in their code context, not just the comment text.

2. **Understand the intent of each comment.**
   - Restate the technical requirement behind each actionable comment.
   - Separate blockers from suggestions, questions, style nits, and reviewer misunderstandings.
   - If a comment is ambiguous enough to cause the wrong action, mark it as needing clarification.

3. **Verify against codebase reality.**
   - Check whether each comment is technically correct for this repository, framework, runtime, and product behavior.
   - Look for existing patterns, compatibility requirements, tests, docs, or prior decisions that support or contradict the comment.
   - Check whether the suggested change would break existing behavior, overbuild unused functionality, duplicate logic, or violate the user's project rules.

4. **Assess merge readiness.**
   - Treat the PR as **not mergeable** if there are unresolved correctness, security, data loss, permission, migration, build, test, or requested-changes issues.
   - Treat maintainability/test gaps as blockers when they affect changed behavior or create meaningful future risk.
   - Treat pure style, minor wording, optional cleanup, or non-actionable preference comments as non-blocking unless repository policy says otherwise.
   - Do not claim checks pass unless current CI or local command output was inspected.

5. **If the PR can merge, report first.**
   - Tell the user the PR appears mergeable and give the evidence: comments reviewed, checks inspected, risks remaining, and assumptions.
   - Draft a concise user-readable message they can use for approval or merge notes.
   - Do not merge or approve until the user explicitly asks.

   Suggested format:

   ```markdown
   结论：可以合并。

   依据：
   - 已检查的 review/CI/diff 范围
   - 没有发现阻塞项
   - 剩余风险或假设

   可发送消息：
   <draft approval or merge note>
   ```

6. **If the PR cannot merge, explain the blockers.**
   - Lead with blocking issues, ordered by severity.
   - For each issue, include file/comment reference when available, what is wrong, why it matters, and the smallest acceptable fix.
   - Separate "must fix before merge" from "can follow up later".
   - If a reviewer appears wrong, explain the evidence and draft a respectful technical reply.

7. **Ask the user for the response path.**
   - If fixes are needed, ask whether to comment back for the PR submitter to change it or directly make the changes locally.
   - If direct changes are requested later, leave this skill and follow normal implementation rules, including tests and verification.

   Suggested question:

   ```markdown
   这个 PR 目前不建议合并。你希望我：
   1. 写 review comments 让 PR 提交者修改
   2. 直接在本地改这些问题
   ```

## Output Requirements

- Always include a clear merge decision: `可以合并`, `不建议合并`, or `证据不足，暂不能判断`.
- Always distinguish verified facts from assumptions.
- Always include the exact checks or evidence inspected.
- Never performative-agree with review comments. Verify them first.
- Never silently ignore an unresolved requested-change thread.
