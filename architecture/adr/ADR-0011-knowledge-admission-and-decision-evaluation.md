# ADR-0011 — Knowledge Admission and Decision Evaluation

**Status:** ACCEPTED FOR BASELINE 0.1  
**Date:** 2026-08-11

## Context

PX00 must distinguish retrieved/generated information from governed knowledge and must improve decisions using observable outcomes rather than model confidence or informal impressions.

Without an admission gate, RAG/LLM output can silently become institutional "truth". Without ex-ante/ex-post evaluation, role and architecture quality cannot be compared or improved systematically.

## Decision

PX00 adopts:

1. **Knowledge Admission Contract** — `SRC/ART → EVD → FIND → Knowledge Gate → KN`, with provenance, contradiction, scope, temporal validity and explainable confidence.
2. **Decision Evaluation Contract** — material `DEC-*` records explicit rationale/evidence/authority and may receive separate `EVAL-*` records before action and after observed outcome.

## Knowledge invariants

- LLM output/RAG ranking is not evidence by itself;
- material knowledge requires admitted provenance;
- contradictory evidence remains addressable;
- hypotheses are never silently converted to facts;
- temporal/regulatory knowledge preserves effective period and supersession;
- unexplained numeric confidence is prohibited;
- retrieval cannot bypass access/classification or knowledge admission.

## Evaluation invariants

- material decisions record authority, rationale, evidence and intended outcome;
- ex-ante assessment is distinct from ex-post outcome evaluation;
- scores require a stated basis/evidence;
- blocking security/compliance failures cannot be averaged away;
- rubric versions are preserved;
- A/B variants remain independently traceable;
- low scores create governed improvement proposals, not silent self-modification.

## Deferred implementation choices

No vector database, embedding provider, RAG framework, scoring library or evaluation platform is selected in Baseline 0.1.

Storage/retrieval technology shall be chosen only after knowledge-volume, privacy, latency, deployment and regional requirements are known.

## Security conclusion

`PASS_WITH_ACTIONS`.

The contracts reduce knowledge poisoning, hallucination-as-fact, stale regulation and self-evaluation gaming risks. Residual risks include malicious/compromised sources, retrieval poisoning, cross-tenant knowledge leakage, evaluator collusion, stale knowledge cache and rubric manipulation. These require runtime isolation, source verification, access controls, test corpora and monitoring.

## Consequences

Positive:

- institutional knowledge becomes reviewable and reversible;
- decision quality can be compared with actual outcomes;
- roles/protocols/KB can improve from evidence rather than intuition;
- historical decision context remains reconstructable.

Cost:

- material knowledge and decisions require explicit gate/evaluation records.

The cost is accepted for accountable organizational use.

## Next gate

Define Protocol Execution Contract and Acceptance Model/fixtures. After those are accepted, instantiate the first governed roles (recommended: Analyst and Socrates) as contract-validation pilots before opening runtime code broadly.
