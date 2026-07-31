# Review Coverage and Risk Routing

Use this reference to select the smallest set of review lenses that still covers the changed behavior and its impact cone. Do not read every subsection mechanically when the change cannot trigger it.

## Contents

1. [Coverage Model](#coverage-model)
2. [Baseline Lens](#baseline-lens)
3. [Intent and Domain Semantics](#intent-and-domain-semantics)
4. [Data and Persistence](#data-and-persistence)
5. [State, Async, and Concurrency](#state-async-and-concurrency)
6. [Security, Privacy, and Trust Boundaries](#security-privacy-and-trust-boundaries)
7. [Reliability, Operations, and Release Safety](#reliability-operations-and-release-safety)
8. [Performance, Capacity, and Cost](#performance-capacity-and-cost)
9. [Architecture and Maintainability](#architecture-and-maintainability)
10. [Dependencies and Supply Chain](#dependencies-and-supply-chain)
11. [Tests, CI, and Validation Integrity](#tests-ci-and-validation-integrity)
12. [UI, Accessibility, and Product Workflow](#ui-accessibility-and-product-workflow)
13. [Agent and Automation Changes](#agent-and-automation-changes)
14. [Scenario and Evidence Templates](#scenario-and-evidence-templates)
15. [Low-Signal Feedback to Avoid](#low-signal-feedback-to-avoid)

## Coverage Model

Apply coverage in three layers:

1. **Baseline**: inspect every non-trivial change for intent, correctness, complexity, tests, security basics, and unexpected scope.
2. **Triggered lenses**: deepen review only when the change touches a corresponding boundary.
3. **Impact cone**: include unchanged code whose assumptions, contracts, callers, or operational behavior the change can invalidate.

Record each selected lens as `Reviewed`, `Partial`, `Skipped`, or `Needs Follow-up`. A skipped lens must include why it cannot be triggered by the change.

Prioritize by:

- User or business impact.
- Security, privacy, data, money, or availability exposure.
- Likelihood and realistic triggerability.
- Blast radius and reversibility.
- Evidence strength.
- Whether the defect is systemic or isolated.

Do not prioritize by line count, novelty, or stylistic dislike alone.

## Baseline Lens

Apply to every non-trivial change.

### Intent fidelity

- Confirm that the diff implements the stated requirement and no unrelated behavior.
- Identify implicit requirements and non-goals from tests, docs, callers, UI, and existing contracts.
- Check for an implementation that runs but encodes the wrong business meaning.
- Compare removed behavior with compatibility promises and users of the old path.

### Local correctness

- Inspect happy path, invalid input, empty input, maximum/minimum values, missing data, and partial failure.
- Check branch conditions, boolean inversions, off-by-one errors, default behavior, and fallthrough.
- Trace error propagation and cleanup.
- Check units, time zones, locales, currency, rounding, identifiers, ordering, and serialization.

### Scope and code health

- Flag unrelated edits, broad rewrites, dead compatibility code, and generated churn that hide the behavioral change.
- Check whether complexity, states, branches, dependencies, or public surface increased unnecessarily.
- Search for an existing entry point before accepting a new helper, service, adapter, hook, validator, or abstraction.
- Check comments and names against actual behavior, not only against the author’s explanation.

### Verification

- Look for a regression test that fails before the change for a bug fix.
- Verify that assertions test externally meaningful behavior.
- Inspect required checks; do not infer pass status from a summary.
- Identify the most important untested invariant.

## Intent and Domain Semantics

**Trigger:** any product behavior, business rule, workflow, entitlement, calculation, prioritization, eligibility, billing, moderation, or state transition changes.

Inspect:

- Authoritative product specification and decision ownership.
- Preconditions, postconditions, invariants, and legal state transitions.
- Conflicting meanings between UI, API, domain model, persistence, and downstream integrations.
- Boundary cases that look technically valid but violate policy.
- Backward compatibility and behavior for existing stored data.
- Partial completion, cancellation, retries, and user-visible recovery.
- Whether a “fallback” silently changes business semantics.
- Whether the change bypasses the established domain service or policy layer.

Escalate as `Needs Decision` when correctness depends on an unstated policy choice.

## Data and Persistence

**Trigger:** schema, migration, query, transaction, cache, serialization, import/export, deletion, retention, or storage behavior changes.

Inspect:

- Forward and backward compatibility during rolling deployment.
- Migration ordering, lock duration, table scans, defaults, nullability, index creation, and rollback limits.
- Transaction boundaries, isolation, lost updates, write skew, duplicate writes, and partial side effects.
- Idempotency keys, uniqueness constraints, foreign keys, and application-level assumptions.
- Data loss, truncation, coercion, encoding, precision, time-zone conversion, and irreversible transforms.
- Cache invalidation, stale reads, cache-key scope, and tenant/user isolation.
- Pagination, stable ordering, cursor validity, and batch limits.
- Retention, deletion, restore, audit-log, and privacy obligations.
- Read/write compatibility between old and new application versions.
- Import/export contracts and malformed or adversarial records.

Require explicit evidence for destructive changes and migrations. A successful local unit test is insufficient.

## State, Async, and Concurrency

**Trigger:** async work, UI state, background jobs, queues, workers, callbacks, timers, subscriptions, streams, locks, parallelism, or shared mutable state changes.

Inspect:

- Race conditions, stale responses, duplicate submissions, re-entrancy, and out-of-order completion.
- Cancellation and cleanup on timeout, navigation, shutdown, or retry.
- Exactly-once assumptions implemented on at-least-once infrastructure.
- Idempotency across process restart and redelivery.
- Lock scope, deadlocks, lock ordering, starvation, and lease expiry.
- State-machine transitions and impossible or ambiguous combinations of flags.
- Retry amplification, thundering herds, poison messages, and backpressure.
- Partial success across database, queue, network, and external service boundaries.
- Event ordering, deduplication, replay, and version compatibility.
- Resource leaks: tasks, sockets, file handles, subscriptions, goroutines/threads, and temporary files.

Prefer state-transition tables or sequence traces when informal reading becomes ambiguous.

## Security, Privacy, and Trust Boundaries

**Trigger:** public input, auth, authorization, tenant boundaries, files, URLs, commands, templates, deserialization, secrets, logging, cryptography, webhooks, integrations, or agent/tool execution changes.

Inspect:

- Authentication on every reachable branch.
- Object-level and action-level authorization after identifier resolution.
- Tenant, organization, account, and user isolation in queries, caches, jobs, and logs.
- Input validation at the trust boundary rather than only in the UI or caller.
- Injection paths: SQL/NoSQL, shell, template, path, header, URL, LDAP, expression, and code execution.
- SSRF, open redirects, unsafe fetches, DNS rebinding, and private-network access.
- Path traversal, archive extraction, symlinks, upload type/size, and unsafe file serving.
- Output encoding, XSS, content-sniffing, and unsafe Markdown/HTML rendering.
- Session fixation, CSRF, token scope, token lifetime, revocation, and replay.
- Secret exposure through code, environment, logs, errors, telemetry, caches, artifacts, or frontend bundles.
- Sensitive-data minimization, purpose limitation, retention, deletion, and auditability.
- Cryptographic algorithm, nonce/IV use, key management, comparison timing, and insecure home-grown crypto.
- Rate limits, abuse controls, account enumeration, and high-cost operations.
- Fail-open behavior and swallowed security errors.

Anchor every security finding to an asset, attacker capability, reachable path, and impact. Do not file speculative vulnerability labels without a credible boundary violation.

## Reliability, Operations, and Release Safety

**Trigger:** deployment, config, environment variables, feature flags, service dependencies, retry logic, logging, metrics, alerts, health checks, migrations, or failure handling changes.

Inspect:

- Configuration defaults, missing/invalid values, environment parity, and secret boundaries.
- Feature-flag lifecycle, targeting, stale flags, kill switches, and behavior when the flag service fails.
- Backward/forward compatibility across versions during rolling deploys.
- Deployment ordering between application, schema, queues, and external contracts.
- Rollback feasibility after writes or migrations.
- Retry policy, timeout budget, jitter, circuit breaking, fallback semantics, and overload behavior.
- Health/readiness checks that reflect actual dependency readiness without causing cascading failure.
- Logs, metrics, traces, and alerts for the changed critical path.
- Whether errors are actionable and preserve correlation identifiers without leaking secrets.
- Graceful degradation, emergency disable, and operator recovery steps.
- Startup/shutdown behavior and in-flight work handling.
- Incident and runbook implications.

Treat “fallback” as a semantic change that requires evidence; a fallback that hides corruption or authorization failure is not resilience.

## Performance, Capacity, and Cost

**Trigger:** loops over unbounded data, database access, network calls, large payloads, caching, rendering, serialization, background processing, or resource-intensive agent/model calls change.

Inspect:

- Complexity relative to realistic input size.
- N+1 queries, repeated remote calls, serial work that should be bounded-parallel, and unbounded fan-out.
- Pagination, streaming, batching, payload size, compression, and memory retention.
- Query plans, indexes, selectivity, table scans, and lock contention.
- Cache hit assumptions, stampede prevention, eviction, and consistency tradeoffs.
- Cold start, startup time, bundle size, client rendering, and main-thread blocking.
- Rate limits and third-party quotas.
- Token, model, storage, compute, and egress cost amplification.
- Benchmark representativeness and whether optimization weakens correctness or safety.

Report performance concerns only with a plausible scale or observed evidence. Avoid theoretical micro-optimization comments.

## Architecture and Maintainability

**Trigger:** shared abstractions, module boundaries, public APIs, cross-cutting concerns, refactors, new layers, broad file movement, or repeated generated patterns.

Inspect:

- Dependency direction and whether the change bypasses an established boundary.
- Single source of truth for domain state, validation, errors, and configuration.
- Duplicate helpers, near-identical components, parallel service layers, and copied tests.
- New interface/factory/configuration with only one real use and no high-risk semantic reason.
- God modules, long functions, deep branching, unclear ownership, and cyclic dependencies.
- Compatibility layers whose old behavior no longer exists.
- Public API growth and whether private/local scope is sufficient.
- Cohesion: whether unrelated responsibilities were placed together for prompt convenience.
- Coupling: whether a local change now requires many unrelated modules to change.
- Documentation/ADR drift and whether future maintainers can recover the intent from the repository.
- Whether the fix makes the next similar change easier or merely adds another exception.

Apply the rule of three cautiously. Shared abstractions can be justified earlier for auth, permissions, money, time, units, persistence, error handling, and other semantics that must remain centralized.

## Dependencies and Supply Chain

**Trigger:** manifest, lockfile, generated code, vendored code, build scripts, package scripts, registries, containers, actions, plugins, MCP servers, or external binaries change.

Inspect:

- Whether the dependency is necessary or native/stdlib/existing functionality is sufficient.
- Correct package name, registry, source, version, maintenance status, license, and ownership.
- Typosquatting, dependency confusion, mutable tags, unpinned actions/images, and install scripts.
- Transitive dependency and lockfile churn relative to the intended change.
- Breaking API changes, runtime support, and platform compatibility.
- Build-time network access, generated artifacts, checksums, signatures, and provenance.
- CI permissions, token exposure, artifact tampering, and release promotion.
- Vulnerability remediation that actually removes reachable risk rather than silencing a scanner.
- Generated or copied code whose origin and update path are unclear.

Do not accept a dependency because its API sounds plausible. Verify it from the repository or an authoritative source.

## Tests, CI, and Validation Integrity

**Trigger:** behavior changes, tests change, CI/config changes, scanners change, broad mocks/fixtures change, or an agent claims success.

Inspect:

- Whether the test would fail before the change and pass after it.
- Happy, failure, boundary, permission, concurrency, migration, and rollback paths relevant to the change.
- Assertions against real outcomes rather than mocks, call counts, snapshots, or generated structure alone.
- Integration coverage at database, filesystem, queue, network, browser, and external-contract boundaries.
- Over-mocking that makes an impossible system pass.
- Flaky retries, test order dependence, shared global state, clock/randomness, and race sensitivity.
- Removed tests, skipped tests, lowered thresholds, softened commands, changed triggers, `|| true`, or deleted negative assertions.
- CI path filters and branch rules that let the changed files bypass required checks.
- Generated baselines or snapshots updated without explaining the behavior change.
- Static analysis, type checking, security scanning, and build outputs that were disabled or narrowed.
- Manual/UI validation when the repository supports browser automation or screenshots.

Treat weakened validation as blocking unless the same protection is demonstrably replaced.

For high-risk pure logic, consider:

- Property-based tests for invariants across broad input spaces.
- Metamorphic tests when a transformation should preserve a relation.
- Differential tests against the previous implementation or a trusted oracle.
- Model-based/state-machine tests for transition-heavy behavior.
- Fuzzing or micro-fuzzing at parsers, decoders, serializers, and security boundaries.

## UI, Accessibility, and Product Workflow

**Trigger:** UI, interaction, styling, routing, forms, localization, notifications, or user-facing error behavior changes.

Inspect:

- Loading, empty, error, disabled, submitting, selected, stale, retry, and offline states.
- Keyboard navigation, focus order/return, labels, semantic controls, screen-reader announcements, and contrast.
- Responsive behavior, overflow, zoom, long text, translated text, RTL, and reduced motion.
- Double submission, optimistic updates, stale responses, and cancellation on navigation.
- Destructive-action confirmation, undo/recovery, and clear scope.
- Form validation consistency between client and server.
- Localization keys, pluralization, dates, numbers, currency, and fallback language.
- Visual/interaction drift from existing information architecture.
- Browser-native behavior replaced by fragile custom controls.
- Telemetry and privacy implications of new UI events.

Inspect actual rendered behavior or repository-supported browser evidence for material UI changes when feasible.

## Agent and Automation Changes

**Trigger:** AI-generated change; prompts, skills, AGENTS files, rules, hooks, workflows, model calls, MCP, connectors, browser tools, memory, sandbox, or autonomous repair changes.

Apply `references/ai-agent-risk-catalog.md` and inspect:

- Model and harness behavior, not the model in isolation.
- Untrusted content flowing into prompts or tool decisions.
- Tool and network permissions, service identities, tokens, and approval gates.
- Model output interpreted as shell, SQL, deployment, or destructive action.
- Agent ability to modify its own instructions, permissions, validators, or completion criteria.
- Progress/state artifacts that can be forged, overwritten, or go stale.
- Evals that measure only final pass/fail and ignore trajectory, side effects, or shortcuts.
- Same-agent author/reviewer correlation and missing independent verification.
- Generated dependencies, configuration, tests, and docs that appear authoritative without provenance.
- Token/unbounded-loop denial of wallet and runaway automation.

## Scenario and Evidence Templates

### Failure scenario

```text
Stimulus: <input, event, attacker action, retry, deploy, or failure>
Environment: <version mix, load, tenant, degraded dependency, data shape>
Path: <entry point -> transformations -> persistence/side effect -> output>
Required invariant: <what must remain true>
Observed evidence: <code/test/runtime evidence>
Failure: <how the invariant can be violated>
Impact: <user/business/security/operations consequence>
```

### Finding evidence

```text
Scope: <files, symbols, route, workflow>
Trigger: <specific reachable condition>
Proof path: <steps or call/data flow>
Disproof attempted: <guard, type, test, contract, runtime check>
Evidence: <references and command output>
Uncertainty: <what remains unknown>
Smallest fix direction: <not a speculative rewrite>
```

### Coverage status

```text
Lens: <name>
Trigger: <why selected>
Scope reviewed: <paths/workflows>
Evidence: <commands/references>
Status: Reviewed | Partial | Skipped | Needs Follow-up
Gap: <remaining risk>
```

## Low-Signal Feedback to Avoid

Do not report:

- Pure formatting already enforced by tools.
- Preference for a different equally valid idiom without project evidence.
- A hypothetical issue with no reachable trigger or affected invariant.
- Duplicate comments for every occurrence of one root cause.
- “Add more tests” without naming the missing behavior or oracle.
- “Could be more performant” without plausible scale or evidence.
- Large rewrites when a local, reversible fix exists.
- Security labels without an asset, trust boundary, path, and impact.
- Findings copied from another reviewer without independent verification.
- Praise, summary, or tutorial content that obscures actionable risk.
