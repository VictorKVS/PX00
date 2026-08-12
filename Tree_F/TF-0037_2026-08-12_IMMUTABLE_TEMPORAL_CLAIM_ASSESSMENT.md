# TF-0037 — Immutable Temporal Claim Assessment

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0032

## Generation
Claim assessments are now immutable time-bounded records over an exact evidence set.

## Surfaces
- `schemas/CLAIM_ASSESSMENT.yaml`
- `px00/assessments.py`
- `tests/test_assessments.py`
- `architecture/adr/ADR-0032-immutable-temporal-claim-assessment.md`

## Invariants
- later evidence creates a new assessment
- prior assessment remains unchanged
- evidence set is canonicalized and hashed
- evaluator identity/version is explicit
- assessment status is not truth

## Next
Govern SOURCE/EVIDENCE quality metadata instead of using reference defaults in the bridge layer.
