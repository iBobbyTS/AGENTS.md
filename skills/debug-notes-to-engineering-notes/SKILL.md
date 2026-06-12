---
name: debug-notes-to-engineering-notes
description: Use after a difficult or long debugging session when the user asks to turn .agent-work/debug records, resolved investigations, failed attempts, git history, or version-specific framework/host behavior into reusable docs/engineering-notes. Use when Codex must separate transferable engineering lessons from project-specific implementation notes, document official-doc gaps or contradictions with observed behavior, and make notes sufficient for someone to reproduce a similar capability or diagnose a similar issue without reading the original code. Do not use for actively debugging a live bug unless the task is specifically to archive or synthesize debug knowledge.
---

# Debug Notes To Engineering Notes

## Overview

Use this skill to convert completed debugging evidence into durable engineering documentation. The output should help a future engineer implement a similar capability or diagnose a similar issue without re-reading the original code or rediscovering the same failed paths.

This skill is for post-debug knowledge extraction. For active repeated debugging, use the project's second-pass debugging workflow first, then use this skill after the evidence is stable.

## Workflow

1. **Inventory the evidence.**
   - Read `.agent-work/debug/INDEX.md` when it exists.
   - Read the relevant files under `.agent-work/debug/resolved/`, `.agent-work/debug/unresolved/`, and `.agent-work/debug/active/`.
   - If the user names an issue that is not in debug records, inspect `git log`, relevant commit diffs, moved/deleted docs, and nearby historical notes before assuming the evidence is missing.
   - Treat prior summaries as leads, not facts. Verify against debug notes, diffs, logs, tests, or official docs.

2. **Classify each finding.**
   - Put transferable engineering knowledge in `docs/engineering-notes/`.
   - Put project-specific implementation choices, product behavior, class names, defaults, feature boundaries, parameter IDs, local debug flags, or current architecture in a normal `docs/` file such as `docs/<topic>-implementation-notes.md`.
   - Keep concrete debug records in `.agent-work/debug/` as evidence; do not copy entire logs into engineering notes.

3. **Split notes by module or failure mode.**
   - Create separate notes for independent concerns such as coordinate systems, host validation, render sampling, API behavior, persistence/writeback, event dispatch, or deployment state.
   - Do not combine unrelated problems into one large catch-all note.
   - Add cross-links only where they prevent confusion.

4. **Write notes from the reader's task perspective.**
   - Write for someone implementing the same kind of capability or facing the same class of bug.
   - Do not write product marketing or a feature walkthrough.
   - Make the note sufficient to reproduce the reasoning without reading implementation code.
   - Prefer layer contracts, data-flow boundaries, failure signatures, diagnostic commands, and validation surfaces over symbol-by-symbol implementation detail.

5. **Record both success and failure.**
   - Include the correct model or fix pattern.
   - Include failed approaches and explain why each was wrong.
   - End each engineering note with `Previous Wrong Attempts` unless the note is purely an index or overview.

## Required Engineering Note Shape

Each substantial file under `docs/engineering-notes/` should include:

- Title.
- `Last updated: <YYYY-MM-DD HH:MM TZ>`.
- `Reference commit: <full git commit hash>`.
- `Observed versions: ...` when behavior depends on a host app, OS, framework, library, SDK, service, model, or tool version.
- Official API or documentation baseline, if external behavior is involved.
- Versioned observations for behavior that official docs do not promise or that contradicts official docs.
- Reproducible layer/module definitions: coordinate spaces, state ownership, data flow, API boundary, lifecycle boundary, or equivalent for the problem domain.
- Diagnostic checklist or evidence sources.
- Correct solution or fix pattern.
- `Previous Wrong Attempts` explaining what was tried, why it failed, and how to recognize that failure mode.

## Official Documentation Rules

- Do not duplicate official documentation for stable, well-documented behavior.
- Record only what the official docs omit, leave ambiguous, or state incorrectly for the observed version.
- Use primary sources when checking external behavior: official docs, SDK headers, source code, changelogs, issue trackers, or verified local version output.
- When observations differ from docs, write the distinction explicitly:
  - "Official docs state..."
  - "Observed on <version>..."
  - "This is not guaranteed by the official API..."
- If versions cannot be discovered from the repo or environment, ask the user or mark the version as unknown. Do not present unversioned host behavior as universal.

## Boundary Between Engineering Notes And Implementation Notes

Use `docs/engineering-notes/` for:

- Framework or host behavior not covered by official docs.
- Debugging methods and decision trees.
- Failure signatures and how to distinguish similar failures.
- Cross-project lessons, API caveats, and validation protocols.
- Successful and failed approaches that can help another implementation.

Use other `docs/` files for:

- Current product shape.
- Project-specific feature behavior.
- Class, function, target, or parameter names.
- Defaults and inspector labels.
- Local debug file paths or flags.
- Current implementation architecture and ownership choices.

If a note needs both, split it: keep the transferable lesson in `engineering-notes`, and link to the project implementation note for local details.

## Validation

Before finishing:

- Search `docs/engineering-notes/` for project-specific names, local file paths, feature defaults, class names, parameter IDs, and product descriptions. Move them out unless they are explicitly part of a versioned observation that is useful outside the project.
- Confirm project-specific implementation choices are documented somewhere under `docs/` outside `engineering-notes` when they still matter.
- Confirm each engineering note has updated timestamp and reference commit metadata.
- Confirm official-doc gaps and contradictions include observed versions.
- Run `git diff --check`.
- For documentation-only changes, code tests are usually unnecessary; state that they were not run because the change is documentation-only.

## Completion Report

In the final response, list:

- Engineering notes created or updated.
- Implementation-note docs created or updated outside `engineering-notes`.
- Evidence sources used: debug records, git commits, official docs, local headers, logs, tests, or user-provided observations.
- Validation commands run and their result.
- Any remaining unknown versions or evidence gaps.
