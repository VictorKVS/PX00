# TF-0033 — Read-only Replay Verifier

Date: 2026-08-12
Status: implemented; final generation CI pending
ADR: ADR-0028

## Generation
Added non-executing historical verification across persisted governed lineage.

## Surfaces
- `px00/replay.py`
- `tests/test_replay.py`
- `schemas/REPLAY_REPORT.yaml`
- `architecture/adr/ADR-0028-read-only-replay-verifier.md`

## Outcome classes
`VERIFIED_RECORD | BROKEN_LINEAGE | TAMPER_DETECTED | POLICY_MISMATCH | INSUFFICIENT_EVIDENCE`

## Critical invariant
`VERIFIED_RECORD` proves record integrity and lineage under PX00 contracts; it is not a declaration of factual truth.

## Next
Bind replay verification into Acceptance without making replay itself an authority source.
