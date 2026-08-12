# TF-0066 — Security Knowledge Canonical Repository Alignment

Date: 2026-08-12
Status: IMPLEMENTED
ADR: ADR-0059

## Objective
Align PX00/FATHER with the already-existing `SEC-PROD-0001 Security Knowledge Base` in `VictorKVS/KNOWLEDGE_CORE` and prevent duplicate Security Knowledge truth from emerging in PX00.

## Canonical ownership
`VictorKVS/KNOWLEDGE_CORE`:
- `security-knowledge/` — canonical Security Knowledge product tree;
- `father/domain-knowledge/` — professional domain registry;
- `father/product-roadmap/` — canonical security and master product roadmaps.

`VictorKVS/PX00`:
- FATHER orchestration/execution/governance;
- Factory Builder;
- runtime trace/review/rework/acceptance;
- route-only product/domain references.

## Existing Security Knowledge state recognized
The product is not at greenfield/M0. Its foundation and schemas already exist and the normative corpus is actively being populated.

Recognized pipeline:
`SOURCE → VERSION → CHUNK → ATOMIC CLAIM/REQUIREMENT → APPLICABILITY → RELATIONS → CONTROL → CHECK → EVIDENCE → EXPERT REVIEW`.

Recognized current build direction:
1. finish FSTEC;
2. fully process FSB P0 including GosSOPKA/NKCKI/SKZI and revision history;
3. Roskomnadzor;
4. base laws/government acts/decrees and inter-document links;
5. sector regulators;
6. GOST;
7. ISO;
8. NIST/CIS/OWASP;
9. BDU/CVE/CWE/ATT&CK;
10. pentest/vulnerability/risk knowledge;
11. vendor hardening;
12. consolidate mature overlaps into Unified Controls, checks, evidence and expert review.

## Critical product rule
Do not reduce the product to ordinary RAG over PDFs.

Retrieval is a lower layer. The product value is the evidence graph:
`requirement ↔ applicability ↔ control ↔ implementation ↔ check ↔ evidence ↔ risk`.

`VERIFIED` requires an admitted primary source and exact locator.

## Changes made
In KNOWLEDGE_CORE:
- created `father/product-roadmap/master-product-roadmap.yaml` as the canonical portfolio plan;
- updated `father/product-roadmap/security-products.yaml` with stable SEC-PROD IDs, owner sequence, current corpus order and the parallel live-provider rule;
- bound `father/domain-knowledge/domain-registry.yaml` SECURITY domain to `KB-SECURITY`, the canonical product tree and roadmap.

In PX00:
- removed duplicate Security KB coverage/readiness/source-backlog artifacts;
- removed the duplicate Security Knowledge readiness runtime;
- converted `father/products/security-knowledge-base/PRODUCT.yaml` to an external canonical product route;
- converted local security/master roadmap files to route-only records.

## Parallelism
`SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR` continues in parallel.

It is **not** a blocker for Security Knowledge corpus population.

Future live model output used inside Security Knowledge remains candidate material until admitted through canonical provenance/review rules.

## Maturity effect
The architecture now has a clean repository boundary:

`KNOWLEDGE_CORE = professional/domain/product knowledge truth`

`PX00 = governed organizational runtime`

This is a prerequisite for long-lived multi-domain FATHER development because future domain KBs can follow the same stable route model without copying truth into the runtime repository.

## Next useful work
- continue normative population in KNOWLEDGE_CORE according to the existing P0 sequence;
- complete SUMMIT-FFB-02 independently in PX00;
- after a sufficient VERIFIED Security Knowledge slice exists, use it for the first closed FATHER security-domain loop and bounded Compliance Engine PoC.
