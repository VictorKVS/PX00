# DJ-0025 — Persistent Claim/Evidence Provenance Graph

Date: 2026-08-12
Tree_F: TF-0036
ADR: ADR-0031

## Completed
Added persistent SOURCE, EVIDENCE_ITEM and CLAIM contracts plus an in-memory reference provenance graph with explicit support, contradiction, derivation and supersession edges.

## Design choice
Revisions create new identities. Historical nodes remain queryable. This prevents the latest conclusion from overwriting the path that produced it.

## Important consequence
FATHER can now represent belief revision as history rather than mutation: new evidence can contradict or supersede an earlier claim while preserving what was believed before and why.

## Next
Resolve graph evidence into ClaimEvidenceEvaluator and persist each assessment as an immutable evaluation artifact linked to the exact claim/evidence set used.
