# DJ-0055 — Cross-Repository Knowledge Snapshot Pinning

Date: 2026-08-12
Generation: TF-0067
ADR: ADR-0060

## What changed
PX00/FATHER can now preserve an immutable reference to external canonical knowledge state instead of treating a mutable repository branch as historical context.

Implemented:
- `KNOWLEDGE_SNAPSHOT` contract;
- snapshot runtime builder and negative tests;
- `CONTEXT_PACKAGE v0.3` with snapshot refs in package hash;
- canonical `KB-SECURITY` route to KNOWLEDGE_CORE;
- producer-side snapshot export schema in KNOWLEDGE_CORE;
- `RISK-0012` for the still-unproven real producer/export/replay path.

## Why
Security Knowledge is actively changing while FATHER must eventually be able to reproduce why an old decision was made with the knowledge available to that RUN.

A mutable route is useful for new work. It is unacceptable as historical evidence.

## Key invariant
`ACTIVE ROUTE != HISTORICAL SNAPSHOT`.

New requests may resolve current knowledge. A RUN receives a pinned snapshot.

## Repository ownership
- KNOWLEDGE_CORE remains the canonical knowledge producer/truth store.
- PX00 remains the consumer/orchestrator/runtime.
- No knowledge was copied into PX00 to implement reproducibility.

## Risk state
`RISK-0012`: MITIGATING.

Contracts exist on both sides, but a real `SEC-*` slice has not yet completed:
`export → validate → context → RUN → historical replay`.

## Next
Build the smallest real cross-repository Security Knowledge slice and prove replay after KNOWLEDGE_CORE head advances.

Parallel work remains allowed:
- factual Security Knowledge corpus population;
- SUMMIT-FFB-02 live executor integration.
