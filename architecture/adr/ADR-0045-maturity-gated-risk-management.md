# ADR-0045 — Maturity-Gated Risk Management

Date: 2026-08-12
Status: accepted

## Context
PX00 must continue learning through prototypes without normalizing unresolved architectural debt. A single global stop/go rule would either freeze experimentation or allow dangerous risks to accumulate invisibly.

## Decision
Adopt a scope-aware maturity-gated risk model with two mandatory treatment layers: immediate containment and final remediation.

Maturity levels are M0 CONCEPT, M1 PROTOTYPE, M2 INTEGRATED_PROTOTYPE, M3 CONTROLLED_PILOT, M4 PRE_PRODUCTION and M5 PRODUCTION.

Severity gates:
- S4: no promotion beyond M0 while unresolved. Acceptance/monitor-only is forbidden; eliminate or isolate/disable immediately.
- S3: may remain through M2 only with verified containment; must be reduced/closed before M3.
- S2: may remain through M3 with owner/review/treatment; must be reduced/accepted before M4.
- S1: may remain through M4; resolve/accept before M5.
- S0: tracked observation.

## Reliability principle
Where functional alternatives are equivalent, prefer determinism, isolation, recoverability, auditability and failure containment over implementation speed. Speed is optimized only above the reliability floor.

## Consequence
Prototype work can continue in bounded scopes while critical boundaries remain fail-closed. Risk debt becomes a planned maturity constraint rather than an informal backlog.
