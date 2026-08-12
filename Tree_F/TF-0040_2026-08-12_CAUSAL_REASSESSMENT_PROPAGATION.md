# TF-0040 — Causal Reassessment Propagation

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0035

## Generation
Accepted quality reviews now causally propagate into new immutable claim assessments.

## Surfaces
- `px00/propagation.py`
- `px00/assessments.py`
- `schemas/CLAIM_ASSESSMENT.yaml`
- `tests/test_propagation.py`
- `architecture/adr/ADR-0035-causal-reassessment-propagation.md`

## Proof chain
`REVIEW -> replacement SRCA/EVDA -> affected EVD/CLAIM -> new CLMA(caused_by_review_ref)`

## Fail-closed rule
A source-quality reassessment cannot propagate until every affected evidence item has a compatible refreshed EVIDENCE_ASSESSMENT bound to the replacement SOURCE_ASSESSMENT.

## Next
Persist propagation records and add dependency-impact queries so downstream decisions/knowledge admissions can be marked stale when their supporting claim assessment is superseded.
