# FFBJ-0016 — Knowledge-Bound RUN Trace and Replay

Date: 2026-08-12
Related: TF-0069 / ADR-0062 / ARGUS_AUDIT_0002

## Factory Builder capability gained
A factory can now bind an externally owned professional knowledge slice to one RUN and preserve that exact knowledge provenance through trace/replay.

Reusable pattern:
`ROLE → BINDING → ROUTE → MANIFEST → SNAPSHOT → CONTEXT PACKAGE → RUN KNOWLEDGE PIN → TRACE → REPLAY`.

## Run identity checks
`RunKnowledgeBinder` rejects:
- context from another RUN;
- role mismatch;
- assignment mismatch;
- snapshot-set mismatch;
- malformed provenance digests.

This prevents the organizational error where a correct knowledge artifact is attached to the wrong worker/run and later appears legitimate in audit history.

## Replay rule
If a trace was knowledge-bound, replay is incomplete without the exact expected knowledge context.

The runtime must never reconstruct historical context from the current knowledge head.

`HISTORICAL REPLAY != CURRENT REASSESSMENT`.

## Maturity boundary
The first proof uses a real `SOURCE_VERIFIED` Security source card but a deterministic synthetic action.

Therefore this generation proves the reusable knowledge-provenance machinery, not the professional competence of a Security role.

ARGUS permits the bounded M1 claim only.

## Risk result
`RISK-0012` is resolved for this bounded cross-repository provenance/replay path with explicit reopen conditions.

## Next Factory Builder work
No new generalized knowledge plumbing is justified immediately.

Next useful evidence must come from either:
- the first live governed AI executor; or
- a genuinely VERIFIED domain requirement used in a professional task.

Only repeated cross-domain need should trigger further abstraction of the knowledge bridge.
