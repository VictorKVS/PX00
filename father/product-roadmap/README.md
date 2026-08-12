# PX00 / FATHER — Product Manufacturing Roadmap

This directory is the portfolio-level plan for turning PX00/FATHER + Factory Builder capabilities into reusable products.

## Canonical plans
- `master-product-roadmap.yaml` — portfolio-wide sequence, dependencies and product gates.
- `security-products.yaml` — first priority domain product line.

## Governing rule
The roadmap is dependency- and evidence-driven, not calendar-driven.

A later product may be explored as an isolated Demo/PoC, but it cannot be promoted as an authoritative MVP/Production product while a declared hard foundation gate remains unsatisfied.

For the Security line the hard foundation is:

`Security Knowledge Base → Expert-Ready Evidence-Based Security Knowledge gate`.

Only after that foundation is proven may downstream Security products be promoted authoritatively:

`Compliance Engine → Evidence-Based Security Architect → Vulnerability & Risk Expert → White-Hat / Continuous Security Assurance → Regulatory Change Engine → Continuous Security Audit Expert`.

## Portfolio distinction
The roadmap explicitly distinguishes:
- `OWNER_PRIORITY` — direction explicitly chosen by the project owner;
- `ARCHITECT_PROPOSED` — supporting/future product tracks proposed by the architecture process;
- `NORTH_STAR` — long-horizon destination rather than present execution authority.

Architect-proposed work must not displace the active owner-priority foundation except where it is a direct dependency, a required maturity control, or critical-risk remediation.

## Product promotion rule
For every material product:

`idea → requirement → evidence/discovery → Demo → PoC → MVP → Production`

is independent from:

`CRISP-ML(Q) process phase`

and independent from:

`PX00 M0..M5 maturity`.

Promotion requires the relevant evidence gate, maturity gate, risk gate, independent review where applicable, and green repository validation.

## Planning behavior
At each summit or material new evidence event the roadmap is reviewed for:
- achieved/blocked products;
- dependencies;
- new or changed risks;
- reusable lessons/patterns;
- the narrowest next build that increases real product capability.

The roadmap is a control surface for prioritization. It is not a capability grant and does not authorize FATHER or any agent to perform external actions.
