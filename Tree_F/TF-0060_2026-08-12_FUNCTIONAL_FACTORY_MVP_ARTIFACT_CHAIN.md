# TF-0060 — Functional Factory MVP artifact chain

Date: 2026-08-12
Status: implemented and audited; final generation CI pending
Project: PROJECT-FFB-0001
ADR: ADR-0053

## Objective
Move the Agent R&D Factory from a control-flow skeleton to a useful functional M1 reference MVP that produces and verifies concrete stage artifacts end to end.

## Implemented
- `schemas/FACTORY_STAGE_ARTIFACT.yaml`;
- typed/content-addressed artifact support in `px00/factory_mvp.py`;
- expanded negative tests in `tests/test_factory_mvp.py`;
- first bounded functional case in `px00/factory_mvp_case.py`;
- end-to-end case tests in `tests/test_factory_mvp_case.py`;
- Socrates review `SOCRATES-FFB-FUNC-0001`;
- ARGUS audit `ARGUS-FFB-FUNC-0001`;
- acceptance `FFB-ACCEPT-FUNC-MVP-0001`;
- new long-lived risk `RISK-0009`.

## First functional run
`MVP-FUNC-RUN-0001` processes one engineering problem through the full chain:

`PROBLEM_BRIEF → RESEARCH_EVIDENCE → CLAIM_ASSESSMENT → DESIGN_OPTIONS → SECURITY_PRECHECK_REPORT → PROTOTYPE_ARTIFACT → VERIFICATION_REPORT → SOCRATES_REVIEW → KNOWLEDGE_ADMISSION_RECORD → DELIVERY_PACKAGE`

The case designs a deterministic idempotency identity for retried synthetic delivery using SHA-256 over canonical JSON `[run_id, operation, target]`.

## Proven invariants
- no stage PASS without a fresh typed artifact;
- artifact IDs are append-only;
- payload digests are deterministic;
- MVP artifact lineage is explicit and strict;
- verification comes from the pinned verifier assignment;
- Socrates is independent from producer and verifier;
- gated artifact verdict and runtime outcome cannot contradict each other;
- successful delivery is terminal;
- idempotency identity is not misrepresented as exactly-once execution.

## Audit findings and corrections
Two defects were discovered before acceptance and fixed:
1. delimiter-based idempotency input was ambiguous; replaced with canonical JSON encoding and negative tests;
2. runtime could previously accept PASS while a gated artifact declared FAIL; explicit verdict/outcome consistency is now enforced.

ARGUS also identified `RISK-0009`: the current digest protects artifact payload but not the complete provenance envelope. This is accepted only for the local in-memory M1 reference scope and must be remediated before persistent evidence maturity.

## Maturity decision
- M0 audited concept: ACCEPTED
- M1 control-flow skeleton: ACCEPTED WITH RESTRICTIONS
- M1 functional reference MVP: `PASS_WITH_RESTRICTIONS`
- live autonomous agent factory: NOT CLAIMED
- production readiness: NOT CLAIMED

## Next gate
Exercise the same artifact contract on several different bounded problems to test generality and collect failure/rework evidence. Then replace exactly one deterministic producer stage with a governed executor adapter while preserving all current gates. Wider external-content scope remains blocked until adversarial treatment of `RISK-0002`; persistent evidence maturity requires treatment of `RISK-0009`.
