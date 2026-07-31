# Source Register

Checked on: 2026-07-15  
AI-agent cutoff: 2025-07-15 inclusive  
Scope: bounded code review, periodic code audit, AI-authored code risks, agent harnesses, review/audit loops, and technical-debt controls.

## Contents

1. [Source Policy](#source-policy)
2. [Local Input Artifacts](#local-input-artifacts)
3. [Current AI-Agent and Coding-Agent Sources](#current-ai-agent-and-coding-agent-sources)
4. [Traditional Code Review Sources](#traditional-code-review-sources)
5. [Traditional Audit and Assurance Sources](#traditional-audit-and-assurance-sources)
6. [Explicit Exclusions](#explicit-exclusions)
7. [Refresh Triggers](#refresh-triggers)

## Source Policy

Use sources in this order of authority:

1. Standards and established engineering guidance define durable control areas.
2. Peer-reviewed or empirical research informs likely failure patterns and testable hypotheses.
3. Official vendor engineering posts inform current harness and product-control techniques, but vendor-reported metrics are directional rather than neutral prevalence estimates.
4. Community reports inform hypothesis generation only. Do not infer frequency, causality, or effectiveness from anecdotes.

Apply the one-year cutoff only to AI-agent-specific claims. Older sources are retained only for stable software-engineering, architecture, security, reliability, and code-review practice.

A source can be useful without being conclusive. The skills therefore convert source claims into review questions, evidence requirements, and falsifiable checks rather than automatic findings.

## Local Input Artifacts

| Artifact | Role in this revision |
| --- | --- |
| `code-review-skill.md` | Existing bounded-review behavior and terminology; retained useful contracts while replacing repeated full-surface loops with evidence-led incremental convergence. |
| `code-audit-skill.md` | Existing whole-system audit coverage; retained its broad control areas while moving detailed material into progressively loaded references. |
| `audit-profile-template.md` | Retained as the project risk/profile template. |
| `anti-bloat.md` | Retained as the safe anti-bloat ladder and finding taxonomy. |
| `skill-creator.md` | Enforced frontmatter, naming, concise `SKILL.md`, progressive disclosure, and absence of auxiliary README-style files. |

## Current AI-Agent and Coding-Agent Sources

All entries in this section satisfy the 2025-07-15 cutoff.

### Vendor engineering and product controls

| ID | Date | Source | Used for | Evidence caveat |
| --- | --- | --- | --- | --- |
| V-01 | 2026-02-11 | [OpenAI — Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | Decompose design/code/review/test; make repository knowledge legible; prefer a map over a monolithic manual; encode recurring judgment as mechanical invariants; use continuous targeted cleanup. | One team's internal experience; architecture and throughput assumptions may not generalize. |
| V-02 | 2026-03-06 | [OpenAI — Codex Security now in research preview](https://openai.com/index/codex-security-now-in-research-preview/) | Security-specific agent review as a layered capability; evidence and validation beyond ordinary code review. | Product announcement and vendor examples, not an independent benchmark. |
| V-03 | 2026-03-16 | [OpenAI — Why Codex Security doesn't include SAST](https://openai.com/index/why-codex-security-doesnt-include-sast/) | Separate semantic reasoning from deterministic scanners; combine rather than substitute layers. | Product-positioning source. |
| V-04 | 2025-09-15 | [OpenAI — Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/) | Current Codex review and agent workflow capabilities. | Product announcement. |
| V-05 | 2025-11-26 | [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Persistent progress state, clean session initialization, repository reality checks, narrow work units, and avoiding premature completion. | Demonstration project, not a controlled comparison of all harness designs. |
| V-06 | 2026-01-09 | [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Layer deterministic tests, rubric graders, static analysis, state checks, transcript/tool-call metrics, and lifecycle evals. | General agent-evaluation guidance; examples are illustrative. |
| V-07 | 2026-01-14 | [Anthropic — Finding bugs across the Python ecosystem with Claude and property-based testing](https://www.anthropic.com/research/property-based-testing) | Infer invariants, generate counterexamples, and validate high-risk logic with property-based testing rather than relying only on examples. | Python/open-source focus; substantial manual validation was still required. |
| V-08 | 2026-06-10 | [Cursor — Bugbot is now over 3x faster, 22% cheaper, and finds 10% more bugs](https://cursor.com/blog/bugbot-updates-june-2026) | Incremental review of only newly added PR code; diff deduplication; optimize cost and latency without repeating unchanged scope. | Performance and quality gains are vendor-reported. |
| V-09 | 2026-04-08 | [Cursor — Bugbot now self-improves with learned rules](https://cursor.com/blog/bugbot-learning) | Turn reactions, reviewer replies, and human-missed issues into candidate rules; promote or disable rules based on accumulated signals. | Resolution rates use public PRs and an LLM judge; not a neutral comparison. |
| V-10 | 2026-06-11 | [Cursor — Agent autonomy with auto-review](https://cursor.com/blog/agent-autonomy-auto-review) | Integrate review into autonomous coding workflows while retaining explicit verification stages. | Product announcement. |
| V-11 | 2025-10-28 | [GitHub — Copilot coding agent now automatically validates code security and quality](https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-automatically-validates-code-security-and-quality/) | Run deterministic security/quality validation on agent-authored changes before handoff. | Product announcement; exact controls depend on repository configuration. |
| V-12 | 2026-06-09 | [GitHub — Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/) | Apply the same validation boundary to changes produced by different agents. | Product announcement. |
| V-13 | 2025-11-14; updated 2026-04-17 | [GitHub — Master your instructions files for Copilot code review](https://github.blog/ai-and-ml/github-copilot/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files/) | Keep project-specific review knowledge discoverable and scoped instead of relying on generic review prompts. | Vendor guidance, not evidence that instructions alone produce sufficient review. |
| V-14 | 2025-09-23 | [Google Cloud — Announcing the 2025 DORA Report](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) | Treat AI adoption as a sociotechnical systems change; quality depends on platform, process, and feedback systems rather than model use alone. | Survey/industry report; associations are not necessarily causal. |
| V-15 | 2026-03-11 | [OpenAI — Designing AI agents to resist prompt injection](https://openai.com/index/designing-agents-to-resist-prompt-injection/) | Constrain the impact of deceptive external content through capability limits, approval boundaries, and data protection rather than assuming perfect input classification. | Product-security design guidance; not a guarantee against prompt injection. |

### Empirical studies and benchmarks

| ID | Date | Source | Used for | Evidence caveat |
| --- | --- | --- | --- | --- |
| E-01 | 2026-03-30; rev. 2026-04-26 | [Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild](https://arxiv.org/abs/2603.28592) | Persistent code smells/correctness/security findings in verified AI-authored commits; motivate durable debt ledgers and root-cause controls. | Preprint; issue attribution relies on static-analysis methodology and studied repositories. |
| E-02 | 2026-01-21 | [Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub](https://arxiv.org/abs/2601.15195) | Larger/more diffuse changes, CI failures, unwanted implementation, duplication, weak reviewer engagement, and task misalignment as merge-risk signals. | Accepted at MSR 2026 but individual project policies and agent versions vary. |
| E-03 | 2026-03-25; rev. 2026-05-07 | [SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks](https://arxiv.org/abs/2603.24755) | Long-horizon structural erosion and verbosity; motivate complexity budgets, architectural invariants, fresh verification, and targeted cleanup. | Benchmark tasks and metrics do not represent every production repository. |
| E-04 | 2026-03 | [Human-AI Synergy in Agentic Code Review](https://arxiv.org/html/2603.15911v1) | AI and human reviewers contribute different feedback; project knowledge is a weak point; adopted AI suggestions can add more code/complexity; avoid treating agent review as sufficient proof. | Preprint; bot identification and adoption inference have construct-validity limits; architecture/security effects are outside its measured scope. |
| E-05 | 2026-06-19; rev. 2026-07-06 | [Sevra-Bench: Social Engineering of Vulnerabilities in Review Agents](https://arxiv.org/html/2606.13757v2) | Treat PR descriptions and approval narratives as untrusted claims; separate claim extraction from repository-grounded verification. | Adversarial benchmark; real-world prevalence is unknown. |
| E-06 | 2025-09-26; rev. 2026-06-06 | [SecureVibeBench](https://arxiv.org/abs/2509.22097) | Functional success does not imply secure implementation; security needs dedicated oracles and adversarial tests. | Benchmark-specific tasks and security definitions. |
| E-07 | 2026-05 | [AI-Generated Code Smells](https://arxiv.org/abs/2605.02741) | Expand AI-aware smell hypotheses while requiring repository evidence before reporting. | Preprint; smell taxonomies are not equivalent to defects. |
| E-08 | 2025-09 | [Your AI, My Shell](https://arxiv.org/abs/2509.22040) | Agent/tool execution, prompt injection, and shell boundary risks. | Research threat models may exceed a given repository's reachable attack surface. |
| E-09 | 2026-05 | [Log analysis is necessary for evaluating coding agents](https://arxiv.org/abs/2605.08545) | Preserve and inspect action traces, commands, and validation logs instead of judging only final patches. | Preprint; evaluation focus, not a complete audit framework. |
| E-10 | 2026-06 | [Human oversight of coding agents](https://arxiv.org/abs/2606.05391) | Place human judgment at semantic/risk decisions and calibrate autonomy rather than requiring line-by-line review everywhere. | Preprint; exact oversight design is context dependent. |

### Community and practitioner reports

| ID | Date | Source | Used for | Evidence caveat |
| --- | --- | --- | --- | --- |
| C-01 | 2026-06-07 | [Addy Osmani — Loop Engineering](https://addyosmani.com/blog/loop-engineering/) | Define the outer-loop pattern; maker/checker separation; persistent state; token-cost and cognitive-surrender risks. | Practitioner synthesis, not an empirical study. |
| C-02 | 2026-06-15 | [Addy Osmani — Agentic Code Review](https://addyosmani.com/blog/agentic-code-review/) | Verification as the new bottleneck; correlated model blind spots; humans retain product/risk judgment. | Practitioner synthesis; includes vendor examples. |
| C-03 | 2026-07-09 | [Addy Osmani — Own the Outer Loop](https://addyo.substack.com/p/own-the-outer-loop) | Treat the workflow, stop conditions, and evidence policy as the owned engineering system. | Practitioner opinion. |
| C-04 | 2026-04-06 | [codecentric — The Ralph Wiggum Loop: Autonomous Code Generation with a Fresh Context](https://www.codecentric.de/en/knowledge-hub/blog/the-ralph-wiggum-loop-autonomous-code-generation-with-a-fresh-context) | Fresh-context iteration, external progress state, and bounded autonomous tasks. | Practitioner implementation report. |
| C-05 | 2026-07-15 | [Reddit — Managing long-term AI-assisted coding without regressions](https://www.reddit.com/r/ClaudeCode/comments/1ufur9x/how_do_you_manage_longterm_aiassisted_coding/) | Hypotheses about regressions, architecture drift, returning bugs, lightweight architecture docs, tests, and fresh agents. | Anecdotal and self-selected. |
| C-06 | 2026-04-23 | [Hacker News discussion on agent over-editing and code quality](https://news.ycombinator.com/item?id=47866913) | Hypotheses about scope explosion, bad-pattern replication, passing tests with poor structure, and unsafe data/secret operations. | Anecdotal and heterogeneous. |
| C-07 | 2026-07-15 | [Reddit — A phased development pipeline built with Claude Code](https://www.reddit.com/r/ClaudeCode/comments/1uq4fja/a_development_pipeline_i_built_with_claude_code/) | Separate research, specification, implementation, mechanical validation, fresh audit, and retrospective; recognize overkill for small changes. | One workflow report, not a controlled evaluation. |
| C-08 | 2026-03 | [Reddit — Deep review and IDE use with coding agents](https://www.reddit.com/r/ClaudeCode/comments/1rh2t7y/do_you_really_not_open_the_ide_anymore/) | Hypotheses about duplicated APIs, accretion, and the value of incremental/fresh-context review. | Anecdotal. |

## Traditional Code Review Sources

These sources may predate the AI cutoff because they define stable review practice.

| ID | Source | Used for |
| --- | --- | --- |
| R-01 | [Google Engineering Practices — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Design, functionality, complexity, tests, naming, comments, style, documentation, and whole-change context. |
| R-02 | [Google Engineering Practices — The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html) | Improve overall code health; distinguish perfection from meaningful quality; balance urgency and maintainability. |
| R-03 | [Google Engineering Practices — Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | Reviewability, focused changes, and reduced defect-hiding surface. |
| R-04 | [OWASP Secure Code Review Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html) | Security review workflow and application-security control areas. |
| R-05 | [Less is More: Supporting Developers in Vulnerability Detection during Code Review](https://arxiv.org/abs/2202.04586) | Dedicated security mindset can materially change discovery; checklists alone do not guarantee better detection. |

## Traditional Audit and Assurance Sources

| ID | Source | Used for |
| --- | --- | --- |
| A-01 | [NIST SP 800-218 — Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final) | Prepare, protect, produce, and respond controls across the development lifecycle. |
| A-02 | [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Risk-calibrated application-security verification requirements. |
| A-03 | [OWASP Top 10](https://owasp.org/Top10/) | Common application-security risk families; not a complete audit by itself. |
| A-04 | [SEI — Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) | Scenario-based architecture evaluation and quality-attribute tradeoffs. |
| A-05 | [Google SRE — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) | Latency, traffic, errors, saturation, actionable monitoring, and operational evidence. |
| A-06 | [Google SRE — Introduction](https://sre.google/sre-book/introduction/) | SLO/error-budget framing and reliability as an explicit product tradeoff. |
| A-07 | [AWS Well-Architected Framework — Pillars](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html) | Operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. |
| A-08 | [SLSA v1.2 — Build Provenance](https://slsa.dev/spec/v1.2/build-provenance) | Traceable build inputs, builder identity, artifacts, provenance, and verification. |
| A-09 | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Agent-specific trust, autonomy, identity, tool, memory, and prompt risks. |
| A-10 | [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) | Least privilege, untrusted inputs, tool allowlists, memory isolation, approval gates, and monitoring. |
| A-11 | [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) | Skill/plugin supply chain and instruction-boundary risks. |

## Explicit Exclusions

- AI-agent-specific material published before 2025-07-15 was excluded from the design evidence, even when influential. In particular, early Ralph-loop articles immediately before the cutoff were not used as evidence.
- Marketing claims without a reproducible method, source date, or meaningful engineering detail were excluded.
- Community claims were not converted into rates or universal statements.
- Static-analysis issue counts were not treated as equivalent to user-visible defects or exploitable vulnerabilities.
- Vendor benchmarks were not used to rank products in the skills.

## Refresh Triggers

Re-run the AI-source search when any of the following occurs:

- Six months pass after 2026-07-15.
- A major model or harness generation changes review/autofix behavior.
- The repository adopts a new coding agent, review agent, MCP server, or autonomous merge path.
- New empirical work contradicts the incremental-review, maker/checker, or long-horizon-degradation assumptions.
- A real incident reveals an unrepresented failure class.
