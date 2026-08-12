# DJ-0021 — Persisted Trace Manifest and RUN Acceptance

Date: 2026-08-12
Tree_F: TF-0032
ADR: ADR-0027

## Completed
Persisted verified TRACE_MANIFEST beside the append-only JSONL event stream. Added canonical manifest SHA-256, verification against current event-chain state, RUN_RECORD trace-manifest references and negative tests for manifest tampering and post-manifest chain mutation.

## Important design boundary
This generation forced an explicit distinction that will matter later for FATHER: cryptographic integrity is not truth. We can prove that a statement/event record is the same record that was committed; we cannot infer from the hash alone that the originating statement was correct. Factual confidence belongs to provenance/evidence/evaluation and potentially independent corroboration.

## Next gate
Build a read-only Replay Verifier. It must reconstruct and verify the governed lineage without calling the tool or producing side effects.
