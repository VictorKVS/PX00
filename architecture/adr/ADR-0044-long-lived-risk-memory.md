# ADR-0044 — Long-Lived Architectural Risk Memory

Date: 2026-08-12
Status: accepted

## Context
PX00 is expected to evolve for years. Architecture, organization, software and security weaknesses discovered today must remain visible through refactors, repository moves, model replacement and organizational changes. A transient audit report is insufficient because findings can be forgotten, silently reintroduced or incorrectly marked fixed.

## Decision
Introduce a durable Architectural Risk Register and durable Audit Finding objects. Every meaningful finding may link to a stable `RISK-*` identity. Risk history is append-only and records discovery, reassessment, mitigation, acceptance, verification, reopening and supersession.

A risk is not removed when code or knowledge moves. `RISK-*` identity is logical and stable. Physical component locations may change while affected-component references and lineage are remapped through stable IDs.

## Lifecycle
OPEN -> MITIGATING / MONITORING / ACCEPTED -> RESOLVED, with REOPENED permitted when new evidence invalidates the prior resolution. SUPERSEDED is reserved for a risk whose model was replaced by a better-defined successor while retaining lineage.

## Governance rules
- mitigation does not equal resolution;
- resolution requires verification evidence;
- risk acceptance requires a named accountable actor and rationale;
- severity/status changes are recorded, never silently overwritten;
- unresolved material risks receive a next-review date;
- ARGUS and future auditors can reopen prior risks;
- historical project progress and audited progress remain distinguishable.

## Consequence
PX00 gains institutional memory of its own weaknesses. Future FATHER versions can query not only current architecture but accumulated known failure modes, accepted risks, recurring defects and previously disproven assumptions.
