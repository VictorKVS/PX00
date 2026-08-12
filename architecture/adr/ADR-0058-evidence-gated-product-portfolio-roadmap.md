# ADR-0058 — Evidence-Gated Product Portfolio Roadmap

Date: 2026-08-12
Status: Accepted

## Context
PX00/FATHER and Factory Builder now produce reusable architectural, governance, knowledge and executor capabilities. Without a portfolio-level roadmap, the project can drift into opportunistic feature expansion or prematurely build downstream products before their evidence foundations are trustworthy.

The project owner has established the first priority domain sequence:

`Security Knowledge Base → Compliance Engine → Evidence-Based Security Architect → Vulnerability & Risk Expert → White-Hat / Continuous Security Assurance → Regulatory Change Engine → Continuous Security Audit Expert`.

A hard owner rule applies: downstream Security products must not become authoritative before the evidence-based Security Knowledge foundation reaches expert-ready quality for its declared scope.

## Decision
Adopt `father/product-roadmap/master-product-roadmap.yaml` as the portfolio control plan and `father/product-roadmap/security-products.yaml` as the canonical first domain product line.

Roadmap items identify their origin:
- `OWNER_PRIORITY`;
- `ARCHITECT_PROPOSED`;
- `NORTH_STAR`.

Architect-proposed work may proceed only when it is:
1. a direct dependency of the active owner-priority product;
2. a critical risk/maturity remediation;
3. an isolated low-cost PoC that does not claim downstream maturity; or
4. explicitly promoted by owner/project governance.

## Hard portfolio rules
1. No foundation bypass.
2. Demo/PoC exploration does not imply MVP/Production promotion.
3. S4 remediation outranks feature roadmap work on the affected path.
4. Product maturity must remain distinct from CRISP-ML(Q) process phase and PX00 M0..M5 maturity.
5. Repeated failures and proven controls should be promoted into reusable shared patterns after review.
6. The roadmap is prioritization metadata, not runtime authority.

## Security foundation gate
The first hard portfolio gate is `SEC-GATE-EXPERT-KNOWLEDGE-0001`.

It requires evidence/provenance, version identity, source-vs-inference separation, conflict visibility, freshness/effective dates, measured coverage, downstream reassessment on material change, expert benchmark evidence, independent review and no unresolved S4 on the knowledge-integrity path.

## Additional proposed product tracks
The architecture process may maintain supporting tracks for:
- FATHER/Factory Builder core;
- generic Knowledge Core;
- Agent Factory;
- Software/Service Factory;
- Research Factory;
- independent Assurance;
- Cyber-Physical/Robotics Factory;
- long-horizon Factory-of-Factories.

These are portfolio options and capability dependencies, not commitments to build all tracks now.

## Consequence
PX00 can now accumulate product ideas without losing sequencing discipline. The active build remains narrow: finish the first governed live executor and raise Security Knowledge toward its expert-ready gate. Downstream security products and future factory types remain visible but cannot silently consume priority or inherit maturity claims from unfinished foundations.
