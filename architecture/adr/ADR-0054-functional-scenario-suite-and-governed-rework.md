# ADR-0054 — Functional Scenario Suite and Governed Rework

Date: 2026-08-12
Status: accepted for M1 reference MVP
Project: PROJECT-FFB-0001

## Context
TF-0060 proved one complete functional Factory MVP path. One successful path is insufficient evidence that the factory behaves correctly under failure, rework and safety blocking.

The original M1 state machine could record `VERIFY_AND_VALIDATE:FAIL` but could not explicitly return the same RUN to implementation. That prevented a complete governed improvement loop inside one append-only lineage.

## Decision
Before integrating a live AI executor, Factory Builder must demonstrate multiple deterministic scenario classes:
1. successful governed delivery;
2. independent verification failure followed by explicit implementation rework and successful re-verification;
3. security-gated refusal before prototype creation when the request exceeds the accepted authority envelope.

Add an explicit `request_rework()` transition to the M1 reference harness. Rework is legal only after a failed stage, requires a reason reference, can move only to an earlier stage, preserves all prior evidence, and resets only assurance state invalidated by the target stage.

Create a stable failure-pattern memory contract and registry so observed failures and safe blocks remain visible across later generations.

## Invariants
- failed evidence is never deleted or rewritten after successful rework;
- rework cannot be used as an arbitrary backward jump after PASS;
- rework cannot move forward;
- the first artifact after rework descends from the failed artifact;
- independent verification remains independent after rework;
- a security block is a valid safe outcome, not a KPI failure to be optimized away;
- failure-pattern memory does not grant runtime authority;
- M1 scenario success does not imply production readiness.

## Evidence
- `px00/factory_mvp.py`
- `px00/factory_mvp_suite.py`
- `tests/test_factory_mvp.py`
- `tests/test_factory_mvp_suite.py`
- `schemas/FACTORY_FAILURE_PATTERN.yaml`
- `FAILURE_PATTERN_REGISTRY_V0_1.yaml`
- `RISK-0010_GOVERNED_REWORK_TRANSITION_GAP.md`

## Consequences
The Factory MVP is no longer evaluated by happy-path completion alone. It must preserve safe refusal and failed-attempt history as first-class outcomes. The next live-executor experiment may replace one deterministic producer step only after this scenario suite remains green.
