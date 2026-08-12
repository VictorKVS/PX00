# TF-0070 — Decision Materiality Project Norm

Date: 2026-08-13
Status: IMPLEMENTED
ADR: ADR-0063

## Objective
Turn the repeatedly stated principle "the higher the cost of error, irreversibility and risk, the stronger the evidence" into a permanent, enforceable project norm across FATHER, Factory Builder and professional domain knowledge.

## Implemented
1. `governance/DECISION_MATERIALITY_STANDARD.md` — canonical `PX00-NORM-DM-0001`.
2. `schemas/DECISION_MATERIALITY.yaml` — D0–D3 machine-readable evidence/review floors.
3. `px00/decision_materiality.py` — fail-closed reference evaluator.
4. `tests/test_decision_materiality.py` — negative and positive behavioral evidence.
5. `governance/FATHER_CONSTITUTION.md` — constitutional invariant added.
6. `projects/FATHER_FACTORY_BUILDER/ROLE_AND_KNOWLEDGE_DESIGN_DOCTRINE.md` — every material role must declare materiality range/promotion rules.
7. KNOWLEDGE_CORE `PROFESSIONAL_DECISION_RECORD` aligned to `PX00-NORM-DM-0001`.

## Core rule
`higher cost of error / irreversibility / uncertainty / risk → stronger evidence + review + approval`.

## Classes
- D0: local/conventional;
- D1: implementation;
- D2: architecture/product;
- D3: regulated/safety/critical.

## Risk floor
- S3 cannot be governed below D2.
- S4 cannot be governed below D3 and keeps veto semantics.

## Anti-bureaucracy
The norm is proportional. D0 remains lightweight. A low-level decision is promoted only when it can materially affect a higher-level property.

## Fail-closed behavior proven by tests
- architecture boundary declared as D0 is rejected as under-classified;
- S3 declared as D1 is rejected;
- S4 declared as D2 is rejected even when all other dimensions are low;
- D2 without full evidence is rejected;
- D2 without independent review is stopped;
- D3 without qualified review/approval is stopped;
- D0 local convention passes without unnecessary review.

## Architectural outcome
Security is no longer the only domain with evidence discipline. The same governance expectation can now be applied to architecture, programming, analytics, SRE, AI/ML, finance, legal and future engineering roles while allowing each professional KB to define its own authoritative source/evidence taxonomy.

## Next
Use the norm in the first real professional decision record. The best first candidate is a bounded Security/architecture decision where hard normative requirements, business constraints, budget and 2–5 viable implementation options can be compared with explicit evidence and independent review.
