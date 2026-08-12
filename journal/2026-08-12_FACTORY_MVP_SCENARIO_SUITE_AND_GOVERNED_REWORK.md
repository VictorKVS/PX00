# DJ-0049 — Factory MVP Scenario Suite and Governed Rework

Date: 2026-08-12
Tree_F: `TF-0061`
ADR: `ADR-0054`
Project: `PROJECT-FFB-0001`

## Result
Factory Builder now proves three bounded behaviors using the same governed M1 harness:
- successful useful delivery;
- failed independent verification followed by explicit implementation rework and successful re-verification;
- security-gated refusal before prototype creation.

## New control
`AgentRdFactoryMvp.request_rework()` closes the in-memory reference gap where a failed gate could be recorded but the same RUN could not formally return to an earlier stage.

Rework requires:
- prior FAIL;
- explicit reason reference;
- earlier target stage;
- preserved append-only evidence and lineage.

## Failure memory
Created `FACTORY_FAILURE_PATTERN` and the first pilot registry:
- `FFB-FP-0001 VERIFICATION_REWORK_REQUIRED`;
- `FFB-FP-0002 SECURITY_SCOPE_BLOCK`.

Created `RISK-0010` to preserve why the rework control exists and why it is not yet production-complete.

## Management meaning
The project is no longer optimized for “all RUNs end in delivery.” Safe refusal and visible failed attempts are intentional outputs of the control system. A future AI executor must operate inside these invariants rather than replacing them.

## Next
Move to `SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR`: replace exactly one bounded deterministic producer step with a governed executor adapter while keeping all deterministic regression scenarios green.
