# FFBJ-0009 — Governed Replaceable Executor Boundary

Date: 2026-08-12
Project: `PROJECT-FFB-0001`
Generation: `TF-0062`
ADR: `ADR-0055`

## Achievement
Factory Builder now has a provider-neutral execution boundary that can pin and replace worker implementations without changing the organizational role/assignment or granting the worker implicit runtime authority.

## Functional proof
`MVP-EXEC-RUN-0001` intentionally invokes a bad local worker first:

`EXEC-TAG-NORM-0001 v0.1 → candidate → independent VERIFY FAIL → REWORK → EXEC-TAG-NORM-0002 v0.2 → corrected candidate → VERIFY PASS → SOCRATES → DELIVERY`.

The failed worker version, candidate and verifier finding remain in append-only history after replacement.

## Controls proven
- exact executor/version/provider/model pinning;
- assignment binding;
- bounded input and output candidate hashes;
- no material external effects in M1;
- no executor call after the security gate has blocked the RUN;
- structured authority/tool injection rejected;
- invocation completion does not equal verification or acceptance;
- bad executor output can enter governed rework.

## Failure memory
Added `FFB-FP-0003 EXECUTOR_CANDIDATE_REJECTED`: an allowed worker can execute successfully and still produce bad content. Therefore worker success and task success are distinct states.

## Risk
Added `RISK-0011 LIVE_EXECUTOR_PROVIDER_BOUNDARY_UNPROVEN`.
The boundary is proven only with local test doubles. Live-provider transport/authentication/timeouts/output variability/model drift and provider-side trust assumptions remain unproven.

## Maturity impact
`SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR` is **not closed**. Its prerequisite boundary is ready.

Next gate: connect exactly one authorized live AI/provider adapter with no material external side effects and keep verifier/Socrates/security/rework controls intact.
