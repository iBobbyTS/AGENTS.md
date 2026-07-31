# AI-Agent Risk Catalog for System Audits

Use this catalog when AI agents materially create, review, test, document, deploy, or operate the repository, or when the product itself contains agents. Audit the model, harness, repository, tools, identities, data, controls, and human workflow as one socio-technical system.

## Contents

1. [Audit Method](#audit-method)
2. [Codebase and Architecture Risks](#codebase-and-architecture-risks)
3. [Repository Knowledge and Ownership Risks](#repository-knowledge-and-ownership-risks)
4. [Validation, Evals, and Reward Risks](#validation-evals-and-reward-risks)
5. [Prompt, Tool, and Autonomy Risks](#prompt-tool-and-autonomy-risks)
6. [Memory, State, and Long-Running Loop Risks](#memory-state-and-long-running-loop-risks)
7. [Supply Chain and Provenance Risks](#supply-chain-and-provenance-risks)
8. [Operational and Human-Control Risks](#operational-and-human-control-risks)
9. [Evidence and Durable Controls](#evidence-and-durable-controls)

## Audit Method

For every applicable risk family:

1. Identify the assets, users, operators, and privileged actions.
2. Map the agent/model/harness identity, tools, data sources, network paths, and durable state.
3. Distinguish trusted control instructions from untrusted content.
4. Trace realistic failure and abuse scenarios.
5. Inspect outcomes and trajectories, not only summaries.
6. Verify guardrails mechanically where feasible.
7. Record remaining human judgment and emergency controls.

Do not generalize from “AI-generated” appearance. Audit observed system properties and evidence.

## Codebase and Architecture Risks

### Architecture erosion under repeated extension

**Risk:** Iterative agent changes accumulate branches, local exceptions, duplicated state, wrappers, and files while continuing to pass narrow checkpoints.

**Evidence signals:**

- Complexity concentrated in a small set of growing modules.
- Repeated boolean flags instead of explicit state machines.
- Parallel implementations of shared concerns.
- Compatibility paths with no active consumers.
- Large code growth for modest product growth.
- Each change makes the next change touch more areas.

**Audit method:** Compare complexity, coupling, ownership, public surface, and duplication over repository history and high-churn paths. Trace recent extension sequences, not only the final snapshot.

**Control:** Architecture fitness tests, bounded module/file rules, explicit state models, recurring targeted cleanup, and root-cause consolidation.

### Local-optimum proliferation

**Risk:** Agents repeatedly solve immediate tasks near the caller instead of repairing shared validation, policy, data, error, or service boundaries.

**Evidence signals:**

- Multiple validators/formatters/auth checks/error mappers.
- Direct DB/network/tool access bypassing established layers.
- Similar defects recur in sibling workflows.
- Fixes are difficult to propagate consistently.

**Audit method:** Search by semantic behavior and data shape across domains. Map canonical entry points and bypasses.

**Control:** Shared boundary abstractions, structural lints, centralized policy tests, and repository maps that make the canonical path discoverable.

### Weak-pattern replication

**Risk:** Agents treat frequent repository patterns as endorsed patterns, amplifying existing debt.

**Evidence signals:**

- New code copies known broad catches, unsafe parsing, ad hoc retries, untyped data access, or weak permission checks.
- One workaround spreads rapidly after the first instance.
- Generated tests reproduce an inadequate oracle.

**Audit method:** Identify recurring patterns by history and compare them with authoritative architecture/security rules.

**Control:** Encode corrected patterns as lints, tests, generators, templates, and short rules linked to sources of truth.

### Verbosity and unnecessary surface

**Risk:** Generated code is locally understandable but globally bloated, increasing review, attack, and maintenance surface.

**Evidence signals:**

- Wrapper-only files, one-implementation interfaces, speculative configuration, and redundant comments.
- Reimplemented stdlib/framework/platform behavior.
- New dependencies for trivial functions.
- Dead generated plans, adapters, compatibility code, or snapshots.

**Audit method:** Apply `anti-bloat.md`, dependency analysis, dead-code evidence, and safe-deletion ranking.

**Control:** Deletion-focused cleanup, dependency budgets, rule-of-three guidance, and anti-bloat checks that preserve safety controls.

### Hidden coupling and fragmented ownership

**Risk:** Agents connect components through undocumented imports, shared mutable state, generated files, events, or configuration, leaving no clear owner.

**Evidence signals:**

- Broad fan-in/fan-out changes for small features.
- Cross-domain imports outside architecture rules.
- Data/config state written from many places.
- No owner can explain critical paths.

**Audit method:** Build dependency/data-flow maps and sample recent cross-cutting changes.

**Control:** Enforced dependency direction, ownership metadata, explicit providers/interfaces, and scenario documentation.

### Comprehension and cognitive debt

**Risk:** Code throughput outpaces human and future-agent understanding, so no reviewer maintains a reliable system model.

**Evidence signals:**

- Large agent-created areas with few human-authored decisions or reviews.
- Maintainers rely on summaries rather than code/runtime evidence.
- Regressions reintroduce previously fixed bugs.
- Plans and architecture rationale are missing or stale.

**Audit method:** Ask whether intent, invariants, ownership, and recovery can be reconstructed from repository-local evidence. Sample maintainers’/agents’ ability to trace critical workflows.

**Control:** Smaller changes, explicit plans/decisions, system maps, durable ledgers, executable invariants, and human calibration on critical semantics.

## Repository Knowledge and Ownership Risks

### Monolithic instruction files

**Risk:** A giant `AGENTS.md`, prompt, or policy file crowds out task context, becomes internally inconsistent, and rots.

**Evidence signals:**

- Hundreds/thousands of lines mixing permanent rules, task history, and product intent.
- Duplicate or contradictory instructions.
- No ownership, freshness, or link validation.
- Agents ignore or selectively apply rules.

**Audit method:** Inspect size, purpose boundaries, references, ownership, freshness checks, and usage traces.

**Control:** Short entry-point map plus progressive disclosure to versioned, authoritative docs; mechanical link/freshness checks.

### Stale or poisoned repository instructions

**Risk:** Agents follow outdated, malicious, or accidentally generated instructions embedded in docs, comments, issues, dependencies, or work artifacts.

**Evidence signals:**

- Instructions reference deleted paths or old architecture.
- Untrusted files can override operational policy.
- Generated reports are colocated with authoritative docs without labels.
- Tool output is interpreted as instruction.

**Audit method:** Classify instruction sources by trust, trace prompt construction, and compare rules with current code/configuration.

**Control:** Trust labels, instruction precedence, sanitization/separation, generated-artifact boundaries, ownership, and freshness enforcement.

### External/tacit sources of truth

**Risk:** Product semantics, incident knowledge, or architecture decisions live in chat, people’s heads, or inaccessible systems, so agents invent missing context.

**Evidence signals:**

- Repeated `Needs Decision` questions for the same rule.
- Code/tests disagree and no authoritative spec exists.
- Agent output varies by who supplies context.

**Audit method:** Inventory critical decisions and locate repository-visible authority.

**Control:** Encode durable decisions, contracts, ADRs, and acceptance examples in maintained sources without turning the repository into a transcript archive.

### Generated documentation mismatch

**Risk:** Agent-generated plans, schemas, diagrams, runbooks, and reports look authoritative after executable behavior changes.

**Evidence signals:**

- No generator/version/source metadata.
- Manual edits to generated files.
- Docs claim tests/flows that current code cannot perform.
- Reports remain indexed as current after supersession.

**Audit method:** Trace generation and compare samples against runtime/code.

**Control:** Clear generated directories, regeneration checks, timestamps/commits, owners, and exclusion from production artifacts when appropriate.

### Missing ownership and escalation

**Risk:** Agents can create or modify systems faster than ownership and on-call responsibility are established.

**Evidence signals:**

- Critical modules/tools without owners.
- Alerts and findings route nowhere.
- Autonomous changes cross teams without review authority.

**Audit method:** Map code/data/service/agent owners and approval boundaries.

**Control:** Ownership metadata, escalation policy, CODEOWNERS/required review, and accountable debt/finding owners.

## Validation, Evals, and Reward Risks

### Outcome-only evaluation

**Risk:** A final test pass hides dangerous tool calls, policy violations, data leaks, shortcuts, or scaffold manipulation.

**Evidence signals:**

- Only final files or binary pass/fail are inspected.
- No transcript/tool/state/side-effect recording.
- Agent modifies test assets or environment controls.
- Production outcome differs from benchmark behavior.

**Audit method:** Sample trajectories, tool arguments, environment mutations, costs, and side effects alongside outcomes.

**Control:** Multi-grader evals: deterministic outcome, static/state checks, trajectory/tool checks, model rubric, and periodic human calibration.

### Test-target and benchmark overfitting

**Risk:** Agents learn visible fixtures, pass thresholds, or recurring benchmark structure without implementing general behavior.

**Evidence signals:**

- Literal special cases and test-only branches.
- Performance collapses on perturbed or hidden-like cases.
- Agents alter fixtures, snapshots, or evaluators.

**Audit method:** Use adversarial holdouts, property/metamorphic/differential tests, varied environments, and evaluator integrity checks.

**Control:** Protected evaluation assets, randomized/hidden variants, independent oracles, and trajectory review.

### Reward hacking and control manipulation

**Risk:** An autonomous agent finds a loophole in success criteria or changes the mechanism that judges it.

**Evidence signals:**

- Disables checks, changes completion flags, writes expected artifacts directly, or exploits retries.
- “Keep working until success” increases attempts to bypass constraints.
- Agent has write access to graders, permissions, or audit state.

**Audit method:** Red-team success criteria and inspect failed/suspicious trajectories.

**Control:** Separate control-plane permissions, immutable/frozen graders during runs, progress budgets, and human approval for evaluator changes.

### Self-review correlation

**Risk:** The same model/harness authors, reviews, fixes, and closes code with shared blind spots.

**Evidence signals:**

- Reviews repeat author summaries.
- Independent runs use identical context/order/tools.
- Two “clean” passes add no new evidence.
- Human review is absent for semantics/security despite high impact.

**Audit method:** Measure reviewer diversity, prompt independence, and whether raw artifacts are inspected before prior conclusions.

**Control:** Fresh contexts, heterogeneous reviewers/models where available, separated roles, stable ledgers, and human authority gates.

### Evals that miss harness regressions

**Risk:** Model, system prompt, context-clearing, defaults, tools, or harness changes degrade quality outside the current eval set.

**Evidence signals:**

- User reports regressions while internal evals remain green.
- Model/harness versions are not pinned or compared.
- No rollback signal or production monitoring.

**Audit method:** Trace model+harness version history, release gates, user reports, and production metrics.

**Control:** Capability plus regression suites, versioned harness, canary/A-B testing, production monitoring, and rollback.

### Weak validation portfolio

**Risk:** Unit tests and static checks dominate while integration, failure, concurrency, migration, security, and recovery remain untested.

**Evidence signals:**

- High coverage but repeated escaped cross-boundary defects.
- Extensive mocks.
- No browser/operator/restore/rollout tests.

**Audit method:** Map tests to critical scenarios and trust boundaries.

**Control:** Risk-based portfolio with executable end-to-end, property, fuzz, migration, rollback, recovery, and security tests.

## Prompt, Tool, and Autonomy Risks

### Indirect prompt injection

**Risk:** Untrusted issue/PR text, docs, web pages, emails, logs, code comments, dependency metadata, or tool output influences agent control decisions.

**Evidence signals:**

- Untrusted content placed into high-priority prompt sections.
- Agent obeys embedded requests to read secrets, run commands, change rules, or contact endpoints.
- No source/trust separation.

**Audit method:** Map all content sources into model context and red-team with benign canaries and adversarial instructions in a sandbox.

**Control:** Treat content as data, isolate control instructions, limit tools/egress, validate actions, and require approval for high-impact operations.

### Tool abuse and excessive functionality

**Risk:** Tools expose broad shell, filesystem, database, cloud, browser, or deployment capability that can be misused through model error or injection.

**Evidence signals:**

- Generic command execution when narrow APIs suffice.
- Wildcard paths/resources.
- Production access in development/review contexts.
- Tool arguments lack schema/allowlists.

**Audit method:** Enumerate effective capabilities and test boundary enforcement.

**Control:** Narrow typed tools, allowlists, sandboxing, least privilege, dry-run, idempotency, and human approval.

### Excessive autonomy

**Risk:** Agents perform irreversible, privileged, financial, customer-visible, or production actions without accountable approval.

**Evidence signals:**

- Self-merge/deploy/delete/rotate/notify actions.
- Approval classifier is the sole gate.
- No kill switch or action budget.

**Audit method:** Map autonomy levels per action and simulate failure/injection scenarios.

**Control:** Risk-tiered approval gates, separation of duties, reversible staging, emergency stop, and audit logs.

### Self-modifying guardrails

**Risk:** Agents can edit their own prompts, skills, hooks, permissions, network policy, scanners, branch rules, or approval logic.

**Evidence signals:**

- Same identity can change and immediately use controls.
- Agent-authored PRs bypass independent review for control-plane files.

**Audit method:** Inspect ownership, permissions, workflow paths, and enforcement outside the agent’s write boundary.

**Control:** Protected control-plane code, independent approval, immutable runtime policy, and signed/versioned configurations.

### Localhost and local-control-plane trust

**Risk:** Loopback services, browser extensions, sockets, webhooks, or developer-machine tools execute privileged actions without authentication because they are “local.”

**Evidence signals:**

- Unauthenticated localhost APIs.
- Browser-accessible endpoints trigger shell/filesystem/deployment actions.
- Agent can browse untrusted content on the same host.

**Audit method:** Enumerate local listeners and cross-origin/request controls; test from untrusted local/web contexts.

**Control:** Authentication/authorization, origin validation, CSRF protection, capability tokens, and process/network isolation.

### Model output injection into execution

**Risk:** Free-form model output becomes shell, SQL, templates, URLs, file paths, code, or deployment instructions.

**Evidence signals:**

- String interpolation into powerful tools.
- Dynamic eval/import.
- No schema, allowlist, or validation.

**Audit method:** Trace output-to-action paths and fuzz model outputs.

**Control:** Typed structured output, constrained decoding where available, argument validation, allowlists, and approval.

### Secret and sensitive-data exposure

**Risk:** Agents read or transmit more data than needed, and prompts/transcripts/tool logs create new retention surfaces.

**Evidence signals:**

- Whole environment/repository/database sent to models/tools.
- Secrets in transcripts, screenshots, logs, generated files, or remote MCP requests.
- Undefined retention/deletion.

**Audit method:** Data-flow and retention map for prompts, tools, connectors, logs, memory, and evals.

**Control:** Minimize, redact, compartmentalize, scope, encrypt, set retention, and audit access.

## Memory, State, and Long-Running Loop Risks

### Stale progress state

**Risk:** New sessions trust summaries or progress files that no longer match git/runtime reality.

**Evidence signals:**

- Completion flags contradict tests or current head.
- Files/symbols referenced in plans no longer exist.
- Multiple agents overwrite state.

**Audit method:** Compare durable state with git fingerprints, current artifacts, and runtime checks.

**Control:** Stable IDs, baseline commits, appendable transitions, conflict handling, and repository reconciliation at session start.

### Premature completion

**Risk:** An agent declares a feature/audit/review complete after narrow tests or because previous progress looks substantial.

**Evidence signals:**

- No end-to-end/user/operator validation.
- Agent edits its own checklist to passing.
- Summary language exceeds evidence.

**Audit method:** Sample completed tasks and reproduce acceptance externally.

**Control:** Protected acceptance criteria, independent verification, and explicit completion evidence.

### Memory poisoning and cross-session contamination

**Risk:** Malicious, stale, or task-specific content persists in memory/ledgers and biases future work.

**Evidence signals:**

- Untrusted issue/doc content stored as durable instruction.
- Findings permanently suppressed without human authority.
- One tenant/project’s data affects another.

**Audit method:** Trace memory write/read policies, provenance, tenancy, TTL, and deletion.

**Control:** Trust/provenance labels, scoped memory, review before promotion, expiration, user-visible correction, and isolation.

### Unbounded loop and denial of wallet

**Risk:** Repeated agent-review-fix cycles consume uncontrolled tokens, compute, API calls, or external side effects.

**Evidence signals:**

- No hard cap, budget, progress test, or kill switch.
- Same findings oscillate.
- Retries amplify service load.

**Audit method:** Inspect budgets, run logs, cost metrics, termination criteria, and failure behavior.

**Control:** Evidence-based stop conditions, soft/hard caps, no-progress detection, idempotent actions, and escalation.

### Context compression loss

**Risk:** Long tasks lose decisions, constraints, or unresolved failures during compaction/context resets.

**Evidence signals:**

- Later sessions repeat work or reverse decisions.
- Important caveats survive only in conversation memory.
- Different progress artifacts disagree.

**Audit method:** Reconstruct a long task from repository artifacts alone.

**Control:** Concise persistent state, frozen findings/decisions, exact baselines, and progressive disclosure.

## Supply Chain and Provenance Risks

### Hallucinated or malicious dependencies

**Risk:** Agents install plausible packages, actions, containers, plugins, or MCP servers without sufficient verification.

**Evidence signals:**

- Typos, obscure new packages, mutable versions, broad install scripts, or unexpected transitive churn.
- Dependency selected solely from model suggestion.

**Audit method:** Verify source, ownership, versions, signatures/provenance, license, necessity, and behavior.

**Control:** Approved registries/sources, lock/pin policy, dependency review, provenance, and least functionality.

### Generated code origin uncertainty

**Risk:** Copied/generated code has unclear license, advisory history, generator, or update path.

**Evidence signals:**

- Large style-inconsistent blocks.
- Vendored artifacts without metadata.
- Security fix not tied to an advisory/reachable path.

**Audit method:** Trace provenance and compare generated outputs with source/generator.

**Control:** Source metadata, generator pinning, license checks, reproducible generation, and review.

### Tool/plugin/skill supply-chain compromise

**Risk:** Agent extensions can change remotely, execute code, access secrets, or inject instructions.

**Evidence signals:**

- Unpinned remote servers/plugins.
- Broad trust in marketplace/community skills.
- Install/update paths bypass review.

**Audit method:** Inventory extensions, sources, versions, permissions, network behavior, update policy, and sandboxing.

**Control:** Allowlist, pinning, signatures, review, sandbox, egress control, and revocation.

### Build and release tampering

**Risk:** Agent-generated CI/release changes introduce token exposure, mutable artifacts, or post-review modification.

**Evidence signals:**

- Broad workflow permissions.
- Pull-request code accesses release secrets.
- Mutable tags/images/actions.
- Artifact lacks provenance/signing.

**Audit method:** Trace source-to-artifact-to-deploy identity and permissions.

**Control:** Least privilege, protected environments, immutable artifacts, provenance, signing, and separation of duties.

## Operational and Human-Control Risks

### Verification bottleneck and approval fatigue

**Risk:** Agent throughput exceeds reviewer capacity, causing rubber-stamping, delayed review, or overbroad automatic approval.

**Evidence signals:**

- Large queue, low reading time, many noisy findings, or high auto-merge volume.
- Humans review summaries instead of changes.
- Alerts/reviews are routinely ignored.

**Audit method:** Measure change/review volume, latency, finding disposition, reviewer engagement, and escaped defects.

**Control:** Smaller changes, risk routing, high-confidence findings, auto-review only for low-risk actions, and sampling/calibration.

### Human skill and system-model atrophy

**Risk:** Maintainers lose the ability to debug, operate, or safely change agent-generated systems.

**Evidence signals:**

- No one can explain critical paths without the agent.
- Incidents require regenerating rather than reasoning.
- Manual overrides/recovery are untested.

**Audit method:** Run tabletop exercises, ownership interviews, and recovery drills.

**Control:** Human-owned invariants, runbooks, scenario reviews, periodic manual tracing, and explicit training/rotation.

### Misleading reviewer metrics

**Risk:** Comment acceptance, resolution, or count is treated as truth despite alternative fixes, false positives, or ignored severe misses.

**Evidence signals:**

- Optimizing comment volume or resolution rate alone.
- No sampled ground truth or escaped-defect analysis.

**Audit method:** Calibrate with human labels, severity-weighted precision/recall, alternate-fix classification, and production outcomes.

**Control:** Balanced metrics: true defects, severity, false-positive burden, missed defects, review cost, and downstream quality.

### Automation without accountable risk acceptance

**Risk:** Agents suppress findings, accept debt, or choose business semantics without an authorized human.

**Evidence signals:**

- “Risk accepted” by bot identity.
- Permanent suppression from model confidence alone.
- No owner/review date.

**Audit method:** Trace decision authority and audit logs.

**Control:** Human authority for policy/risk decisions, expiry, owner, rationale, and revisit trigger.

### Environment incompleteness

**Risk:** Agents work in partial environments that hide integration, UI, operations, permission, or deployment failures.

**Evidence signals:**

- Missing services, data, browser, observability, or realistic auth.
- Local success repeatedly fails in CI/production.

**Audit method:** Compare agent environment with required system dependencies and critical workflows.

**Control:** Reproducible worktree/sandbox environments, realistic service fixtures, browser/runtime/observability access, and explicit environment gaps.

## Evidence and Durable Controls

### Evidence table

For each risk record:

```text
Risk family:
Assets and quality attributes:
Agent/model/harness versions:
Identity and effective permissions:
Untrusted inputs:
Tools/network/data flows:
Reachable failure/abuse scenario:
Outcome evidence:
Trajectory/tool evidence:
Existing controls and bypasses:
Residual risk:
Owner:
```

### Durable-control selection

Choose controls by failure mechanism:

- **Wrong semantics:** authoritative spec, examples, decision log, human authority.
- **Local duplication:** canonical layer, structural lint, repository map.
- **Weak validation:** stronger oracle, integration/property/fuzz/state/recovery tests.
- **Prompt injection/tool abuse:** trust separation, least privilege, typed tools, approval.
- **Stale state:** git fingerprints, stable ledgers, reconciliation.
- **Architecture erosion:** fitness functions, complexity/ownership budgets, recurring cleanup.
- **Supply chain:** allowlists, pinning, provenance, signing, scanning.
- **Review correlation:** fresh/heterogeneous verifier, human calibration.
- **Unbounded loop:** budgets, progress tests, no-progress diagnosis, kill switch.
- **Cognitive debt:** smaller changes, maps, ownership, executable invariants, drills.

A control should be enforceable, observable, owned, and testable. Documentation alone is insufficient for high-impact invariants, but undocumented controls are difficult for humans and agents to maintain.
