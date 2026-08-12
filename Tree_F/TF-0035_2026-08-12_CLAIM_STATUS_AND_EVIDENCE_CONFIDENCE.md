# TF-0035 — Claim Status and Evidence Confidence

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0030

## Generation
Added an explicit epistemic layer above replay/acceptance. Claims now have support-state semantics independent of execution integrity.

## Surfaces
- `schemas/CLAIM_STATUS.yaml`
- `px00/epistemics.py`
- `tests/test_epistemics.py`
- `architecture/adr/ADR-0030-claim-status-and-evidence-confidence.md`

## Invariants
- integrity is not truth
- corroboration requires materially independent source groups
- contradiction remains visible
- duplicated/dependent sources cannot manufacture corroboration
- no scalar truth score

## Next
Persist claim/evidence lineage and model claim revision/supersession over time.
