# ADR-0056 — AI Project Lifecycle Evidence Gates and Quantitative Risk Overlay

Date: 2026-08-12
Status: ACCEPTED

## Context
New OTUS course material and the CRISP-ML(Q) process model expose a recurring architecture risk: teams often collapse different meanings of Demo, PoC, MVP, Production, ML lifecycle phase and system maturity into one informal progress label. This encourages premature production architecture, accidental promotion of disposable PoC code, business-value claims based only on model metrics, and risk registers that hide tail exposure behind qualitative color/severity labels.

The supplied retail recommendation case also demonstrates why the distinction matters: aggressive business and latency goals coexist with missing raw behavioral data, an overloaded legacy monolith, cross-system data dependencies, absent DS/DE capability and explicit personal-data constraints.

## Decision
PX00 / Factory Builder adopts three independent axes for AI/ML projects:

1. `CRISP-ML(Q) PROCESS PHASE` — what lifecycle work is being performed;
2. `DELIVERY EVIDENCE STAGE` — what question is currently being proven to stakeholders: `DEMO → POC → MVP → PRODUCTION`;
3. `PX00 SYSTEM MATURITY` — assurance/operational maturity `M0..M5`.

No axis may be inferred from another.

For each CRISP-ML(Q) phase, records must explicitly contain requirements/constraints, tasks, risks and QA methods. The process is iterative: later evidence may trigger governed rework to earlier phases.

Delivery promotion is evidence-gated:
- Demo proves shared understanding, not technical feasibility;
- PoC proves a bounded technical hypothesis and produces GO/NO-GO evidence;
- MVP proves measurable value with real users/data in a narrow usable system;
- Production proves dependable operation including SLA/SLO, release governance, security, observability, drift/maintenance, recovery and support.

CI/CD obligations scale with delivery stage. Production controls are not required merely to make an early PoC look mature, but PoC shortcuts must carry explicit expiry stage and may not silently survive promotion.

Qualitative S0..S4 risk remains the governance/severity axis. A second `QUANTITATIVE_RISK_ASSESSMENT` axis is added for measurable risks using a reproducible bounded simulation:
`LOSS = BERNOULLI(probability) × TRIANGULAR(minimum, mode, maximum)`.
At minimum report mean/expected loss, selected tail percentile and probability of exceeding a declared tolerance limit. Seed and trial count are pinned.

## Consequences
Positive:
- avoids false equivalence between PoC, prototype maturity and production readiness;
- makes stage-specific technical debt explicit and disposable where appropriate;
- forces business/product evidence at MVP rather than accepting only technical metrics;
- keeps operational reliability as a separate Production proof;
- adds reproducible quantitative evidence for budget/schedule/cost/outage risks while retaining hard qualitative vetoes;
- gives FATHER an explicit GO/NO-GO/HOLD control surface rather than calendar-driven promotion.

Trade-offs:
- project state becomes multi-dimensional rather than one progress label;
- quantitative risk results depend on assumptions and can create false precision if inputs are weak;
- stage gates require more explicit evidence bookkeeping.

## Guardrails
- unknown risk inputs remain unknown/TBD rather than fabricated;
- mean expected loss never replaces tail risk or S4 veto logic;
- a successful CI workflow is not business acceptance;
- a technically successful PoC is not MVP evidence;
- a successful MVP is not Production reliability evidence;
- risk simulation does not accept risk or grant authority;
- commercial contract guidance is stage/uncertainty guidance, not automatic procurement policy.

## Implementation
- `projects/FATHER_FACTORY_BUILDER/contracts/AI_PROJECT_LIFECYCLE_PROFILE.yaml`
- `projects/FATHER_FACTORY_BUILDER/contracts/AI_DELIVERY_STAGE_GATE.yaml`
- `projects/FATHER_FACTORY_BUILDER/contracts/AI_CICD_STAGE_PROFILE.yaml`
- `schemas/QUANTITATIVE_RISK_ASSESSMENT.yaml`
- `px00/ai_project_lifecycle.py`
- `tests/test_ai_project_lifecycle.py`
- `projects/FATHER_FACTORY_BUILDER/FACTORY_CONSTRUCTION_LIFECYCLE.md`
- `projects/FATHER_FACTORY_BUILDER/RISK_AND_FAILURE_ATLAS.md`
- educational regression seed `projects/FATHER_FACTORY_BUILDER/pilots/retail_ai_recommendation/TECHNOMART_STRATEGY_SEED.yaml`
