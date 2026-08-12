# ADR-0030 — Claim Status and Evidence Confidence

Date: 2026-08-12
Status: accepted

## Context
PX00 can now verify execution lineage and gate acceptance through replay. Neither mechanism establishes factual truth. FATHER needs a separate epistemic layer that records how strongly a claim is supported, contradicted, or independently corroborated.

## Decision
Introduce CLAIM_STATUS and a deterministic reference ClaimEvidenceEvaluator.

The evaluator keeps support and contradiction separate and exposes dimensions rather than collapsing them into a single truth score. Source independence is represented by explicit independence groups; multiple copies or dependent sources do not count as corroboration.

Initial runtime-derived states are UNSUPPORTED, SINGLE_SOURCE, CORROBORATED, CONTRADICTED, DISPUTED, and REFUTED. UNKNOWN and SUPERSEDED are contract states reserved for lifecycle/context handling rather than inferred from one evidence batch.

## Critical boundary
`VERIFIED_RECORD` proves governed lineage/integrity only. `CORROBORATED` describes evidence topology/support only. Neither is equivalent to `TRUE`.

## Consequences
FATHER can distinguish a perfectly preserved weak claim from a strongly corroborated claim, preserve contradictory evidence, and avoid laundering duplicated sources into false consensus.
