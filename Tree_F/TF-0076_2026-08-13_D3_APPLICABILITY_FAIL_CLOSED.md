# TF-0076 — D3 Applicability Fail-Closed

Status: IMPLEMENTED_PENDING_CI
Date: 2026-08-13

## Goal
Close one bounded Security D3 governance gap without expanding the knowledge architecture.

## Observed defect
The D3 gate required the APPLICABILITY evidence category, but category presence alone could still lead to PASS even when the applicability conclusion was unresolved.

## Canonical trigger
KNOWLEDGE_CORE commit `90f2d7e16e37b99379901ec9d11f51964f5256f1`, requirement `RU-FZ152-A22-C1-R01`, explicitly states that the Article 22 part 1 notification duty is conditional on a part 2 exception not applying. The same canonical file records part 2 exception evaluation as an open red-team condition.

## Change
`DecisionMaterialityAssessment` now carries `applicability_determination`.
For D3, only explicit `APPLICABLE` or `NOT_APPLICABLE` resolves the applicability floor. Any other state returns:
- status: `INSUFFICIENT_EVIDENCE`
- reason: `D3_APPLICABILITY_UNRESOLVED`
- missing evidence: `APPLICABILITY_DETERMINATION`

This check executes before review/approval, so human approval cannot convert an unresolved legal applicability question into PASS.

## Scope
No KNOWLEDGE_CORE content was duplicated or changed. No new general reasoning framework was introduced. This is a narrow runtime enforcement of existing `PX00-NORM-DM-0001` semantics.

## Acceptance
- existing D0-D2 behavior remains unchanged;
- D3 happy path requires explicit applicability resolution;
- unresolved applicability fails closed even if the APPLICABILITY category, reviewer, and approver are present;
- full PX00 Contract Validation must be green before promotion to main.

## Known limitation / next proof
This gate proves governance semantics, not the substantive Article 22 part 2 legal determination. The next Security Knowledge step is to atomize/verify the exceptions or provide a governed case-specific applicability assessment. `SUMMIT-FFB-02` remains OPEN until a real authorized Gemini run exists.
