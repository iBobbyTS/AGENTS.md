# Audit Coverage and Scenario Catalog

Use this reference to construct a baseline or periodic audit scope from the project profile, system map, recent change history, incidents, coverage freshness, and open risk. It is a catalog, not a requirement to reread every item on every cycle.

## Contents

1. [Coverage Principles](#coverage-principles)
2. [Governance, Context, and Risk Framing](#governance-context-and-risk-framing)
3. [Architecture and Quality Attributes](#architecture-and-quality-attributes)
4. [Business Correctness and Critical Workflows](#business-correctness-and-critical-workflows)
5. [Identity, Access, Security, and Privacy](#identity-access-security-and-privacy)
6. [Data Lifecycle and Persistence](#data-lifecycle-and-persistence)
7. [Concurrency, Jobs, and Distributed State](#concurrency-jobs-and-distributed-state)
8. [Reliability, Operations, and Recovery](#reliability-operations-and-recovery)
9. [Release, Configuration, and Change Safety](#release-configuration-and-change-safety)
10. [Performance, Capacity, and Cost](#performance-capacity-and-cost)
11. [Supply Chain, Build, and Artifact Integrity](#supply-chain-build-and-artifact-integrity)
12. [Testing, Verification, and Evaluation](#testing-verification-and-evaluation)
13. [Maintainability, Ownership, and Evolution](#maintainability-ownership-and-evolution)
14. [UI, Accessibility, and User Operations](#ui-accessibility-and-user-operations)
15. [AI-Agent Repository and Runtime](#ai-agent-repository-and-runtime)
16. [Anti-Bloat and Simplification](#anti-bloat-and-simplification)
17. [Sampling and Evidence](#sampling-and-evidence)
18. [Scenario Templates](#scenario-templates)

## Coverage Principles

### Start from system outcomes

Begin with users, operators, business/mission goals, critical workflows, crown-jewel data, privileged actions, and expensive failure modes. Code structure is evidence, not the definition of risk.

### Audit quality attributes explicitly

Rank at least:

- Correctness.
- Security and privacy.
- Reliability and recoverability.
- Modifiability and maintainability.
- Performance and capacity.
- Operability and observability.
- Portability/interoperability where relevant.
- Cost.

A design can be reasonable for one attribute and harmful to another. Record the tradeoff rather than declaring architecture “good” or “bad” in the abstract.

### Combine coverage sources

A credible periodic audit combines:

- Profile-mandated always-on surfaces.
- Changed and high-churn areas.
- Dependency-invalidation cones.
- Rotating deep slices.
- Incidents, escaped defects, flaky checks, and operator pain.
- Open findings and accepted debt.
- End-to-end scenarios crossing subsystem boundaries.

### Separate findings from gaps

- A `finding` has evidence of a defect, control weakness, or bounded structural risk.
- A `gap` means evidence is insufficient to conclude.
- `No Action` means the reviewed area is reasonable under the approved profile and available evidence.

Do not convert every unknown into a defect or every clean scan into proof of safety.

## Governance, Context, and Risk Framing

Review:

- System/workload boundary and excluded adjacent systems.
- Primary users, operators, owners, data stewards, security contacts, and decision authorities.
- Business/mission goals and critical workflows.
- Crown-jewel data, secrets, funds, entitlements, privileged operations, and irreversible actions.
- External systems, processors, vendors, and contractual dependencies.
- Legal, privacy, regulatory, industry, and customer obligations.
- Risk appetite, explicit non-goals, accepted risk, and escalation rules.
- Incident history, near misses, abuse reports, support escalations, and operational pain.
- Asset inventory and data classification.
- Threat actors and realistic abuse cases.
- Secure-development ownership, vulnerability disclosure, triage, remediation, and exception process.
- Audit profile approval, freshness, and change control.

Evidence may include profile, architecture docs, contracts, threat models, data maps, incident reports, service catalogs, ownership files, and interviews. Mark tacit knowledge that is not repository-visible as a maintainability and agent-legibility risk when agents are expected to operate independently.

## Architecture and Quality Attributes

Review:

- Domain/module boundaries, ownership, dependency direction, and extension points.
- Public APIs, events, schemas, contracts, versioning, and compatibility policy.
- Architecture decisions and whether code, ADRs, diagrams, and runtime topology agree.
- Central versus distributed state ownership.
- Coupling, cohesion, cycles, god modules, service sprawl, and cross-cutting concern entry points.
- Fault containment, blast-radius boundaries, multi-tenant isolation, and privilege separation.
- Synchronous/asynchronous choices and consistency tradeoffs.
- Build-versus-buy decisions and opaque dependencies.
- Portability and environment-specific assumptions.
- Evolution pressure: likely next features, scale changes, regulations, and integrations.
- Architecture fitness functions or structural tests.
- Generated architecture maps and their source/update path.

Use quality-attribute scenarios for material decisions:

- **Stimulus:** change, failure, load, attack, operator action, or new requirement.
- **Environment:** normal, degraded, peak, rolling deploy, partial outage, or recovery.
- **Artifact:** affected service/module/data flow.
- **Response:** expected behavior.
- **Measure:** latency, error rate, recovery time, affected tenants, change effort, or evidence.
- **Tradeoff:** what improves and what worsens.

Audit architecture against scenarios, not diagram aesthetics.

## Business Correctness and Critical Workflows

Review:

- End-to-end critical user and operator journeys.
- Domain invariants and legal state transitions.
- Calculations involving money, units, dates, time zones, quotas, ordering, eligibility, or entitlement.
- Defaults, missing data, empty states, maximum/minimum values, invalid transitions, and legacy records.
- Error, cancellation, retry, timeout, and partial-completion behavior.
- Backward compatibility and mixed-version behavior.
- Import/export and external contract fidelity.
- Idempotency and duplicate requests.
- Reconciliation between source systems, ledgers, caches, and derived views.
- Human override, audit trail, appeal, rollback, and correction paths.
- Feature flags and experiments that alter semantics.
- Product specification drift and rules that exist only in code or people’s heads.
- Operator tooling that can bypass normal validation.

Trace each critical invariant from entry validation through domain logic, persistence, side effects, and user-visible result. A locally correct function does not prove the workflow.

## Identity, Access, Security, and Privacy

### Identity and sessions

Review:

- Authentication mechanisms, account recovery, MFA, enrollment, and credential lifecycle.
- Session creation, rotation, revocation, expiry, fixation, replay, and device/session visibility.
- Service-to-service identity, workload identity, certificate/token issuance, and rotation.
- Separate agent/service identities versus shared developer credentials.

### Authorization and isolation

Review:

- Object-level and action-level authorization.
- Tenant, organization, project, account, and user isolation.
- Role/permission model, privilege escalation, delegation, impersonation, and break-glass access.
- Authorization in background jobs, caches, exports, webhooks, and administrative tooling.
- Central policy enforcement and bypass paths.
- Default-deny behavior and fail-open conditions.

### Input, output, and execution

Review:

- Validation at trust boundaries.
- Injection: SQL/NoSQL, shell, template, path, header, expression, query language, deserialization, and code execution.
- SSRF, URL fetching, redirects, DNS/private-network access, and webhook validation.
- File upload/download, path traversal, archives, symlinks, media processing, and unsafe serving.
- Output encoding, XSS, content security policy, and untrusted rich text/Markdown.
- Cryptographic use, key storage, nonce/IV behavior, randomness, signing, and verification.
- Dynamic plugin/module loading and extension points.

### Secrets and sensitive data

Review:

- Secret storage, scope, rotation, revocation, and exposure through logs/errors/telemetry/build artifacts/frontend bundles.
- Data minimization, purpose limitation, consent, retention, deletion, export, and residency.
- Encryption in transit/at rest and key-management boundaries.
- Production-data access from development, CI, agents, analytics, and support tools.
- Backups, snapshots, crash dumps, transcripts, and temporary files.
- Audit logs and tamper resistance.

### Abuse and resilience

Review:

- Rate limits, quotas, enumeration, scraping, fraud, spam, denial of service, and expensive operations.
- Abuse-case tests and monitoring.
- Vulnerability disclosure, dependency response, incident response, and patch deployment.
- Threat-model freshness and security requirements traced to implementation/tests.

Anchor every security finding to assets, trust boundaries, attacker capabilities, reachability, and impact.

## Data Lifecycle and Persistence

Review:

- Data model, schema ownership, constraints, indexes, defaults, nullability, and referential integrity.
- Migration design, locking, backfill, online compatibility, rollback, and disaster recovery.
- Transactions, isolation, consistency, lost updates, write skew, and partial writes.
- Cache keys, invalidation, stale data, consistency, and tenant scope.
- Event schemas, versioning, ordering, deduplication, replay, and dead-letter handling.
- Derived state, materialized views, search indexes, analytics, and reconciliation.
- Serialization formats, precision, encoding, time zones, and irreversible transforms.
- Import/export, bulk operations, pagination, batch limits, and stable ordering.
- Retention, legal holds, deletion propagation, anonymization, and restore interactions.
- Backup frequency, integrity, encryption, restore tests, recovery point/time objectives, and ownership.
- Auditability and correction of erroneous records.
- Data lineage and external processors.

Do not accept “backups exist” without restore evidence. Do not accept a migration because it runs on an empty development database.

## Concurrency, Jobs, and Distributed State

Review:

- Shared mutable state, locks, transactions, leases, compare-and-swap, and optimistic concurrency.
- Race conditions, re-entrancy, stale responses, duplicate submission, and out-of-order completion.
- Queue delivery semantics, idempotency, deduplication, poison messages, and redrive.
- Retry classification, backoff, jitter, limits, retry storms, and side-effect safety.
- Cancellation, timeouts, task cleanup, shutdown, and in-flight work.
- Scheduler overlap, clock skew, leader election, and missed/duplicate runs.
- Eventual consistency, reconciliation, conflict resolution, and user-visible staleness.
- Distributed transactions, sagas, compensating actions, and partial failure.
- Backpressure, rate limits, queue growth, saturation, and admission control.
- Stream/subscription lifecycle and resource leaks.
- State-machine clarity versus accumulated boolean flags.
- Exactly-once claims on infrastructure that does not provide it.

Use sequence diagrams, event traces, state-transition tables, targeted stress tests, or model-based tests when informal review is insufficient.

## Reliability, Operations, and Recovery

Review:

- Service-level indicators/objectives or equivalent reliability targets.
- Error-budget or release-risk policy.
- Dependency map and critical-path availability.
- Timeouts, retries, circuit breakers, bulkheads, load shedding, and graceful degradation.
- Startup, readiness, health, liveness, and shutdown behavior.
- Logs, metrics, traces, dashboards, and alert quality for critical workflows.
- Golden signals: latency, traffic, errors, and saturation where applicable.
- Alert actionability, ownership, routing, suppression, and runbooks.
- Incident detection, triage, mitigation, communication, and postmortem follow-through.
- Backup, restore, disaster recovery, failover, region/account recovery, and exercises.
- Degraded mode, kill switches, feature disablement, and safe defaults.
- Queue recovery, stuck jobs, reconciliation, and operational repair tools.
- Capacity limits, quotas, certificate/domain expiry, and third-party failure.
- Operational changes agents can make autonomously.

Verify recovery paths, not only normal operation. A control with no owner, alert, or exercised runbook may be nominal rather than effective.

## Release, Configuration, and Change Safety

Review:

- Environment separation and parity.
- Configuration source, schema, defaults, validation, precedence, and secret separation.
- Feature-flag targeting, failure behavior, expiry, cleanup, and emergency disable.
- CI/CD triggers, branch/tag protection, approvals, permissions, and separation of duties.
- Build, test, artifact promotion, release signing, deployment, and rollback.
- Database/application sequencing and mixed-version compatibility.
- Canary, staged rollout, health gates, automatic rollback, and manual intervention.
- Release notes, migration/operator instructions, and customer-impact communication.
- Immutable versus mutable artifacts and post-review tampering risk.
- Rollback after irreversible data writes.
- Hotfix and break-glass process.
- Reproducibility and provenance from source to production artifact.
- Generated deployment changes and infrastructure drift.

Inspect the actual effective workflow and permissions, not only YAML intent.

## Performance, Capacity, and Cost

Review:

- Workload assumptions, growth, peak patterns, and service limits.
- Algorithmic complexity and unbounded inputs.
- Query plans, N+1 access, indexes, pagination, and batch behavior.
- Network fan-out, serialization, payload size, compression, and streaming.
- Cache behavior, stampede prevention, and consistency cost.
- CPU, memory, file descriptors, connections, threads/tasks, and storage growth.
- Cold starts, startup time, client bundle/rendering, and latency budgets.
- Backpressure, queue depth, admission control, and overload behavior.
- Third-party quotas, API latency, egress, and cost.
- Agent/model token use, context size, retries, parallelism, tool calls, and denial-of-wallet exposure.
- Benchmark/load-test representativeness and regression thresholds.
- Performance optimizations that weaken correctness, security, or operability.

Tie findings to realistic volume or observed behavior. Avoid speculative micro-optimization.

## Supply Chain, Build, and Artifact Integrity

Review:

- Direct/transitive dependency inventory, ownership, maintenance, support, and license policy.
- Lockfiles, vendoring, generated code, binaries, containers, actions, and plugins.
- Typosquatting, dependency confusion, mutable tags, unpinned sources, and install scripts.
- Vulnerability monitoring, reachability, remediation, exception, and end-of-life runtimes.
- Build-time network access and hermeticity.
- Source control protections and contributor identity.
- CI runners, token scope, secret boundaries, cache poisoning, and artifact access.
- Reproducible/traceable builds, provenance attestations, signatures, checksums, and SBOM/inventory.
- Artifact promotion, registry controls, immutable releases, and rollback integrity.
- Generator versions and update paths.
- Third-party MCP servers, skills, plugins, agent tools, remote instructions, and model endpoints.
- License/security implications of AI-generated copied code.

Treat SAST, dependency scanning, secret scanning, provenance, review, and runtime defenses as layers. No single tool proves supply-chain safety.

## Testing, Verification, and Evaluation

Review the portfolio, not only coverage percentage:

- Unit tests for local logic.
- Integration tests for data, filesystem, network, queue, and service contracts.
- End-to-end/system tests for critical workflows.
- Migration, rollback, restore, failover, and disaster-recovery tests.
- Permission, tenant isolation, abuse, and negative security tests.
- Concurrency, retry, idempotency, and state-machine tests.
- Performance, load, soak, and capacity tests where risk warrants.
- UI/browser/accessibility/manual validation.
- Property-based, metamorphic, differential, model-based, fuzz, and chaos tests for broad invariant spaces.
- Static analysis, types, lint, secret scanning, dependency scanning, SAST/DAST, and policy checks.
- Test flakiness, order dependence, environment drift, fixture realism, and data contamination.
- Mock balance and whether oracles measure real outcomes.
- CI path/branch coverage and required checks.
- Scanner suppression and test deletion history.

For agent systems also review:

- Capability and regression eval suites.
- Multiple trials for stochastic behavior.
- Outcome, transcript/trajectory, tool-call, side-effect, state, and human-calibration graders.
- Model/harness version gates and rollback signals.
- Reward hacking, benchmark leakage, grader manipulation, and shortcut behavior.
- Production monitoring and feedback loops.
- Retention/redaction of transcripts and eval data.

A passing outcome can hide dangerous actions or evaluator exploitation. Inspect trajectories for high-impact agents.

## Maintainability, Ownership, and Evolution

Review:

- Module/service/data ownership and escalation paths.
- Onboarding and whether intent can be recovered from repository-local sources.
- Naming, comments, documentation, ADRs, diagrams, contracts, and runbooks.
- Generated versus authoritative documentation and freshness enforcement.
- Complexity/churn hotspots and areas no maintainer can explain.
- Duplicate helpers, parallel abstractions, inconsistent patterns, and bypasses.
- Public API growth, extension points, deprecation, and compatibility debt.
- God modules, long functions, deep branches, cycles, and unclear responsibility.
- Technical-debt entries, owners, ceilings, triggers, and aging.
- Repeated incident/finding classes and missing durable controls.
- Team bus factor and tacit knowledge.
- Agent legibility: maps, stable sources of truth, predictable structure, and tool-accessible evidence.
- Whether the next likely change becomes easier or more fragile.
- Cognitive debt: code production exceeds human/agent understanding and ownership.

Separate acceptable local complexity from structural debt that compounds across changes.

## UI, Accessibility, and User Operations

Review:

- Information architecture and consistency across accumulated changes.
- Responsive layout, zoom, long/translatable text, RTL, and device/browser support.
- Semantic controls, keyboard access, focus, labels, screen-reader behavior, contrast, and motion.
- Loading, empty, error, stale, disabled, submitting, selected, retry, and offline states.
- Destructive actions, confirmation, undo, scope visibility, and recovery.
- Client/server validation consistency and secure failure messages.
- Localization, dates, numbers, currency, and pluralization.
- Optimistic updates, duplicate actions, cancellation, and stale response handling.
- Operator/admin interfaces, bulk actions, permission clarity, and audit trail.
- Telemetry/privacy implications and consent.
- Browser-native behavior replaced by fragile custom controls.

Sample real workflows, not only screenshots of the happy path.

## AI-Agent Repository and Runtime

When agents create, review, test, deploy, or operate the system, audit them as part of the engineering control plane.

Review:

- Agent/model/harness inventory and version/update policy.
- Agent identities, credentials, token scope, revocation, network access, filesystem access, and sandbox profiles.
- Human approval gates for production, destructive, privileged, financial, or data-export actions.
- MCP servers, connectors, plugins, hooks, skills, browser tools, local control planes, and remote behavior.
- Prompt injection from issues, PRs, docs, web pages, emails, logs, tool output, dependencies, and generated files.
- Separation of untrusted content, control instructions, and tool arguments.
- Model output validation before shell, SQL, code execution, deployment, or other side effects.
- Agent memory, state, progress ledgers, cross-session contamination, and poisoning.
- Ability to modify its own rules, permissions, tests, scanners, or completion criteria.
- Unbounded loops, denial of wallet, runaway retries, and kill switches.
- Outcome and trajectory observability; transcript retention and secret/PII redaction.
- Evals, model-upgrade gates, rollback, human calibration, and production drift.
- Same-model author/reviewer/fixer correlation.
- Generated dependencies, code provenance, documentation, and test validity.
- Repository instructions as maintained control-plane code.

Use `references/ai-agent-risk-catalog.md` for detailed patterns and evidence strategies.

## Anti-Bloat and Simplification

When in scope, read `references/anti-bloat.md` and inspect:

- Dead code, obsolete compatibility paths, unused configuration, speculative features, and stale generated artifacts.
- Standard-library, framework, database, browser, or platform capabilities replaced by custom code.
- Dependencies whose value does not justify transitive/security/operational cost.
- One-implementation interfaces, one-product factories, wrapper-only files, and layers with one caller.
- Repeated states, branches, files, or abstractions that can be collapsed safely.
- Parallel abstractions that should reuse an established entry point.
- Agent-generated verbosity and architecture erosion across successive changes.

Rank safe reduction by systemic benefit, not raw deleted lines. Preserve necessary controls, tests, accessibility, migrations, recoverability, and explicitly required behavior.

## Sampling and Evidence

### Sampling signals

Prioritize areas with:

- High business/security/data/availability criticality.
- High churn, complexity, ownership turnover, or defect density.
- Broad fan-in/fan-out or cross-cutting behavior.
- Public inputs, privileged actions, or irreversible side effects.
- Weak tests or observability.
- New dependencies, migrations, runtime/platform changes, or agent tooling.
- Past incidents/findings or accepted debt near its trigger.
- Stale/invalidated/unknown coverage.

### Evidence hierarchy

Prefer:

1. Reproduced behavior and current runtime evidence.
2. Executable tests/checks against the current head/environment.
3. Concrete code/configuration/data-flow evidence.
4. Authoritative repository docs/contracts and verified generated sources.
5. Version-control history and incident records.
6. Vendor documentation and standards.
7. Agent/human summaries, which require verification.

### Coverage recording

For each area record:

- Scope and boundaries.
- Quality attributes/scenarios.
- Files/interfaces/workflows inspected.
- Commands and runtime evidence.
- Findings and candidate disposition.
- Gaps and assumptions.
- Last reviewed commit/date/environment.
- Dependencies and invalidation triggers.
- Freshness state and next rotation reason.

Do not use a single percentage to summarize heterogeneous audit coverage.

## Scenario Templates

### Quality-attribute scenario

```text
Scenario ID:
Attribute: Correctness | Security | Reliability | Modifiability | Performance | Operability | Cost
Stimulus:
Source of stimulus:
Environment:
Affected artifact/workflow:
Expected response:
Response measure:
Architecture decisions/tradeoffs:
Evidence inspected:
Result: Satisfied | Partially Satisfied | Not Satisfied | Unknown
Gaps and follow-up:
```

### Abuse case

```text
Asset:
Threat actor/capability:
Entry/trust boundary:
Preconditions:
Attack path:
Expected controls:
Evidence:
Impact/blast radius:
Detection/response:
Residual risk:
```

### Failure/recovery case

```text
Dependency or component failure:
Timing/load/deploy state:
User/operator-visible effect:
Containment/degraded behavior:
Data consistency consequences:
Detection and alert:
Recovery/rollback/restore steps:
RTO/RPO or equivalent target:
Evidence/exercise result:
```

### Change/evolution case

```text
Likely future change:
Affected modules/contracts:
Expected effort and owners:
Compatibility/migration need:
Current architecture support:
Coupling or duplication risk:
Evidence:
Recommended control or boundary:
```
