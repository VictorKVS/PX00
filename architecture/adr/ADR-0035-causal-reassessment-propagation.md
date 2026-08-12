# ADR-0035 — Causal Reassessment Propagation

Date: 2026-08-12
Status: accepted

## Context
Accepted quality reviews can supersede SOURCE_ASSESSMENT or EVIDENCE_ASSESSMENT objects. Claims that depend on those quality objects must be reassessed without rewriting prior belief state and with an explicit explanation of why the reassessment occurred.

## Decision
Introduce a deterministic causal propagation layer. An accepted review updates the active quality-assessment view, determines affected claims from the provenance graph, and creates new immutable CLAIM_ASSESSMENT records carrying `caused_by_review_ref`.

A source-quality replacement invalidates evidence-quality assessments bound to the superseded source assessment. Compatible refreshed evidence assessments are required before propagation may continue. Missing refreshed assessments fail closed.

## Invariants
- rejected or escalated reviews cannot propagate
- prior claim assessments are never mutated
- propagated assessments point to the exact causal review
- source reassessment requires compatible refreshed evidence assessments
- evidence reassessment must reference the active source assessment
- affected claims are derived from provenance edges, not guessed by the evaluator

## Consequences
PX00 can explain status changes as a causal chain: REVIEW -> quality replacement -> affected evidence/claims -> new CLAIM_ASSESSMENT, while preserving the previous assessment as historical state.
