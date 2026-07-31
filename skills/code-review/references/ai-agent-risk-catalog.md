# AI-Agent Risk Catalog for Bounded Code Review

Use this catalog when an AI coding agent authored, repaired, reviewed, or materially influenced the change, or when the change affects an agent harness. Treat each entry as a hypothesis family, not an automatic finding.

## Contents

1. [How to Use the Catalog](#how-to-use-the-catalog)
2. [Intent and Scope Failures](#intent-and-scope-failures)
3. [Architecture and Maintainability Failures](#architecture-and-maintainability-failures)
4. [Correctness and Validation Failures](#correctness-and-validation-failures)
5. [Security and Autonomy Failures](#security-and-autonomy-failures)
6. [State, Context, and Evidence Failures](#state-context-and-evidence-failures)
7. [Review-System Failures](#review-system-failures)
8. [Durable Responses](#durable-responses)

## How to Use the Catalog

For each applicable pattern:

1. Identify a concrete trigger in the diff or harness.
2. Locate the repository invariant or source of truth it can violate.
3. Seek direct evidence, not stylistic resemblance to “AI code.”
4. Attempt to falsify the concern.
5. Report only reachable, material issues.

Do not infer authorship from code style. The risk is the observed pattern, not whether a human or model produced it.

## Intent and Scope Failures

### Plausible but wrong semantics

**Pattern:** The implementation is coherent and tests pass, but it encodes an invented interpretation of the requirement.

**Signals:**

- New defaults or eligibility rules have no authoritative source.
- Edge cases are resolved by generic convention instead of domain policy.
- Product text, API behavior, persistence, and tests disagree.
- The PR summary sounds more certain than the repository evidence.

**Check:** Trace one critical workflow from user intent through side effects and output. Convert ambiguity into `Needs Decision`.

### Scope expansion

**Pattern:** The agent “helpfully” edits adjacent code, upgrades dependencies, reformats files, or redesigns abstractions beyond the goal.

**Signals:**

- Changed files with no path to the requested behavior.
- Large mechanical churn surrounding a small semantic change.
- New public APIs or configuration for hypothetical future needs.
- Unrequested cleanup mixed with a bug fix.

**Check:** Require a reason for every changed area. Split or revert unrelated work before trusting the review surface.

### Unwanted feature completion

**Pattern:** A partial request is interpreted as permission to implement a broader feature or policy.

**Signals:**

- New user-visible states not present in acceptance criteria.
- “For completeness” branches.
- Automatic destructive, migration, or notification behavior.
- New permissions or data collection not requested.

**Check:** Compare every externally visible behavior with explicit requirements and non-goals.

### Compatibility theater

**Pattern:** The agent adds fallbacks, aliases, version checks, or dual paths without evidence that compatibility is required.

**Signals:**

- Old behavior is not used or documented.
- Fallback swallows an error and guesses.
- Both implementations can drift.
- A compatibility flag has no owner or removal condition.

**Check:** Identify actual consumers and version-mix requirements. Prefer removal or a tracked, bounded compatibility plan.

## Architecture and Maintainability Failures

### Local-optimum patch

**Pattern:** The change fixes one symptom by bypassing a shared policy, validation, state, error, or service layer.

**Signals:**

- Direct database/network access beside an established abstraction.
- Permission checks copied into one route.
- One-off parsing or formatting near the caller.
- Special-case branching instead of repairing the root cause.

**Check:** Search for the project’s canonical entry point and sibling paths. Fix the root cause or document why the exception is necessary.

### Reuse blindness

**Pattern:** A new helper, hook, service, adapter, validator, or component duplicates existing behavior.

**Signals:**

- Similar names or signatures in another directory.
- Near-identical tests or error handling.
- A second source of truth for constants or state.
- Slightly different semantics with no deliberate distinction.

**Check:** Search by concepts, call patterns, data shapes, and outputs—not only exact names. Prefer extending the canonical path.

### Architecture erosion by accretion

**Pattern:** Each iteration adds flags, wrappers, branches, files, or layers while preserving all previous paths.

**Signals:**

- State represented by multiple booleans instead of explicit transitions.
- Wrapper chains that only delegate.
- Repeated “temporary” adapters.
- Fixes that increase surface area more than behavior.

**Check:** Compare complexity and ownership before/after. Ask what can be deleted or collapsed after the intended behavior is clear.

### Premature abstraction

**Pattern:** The agent creates generic interfaces, factories, registries, or configurable frameworks for one current case.

**Signals:**

- One implementation and one caller.
- Configuration nobody sets.
- Generic type parameters that obscure simple domain behavior.
- Scaffolding justified only by possible future work.

**Check:** Prefer a local expression unless the concern centralizes a high-risk invariant such as permissions, money, time, persistence, or error semantics.

### Pattern replication

**Pattern:** The agent copies a weak existing pattern because repository precedent is treated as authority.

**Signals:**

- A known workaround appears in new modules.
- Repeated untyped parsing, broad catches, or ad hoc retries.
- Multiple new instances of an existing technical-debt marker.

**Check:** Determine whether the precedent is intentional or merely common. When recurrent, propose a durable lint, test, rule, or shared abstraction.

### Verbose scaffolding and cognitive debt

**Pattern:** The change is technically readable line by line but too large, repetitive, or indirection-heavy for maintainers to build a reliable mental model.

**Signals:**

- Generated explanatory layers that do not enforce behavior.
- Long comments restating code.
- Many tiny files with trivial exports.
- Excessive defensive branches for impossible states.

**Check:** Evaluate whether a new maintainer can identify ownership, invariants, and extension points. Prefer smaller, locally complete code.

## Correctness and Validation Failures

### Test-target overfitting

**Pattern:** The implementation is shaped to satisfy visible tests rather than the intended rule.

**Signals:**

- Literal special cases matching fixtures.
- Narrow conditionals around tested values.
- Production code imports test-only concepts.
- Negative behavior outside fixtures is undefined.

**Check:** Derive properties and new adversarial examples independent of the visible tests. Use hidden-like boundary cases.

### Weak oracle or reward hacking

**Pattern:** The agent obtains a green outcome by exploiting the evaluator rather than solving the task.

**Signals:**

- Tests, fixtures, snapshots, or thresholds changed alongside the implementation without necessity.
- Checks are skipped, narrowed, retried until green, or moved out of required CI.
- The agent writes output files the grader expects without performing the underlying operation.
- Completion is based on self-authored summaries.

**Check:** Inspect the trajectory and environment changes, not only final pass/fail. Freeze validation assets when practical.

### Over-mocked validation

**Pattern:** Tests prove that mocks return configured values, not that real boundaries work.

**Signals:**

- Every collaborator is mocked.
- Assertions focus on call counts and internal methods.
- Database, serialization, routing, filesystem, or browser behavior is absent.
- The test cannot fail for a broken contract.

**Check:** Add or inspect the smallest integration test at the changed boundary.

### Hallucinated API, config, or convention

**Pattern:** The code references a plausible but nonexistent or misused package API, CLI flag, environment variable, schema field, framework hook, or project convention.

**Signals:**

- New names appear only in the diff.
- No documentation, declaration, or runtime consumer exists.
- Similar APIs from another language or version are mixed in.
- A fallback masks the failure.

**Check:** Verify against installed versions, local definitions, generated schemas, and authoritative documentation.

### Fabricated dependency or unsafe package choice

**Pattern:** The agent adds a package because its name appears to fit the task.

**Signals:**

- Misspelled or obscure package.
- Mutable source or unpinned action.
- Large transitive lockfile change for a small utility.
- Install scripts, broad permissions, or unclear ownership.

**Check:** Verify registry/source, necessity, version, license, maintenance, provenance, and transitive impact.

### Error swallowing and plausible fallback

**Pattern:** Broad exception handling converts a real failure into a default value, empty result, retry, or alternate path.

**Signals:**

- `catch Exception`, `except:`, or promise rejection ignored.
- Errors logged without propagation where correctness matters.
- Security, data, or migration failure becomes “not found” or success.
- Retry without classification or limit.

**Check:** Classify errors and confirm fail-open/fail-closed semantics from domain requirements.

### CI integrity weakening

**Pattern:** The change makes required validation easier to pass.

**Signals:**

- Removed/skipped tests, lower thresholds, path filters, conditional steps, `continue-on-error`, `|| true`, changed workflow triggers, or write-token escalation.
- Scanner suppression without root-cause remediation.
- Flaky but valuable tests deleted rather than stabilized.

**Check:** Compare effective required checks before/after, including branch protection and workflow permissions.

## Security and Autonomy Failures

### Prompt injection through repository or external content

**Pattern:** Issue text, PR descriptions, comments, docs, web pages, logs, dependencies, or tool output can instruct an agent to take privileged actions.

**Signals:**

- Untrusted text is concatenated into system-like instructions.
- Tool output is treated as authoritative commands.
- The agent has shell, network, secret, deployment, or write access while reading untrusted content.
- No content/source separation exists.

**Check:** Trace untrusted input to model prompts, decisions, and tool execution. Require least privilege, explicit trust labels, and approval for high-impact actions.

### Adversarial PR narrative

**Pattern:** A title, description, comment, test claim, prior approval, or compatibility rationale socially engineers the reviewer into lowering scrutiny.

**Signals:**

- “Only refactor,” “safe,” “tests prove,” or “requested by security” is accepted without code evidence.
- Reviewer follows instructions embedded in comments or generated files.
- The narrative directs attention away from sensitive hunks.

**Check:** Extract claims, then independently verify each against raw code and repository policy before reading persuasive explanations deeply.

### Excessive tool or workflow permissions

**Pattern:** An agent, CI job, action, connector, or bot receives broader filesystem, network, repository, cloud, or deployment permissions than required.

**Signals:**

- Write-scoped tokens for read-only review.
- Production secrets in pull-request contexts.
- Broad cloud roles or unrestricted egress.
- Shared developer identity instead of a scoped service identity.

**Check:** Enumerate capabilities and reduce to the minimum required action, environment, repository, path, and lifetime.

### Self-modifying controls

**Pattern:** The agent can edit the rules, tests, scanners, permissions, hooks, or completion criteria that constrain it.

**Signals:**

- Same workflow both changes and approves branch protection or security policy.
- Agent-generated patches alter instruction files and validation in one wave.
- Completion state is writable without independent evidence.

**Check:** Require separate human or independently privileged approval for control-plane changes.

### Model output executed directly

**Pattern:** Generated shell, SQL, code, URLs, deployment plans, or file paths are executed without validation.

**Signals:**

- `eval`, shell interpolation, dynamic imports, or direct command construction.
- LLM output controls destructive or production operations.
- No allowlist, schema, dry run, or approval gate.

**Check:** Constrain output to typed schemas and allowlisted actions; validate arguments and require approval for high-impact operations.

### Secret and data exfiltration

**Pattern:** Prompts, transcripts, tool output, generated files, logs, or external connectors expose secrets or sensitive data.

**Signals:**

- Whole environment or repository uploaded to a model/tool.
- Debug logs include tokens, credentials, user data, or database records.
- Artifacts are published from an agent work directory.
- Remote MCP/plugin behavior is mutable or untrusted.

**Check:** Map data flow and retention. Minimize, redact, scope, and audit access.

### Unbounded autonomous loop

**Pattern:** A repair/review agent can consume unbounded tokens, API calls, compute, or external side effects while chasing completion.

**Signals:**

- No iteration/cost/time/action budget.
- “Keep working until done” with self-defined success.
- Repeated retries or reviewer/fixer ping-pong.
- External actions are not idempotent.

**Check:** Add hard budgets, progress tests, idempotency, kill switches, and accountable escalation.

## State, Context, and Evidence Failures

### Stale repository state

**Pattern:** The agent relies on an old summary, plan, diff, or branch state.

**Signals:**

- Referenced files/symbols no longer exist.
- Claimed tests correspond to an earlier head.
- The base moved or another agent edited the worktree.
- Findings target already-replaced code.

**Check:** Reconcile `git status`, current head, patch fingerprint, and evidence timestamps before closure.

### Premature completion

**Pattern:** The agent declares success after local edits or narrow unit tests without end-to-end verification.

**Signals:**

- Feature checklist changed to pass by the implementation agent.
- No realistic user/operator flow.
- Required services or browser were never started.
- Summary uses “should” instead of observed evidence.

**Check:** Verify from the external behavior and current repository state.

### Progress-ledger corruption

**Pattern:** Durable state exists but is overwritten, vague, self-serving, or disconnected from git reality.

**Signals:**

- Findings disappear rather than close.
- No stable IDs or baseline commits.
- A progress file says complete while open failures remain.
- Multiple agents edit the same ledger without conflict rules.

**Check:** Use appendable round records, stable IDs, explicit status transitions, and repository fingerprints.

### Generated documentation drift

**Pattern:** Plans, diagrams, schemas, comments, or reports appear authoritative but no longer match executable behavior.

**Signals:**

- Generated docs are edited manually without regeneration.
- Completion summaries cite old paths.
- Runtime and documentation disagree on configuration or contracts.

**Check:** Identify the source of truth and regeneration path; treat stale generated artifacts as evidence gaps.

### Missing provenance

**Pattern:** Generated code, dependencies, snippets, migrations, or fixtures have no traceable source or review context.

**Signals:**

- Large pasted blocks with unfamiliar conventions.
- Vendored/generated files lack a generator/version.
- Security fixes cite no advisory or affected path.

**Check:** Establish origin, version, license, update mechanism, and validation evidence.

## Review-System Failures

### Same-agent correlated blind spots

**Pattern:** The author, reviewer, fixer, and final verifier share the same assumptions and context.

**Signals:**

- Review repeats the implementation summary.
- The same model accepts its own explanation without reproduction.
- Successive rounds find only cosmetic variants.

**Check:** Use fresh context, different framing/model where available, and raw artifacts before prior conclusions.

### Review verbosity without signal

**Pattern:** Long explanations, severity labels, and downstream lists obscure whether the issue is real.

**Signals:**

- Comment length greatly exceeds the evidence.
- Tutorial content replaces a specific trigger and impact.
- Many low-confidence suggestions create triage burden.

**Check:** Require a compact root-cause finding and put structured evidence in the ledger rather than the human-facing comment.

### Autofix regression loop

**Pattern:** Reviewer and fixer alternate local changes that reopen old bugs or create new branches.

**Signals:**

- Findings oscillate open/closed.
- Each repair grows the diff and impact cone.
- Same error class reappears under a different symptom.

**Check:** Stop, identify the missing specification/oracle/architecture boundary, and reset only after resolving it.

### Reviewer claim contamination

**Pattern:** Prior comments bias later reviewers into confirming the same diagnosis.

**Signals:**

- Independent passes quote previous findings before inspecting code.
- New reviewers focus only on suspected files.
- No one challenges rejected hypotheses or unaffected paths.

**Check:** Give discovery reviewers minimal prompts and delay prior rationalizations until after independent inspection.

### False independence from repeated prompts

**Pattern:** Re-running the same model with the same whole-diff prompt is treated as independent assurance.

**Signals:**

- Identical lens order, context, tools, and source summaries.
- “Two empty rounds” is the only completion criterion.
- No coverage or evidence changes between rounds.

**Check:** Vary review role/lens/input order, use fresh context, and measure evidence coverage rather than repeated agreement.

## Durable Responses

Promote a recurring issue into a durable repository control when it has:

- At least two evidence-backed occurrences or one severe systemic occurrence.
- A clear invariant.
- A mechanically testable or teachable rule.
- Acceptable false-positive and maintenance cost.
- An owner and update path.

Possible controls:

- Regression, property, metamorphic, integration, or state-machine test.
- Type/schema validation at the boundary.
- Static, structural, dependency, or policy lint.
- Shared policy/validation/error-handling entry point.
- Generator or template correction.
- CI permission and required-check rule.
- Short repository instruction pointing to an authoritative source.
- Audit/review rule learned from accepted and rejected findings.

Do not encode every one-off review preference. Bad rules scale faster than bad comments.
