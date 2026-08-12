# FFBJ-0008 — Scenario Suite and Governed Rework

Date: 2026-08-12
Project: `PROJECT-FFB-0001`
Generation: `TF-0061`
ADR: `ADR-0054`

## What changed
Factory Builder moved from one audited functional happy path to a three-scenario behavioral suite.

Implemented:
- explicit governed rework transition after a failed stage;
- one delivered baseline scenario;
- one verification-failure → implementation-rework → re-verification scenario;
- one security-gated refusal scenario;
- machine contract and registry for reusable failure patterns;
- long-lived risk memory for the original missing rework transition.

## Functional evidence
### MVP-FUNC-RUN-0001
`DELIVERED` — deterministic idempotency design remains the baseline useful run.

### MVP-FUNC-RUN-0002
`DELIVERED_AFTER_REWORK`.

Observed chain:
`IMPLEMENT v0 → VERIFY FAIL → REWORK → IMPLEMENT v1 → VERIFY PASS → SOCRATES → KNOWLEDGE → DELIVERY`.

The failed verifier artifact `RW-ART-007` remains preserved. The corrected artifact `RW-ART-008` descends from it, so successful rework does not rewrite the failed history.

### MVP-FUNC-RUN-0003
`BLOCKED_BY_SECURITY`.

A request that would require arbitrary shell execution was stopped at `SECURITY_PRECHECK`. No prototype artifact was created. This is treated as a correct safety outcome, not as a delivery KPI failure.

## Failure memory
- `FFB-FP-0001 VERIFICATION_REWORK_REQUIRED` — controlled by the new explicit rework transition.
- `FFB-FP-0002 SECURITY_SCOPE_BLOCK` — controlled by retaining the bounded M1 authority envelope.

## Risk memory
`RISK-0010` records the discovered workflow gap: the initial state machine could record a failed verification but could not legally return the same RUN to implementation. It is now mitigated for the in-memory M1 reference MVP, but durable distributed rework remains unresolved.

## Maturity impact
The reference MVP now proves behavior under three materially different outcomes instead of a single success case.

Current status:
- M0 audited concept: PASS_WITH_ACTIONS;
- M1 control-flow skeleton: PASS_WITH_RESTRICTIONS;
- M1 functional reference run: PASS_WITH_RESTRICTIONS;
- M1 multi-scenario/rework behavior: implemented, repository CI is the final generation gate;
- live AI executor: not yet integrated;
- production maturity: not claimed.

## Next summit
`SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR`.

Acceptance intent:
replace exactly one bounded deterministic producer step with a governed executor/AI adapter while keeping the deterministic scenario suite green and preserving:
- lineage;
- verifier independence;
- Socrates independence;
- security refusal;
- explicit rework;
- no implicit authority.

If a live executor breaks any of those controls, the experiment is REWORK, not PASS.
