# DJ-0028 — Governed Quality Challenge, Review and Supersession

Date: 2026-08-12
Tree_F: TF-0039
ADR: ADR-0034

## Completed
Added immutable challenge and review objects over SOURCE_ASSESSMENT and EVIDENCE_ASSESSMENT. Challenges may propose bounded revisions but cannot change assessments. Accepted reviews require a new same-subject replacement assessment and record explicit supersession lineage. Rejected reviews leave the original assessment unchanged.

## Example
`SRCA-1 reliability=0.85 -> CHAL-1 -> REVIEW-1 ACCEPT_WITH_MODIFICATION -> SRCA-2 reliability=0.55 -> supersedes SRCA-1`

The original `SRCA-1` remains addressable, preserving why earlier claim assessments may have differed from later ones.

## Next
Causally propagate accepted replacement quality assessments into new immutable CLAIM_ASSESSMENT records and record which challenge/review caused the claim-level re-evaluation.
