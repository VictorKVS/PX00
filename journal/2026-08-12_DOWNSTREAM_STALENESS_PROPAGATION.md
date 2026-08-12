# DJ-0030 — Downstream Staleness Propagation

Date: 2026-08-12
Tree_F: TF-0041
ADR: ADR-0036

## Completed
Implemented a directed acyclic downstream dependency graph across claim assessments, knowledge, decisions, and plans. A changed claim assessment now produces an immutable impact record containing affected objects, old/new review statuses, propagation depth, causal paths, and the governing review/change that triggered propagation.

## Critical boundary
The engine marks knowledge STALE, decisions REASSESSMENT_REQUIRED and plans REVIEW_REQUIRED. It does not delete knowledge, reverse decisions, cancel plans, or execute any side effect. Staleness is an obligation to review, not authority to act.

## Next
Turn impact records into governed reassessment work items routed through roles/protocols, with prioritization based on downstream criticality and side-effect exposure.
