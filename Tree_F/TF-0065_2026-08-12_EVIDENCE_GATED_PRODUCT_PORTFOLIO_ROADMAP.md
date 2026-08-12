# TF-0065 — Evidence-Gated Product Portfolio Roadmap

Date: 2026-08-12
Status: implemented; final generation CI pending
ADR: ADR-0058

## Objective
Create one master product manufacturing plan for PX00/FATHER + Factory Builder and prevent product drift or premature downstream promotion.

## Owner-priority Security line
Canonical plan: `father/product-roadmap/security-products.yaml`.

Sequence:
`Security Knowledge Base → Compliance Engine → Evidence-Based Security Architect → Vulnerability & Risk Expert → White-Hat / Continuous Security Assurance → Regulatory Change Engine → Continuous Security Audit Expert`.

Hard rule: downstream Security products may be researched as bounded PoCs, but cannot become authoritative MVP/Production products until `SEC-GATE-EXPERT-KNOWLEDGE-0001` is passed for the declared Security Knowledge scope.

## Master portfolio
Canonical plan: `father/product-roadmap/master-product-roadmap.yaml`.

The portfolio now contains distinct tracks for:
- FATHER + Factory Builder core;
- Security products;
- general Knowledge infrastructure;
- Agent Factory products;
- Software / Service Factory;
- Research Factory;
- Independent Assurance;
- Cyber-Physical / Robotics Factory;
- long-horizon Factory-of-Factories.

Each track records its source as `OWNER_PRIORITY`, `ARCHITECT_PROPOSED` or `NORTH_STAR`.

## Priority protection
Architect-proposed work cannot displace the active Security Knowledge foundation unless it is a direct dependency, an S4/maturity remediation, or explicitly promoted by project governance.

## Promotion logic
Product delivery stage, CRISP-ML(Q) process phase and PX00 M0..M5 maturity remain independent dimensions.

A later product can run an isolated PoC without claiming that the product line foundation or downstream MVP is ready.

## Immediate execution plan
1. Finish `SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR`.
2. Build `Security Knowledge Base` toward expert-ready evidence quality.
3. Close the first FATHER end-to-end corporate loop using a Security-domain task.
4. Then start the first bounded Compliance Engine PoC from governed Security Knowledge.

## Outcome
PX00 now has a portfolio-level product map that can accumulate new product ideas while preserving dependency order, hard knowledge gates, risk priority and MVP-first discipline.
