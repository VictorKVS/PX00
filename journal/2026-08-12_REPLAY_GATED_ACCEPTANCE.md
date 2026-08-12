# DJ-0023 — Replay-gated Acceptance

Date: 2026-08-12
Tree_F: TF-0034
ADR: ADR-0029

## Completed
Bound read-only replay evidence into Acceptance. Added `ReplayGatedAcceptance` reference implementation and tests proving that non-verified replay blocks material acceptance, while VERIFIED_RECORD cannot override failed blocking criteria.

## Layer separation
- recorder integrity: was the recorded history modified?
- replay verification: does governed lineage reconstruct consistently?
- acceptance: do declared criteria permit promotion?
- factual truth: remains outside these three guarantees and belongs to evidence/provenance/corroboration evaluation.

## CI incident carried forward
The replay generation initially produced a false tamper finding because JSON persistence converted tuples to lists. The verifier was corrected to compare canonical JSON rather than Python container identity. This is recorded as a canonicalization defect, not hidden as a test-only change.

## Next
Design evidence confidence/provenance semantics so the system can express `well-recorded but weakly-supported`, `corroborated`, `contradicted`, and `unknown` without collapsing them into true/false.
