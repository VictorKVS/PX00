# FFBJ-0017 — Decision Materiality Project Norm

Date: 2026-08-13
Status: IMPLEMENTED
Related: ADR-0063, TF-0070, PX00-NORM-DM-0001

Factory Builder now treats decision materiality as mandatory role/protocol design input rather than an informal reviewer preference.

For every material responsibility, a Role Package must identify:
- typical D0–D3 materiality range;
- promotion triggers;
- acceptable evidence classes;
- independent review requirements;
- approval/escalation requirements;
- verification and outcome-learning obligations.

Core invariant:
`higher cost of error / irreversibility / uncertainty / risk → stronger evidence + independent review + approval`.

The design remains proportional: local/conventional D0 choices do not require architecture-review ceremony. A nominally local choice is promoted when its effect is material to security, reliability, legal/safety, cost, public/customer impact or other higher-level properties.

Risk remains a separate axis, but S3 imposes a D2 floor and S4 imposes D3 while keeping veto semantics.

This lets the evidence-first Security Knowledge approach become a reusable Factory Builder principle for all future professional roles without cloning Security-specific source semantics into unrelated professions.
