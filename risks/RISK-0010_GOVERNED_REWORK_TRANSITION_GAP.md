# RISK-0010 — Governed Rework Transition Gap

Status: MITIGATED_FOR_M1_REFERENCE_MVP
Severity: S3
Category: WORKFLOW / ASSURANCE / SOFTWARE
Source: FFB-FP-0001 / MVP-FUNC-RUN-0002
Owner: FFB-ROLE-0007 Quality and Assurance Architect + FFB-ROLE-0006 Principal Software Engineer

## Risk
The first functional MVP state machine could record `VERIFY_AND_VALIDATE:FAIL` but had no explicit governed transition back to an earlier implementation stage. A failed verification could therefore be repeated, but the work that caused the failure could not be formally revised inside the same append-only RUN lineage.

## Consequence
Without a rework transition, a future agent or orchestrator could be tempted to bypass the failed verification, start an unrelated RUN without explicit causal linkage, or mutate prior evidence. Any of those outcomes would weaken auditability and the closed improvement loop.

## Mitigation implemented
`AgentRdFactoryMvp.request_rework()` now:
- requires a real failed stage outcome;
- requires an explicit reason reference;
- permits movement only to an earlier stage;
- preserves all prior artifacts and failed evidence;
- links the first rework artifact to the failed artifact;
- increments rework count and records the transition in the RUN trace;
- resets only assurance state invalidated by the selected rework target.

The synthetic canonical-tag scenario proves:
`IMPLEMENT v0 → VERIFY FAIL → REWORK → IMPLEMENT v1 → VERIFY PASS → SOCRATES → DELIVERY`.

## Residual risk
This mitigation is only for the in-memory M1 reference harness. Durable distributed rework needs transaction semantics, persistence, concurrency control, authorization integration and full artifact-envelope integrity before production use.

## Closure condition
Do not mark this risk fully closed until durable orchestration can replay and recover a rework cycle without ambiguity, evidence loss or duplicate material action.
