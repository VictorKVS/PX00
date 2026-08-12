# ADR-0064 — Professional Decision Context in Trace and Replay

Status: ACCEPTED
Date: 2026-08-13

## Context

`PX00-NORM-DM-0001` established that assurance depth scales with decision materiality. PX00 could already preserve governed events, policy snapshots and pinned knowledge context, but a historical RUN could still lack a durable answer to a separate question: **which evidence-backed professional decision was relied on, under which D0–D3 materiality class, and which formal decision record existed at that time?**

Keeping this only in free-form logs would make replay of professional rationale non-deterministic and would weaken the evidence-first model being built in `KNOWLEDGE_CORE`.

## Decision

Professional decision provenance is a first-class trace context.

Before a material professional decision can be bound to a RUN:

1. its declared class must satisfy `PX00-NORM-DM-0001`;
2. required evidence/review/approval obligations for that class must pass fail-closed;
3. decision identity must match the expected RUN, role and assignment;
4. selected options must be part of the declared option set;
5. a canonical digest of the governed decision record is produced.

The persisted TRACE manifest records only the minimum provenance envelope:

`decision_ref + decision_digest + materiality_class`.

Full professional evidence and rationale remain in their governed records. TRACE does **not** store or require hidden model chain-of-thought.

Historical replay of a trace that contains decision context requires the expected decision context. Silent omission or digest substitution fails closed.

## Separation of responsibilities

- `KNOWLEDGE_CORE` defines domain evidence semantics and professional decision records.
- PX00 defines materiality, runtime binding, trace integrity and replay obligations.
- Evidence supports a decision but never grants runtime authority.
- Runtime authority remains governed through the existing ActionRequest → AuthorityDecision → CapabilityGrant → Tool Boundary chain.

## Historical semantics

`HISTORICAL DECISION REPLAY != CURRENT PROFESSIONAL REASSESSMENT`.

New evidence or changed requirements produce a new/superseding professional decision. Historical records are not rewritten.

## Backward compatibility

Traces that contain no professional decision context remain valid under the prior contract. Existing knowledge-only replay reason codes are preserved. Decision-only and combined knowledge+decision mismatch codes are distinct.

## Scope limitation

This decision proves the M1 reference runtime contract. It does not claim a production-grade durable professional decision store, organization-wide approval workflow, or a fully proven professional Security reasoning RUN.

## Consequences

Positive:
- replay can prove not only what happened and which knowledge was pinned, but also which formal professional decision was relied on;
- D2/D3 decisions cannot enter the trace through a lightweight D0-style justification;
- decision provenance becomes reusable across architecture, analytics, software engineering, Security and future engineering domains.

Cost:
- material decisions require structured records and review evidence proportional to D0–D3;
- future role/protocol designs must declare which decisions they may make and the expected materiality range.

## Evidence

- `schemas/DECISION_MATERIALITY.yaml`
- `schemas/DECISION_TRACE_CONTEXT.yaml`
- `schemas/TRACE_MANIFEST.yaml`
- `px00/decision_materiality.py`
- `px00/decision_context.py`
- `px00/recorder.py`
- `px00/replay.py`
- `tests/test_decision_materiality.py`
- `tests/test_decision_trace_context.py`
