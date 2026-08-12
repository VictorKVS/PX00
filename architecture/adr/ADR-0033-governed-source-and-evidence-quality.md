# ADR-0033 — Governed Source and Evidence Quality

Date: 2026-08-12
Status: accepted

## Context
Claim assessment previously bridged provenance nodes into the evidence evaluator with temporary `1.0` defaults for source reliability, evidence quality, recency and directness. That placeholder made the pipeline executable but was not an acceptable epistemic model.

## Decision
Introduce immutable SOURCE_ASSESSMENT and EVIDENCE_ASSESSMENT objects. Every material claim assessment with evidence must reference exact governed quality assessments. Missing or mismatched quality assessments fail closed.

Source assessment dimensions remain distinct: reliability, authority, recency and conflict_of_interest. Evidence assessment dimensions remain distinct: quality, directness, completeness, reproducibility and relevance. Each assessment records evaluator identity/version, evaluation time, basis references and a canonical SHA-256.

## Boundary
A source-quality assessment is itself an evaluated claim about a source, not an intrinsic property and not proof of truth. No numeric quality dimension may be treated as a metaphysical truth probability.

## Consequences
- temporary `1.0` defaults are removed from ClaimAssessmentStore;
- claim evidence-set digest includes exact source/evidence assessment identities;
- reassessing a source or evidence item produces a materially new claim assessment without rewriting prior history;
- future reviewer/Socrates roles can challenge quality assessments independently of the underlying claim.
