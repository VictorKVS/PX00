# FFBJ-0013 — Security Knowledge Canonical Route

Date: 2026-08-12
Project: PROJECT-FFB-0001
Related: ADR-0059, TF-0066

## Decision
Factory Builder must not create a duplicate professional knowledge product merely because a factory/role needs that knowledge.

For SECURITY, the canonical professional product already exists in `VictorKVS/KNOWLEDGE_CORE`:
- product tree: `security-knowledge/`;
- domain registry: `father/domain-knowledge/`;
- product roadmap: `father/product-roadmap/`.

Factory Builder therefore designs **knowledge requirements and bindings**, not a competing source of domain truth.

## Role/knowledge consequence
A Factory Builder role that requires security knowledge binds to stable logical identity `KB-SECURITY` and declares the required scope/context. FATHER resolves that binding through the canonical route and pins the resolved knowledge/version context for RUN reproducibility.

`ROLE KNOWLEDGE REQUIREMENT ≠ OWNED LOCAL KNOWLEDGE COPY`.

## Product boundary
Security Knowledge canonical pipeline:
`SOURCE → VERSION → CHUNK → ATOMIC CLAIM/REQUIREMENT → APPLICABILITY → RELATIONS → CONTROL → CHECK → EVIDENCE → EXPERT REVIEW`.

The Factory Builder may propose new required coverage, missing capability or review work, but cannot mark domain knowledge VERIFIED by itself.

## Important anti-pattern rejected
`new factory needs security knowledge → copy PDFs into local RAG → call it Security KB` is forbidden.

Retrieval is only a lower layer. The value of the canonical product is the evidence-linked graph and reviewed source-to-decision lineage.

## Parallelism
Agent/live-provider work may continue independently. A live model can later assist extraction or interpretation, but its output remains candidate material until canonical Security Knowledge review/admission.

## Maturity impact
This creates the reusable rule for all future Factory Builder domains:
- professional knowledge has a stable logical ID;
- authoritative domain truth has one canonical ownership location;
- roles consume bounded governed context;
- repository relocation does not change logical identity;
- factory construction must not fork domain truth.
