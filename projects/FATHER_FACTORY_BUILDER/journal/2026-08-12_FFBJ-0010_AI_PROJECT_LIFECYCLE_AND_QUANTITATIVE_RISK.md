# FFBJ-0010 — AI Project Lifecycle Evidence Gates and Quantitative Risk

Date: 2026-08-12
Project: PROJECT-FFB-0001
Generation: TF-0063
ADR: ADR-0056

## Trigger
New OTUS study material introduced a strategic ascent from Demo through PoC and MVP to Production, together with a CRISP-ML(Q) reference, CI/CD workflow material, a retail recommendation case and a quantitative risk calculator.

## Design response
The material was not copied as a course checklist. It was translated into governed Factory Builder contracts and executable gates.

The central correction is that three labels describe different facts and must never be collapsed:
- CRISP-ML(Q) phase = lifecycle work;
- Demo/PoC/MVP/Production = stakeholder evidence question;
- M0..M5 = implementation assurance/operational maturity.

## Implementation
Added:
- lifecycle profile contract;
- delivery-stage evidence gate contract;
- stage-aware CI/CD profile;
- quantitative risk assessment contract;
- executable lifecycle/risk module;
- unit tests;
- lifecycle doctrine update;
- risk atlas update;
- TechnoMart educational strategy seed.

## Risk lesson
Qualitative risk severity alone is insufficient for economic/project decisions. When meaningful estimates exist, the system now supports reproducible Bernoulli occurrence × triangular impact simulation and keeps mean, tail percentile and probability above tolerance separate.

Quantification is deliberately not used to override hard S4/security/legal/safety vetoes.

## Anti-overengineering decision
The existing repository CI already satisfies the present project need. The CI/CD lesson is therefore captured as a stage-aware contract rather than adding unnecessary deployment jobs now. Production CI/CD complexity will be activated only when the delivery stage requires it.

## Effect on current roadmap
`SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR` remains open. TF-0063 is an evidence-driven inserted generation, not a substitution for the live-provider experiment.

## Next
Integrate one authorized live AI provider through the governed executor boundary and require its run to carry explicit lifecycle stage, CRISP-ML(Q) context, measurable success criteria and risk posture.
