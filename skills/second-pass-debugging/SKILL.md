---
name: second-pass-debugging
description: Use when a previous bug fix attempt did not resolve the issue, the user says the bug still happens, a test still fails after one repair round, or Codex is starting a second or later debugging pass. Do not use for the first ordinary bug-fix attempt unless explicitly requested.
---

# Second Pass Debugging

## Overview

Use this skill to stop repeated guess-and-patch debugging. On the second failed attempt, reset to evidence, identify the root cause, make one minimal fix, and verify the original symptom.

## Trigger Discipline

- Use this skill when the user says a previous fix did not work, the same test still fails, the bug still reproduces, or another debugging pass is starting after one unsuccessful attempt.
- Use this skill if the user explicitly asks for systematic debugging or root-cause debugging.
- Do not use this skill for the first ordinary bug-fix pass unless explicitly requested.

## Workflow

1. **Reset to evidence.**
   - State that this is a second-pass debug and that the next step is evidence gathering.
   - Inspect current repository state with `git status` or equivalent when in a git repository.
   - Review the previous attempted fix, changed files, failing command, observed output, and the user's report of what still fails.
   - Treat subagent reports, earlier summaries, and assumptions as untrusted until verified in code, diff, logs, or test output.

2. **Reproduce or preserve the failure.**
   - Run the smallest command or manual flow that demonstrates the bug when environment permits.
   - Read the complete error, stack trace, logs, or UI symptom before proposing a fix.
   - If the issue cannot be reproduced locally, identify what evidence is missing and gather diagnostics instead of guessing.

3. **Trace the root cause.**
   - Check recent diffs and nearby working examples.
   - Follow bad data, incorrect state, or failing control flow backward to its source.
   - For multi-component paths, inspect boundaries: caller to callee, UI to state, API to service, service to persistence, job to worker, or config to runtime.
   - Prefer fixing the source of the incorrect behavior over adding a guard at the symptom.

4. **Compare against known-good patterns.**
   - Search the same codebase for similar working implementations.
   - Compare inputs, state ownership, validation, error handling, async behavior, and cleanup.
   - If the pattern depends on framework behavior or an external API and uncertainty remains, verify against primary documentation or existing local examples.

5. **Form one hypothesis.**
   - Write a concise hypothesis: "Root cause appears to be X because evidence Y."
   - Test the hypothesis with the smallest possible diagnostic or code-reading check.
   - Change only one variable at a time; do not stack speculative fixes.

6. **Add or identify a failing regression surface.**
   - Prefer an automated test that fails for the current bug and verifies real behavior.
   - If no test framework exists, create or describe the smallest repeatable manual or script-based repro.
   - Do not add assertions that only execute code without verifying the broken behavior.

7. **Implement the minimal fix.**
   - Fix the confirmed root cause.
   - Avoid unrelated refactors, broad rewrites, new compatibility layers, or hidden fallback logic.
   - If the direct fix would worsen an oversized module, unclear state owner, fragile state machine, or under-tested core path, pause and explain the smallest enabling refactor before editing.

8. **Verify before claiming progress.**
   - Re-run the original failing command or repro.
   - Run relevant tests, type checks, lint, build, or browser validation as appropriate for the changed behavior.
   - Report exact commands and results. If checks cannot run, state the blocker and the remaining verification needed.

9. **Escalate after repeated failures.**
   - If this pass fails, return to evidence gathering with the new result instead of layering another fix.
   - After three unsuccessful fix attempts for the same symptom, stop and reassess architecture, state ownership, concurrency, stale assumptions, or test validity with the user before trying another implementation.

## Subagent Use

- Use a subagent only for bounded, independently verifiable investigation such as tracing a call chain, comparing similar implementations, or triaging test output.
- The main agent owns the hypothesis, final fix, diff review, and verification.
- Do not delegate high-risk architecture, data deletion, migrations, security decisions, or release decisions.
