# DJ-0022 — Read-only Replay Verifier

Date: 2026-08-12
Tree_F: TF-0033
ADR: ADR-0028

## Completed
Implemented `ReadOnlyReplayVerifier` and `ReplayReport`. The verifier reconstructs ActionRequest -> AuthorityDecision -> PolicySnapshot -> material EVT -> persisted TRACE_MANIFEST consistency without importing or calling any execution tool.

## Negative coverage
- missing events -> INSUFFICIENT_EVIDENCE
- authority/snapshot mismatch -> POLICY_MISMATCH
- event authority mismatch -> BROKEN_LINEAGE
- manifest hash tampering -> TAMPER_DETECTED
- verifier has no Tool Boundary dependency

## Epistemic boundary
Replay verification is evidence about integrity, lineage and reproducibility. It is intentionally not an oracle of truth. A factual claim may be faithfully recorded and still be false; later evidence/provenance/corroboration logic must handle that distinction.

## Next gate
Integrate replay verification into Acceptance so promotion requires verified execution records, while preserving separation between verification evidence and final acceptance authority.
