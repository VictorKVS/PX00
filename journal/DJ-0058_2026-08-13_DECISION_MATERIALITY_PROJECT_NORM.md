# DJ-0058 — Decision Materiality Project Norm

Date: 2026-08-13
Related: ADR-0063, TF-0070

A repeatedly discussed design principle was promoted into a permanent project invariant:

> the higher the cost of error, irreversibility, uncertainty and risk, the stronger the required evidence, independent review and approval.

Implemented `PX00-NORM-DM-0001` with D0–D3 classes, risk floors, proportional evidence obligations, constitutional linkage and a fail-closed runtime reference gate.

Important distinction preserved:
`DECISION MATERIALITY != RISK SEVERITY != MATURITY != DELIVERY STAGE`.

The norm prevents two opposite failures: over-governing trivial decisions and under-governing material architecture/regulated/critical decisions.

Security Knowledge remains the first evidence-first professional domain, but the norm is now general: architecture, software, analytics, operations, finance, legal and future engineering domains must support evidence-backed decisions according to materiality.

Next evidence target: create and exercise a real D2/D3 `PROFESSIONAL_DECISION_RECORD` over canonical professional knowledge and governed independent review.
