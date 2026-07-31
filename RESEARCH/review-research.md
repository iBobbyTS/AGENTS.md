# Code Review Skill Research

Research date: 2026-07-15  
AI-agent source window: 2025-07-15 through 2026-07-15  
Output target: `code-review/SKILL.md` and its `references/` directory  
Source details: [source-register.md](source-register.md)

## Contents

1. [Executive Conclusion](#executive-conclusion)
2. [Research Question and Boundary](#1-research-question-and-boundary)
3. [Research Method](#2-research-method)
4. [Diagnosis of the Existing Loop](#3-diagnosis-of-the-existing-loop)
5. [Traditional Review Surface](#4-traditional-review-surface)
6. [AI-Agent-Specific Review Risks](#5-ai-agent-specific-review-risks)
7. [Making One Agent Find More in One Pass](#6-making-one-agent-find-more-in-one-pass)
8. [Current Vendor Quality-Control Patterns](#7-current-vendor-quality-control-patterns)
9. [Loop Engineering](#8-loop-engineering-what-it-solves-and-what-it-creates)
10. [Derived Review Loop](#9-derived-review-loop)
11. [Preventing Review-Created Technical Debt](#10-preventing-review-created-technical-debt)
12. [Skill Architecture Produced](#11-skill-architecture-produced)
13. [Alternatives Rejected](#12-alternatives-rejected)
14. [Limitations and Validation Needs](#13-limitations-and-validation-needs)
15. [References](#references)

## Executive Conclusion

The expensive part of the existing workflow is not that it permits many rounds. It is that each round reopens nearly the same complete review surface, while discovery, repair, and self-verification remain coupled. Repetition can still find additional issues, but it spends most of its budget rediscovering context and produces correlated confidence rather than independently verified coverage.

The replacement design uses:

1. One broad, staged discovery pass over the original bounded change.
2. Explicit review lenses selected from the change's actual risk boundaries.
3. Candidate generation before repair, followed by evidence-based falsification.
4. Stable finding IDs and root-cause deduplication.
5. A human decision gate for product or risk semantics.
6. Batched repairs followed by delta-and-impact-cone review, not routine whole-diff rescans.
7. Full-review reset triggers for material semantic or architectural expansion.
8. One fresh-context adversarial verifier near the end.
9. Evidence-based stop conditions and a convergence diagnosis at the hard cap.
10. Promotion of recurring issue classes into tests, lints, shared boundaries, or repository rules.

This preserves the reason the original loop sometimes finds a dozen real defects, while eliminating most unchanged-surface rereading.

## 1. Research Question and Boundary

### 1.1 Review use case

The review skill is for one bounded change:

- A pull request.
- A commit range.
- Staged or unstaged changes.
- A large implementation wave before merge.
- A repair-enabled merge-readiness loop.

It is not a periodic whole-system assurance process. Long-lived system maps, rotating audit coverage, recovery controls, and repository-wide debt belong to the audit skill.

### 1.2 Questions investigated

- Which traditional review areas remain mandatory?
- Which review areas should be activated only by risk triggers?
- What failure patterns are unusually common or newly important in agent-authored changes?
- How can one reviewer produce more high-quality candidates in the first pass?
- When does a second or fresh agent add real independence?
- What should be re-reviewed after a repair?
- Which conditions invalidate the initial review and require a reset?
- How should the loop stop without relying on arbitrary repeated empty scans?
- How should repeated findings improve the repository instead of consuming the same review budget again?

### 1.3 Non-goals

- Do not rank coding-agent products.
- Do not infer that suspicious code style proves AI authorship.
- Do not convert a code smell into a blocker without a reachable impact.
- Do not replace deterministic checks with an LLM reviewer.
- Do not require multiple agents for every trivial change.
- Do not claim whole-codebase assurance from a bounded review.

## 2. Research Method

### 2.1 Input analysis

The existing review skill already had strong foundations:

- A bounded-change contract.
- Small, medium, and large review modes.
- Correctness, security, data, operations, testing, and maintainability coverage.
- AI-aware checks for CI weakening, reuse blindness, hallucinated APIs, dependencies, over-mocking, local-optimum patches, and agent permission boundaries.
- Evidence-oriented findings and an explicit merge decision.

The main structural problem was density and loop semantics. Most coverage lived in one large skill body, and the orchestration model encouraged another independent full review rather than a durable first-pass ledger followed by scoped invalidation.

### 2.2 Search tracks

The research was split into four tracks:

| Track | Question | Primary sources |
| --- | --- | --- |
| Traditional review | What should a senior reviewer inspect regardless of authorship? | Google Engineering Practices, OWASP secure review, vulnerability-review research. |
| Current agent failures | What changes when agents write or review code at high volume? | 2025–2026 empirical studies and security benchmarks. |
| Vendor controls | What are current coding-agent systems doing to improve quality and convergence? | OpenAI, Anthropic, Cursor, GitHub, and Google/DORA engineering material. |
| Practitioner loops | What do loop users report as benefits and failure modes? | Current practitioner articles and community discussions. |

### 2.3 Evidence grading

- Standards and established engineering guidance define durable review surfaces.
- Empirical work supports risk hypotheses, but each study's population and measurement limits are preserved.
- Vendor posts are used for current design patterns, not neutral product-quality estimates.
- Community reports are used only to generate hypotheses that the reviewer must verify in repository reality.

### 2.4 Date handling

All AI-agent-specific sources were checked against the 2025-07-15 cutoff. Older sources were used only for stable traditional code-review or security-review practice. An influential early Ralph-loop article dated immediately before the cutoff was explicitly excluded.

## 3. Diagnosis of the Existing Loop

The original loop can be summarized as:

```text
full review -> classify -> fix -> full review -> fix -> ...
complete after two consecutive empty reviews
```

### 3.1 What it gets right

- Fresh subagents reduce direct anchoring on the previous reviewer's explanation.
- Multiple passes can expose issues missed by a single stochastic run.
- Separating business decisions from mechanical repairs prevents the agent from inventing product policy.
- Requiring consecutive clean rounds is more conservative than accepting the first “looks good.”
- The loop continues until code, not only prose, has changed.

### 3.2 Why it becomes slow

| Failure | Cost |
| --- | --- |
| Every round rebuilds the entire diff and repository context. | High repeated token and tool cost. |
| Review lenses are not recorded as completed or invalidated. | The next agent cannot distinguish new risk from already verified scope. |
| Findings lack stable root-cause identity across rounds. | Duplicate symptoms appear as “new” work. |
| The same review prompt is used even after scope narrows to a few repairs. | The search surface remains much larger than the changed evidence. |
| Repair and closure happen in one local reasoning chain. | The fixer can rationalize its own patch or silently weaken the finding. |
| “Two empty reviews” is the oracle. | It measures repeated agreement, not whether required risks and evidence were covered. |
| Round caps are numeric rather than diagnostic. | A loop can oscillate until an arbitrary threshold without identifying the missing requirement, oracle, environment, or architecture decision. |
| Recurring failures remain review comments. | The repository does not become easier to review next time. |

### 3.3 Why the same subagent is not the core issue

Using the same agent identity is risky only when it preserves the same assumptions, owns both the patch and the acceptance decision, or receives no phase boundary. A single agent can still perform a useful first pass if it:

- Separates divergent candidate generation from convergent validation.
- Freezes findings before repair.
- Attempts to disprove its candidates.
- Uses repository and runtime evidence.
- Revalidates from the current diff rather than its prior narrative.
- Defers final closure to a fresh verifier for high-risk changes.

Conversely, several fresh agents can still share correlated blind spots, especially with the same model family, same prompt, same tests, and same repository assumptions (C-02). Independence must come from different evidence, risk lenses, or stop authority—not merely a new process ID.

## 4. Traditional Review Surface

The new skill expresses the traditional surface as a baseline plus triggered lenses. This prevents both under-review and a giant checklist on every change.

### 4.1 Always-on baseline

| Lens | Core questions | Minimum evidence |
| --- | --- | --- |
| Intent fidelity | Does the change implement the requested behavior and no unrelated policy? | Requirement, issue, tests, callers, UI/API behavior, explicit non-goals. |
| Local correctness | Are branches, defaults, boundaries, errors, and cleanup correct? | Diff plus necessary unchanged context; targeted tests or trace. |
| Scope and complexity | Is every changed area needed? Did states, branches, dependencies, or public surface grow unnecessarily? | Changed-file map, existing project patterns, alternative smaller path. |
| Verification integrity | Would a regression test fail before the fix? Do assertions prove behavior rather than implementation? | Test diff, CI configuration, executed checks, missing oracle. |
| Security basics | Did the change alter inputs, outputs, secrets, logging, permissions, or dynamic execution? | Trust-boundary trace and relevant negative case. |
| Repository consistency | Does it extend the existing owner or create a parallel abstraction? | Search for same-purpose utilities, services, validators, hooks, and conventions. |

### 4.2 Triggered lenses

| Trigger in the change | Activate deep review of |
| --- | --- |
| Product rules, eligibility, pricing, moderation, workflow states | Domain semantics, legal transitions, source of truth, ambiguous policy. |
| Schema, query, migration, cache, serialization, retention | Compatibility, transactional behavior, data loss, rollback, consistency, privacy lifecycle. |
| Async task, queue, retry, timer, event, shared state | Races, cancellation, stale writes, ordering, idempotency, partial failure, cleanup. |
| Auth, tenant, object access, file/URL/command input | Authentication, authorization on every path, isolation, injection, SSRF, path traversal, output encoding. |
| API/public contract/config/env | Backward/forward compatibility, version mixtures, validation, defaults, consumers, documentation. |
| Deployment, feature flag, CI, release script | Rollout, rollback, emergency disable, permission scope, secrets, required checks, observability. |
| Performance-sensitive loop/query/payload | Complexity, N+1, pagination, capacity, quotas, memory, latency, cost, degradation behavior. |
| New dependency/build change | Necessity, package identity, license, maintenance, transitive risk, lockfile, provenance, build scripts. |
| UI or interaction | Loading/empty/error/disabled states, accessibility, localization, destructive actions, responsive behavior. |
| Agent/MCP/plugin/prompt/permission change | Untrusted instructions, tool scope, secret/data exposure, approval gates, memory, self-modifying controls. |

### 4.3 Review standard

Google's review guidance supports evaluating design, functionality, complexity, tests, naming, comments, documentation, and context while improving overall code health rather than demanding perfection (R-01, R-02). Small, focused changes remain easier to understand and validate (R-03).

Security review needs an explicit mindset. A controlled study found that asking reviewers to focus on security materially increased vulnerability detection, while adding a tailored checklist did not significantly improve the outcome further (R-05). The design implication is not to remove checklists; it is to make “security adversary” a distinct reasoning phase rather than expecting a long mixed checklist to create the mindset automatically.

## 5. AI-Agent-Specific Review Risks

These patterns are not exclusive to AI code. They become more important when code is generated quickly, locally optimized, and repeatedly extended.

| Risk family | Typical manifestation | Why ordinary diff reading may miss it | Review response |
| --- | --- | --- | --- |
| Plausible but invented semantics | Coherent defaults or edge-case policy unsupported by product evidence. | Syntax and tests can look complete. | Reconstruct invariants; classify ambiguity as `Needs Decision`. |
| Local-optimum patch | Direct DB/network/state access bypasses a shared policy or owner. | The touched path works in isolation. | Trace the established entry point and impact cone. |
| Reuse blindness | New helper/service/hook/validator duplicates existing behavior. | Each local implementation is readable. | Search same-purpose symbols before accepting a new abstraction. |
| Structural erosion | Successive changes concentrate branches/state in one area or add redundant scaffolding. | Every checkpoint can still pass. | Compare state/branch/public-surface growth; apply simplification pass. |
| Test accommodation | Tests are rewritten to match implementation, over-mocked, or assert generated structure. | CI is green. | Seek a pre-fix failing regression and real contract/integration evidence. |
| Hallucinated interface | Invented API, option, environment key, database field, package, or CLI flag. | Code is syntactically plausible. | Verify local definition or authoritative current documentation. |
| Compatibility theater | Fallbacks, aliases, dual paths, or swallowed errors without real consumers. | Looks defensive. | Identify concrete compatibility requirement, owner, and removal trigger. |
| Scope explosion | Adjacent refactors, dependency upgrades, or feature completion mixed into a narrow task. | Agent frames it as helpful cleanup. | Account for every changed file and split unrelated work. |
| CI/security weakening | Skips, threshold reductions, softened commands, workflow trigger changes, broader tokens. | Patch can “fix” a failing build. | Treat validation posture as a first-class diff and block unjustified weakening. |
| Context drift | Agent relies on stale plans, summaries, or earlier file layout. | The final prose can be confident. | Reconcile `git status`, diff, current docs, and runtime before judgment. |
| Self-review closure | Fixer says its patch resolves the issue without independent evidence. | Explanation is internally consistent. | Freeze acceptance criteria; require code-visible evidence and fresh/phase-separated verification. |
| Narrative manipulation | PR description, urgency, prior approval, or claimed test result lowers scrutiny. | Review agent treats surrounding text as trusted context. | Extract claims, then verify each against repository evidence; never let narrative override the diff. |
| Tool/autonomy escalation | Agent gains write tokens, network access, MCP tools, or ability to change its own gates. | Tooling is treated as developer convenience. | Review as privileged infrastructure with least privilege and separate approval. |
| Comprehension debt | Large generated change is mergeable only because no human or future agent understands the ownership model. | Functional tests may pass. | Require repository-local intent, architecture, and high-risk workflow evidence. |

Empirical work reinforces the need for these hypotheses without proving that every agent change has them:

- A 2026 study of 33,000 agent-authored PRs found that unmerged PRs tended to be larger, touch more files, fail CI more often, and include socio-technical issues such as unwanted or duplicate work and misalignment (E-02).
- A large-scale preprint over verified AI-authored commits reported that more than 15% of commits from each studied assistant introduced at least one statically detected issue and that 22.7% of tracked issues persisted to the latest studied revision (E-01). Static-analysis findings are not identical to user defects, but persistence supports durable debt tracking.
- A long-horizon benchmark found agents could pass intermediate checkpoints while accumulating structural erosion and verbosity (E-03).
- A review-conversation study reported much lower adoption of agent suggestions than human suggestions and larger measured complexity/size increases for adopted agent suggestions; it also identified project-specific knowledge transfer as a relative weakness (E-04). The study does not measure system-wide architecture or security, so the skill uses it only to justify project-knowledge retrieval and simplification checks.
- Sevra-Bench showed that current review agents can be influenced by deceptive PR narratives, supporting explicit separation of claims from code evidence (E-05).

## 6. Making One Agent Find More in One Pass

The goal is not “think longer.” It is to change the search protocol so one context explores different failure families before anchoring on a fix.

### 6.1 Use a divergent-then-convergent protocol

```text
intent/invariants
    -> change map and impact cone
    -> independent risk-lens hypotheses
    -> evidence-based falsification
    -> root-cause deduplication
    -> only then repair/decision
```

During divergent discovery:

- Do not edit code.
- Do not stop after the first convincing issue.
- Generate failure hypotheses per triggered lens.
- Prefer boundary values, illegal state transitions, partial failures, adversarial inputs, retries, rollback, and stale data.
- Trace at least one critical workflow end to end for medium/large changes.

During convergence:

- State the violated invariant.
- Prove a reachable trigger.
- Attempt to disprove the concern.
- Run the smallest relevant experiment.
- Discard speculative low-confidence items.
- Merge repeated symptoms into one root cause.

This creates more breadth without multiplying complete agents.

### 6.2 Build the review map before line-by-line reading

A reviewer should first identify:

- Entry points and externally visible behavior.
- Public contracts, schemas, migrations, and compatibility consumers.
- State owners, queues, jobs, side effects, and transactional boundaries.
- Auth, permissions, tenant boundaries, files, URLs, and command execution.
- Configuration, CI, deployment, observability, and rollback.
- Direct callers/callees and shared abstractions.

The map turns “review all files” into a set of falsifiable paths and reveals unchanged code whose assumptions can be invalidated.

### 6.3 Explicitly switch mental models

Do not rerun “review this PR.” Use distinct lenses:

1. Product owner/domain model: Is this the right behavior?
2. State-machine/concurrency reviewer: Can ordering, retry, or partial failure violate invariants?
3. Security adversary: How can an untrusted actor cross the boundary?
4. Operator/SRE: How does this roll out, fail, alert, recover, and roll back?
5. Architect/maintainer: Does it preserve ownership and make the next change easier?
6. Test skeptic: What does green CI fail to prove?
7. Agent-harness reviewer: Which claims, tools, permissions, memories, or generated artifacts are untrusted?

The security-review experiment (R-05) supports this explicit mindset shift more strongly than simply appending more checklist items.

### 6.4 Use stronger test oracles

Example tests sample known cases. For high-risk deterministic logic, ask the reviewer to infer properties and search for counterexamples:

- Serialize/deserialize round trips.
- Idempotency under duplicate delivery.
- Monotonicity or conservation rules.
- Authorization invariance under object identifiers and tenant changes.
- Ordering independence where required.
- No negative or impossible domain values.
- Metamorphic relations across equivalent inputs.

Anthropic's property-based testing work demonstrates a current agent workflow that reads code/docs, proposes properties, writes tests, runs them, and then questions whether a failure is a real defect or a bad property (V-07). The skill therefore recommends property/metamorphic tests selectively, followed by manual validation of findings.

### 6.5 Make repository knowledge retrievable

A generic reviewer cannot reliably infer local policy. Improve first-pass recall by giving it:

- A short repository entry point that routes to architecture, product, reliability, security, and test sources.
- Current migrations/schema/docs rather than copied summaries.
- Existing helper/service/validator search paths.
- Known quality rules and authoritative examples.
- Prior accepted human decisions, but not prior suspected defects during an independent discovery pass.

OpenAI's current harness report argues for a map rather than a monolithic instruction manual and for mechanically enforced repository knowledge (V-01). The review skill mirrors that pattern through progressive references rather than one huge `SKILL.md`.

### 6.6 Treat narratives as claims

Read PR descriptions, plans, test summaries, and prior comments, but convert every material statement into a claim:

| Claim | Verification |
| --- | --- |
| “Backward compatible” | Enumerate consumers/version mixtures and inspect contracts. |
| “Only tests changed” | Compare executable/build behavior and fixtures. |
| “Safe fallback” | Trace failure path and whether it masks an error. |
| “All checks pass” | Inspect actual check status/output and required workflow triggers. |
| “No migration needed” | Compare schema/data assumptions and deployed versions. |
| “Already approved” | Check current unresolved threads and authoritative approval state. |

This directly addresses the review-agent manipulation studied by Sevra-Bench (E-05).

### 6.7 Separate finding quality from finding count

Maximizing raw comments creates noise. A high-value finding needs:

- A stable ID.
- One root cause.
- Reachable trigger.
- Violated invariant.
- Material impact.
- Evidence and uncertainty.
- Smallest credible repair.

A broad candidate phase can generate many hypotheses; the validation phase should aggressively delete unsupported ones.

## 7. Current Vendor Quality-Control Patterns

### 7.1 OpenAI

Current harness guidance emphasizes decomposing complex goals into design, code, review, and test work; treating failures as missing capabilities, context, or guardrails rather than merely asking the agent to try harder; keeping repository knowledge navigable; enforcing architecture mechanically; and turning repeated cleanup into continuous “golden principles” (V-01).

Design consequences:

- The review loop has explicit phases and durable ledgers.
- A recurring finding becomes a control candidate.
- Skill details live in references loaded on demand.
- Runtime/UI/log evidence is preferred over summaries.

### 7.2 Anthropic

Long-running-agent guidance uses persistent progress artifacts, explicit feature state, git history, startup checks, and basic functional verification before new work (V-05). Agent-evaluation guidance combines deterministic tests, LLM rubrics, static analysis, state checks, tool-call expectations, and transcript/cost metrics (V-06).

Design consequences:

- Resume from written state, not conversational memory.
- Reconcile repository reality at the start of each phase.
- Use multiple evidence types for closure.
- Track loop cost and tool behavior, not only final code.

### 7.3 Cursor

Cursor reports an incremental mode that reviews only what is new in a PR and a learned-rule system that derives candidate rules from reactions, replies, and human-missed issues (V-08, V-09).

Design consequences:

- Re-review the repair delta and impact cone by default.
- Do not repeatedly pay for unchanged original hunks.
- Convert repeated false positives and misses into governed project rules.
- Treat vendor metrics as directional; the design does not depend on the reported percentages.

### 7.4 GitHub

GitHub's current coding-agent flow adds automatic security and quality validation and extends validation to third-party coding agents (V-11, V-12).

Design consequence:

- Agent authorship should not create a separate, weaker validation path.
- LLM review is one layer around existing tests, type checks, linters, scanners, and policy checks.

## 8. Loop Engineering: What It Solves and What It Creates

“Loop engineering” is an informal practitioner term for designing an outer system that finds work, delegates it, checks results, persists state, and decides what happens next (C-01). It is useful, but the loop itself is software and must have an oracle, permissions, budgets, and failure handling.

### 8.1 Problems it solves

- Repeated manual prompting and state reconstruction.
- Long-running work that crosses context windows.
- Mechanical iteration on test failures and review feedback.
- Parallel or role-separated discovery, implementation, and verification.
- Persistent progress and auditable decisions.
- Continuous cleanup and policy enforcement.

### 8.2 Problems it can create

| Failure | Mechanism |
| --- | --- |
| Token and latency explosion | Complete agents repeatedly reread unchanged context and execute overlapping tools. |
| Correlated blind spots | Writer, reviewer, and judge share model family, prompt assumptions, tests, and repository gaps. |
| Cognitive surrender | Humans inherit the loop's confidence without understanding the semantic decision. |
| Goal gaming | The agent optimizes visible tests, scanners, or stop conditions rather than intended behavior. |
| Architecture drift | Each iteration adds the locally easiest patch and repeats existing weak patterns. |
| Context contamination | Later reviewers receive prior rationalizations and search for confirmation. |
| Oscillation | Repair A reopens B, repair B reopens A, or an undefined requirement is repeatedly guessed. |
| Permission amplification | An unattended loop can change CI, tokens, deployment, or its own controls. |
| Comprehension debt | High output volume exceeds human ability to understand ownership and invariants. |

Current practitioner writing explicitly recommends maker/checker separation but also warns that multiple model agents can have correlated blind spots and that unattended “done” remains a claim, not proof (C-01, C-02).

### 8.3 Assessment

Loops are strongest for mechanically observable work with a stable oracle. They are weakest when the unresolved issue is product semantics, risk tolerance, architecture tradeoffs, or inaccessible production behavior. Therefore:

- Automate iteration around evidence.
- Escalate judgment rather than asking the loop to guess harder.
- Buy independent fresh-agent passes only at high-risk points.
- Keep a human or accountable authority at semantic and irreversible gates.

## 9. Derived Review Loop

### 9.1 State machine

```text
INITIALIZE
  -> FULL_DISCOVERY
  -> DECISION_GATE
  -> REPAIR_WAVE (optional)
  -> DELTA_VERIFY
       -> REPAIR_WAVE when open fixable findings remain
       -> FULL_DISCOVERY when a reset trigger fires
       -> FINAL_FRESH_VERIFY when closure criteria are met
  -> COMPLETE | BLOCKED
```

### 9.2 Initial discovery

Run exactly one full discovery over the original bounded change unless the baseline changes. It must:

- Fix the base/head and patch fingerprint.
- Reconstruct intent, non-goals, and invariants.
- Map the impact cone.
- Complete baseline and triggered lenses.
- Generate candidates before repair.
- Validate, falsify, and root-cause-deduplicate.
- Classify business decisions separately from agent-fixable items.

### 9.3 Decision gate

Block only when a decision is necessary to choose a safe behavior, such as:

- Which product semantic is authoritative.
- Whether compatibility is required.
- What migration/data-loss behavior is acceptable.
- Which security/reliability risk can be accepted.
- Which architecture tradeoff or public contract is intended.

Do not ask users to choose implementation details that repository conventions already settle.

### 9.4 Repair wave

- Freeze finding wording and acceptance criteria first.
- Batch compatible findings into the smallest coherent patch.
- Keep unrelated cleanup out.
- Record the exact diff and evidence per finding ID.
- Do not let the fixer close its own finding by explanation.

### 9.5 Delta verification

Review only:

- Repair hunks.
- Direct callers/callees.
- Contracts, schemas, migrations, tests, config, permissions, state transitions, and release paths affected by the repair.
- Prior review conclusions whose evidence was invalidated.

This is the principal cost reduction. The original change remains in the ledger; unchanged areas are not reread without a dependency reason.

### 9.6 Full-review reset triggers

Reset to broad discovery when a repair:

- Changes a public API, schema, migration, authorization, tenant boundary, or product semantic.
- Introduces or rewrites concurrency, persistence, destructive behavior, deployment, rollback, or CI policy.
- Changes the architecture direction or creates a new shared abstraction.
- Expands into previously unrelated modules.
- Rewrites a material portion of the original semantic change such that prior evidence no longer applies.
- Changes the base/head or invalidates the patch ledger.

A configurable changed-surface threshold can be a warning signal, but semantic triggers take precedence over line percentages.

### 9.7 Final fresh verification

Use one fresh-context verifier for large or high-risk reviews. Give it:

- The current bounded change.
- Authoritative requirements and accepted decisions.
- Required repository entry points.

Do not initially provide prior rationalizations or a list of expected defects. Ask it to inspect merge risk independently. Then reconcile its candidates against the ledger and evidence. This spends independence where it has the highest marginal value instead of on every repair wave.

### 9.8 Stop conditions

Complete when all hold:

- No unresolved `Must Fix` or unaccepted `Should Fix` remains.
- Every triggered mandatory lens has evidence or an explicit blocker.
- Required deterministic checks pass, or missing evidence is visible.
- Every repair is mapped to a frozen finding and acceptance evidence.
- The fresh verifier finds no new material root-cause class, or its candidates are disproved.
- Residual risk, unreviewed areas, and human decisions are recorded.
- Repository state and report agree.

Do not require two consecutive whole-diff “no issue” runs.

### 9.9 Convergence caps

Use a default soft cap of three repair waves and a hard cap of five. At the soft cap, diagnose why new findings continue. At the hard cap, block with a specific cause:

- Ambiguous or changing requirement.
- Weak/missing test oracle.
- Inaccessible environment or production evidence.
- Unstable base branch.
- Architecture conflict.
- Repair scope expanding faster than it closes.
- Repeated systemic pattern requiring a repository control.

The user should decide the missing authority or scope, not merely whether to spend ten more undirected rounds.

### 9.10 Progress rule

A repair wave counts as progress only if it does at least one of:

- Closes an accepted finding with evidence.
- Adds a new material root cause backed by evidence.
- Closes a named coverage gap.
- Produces a durable guardrail for a recurring issue class.

Repeated commentary, restated symptoms, or unchanged test results do not count.

## 10. Preventing Review-Created Technical Debt

A review loop can itself produce debt by adding defensive branches, wrappers, fallbacks, and narrow tests. The new skill includes a simplification pass and durable-response rule.

For recurring findings, consider:

- Boundary validation or schema enforcement.
- Shared authorization/policy entry point.
- Static architecture or dependency lint.
- Regression/property/integration test.
- Generator/template correction.
- CI/release policy.
- Short repository rule linked to the source of truth.

Do not encode every reviewer preference. A durable rule needs:

- A real repeated failure.
- A clear invariant.
- Low enough false-positive cost.
- An owner and update/removal path.

Cursor's learned-rule workflow and OpenAI's “golden principles” independently point toward using review feedback to improve the harness rather than paying to rediscover the same class indefinitely (V-01, V-09).

## 11. Skill Architecture Produced

| File | Responsibility |
| --- | --- |
| `code-review/SKILL.md` | Compact executable workflow, phase boundaries, finding classification, repair and reset rules, stop conditions. |
| `code-review/references/review-coverage.md` | Traditional and triggered review lenses, risk routing, scenario/evidence templates. |
| `code-review/references/ai-agent-risk-catalog.md` | Current AI-authored code and agent-harness failure hypotheses. |
| `code-review/references/review-loop-protocol.md` | Detailed orchestration state machine, incremental invalidation, caps, prompts, and metrics. |
| `code-review/references/ledger-templates.md` | Persistent `STATE.md`, `FINDINGS.md`, `CURRENT.md`, and Chinese report templates. |

The core skill remains below the skill-creator's recommended size, while detailed material is one link away and loaded only when triggered.

## 12. Alternatives Rejected

### Repeat complete review until two clean rounds

Rejected because it pays the highest context cost every time and uses agreement as a proxy for coverage.

### Give one agent one enormous checklist

Rejected because long undifferentiated instructions consume context, weaken prioritization, and do not reliably create distinct security or operational mindsets. Checklists remain useful as routed references.

### Let the fixer rewrite and close findings in one pass

Rejected because acceptance criteria can drift toward the patch and self-verification is vulnerable to confirmation bias.

### Use a new subagent for every lens and every wave

Rejected as the default because it multiplies context reconstruction and tool use. Reserve parallel/fresh agents for high-risk independent discovery or final verification.

### Stop after a fixed number of rounds

Rejected as the primary criterion. Numeric caps control budget, but completion is based on evidence and the hard-cap action is a convergence diagnosis.

### Trust scanners or green CI as the oracle

Rejected because semantic, authorization, migration, architecture, and operational failures can remain outside deterministic coverage. Scanners remain required layers where applicable.

### Always re-review only the literal patch

Rejected because repairs can invalidate unchanged callers, contracts, state assumptions, tests, configuration, and rollout paths. The correct unit is the delta plus impact cone.

## 13. Limitations and Validation Needs

- Current AI studies are rapidly changing and many are preprints.
- Vendor metrics are not neutral cross-product evaluations.
- Community reports are anecdotal.
- The optimal repair-wave cap depends on repository size and risk.
- Impact-cone accuracy depends on a legible architecture and reliable search/tooling.
- Fresh verifiers can still share model-family blind spots.
- Property tests can encode a wrong invariant and require validation.
- The new skill should be forward-tested on at least one small, one medium, and one high-risk large change; measure accepted findings, duplicates, false positives, repair waves, full resets, and token/tool cost.

The design therefore treats every source as input to an evidence protocol, not as proof that a particular repository has a defect.

## References

See [source-register.md](source-register.md). The principal review sources are R-01 through R-05, V-01, V-05 through V-13, E-01 through E-10, and C-01 through C-08.
