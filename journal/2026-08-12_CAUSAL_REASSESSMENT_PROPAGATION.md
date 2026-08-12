# DJ-0029 — Causal Reassessment Propagation

Date: 2026-08-12
Tree_F: TF-0040
ADR: ADR-0035

## Completed
Added deterministic propagation from accepted quality reviews into new immutable CLAIM_ASSESSMENT objects. The new assessment stores `caused_by_review_ref`, preserving why the belief-state changed.

## Important dependency rule
When a SOURCE_ASSESSMENT is superseded, EVIDENCE_ASSESSMENT objects that referenced the old source assessment are no longer compatible with the active source-quality view. Propagation therefore requires refreshed evidence-quality assessments before claim reassessment. Missing refreshes fail closed.

## Result
PX00 can now produce an explicit causal explanation:
`REVIEW -> SRCA/EVDA replacement -> affected claim -> new CLMA`.
Prior CLMA records remain unchanged.

## Next
Persist propagation records and compute downstream impact so KN/DEC/ACCEPTANCE objects that depended on superseded claim assessments can be marked STALE / REASSESSMENT_REQUIRED rather than silently remaining current.
