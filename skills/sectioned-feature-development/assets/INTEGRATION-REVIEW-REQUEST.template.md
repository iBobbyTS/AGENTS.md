# Feature Integration Review Request

- Review mode: `INTEGRATION`
- Working path: `<path>`
- Feature: `<name>`
- Feature base: `<commit>`
- Feature head: `<commit>`
- Feature contract: `.agent-work/PLAN-FULL.md`
- Feature state: `.agent-work/FEATURE-STATE.md`
- Section artifacts: `.agent-work/sections/`
- Review index: `.agent-work/reviews/`
- Output: `.agent-work/reviews/FEATURE-INTEGRATION-r01.md`
- Review skill: `$code-review`

## Required Focus

- Original full-feature goal, non-goals, and requirement coverage.
- Cross-section API/schema/state/permission/order/error contracts.
- End-to-end happy, negative, and partial-failure paths.
- Migration, compatibility, rollout, rollback, feature flags, and cleanup.
- Security, privacy, reliability, performance, observability, and operations.
- Deferred-work closure and branch-scope integrity.

## Review Semantics

Do not mechanically replay every accepted section line by line. Form an independent view of the current integrated state, then use prior section ledgers to verify closure and identify evidence gaps. Report `mergeable`, `not-mergeable`, or `insufficient-evidence`.
