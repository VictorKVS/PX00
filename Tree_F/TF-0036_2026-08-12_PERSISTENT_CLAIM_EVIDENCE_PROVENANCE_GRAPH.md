# TF-0036 — Persistent Claim/Evidence Provenance Graph

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0031

## Generation
Added persistent SRC/EVD/CLM contracts and an explicit reference provenance graph preserving support, contradiction, source derivation and claim supersession.

## Surfaces
- `schemas/SOURCE.yaml`
- `schemas/EVIDENCE_ITEM.yaml`
- `schemas/CLAIM.yaml`
- `px00/knowledge_graph.py`
- `tests/test_knowledge_graph.py`
- `architecture/adr/ADR-0031-persistent-claim-evidence-provenance-graph.md`

## Invariants
- immutable node identity
- explicit support and contradiction edges
- acyclic supersession
- prior claim history retained
- source independence is not inferred from distinct locators

## Next
Integrate ClaimEvidenceEvaluator with graph-resolved evidence and persist claim assessments as versioned evaluation artifacts.
