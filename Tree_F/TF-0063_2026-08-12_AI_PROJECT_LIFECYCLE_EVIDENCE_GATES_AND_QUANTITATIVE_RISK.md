# TF-0063 — AI Project Lifecycle Evidence Gates and Quantitative Risk

Date: 2026-08-12
Status: implemented; final generation CI pending
Project: PROJECT-FFB-0001
ADR: ADR-0056

## Objective
Integrate the new OTUS strategic-delivery material, CRISP-ML(Q), CI/CD maturity guidance and the supplied quantitative risk calculator into the Factory Builder so future AI projects are promoted by evidence rather than by ambiguous labels or calendar pressure.

## Main architecture correction
Three dimensions are now explicitly independent:

`CRISP-ML(Q) PROCESS PHASE ≠ DEMO/POC/MVP/PRODUCTION DELIVERY STAGE ≠ PX00 M0..M5 SYSTEM MATURITY`.

This prevents accidental claims such as `PoC = M1 = ready for MVP` or `MVP = production-ready`.

## Implemented contracts
- `AI_PROJECT_LIFECYCLE_PROFILE.yaml`;
- `AI_DELIVERY_STAGE_GATE.yaml`;
- `AI_CICD_STAGE_PROFILE.yaml`;
- global `QUANTITATIVE_RISK_ASSESSMENT.yaml`.

## Implemented runtime
`px00/ai_project_lifecycle.py` adds:
- CRISP-ML(Q) phase validation requiring requirements/constraints, tasks, risks and QA methods;
- evidence requirements for Demo, PoC, MVP and Production;
- blocking-risk-aware stage evaluation;
- reproducible Bernoulli × triangular risk simulation;
- expected loss, tail percentile and probability-above-tolerance outputs;
- pinned random seed and trial count.

## Tested invariants
`tests/test_ai_project_lifecycle.py` proves that:
- a Demo cannot pass merely because technical metrics exist if stakeholder/problem evidence is absent;
- a PoC can legitimately pass without real users;
- an MVP cannot pass without real users and business evidence;
- Production cannot pass on model/business quality alone without CI/CD, monitoring and recovery evidence;
- an explicit blocking risk prevents promotion even when other evidence is complete;
- quantitative risk simulation is reproducible;
- Monte Carlo mean converges near the analytic expected value for the reference distribution;
- invalid impact distributions fail closed.

## Lifecycle doctrine update
`FACTORY_CONSTRUCTION_LIFECYCLE.md` now includes:
- the six CRISP-ML(Q) phases;
- iterative return to earlier phases;
- stage-specific proof questions;
- explicit disposable PoC debt with expiry stage;
- MVP business/product evidence;
- Production operational evidence;
- stage-aware contract and CI/CD guidance.

## Quantitative risk doctrine
`RISK_AND_FAILURE_ATLAS.md` now keeps qualitative S0..S4 while adding a second measurable risk axis.
Reference model:
`LOSS = BERNOULLI(probability) × TRIANGULAR(minimum, mode, maximum)`.
Report mean, configured percentile and probability above tolerance separately. Quantitative results never override S4 or authorize risk acceptance.

## Educational regression seed
Added `TECHNOMART_STRATEGY_SEED.yaml` from the supplied retail recommendation case. Source facts are separated from open questions and architectural inference. Unknown probabilities/impact ranges remain `TBD` rather than being invented.

The seed encodes:
- 2M MAU, 150 stores, >50k SKU;
- current rule-based recommendation baseline;
- stated +10% AOV goal;
- ≤200 ms recommendation requirement;
- Bitrix/MySQL legacy constraints;
- 1C order source and sparse raw clickstream;
- absent DS/DE team;
- cloud preference and personal-data/public-LLM restriction;
- explicit Demo → PoC → MVP → Production strategy.

## CI/CD implication
The current PX00 validation workflow already has explicit push/PR triggers, a bounded timeout, pinned actions, unit/integration tests, dependency checks, secret scanning and contract validation. This generation therefore does not add deployment complexity prematurely. New stage-aware CI/CD requirements are encoded as project contracts and will be activated when a project reaches the corresponding delivery stage.

## Effect on current summit
`SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR` remains OPEN. TF-0063 is an inserted control-generation triggered by new course evidence; it does not fake progress on the live provider. The live executor will now also carry explicit delivery-stage and CRISP-ML(Q) evidence context.

## Next gate
Continue SUMMIT-FFB-02 by integrating exactly one authorized live AI provider through the already proven executor boundary, while preserving the new stage gate, risk and CI/CD evidence model.
