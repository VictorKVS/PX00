# TF-0061 — Factory MVP Scenario Suite and Governed Rework

Date: 2026-08-12
Status: implemented; final CI pending
Project: PROJECT-FFB-0001
ADR: ADR-0054

## Objective
Prove that the Agent R&D Factory M1 reference MVP behaves correctly across success, failed verification with rework, and security-gated refusal before introducing a live AI executor.

## Implemented
- governed `request_rework()` transition in `px00/factory_mvp.py`;
- multi-scenario harness `px00/factory_mvp_suite.py`;
- `tests/test_factory_mvp_suite.py` plus rework invariants in `tests/test_factory_mvp.py`;
- `schemas/FACTORY_FAILURE_PATTERN.yaml`;
- first failure-pattern registry for the Agent R&D Factory pilot;
- long-lived risk memory `RISK-0010` for the original rework transition gap.

## Functional scenarios
### SCENARIO-IDEMPOTENCY
Outcome: `DELIVERED`.
Purpose: retain the TF-0060 deterministic functional success baseline.

### SCENARIO-VERIFICATION-REWORK
Outcome: `DELIVERED_AFTER_REWORK`.
Observed chain:
`IMPLEMENT v0 → VERIFY FAIL → REWORK → IMPLEMENT v1 → VERIFY PASS → SOCRATES → DELIVERY`.

The failed verifier artifact `RW-ART-007` remains in the append-only lineage. The corrected implementation artifact explicitly descends from it.

### SCENARIO-SECURITY-BLOCK
Outcome: `BLOCKED_BY_SECURITY`.
A request for arbitrary shell material is stopped at `SECURITY_PRECHECK` because material external action is outside this M1 authority envelope. No prototype artifact is created.

## Failure memory
- `FFB-FP-0001 VERIFICATION_REWORK_REQUIRED` — controlled by explicit governed rework;
- `FFB-FP-0002 SECURITY_SCOPE_BLOCK` — retained as a correct safety outcome, not a failure metric to suppress.

## Architectural meaning
Factory Builder now demonstrates three different operational outcomes instead of one happy path. It can preserve a failed attempt, route work backward for explicit correction, re-verify independently, and also refuse unsafe scope before implementation.

## Risk impact
`RISK-0010` is mitigated for the in-memory M1 reference MVP, not fully closed. Durable rework still depends on persistence, transaction semantics, concurrency control, authority integration and full artifact-envelope integrity.

## Summit position
- M0 audited concept: ✅
- M1 control-flow skeleton: ✅
- M1 functional artifact chain: ✅
- M1 multi-scenario + governed rework: ✅ implementation complete, CI pending
- live AI executor: ⏭️ next experiment
- production maturity: not claimed

## Next gate
Keep the entire deterministic scenario suite green while replacing exactly one bounded producer step with a governed live AI/executor adapter. Any regression in lineage, independence, security blocking or rework behavior blocks that experiment.
