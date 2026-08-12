# RISK-0001 — Knowledge Context Reproducibility Gap

Status: VERIFYING
Severity: S4
Category: KNOWLEDGE / SECURITY
Source: ARGUS-SEC-001
Owner: ROLE-ARCHITECT

## Risk
Historical Context Packages must bind the exact semantic material delivered to an agent, not only a stable object ID.

## Immediate containment
Material replay/acceptance must not rely on ID-only Context Packages.

## Implemented remediation
`ContextPackage` v0.2 now requires every selected knowledge object to provide:
- stable `object_id`;
- exact `version_id`;
- SHA-256 `content_digest`.

The compound immutable reference `object_id@version_id#content_digest` is included in package hashing. Missing/invalid digests fail closed.

## Verification criteria
- changing content digest under the same logical object ID changes the Context Package hash;
- changing object version under the same logical object ID changes the Context Package hash;
- invalid/missing content digest fails closed;
- physical route migration does not change logical/content identity but remains visible via route snapshot history;
- full CI passes on the generation containing these tests.

## Closure rule
Do not mark RESOLVED until the above tests and repository contract gates are green. If later KB storage permits mutable content behind a pinned version ID, reopen this risk.
