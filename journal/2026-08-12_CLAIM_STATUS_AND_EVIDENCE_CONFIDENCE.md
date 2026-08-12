# DJ-0024 — Claim Status and Evidence Confidence

Date: 2026-08-12
Tree_F: TF-0035
ADR: ADR-0030

## Completed
Added CLAIM_STATUS contract, deterministic evidence evaluator, independence-aware corroboration and contradiction-preserving states.

## Design boundary
A hash can establish record integrity. Replay can establish governed lineage. Acceptance can establish satisfaction of declared criteria. Evidence evaluation can establish a degree and topology of support. None of these alone licenses the system to declare absolute truth.

## Important anti-pattern prevented
Ten copied articles derived from one original source are not ten independent confirmations. Independence is explicit and must not be inferred from source count.

## Next
Persist CLAIM and EVIDENCE objects with provenance edges, then implement temporal revision: a later claim may supersede an earlier assessment without deleting history.
