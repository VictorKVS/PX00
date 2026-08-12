# DJ-0020 — Append-only Event Recorder and Trace Integrity

Date: 2026-08-12
Tree_F: TF-0031
ADR: ADR-0026

## Work completed
Extended the existing TRACE_MANIFEST contract instead of creating a parallel trace model. Implemented `AppendOnlyEventRecorder` using deterministic JSONL serialization and a SHA-256 event hash chain. Added verification that rejects event identity reuse, RUN/TASK context drift, payload tampering, deletion and reordering.

## Engineering decision
The filesystem implementation is intentionally a proof boundary, not a production storage commitment. It proves append-preserving semantics and trace integrity before selecting a database, broker, WORM store or observability backend.

## Current proof chain
`EVT -> ACTREQ -> AUTH -> POLSNAP -> PolicyProfile@version`, persisted in ordered trace history with tamper-evident hashes.

## Next gate
Persist an explicit TRACE manifest artifact alongside the JSONL event stream and bind its integrity summary into RUN completion/acceptance evidence. After that, evaluate a replay/verifier command that reconstructs a RUN without executing side effects.
