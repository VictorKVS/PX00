# ADR-0003 — Compliance/Knowledge Graph and Requirement-to-Evidence Traceability

Status: ACCEPTED FOR BASELINE 0.1

## Context

Raw RAG retrieval is insufficient for defensible compliance, audit, legal, engineering, and management decisions.

## Decision

PX00 shall represent normative and organizational knowledge through typed, versioned objects and explicit relationships. At minimum the model must support:

- Authority / Jurisdiction / Standard / Regulation / Policy
- Requirement
- Canonical Control
- Risk
- Role / Process / Project / Asset
- Evidence
- Finding
- Decision
- Exception / Conflict
- Knowledge Node

Required traceability path:

`Authoritative Source -> Requirement -> Applicability -> Control -> Implementation -> Evidence -> Verification -> Decision/Status`.

## Consequences

- Presence in a knowledge base does not imply applicability.
- Every material compliance claim must link to evidence.
- Supporting and contradicting evidence can coexist.
- Superseded requirements/knowledge remain historically traceable.
- RAG may assist retrieval but does not replace the canonical graph or provenance model.
