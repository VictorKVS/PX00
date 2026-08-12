# TF-0034 — Replay-gated Acceptance

Date: 2026-08-12
Status: implemented; final generation CI pending
ADR: ADR-0029

## Generation
Replay verification now gates material Acceptance without becoming an authority source itself.

## Surfaces
- `schemas/ACCEPTANCE_RECORD.yaml`
- `px00/acceptance.py`
- `tests/test_acceptance_replay.py`
- `architecture/adr/ADR-0029-replay-gated-acceptance.md`

## Rule
Integrity/replay evidence can block acceptance, but cannot by itself create PASS when blocking criteria fail.

## Next
Introduce evidence/provenance confidence semantics above integrity, keeping truth claims separate from cryptographic verification.
