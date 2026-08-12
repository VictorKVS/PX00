# TF-0039 — Governed Quality Challenge, Review and Supersession

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0034

## Generation
Added formal immutable challenge/review records for source/evidence quality assessments and replacement-based supersession.

## Surfaces
- `schemas/ASSESSMENT_CHALLENGE.yaml`
- `schemas/ASSESSMENT_REVIEW.yaml`
- `px00/challenges.py`
- `tests/test_challenges.py`
- `architecture/adr/ADR-0034-governed-quality-challenge-review-supersession.md`

## Core chain
`ASSESSMENT -> CHALLENGE -> REVIEW -> replacement ASSESSMENT -> supersedes old ASSESSMENT`

## Invariant
No challenge or review mutates historical assessment content.

## Next
Propagate accepted quality supersession into a new CLAIM_ASSESSMENT and record causal lineage from review to changed claim status.
