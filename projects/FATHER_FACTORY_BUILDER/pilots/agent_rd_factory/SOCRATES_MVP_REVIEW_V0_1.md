# SOCRATES MVP REVIEW V0.1

Review target: `px00/factory_mvp.py` + `tests/test_factory_mvp.py` + `FFB-MVP-0001`
Reviewer role: Critical Reviewer / Socrates
Date: 2026-08-12
Verdict: REWORK

## What is good
- MVP scope is deliberately narrow.
- Stage skipping is fail-closed.
- producer/verifier assignment equality is rejected.
- untrusted input is blocked before prototype execution unless an explicit trust gate exists.
- security precheck, verification and Socrates are represented as execution gates rather than prose-only promises.
- no material external action exists in the current harness.

## Blocking finding
### SOC-MVP-001 — successful delivery is not terminal
Severity: MAJOR

After `GOVERNED_DELIVERY:PASS`, `stage_index` remains on `GOVERNED_DELIVERY` and `delivered=True`, but `advance()` contains no terminal-state guard. The same RUN can therefore invoke successful delivery repeatedly and append repeated delivery events.

Why it matters:
- weakens exactly-once delivery semantics;
- creates a replay/double-effect design smell before external effects are introduced;
- contradicts the project's wider anti-replay posture.

Required fix:
- successful delivery must make the RUN terminal;
- any further stage advancement must fail closed;
- add a negative test proving duplicate delivery is rejected.

## Non-blocking findings retained for post-MVP hardening
### SOC-MVP-002 — trust gate is currently declarative
`pass_trust_gate()` records a boolean without evidence object, assessor identity or adversarial classifier behavior. Acceptable only because the present MVP uses synthetic/explicitly bounded inputs and no material external action. It is not evidence that `RISK-0002` is closed.

### SOC-MVP-003 — retry after FAIL has no explicit rework object
A failed stage can be retried because the stage does not advance. Trace history preserves FAIL then PASS, which is acceptable for this narrow MVP, but production maturity should bind retry to a rework/replan reason.

## Recommendation
Fix SOC-MVP-001 immediately. Keep SOC-MVP-002 and SOC-MVP-003 visible as maturity backlog. Do not expand features while these are being resolved.
