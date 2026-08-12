# TF-0038 — Governed Source and Evidence Quality

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0033

## Generation
Removed reference-default quality values from temporal claim assessment and introduced immutable governed source/evidence quality assessments.

## Surfaces
- `schemas/SOURCE_ASSESSMENT.yaml`
- `schemas/EVIDENCE_ASSESSMENT.yaml`
- `schemas/CLAIM_ASSESSMENT.yaml` v0.2
- `px00/quality.py`
- `px00/assessments.py`
- `tests/test_quality.py`
- `tests/test_assessments.py`
- `architecture/adr/ADR-0033-governed-source-and-evidence-quality.md`

## Invariants
- source/evidence quality is assessed, never assumed
- missing quality metadata fails closed
- evidence assessment must bind to the exact source assessment used
- reassessment creates new history rather than rewriting old history
- quality dimensions are not a scalar truth probability

## Next
Persist quality assessment history and let reviewer/Socrates roles challenge, supersede and compare quality assessments with explicit reasons.
