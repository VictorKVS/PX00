# DJ-0027 — Governed Source and Evidence Quality

Date: 2026-08-12
Tree_F: TF-0038
ADR: ADR-0033

## Completed
Replaced temporary `1.0` bridge defaults with immutable SOURCE_ASSESSMENT and EVIDENCE_ASSESSMENT objects. ClaimAssessmentStore now requires exact governed quality assessments and records their identities in the evidence-set digest.

## Fail-closed behavior
Claim assessment is blocked if source quality is missing, evidence quality is missing, or an evidence assessment references a different source assessment than the one supplied for its source.

## Epistemic note
The sentence “this source is reliable” is itself an assessment. It now has evaluator identity, version, basis references, time and integrity hash. The value is contestable and revisable without deleting history.

## Next
Add quality-assessment history and challenge/supersession semantics so Critical Reviewer / Socrates can dispute the quality basis itself, not only the final claim.
