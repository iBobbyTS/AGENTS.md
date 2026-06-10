---
name: second-pass-debugging
description: Use when a previous bug fix attempt did not resolve the issue, the user says the bug still happens, a test still fails after one repair round, Codex is starting a second or later debugging pass, or a debugging session is long/repetitive enough to need persistent state across context compaction. Also use when the user asks for systematic debugging, root-cause debugging, or durable debug notes in .agent-work/debug/. Do not use for the first ordinary bug-fix attempt unless explicitly requested or the session is already becoming long-running.
---

# Second Pass And Persistent Debugging

## Overview

Use this skill to stop repeated guess-and-patch debugging. On the second failed attempt, or when debugging becomes long-running, reset to evidence, persist useful state, identify the root cause, make one minimal fix, and verify the original symptom.

## Trigger Discipline

- Use this skill when the user says a previous fix did not work, the same test still fails, the bug still reproduces, or another debugging pass is starting after one unsuccessful attempt.
- Use this skill if the user explicitly asks for systematic debugging or root-cause debugging.
- Use this skill for long debugging sessions, repeated experiments, or situations where context compaction may cause loss of important observations.
- Do not use this skill for the first ordinary bug-fix pass unless explicitly requested or the work is already clearly becoming long-running.

## Persistent Debug State

Use `.agent-work/debug/` only for debugging state that can save future work. Keep it concise and evidence-based.

Expected structure:

```text
.agent-work/debug/
├── INDEX.md
├── active/
├── unresolved/
└── resolved/
```

`INDEX.md` should contain three two-column tables:

```md
## Active

| file | summary |
| --- | --- |

## Unresolved

| file | summary |
| --- | --- |

## Resolved

| file | summary |
| --- | --- |
```

- Put the current investigation in `active/`.
- Move paused or still-failing investigations to `unresolved/`.
- Move verified fixes to `resolved/`.
- In each table, `file` is the relative note path and `summary` explains why a future agent should read it.
- Before continuing the same problem, read `INDEX.md` and the relevant `active/` or `unresolved/` note.
- When a resolved debug session produces reusable project knowledge, record the general practice in the appropriate project documentation such as `docs/engineering-notes/`. Keep the debug note as the concrete evidence chain.

## Workflow

1. **Reset to evidence.**
   - State that this is a second-pass debug and that the next step is evidence gathering.
   - Inspect current repository state with `git status` or equivalent when in a git repository.
   - Review the previous attempted fix, changed files, failing command, observed output, and the user's report of what still fails.
   - Treat subagent reports, earlier summaries, and assumptions as untrusted until verified in code, diff, logs, or test output.

2. **Recover or create persistent debug state.**
   - If `.agent-work/debug/INDEX.md` exists, read it before repeating investigation.
   - If this is a long-running or repeated investigation, create or update one `active/` note and add it to `INDEX.md`.
   - Record only confirmed observations, failed approaches, current hypothesis, next diagnostic, and relevant commands or manual repro steps.

3. **Reproduce or preserve the failure.**
   - Run the smallest command or manual flow that demonstrates the bug when environment permits.
   - Read the complete error, stack trace, logs, or UI symptom before proposing a fix.
   - If the issue cannot be reproduced locally, identify what evidence is missing and gather diagnostics instead of guessing.

4. **Trace the root cause.**
   - Check recent diffs and nearby working examples.
   - Follow bad data, incorrect state, or failing control flow backward to its source.
   - For multi-component paths, inspect boundaries: caller to callee, UI to state, API to service, service to persistence, job to worker, or config to runtime.
   - Prefer fixing the source of the incorrect behavior over adding a guard at the symptom.

5. **Compare against known-good patterns.**
   - Search the same codebase for similar working implementations.
   - Compare inputs, state ownership, validation, error handling, async behavior, and cleanup.
   - If the pattern depends on framework behavior or an external API and uncertainty remains, verify against primary documentation or existing local examples.

6. **Form one hypothesis.**
   - Write a concise hypothesis: "Root cause appears to be X because evidence Y."
   - Test the hypothesis with the smallest possible diagnostic or code-reading check.
   - Change only one variable at a time; do not stack speculative fixes.
   - Update the active debug note when the hypothesis changes.

7. **Add or identify a failing regression surface.**
   - Prefer an automated test that fails for the current bug and verifies real behavior.
   - If no test framework exists, create or describe the smallest repeatable manual or script-based repro.
   - Do not add assertions that only execute code without verifying the broken behavior.

8. **Implement the minimal fix.**
   - Fix the confirmed root cause.
   - Avoid unrelated refactors, broad rewrites, new compatibility layers, or hidden fallback logic.
   - If the direct fix would worsen an oversized module, unclear state owner, fragile state machine, or under-tested core path, pause and explain the smallest enabling refactor before editing.

9. **Verify before claiming progress.**
   - Re-run the original failing command or repro.
   - Run relevant tests, type checks, lint, build, or browser validation as appropriate for the changed behavior.
   - Report exact commands and results. If checks cannot run, state the blocker and the remaining verification needed.
   - If the fix is verified, move the debug note from `active/` to `resolved/` and update `INDEX.md`.
   - If work stops before verification or the issue remains, move or keep the note under `unresolved/` and update `INDEX.md`.

10. **Escalate after repeated failures.**
   - If this pass fails, return to evidence gathering with the new result instead of layering another fix.
   - After three unsuccessful fix attempts for the same symptom, stop and reassess architecture, state ownership, concurrency, stale assumptions, or test validity with the user before trying another implementation.

## Subagent Use

- Use a subagent only for bounded, independently verifiable investigation such as tracing a call chain, comparing similar implementations, or triaging test output.
- The main agent owns the hypothesis, final fix, diff review, and verification.
- Do not delegate high-risk architecture, data deletion, migrations, security decisions, or release decisions.
