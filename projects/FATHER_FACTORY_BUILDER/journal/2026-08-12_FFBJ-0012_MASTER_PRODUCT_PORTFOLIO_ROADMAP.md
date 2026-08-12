# FFBJ-0012 — Master Product Portfolio Roadmap

Date: 2026-08-12
Project: PROJECT-FFB-0001
Related: TF-0065 / ADR-0058

## Change
Factory Builder is now connected to a portfolio-level product manufacturing roadmap rather than receiving product ideas as unrelated one-off requests.

Created:
- `father/product-roadmap/master-product-roadmap.yaml`;
- `father/product-roadmap/security-products.yaml`;
- `father/product-roadmap/README.md`.

## Owner-priority product line
The first domain line is Security:

`Security Knowledge Base → Compliance Engine → Evidence-Based Security Architect → Vulnerability & Risk Expert → White-Hat / Continuous Security Assurance → Regulatory Change Engine → Continuous Security Audit Expert`.

The foundational Security Knowledge gate is blocking. Later products may be researched as isolated PoCs, but they cannot become authoritative products while the expert-ready evidence-based Security Knowledge gate remains unsatisfied.

## Architect-proposed portfolio additions
Supporting/future tracks are recorded separately as architecture proposals:
- FATHER/Factory Builder platform core;
- generic Knowledge Core;
- Agent Factory;
- Software/Service Factory;
- Research Factory;
- Independent Assurance;
- Cyber-Physical/Robotics Factory;
- Factory-of-Factories horizon.

These do not automatically become current build priorities.

## Priority behavior
Architect-proposed work may interrupt the active owner-priority track only for:
1. a direct product dependency;
2. S4 remediation or mandatory maturity control;
3. an isolated low-cost PoC without maturity promotion;
4. explicit governance/owner reprioritization.

## Factory Builder implication
Future factory designs must reference the product roadmap and declare:
- which product/track they serve;
- which foundation gate they depend on;
- whether the work is Demo, PoC, MVP or Production;
- what PX00 maturity is actually proven;
- what critical risks block promotion.

## Current direction
Continue `SUMMIT-FFB-02` to first governed live executor while beginning the Security Knowledge foundation. Avoid broad platform expansion that does not directly support these two goals.
