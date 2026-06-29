# Audit Profile Template

Use this template when a project has no audit profile or when the user asks to define or revise one.

Field rationale:

- NIST CSF Profiles: current/target posture, tiers, outcomes, governance, and supply-chain context.
- NIST RMF and SP 800-53B tailoring: system categorization, mission/business context, impact, risk tolerance, and tailored baselines.
- NIST SSDF: secure-development outcomes across Prepare, Protect, Produce, and Respond.
- OWASP ASVS: application security verification level and requirement identifiers.
- SEI ATAM: quality-attribute scenarios and architecture tradeoff evaluation.
- AWS Well-Architected and Google SRE: workload boundary, operational excellence, reliability, SLOs, error budgets, observability, and improvement actions.
- SLSA/OpenSSF: source, dependency, build provenance, and artifact integrity expectations.

```markdown
# Project Audit Profile

Status: Draft | Approved
Owner:
Last reviewed:
Review cadence:

## 1. System Context
- Project/workload boundary:
- Primary users and stakeholders:
- Business or mission goals:
- Critical user/business workflows:
- Crown-jewel data, assets, and secrets:
- External systems and third-party dependencies:
- Deployment environments:
- Legal, privacy, regulatory, or contractual constraints:

## 2. Risk And Impact Classification
- Security impact: Low | Moderate | High; rationale:
- Privacy/data impact: Low | Moderate | High; rationale:
- Availability/reliability impact: Low | Moderate | High; rationale:
- Financial/operational impact: Low | Moderate | High; rationale:
- Risk tolerance and explicit non-goals:
- Most expensive failure modes:
- Realistic abuse cases and threat actors:

## 3. Quality Attribute Priorities
| Attribute | Priority | Target or Scenario | Evidence |
| --- | --- | --- | --- |
| Correctness |  |  |  |
| Security |  |  |  |
| Reliability |  |  |  |
| Modifiability |  |  |  |
| Performance |  |  |  |
| Operability |  |  |  |
| Cost |  |  |  |

## 4. Required Audit Coverage
- Always inspect:
- Rotate each audit:
- Recently changed or high-churn areas:
- Public entry points and external interfaces:
- Auth, authorization, tenant/data isolation, and trust boundaries:
- Persistence, migrations, retention, deletion, backup, and restore:
- Background jobs, queues, retries, concurrency, and idempotency:
- Release, deployment, rollback, configuration, and feature flags:
- Observability, alerts, runbooks, and incident recovery:
- Exclusions and rationale:

## 5. Security Verification Baseline
- Target ASVS or equivalent level:
- Required threat model or abuse-case coverage:
- Required security controls:
- Secure-development expectations:
- Vulnerability disclosure, triage, and response expectations:

## 6. Reliability And Operations Baseline
- Critical SLOs/SLIs or equivalent reliability targets:
- Error budget or release-risk policy:
- Backup/restore and disaster-recovery expectations:
- Degraded-mode and emergency-disable expectations:
- Required operational evidence:

## 7. Supply Chain And Build Baseline
- Dependency and license policy:
- Lockfile, vendoring, and generated-code policy:
- Build provenance, artifact integrity, and release-signing expectations:
- CI/CD permission and secret boundaries:
- SBOM or dependency inventory expectations:

## 8. AI-Agent And Tooling Baseline
- Agent/tooling used in this repository:
- Allowed autonomy and required human approval gates:
- Agent identities, tokens, sandboxing, and network/tool permissions:
- MCP/connectors/plugins/hooks policy:
- Untrusted content and prompt-injection boundaries:
- Agent-generated artifact retention and publication policy:

## 9. Sampling And Severity Calibration
- Minimum sampling strategy:
- Must Fix:
- Should Plan:
- Track as Debt:
- No Action:
- Evidence required before a finding can be reported:
```
