# TF-0032 — Persisted Trace Manifest and RUN Acceptance

Date: 2026-08-12
Status: implemented; final generation CI pending
ADR: ADR-0027

## Generation
Persisted TRACE_MANIFEST artifacts now have independent SHA-256 identity and are re-verified against the append-only event chain before RUN acceptance.

## Surfaces
- `schemas/RUN_RECORD.yaml`
- `px00/recorder.py`
- `tests/test_recorder.py`
- `architecture/adr/ADR-0027-persisted-trace-manifest-and-run-acceptance.md`

## Invariant
Integrity is evidence about record stability, not a proof of factual truth.

## Next
Non-executing Replay Verifier across RUN -> POLSNAP -> AUTH -> EVT -> TRACE_MANIFEST.
