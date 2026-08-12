# RISK-0001 — Knowledge Context Reproducibility Gap

Status: RESOLVED
Historical severity: S4
Category: KNOWLEDGE / SECURITY
Source: ARGUS-SEC-001
Owner: ROLE-ARCHITECT
Resolved: 2026-08-12

## Risk
Historical Context Packages must bind the exact semantic material delivered to an agent, not only a stable object ID.

## Immediate containment
Material replay/acceptance was prohibited from relying on ID-only Context Packages until exact knowledge versions were pinned.

## Implemented remediation
`ContextPackage` v0.2 requires every selected knowledge object to provide:
- stable `object_id`;
- exact `version_id`;
- SHA-256 `content_digest`.

The compound immutable reference `object_id@version_id#content_digest` is included in package hashing. Missing/invalid digests fail closed.

## Verification evidence
Verified by the full PX00 Contract Validation run on head `78174e61a900c99bed1948fc09a96d1026ac7ba3` (workflow run `31613685285`), conclusion SUCCESS.

Verified behaviors include:
- changing content digest under the same logical object ID changes the Context Package hash;
- changing object version under the same logical object ID changes the Context Package hash;
- invalid content digest fails closed;
- physical route migration preserves logical/content identity while route snapshot change remains visible;
- task-routing fixtures were migrated to the versioned Context Package contract;
- repository contract validation passed after Tree_F identity repair.

## Residual/reopen condition
Reopen this risk immediately if any future KNOWLEDGE_CORE/KB implementation permits mutable content behind an already-pinned `version_id`, fails to preserve historical content-addressable material, or allows resolution of a historical Context Package without verifying the pinned content digest.

## Decision
The original S4 gap is resolved at the PX00 contract/reference-model layer. Production KB integration must independently prove the same invariant before higher maturity promotion.
