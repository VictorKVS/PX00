# ADR-0036 — Downstream Staleness Propagation

Date: 2026-08-12
Status: accepted

## Context
A revised claim assessment may invalidate assumptions embedded in admitted knowledge, decisions, and plans. PX00 must identify this impact without silently rewriting or revoking previously governed objects.

## Decision
Introduce a directed acyclic dependency graph across CLAIM_ASSESSMENT -> KNOWLEDGE -> DECISION -> PLAN. A changed upstream assessment creates an immutable DOWNSTREAM_IMPACT record and marks downstream objects with review states:

- KNOWLEDGE -> STALE
- DECISION -> REASSESSMENT_REQUIRED
- PLAN -> REVIEW_REQUIRED

Propagation preserves the causal path and the review/change that triggered it.

## Authority boundary
Staleness is not revocation authority. The propagation engine MUST NOT cancel a plan, reverse a decision, delete knowledge, or trigger an external side effect. Those actions require their own governed review/authority path.

## Consequences
PX00 can explain which downstream decisions became questionable after a change in evidence and why, while preserving all historical objects and preventing epistemic updates from bypassing operational authority.
