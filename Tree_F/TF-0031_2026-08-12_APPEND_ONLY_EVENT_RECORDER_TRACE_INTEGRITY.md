# TF-0031 — Append-only Event Recorder and Trace Integrity

Date: 2026-08-12
Status: implemented; full-generation CI pending
ADR: ADR-0026

## Material generation
Introduces deterministic filesystem-backed append-only persistence for material events and a SHA-256 hash chain per TRACE.

## Changed surfaces
- `schemas/TRACE_MANIFEST.yaml`
- `architecture/adr/ADR-0026-append-only-event-recorder-and-trace-integrity.md`
- `px00/recorder.py`
- `tests/test_recorder.py`

## Integrity model
`event_hash_n = SHA256(event_hash_(n-1) || canonical_event_payload_n)` with a fixed genesis hash.

The trace manifest records ordered event refs, ordered event hashes, event_count, algorithm, and chain head hash.

## Acceptance evidence required
The complete generation must pass tests for normal recording, event identity reuse rejection, context mismatch rejection, payload tampering detection, event deletion detection, and event reordering detection, plus all existing repository gates.
