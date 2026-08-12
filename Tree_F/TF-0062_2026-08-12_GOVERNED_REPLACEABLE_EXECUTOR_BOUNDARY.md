# TF-0062 — Governed Replaceable Executor Boundary

Date: 2026-08-12
Status: implemented; final generation CI pending
Project: PROJECT-FFB-0001
ADR: ADR-0055

## Objective
Create the boundary required to replace one deterministic producer step with a real worker later, without coupling FATHER/Factory Builder to one provider or allowing executor output to become implicit authority or acceptance.

## Implemented
- `schemas/EXECUTOR_DEFINITION.yaml`;
- `schemas/EXECUTOR_INVOCATION.yaml`;
- `px00/executors.py` with `GovernedExecutorBoundary` and adapter protocol;
- local `ScriptedExecutorAdapter` test worker;
- `px00/factory_executor_case.py` proving worker replacement after verifier failure;
- `tests/test_executors.py` covering pinning, stage/assignment controls, authority injection rejection, external-effect prohibition, security-before-executor behavior and replacement lineage;
- `FFB-FP-0003 EXECUTOR_CANDIDATE_REJECTED`;
- `RISK-0011 LIVE_EXECUTOR_PROVIDER_BOUNDARY_UNPROVEN`.

## Proven functional chain
`EXEC-TAG-NORM-0001 v0.1 → candidate EX-ART-006 → verifier EX-ART-007 FAIL → governed rework → EXEC-TAG-NORM-0002 v0.2 → candidate EX-ART-008 → verifier PASS → Socrates → delivery`.

Historical facts remain pinned:
- exact executor ID/version/provider/model metadata;
- assignment;
- input artifact;
- bounded input SHA-256;
- candidate output SHA-256;
- output artifact;
- failed verifier evidence.

## Security boundary
The executor experiment cannot:
- enable material external effects;
- run outside the allowed implementation stage;
- impersonate another assignment;
- inject structured `capability_grant`, `authority_decision`, `tool_call`, `tool_result` or `acceptance_record` as runtime authority;
- bypass verification/Socrates merely because invocation completed.

The existing security-block scenario remains before executor invocation and proves that unsafe scope can still stop the RUN without calling the worker.

## Maturity decision
- governed replaceable executor boundary: ✅ implemented and locally proven;
- non-deterministic live provider: ❌ not yet proven;
- `SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR`: 🟡 boundary ready, summit still OPEN;
- production maturity: not claimed.

## Risk
`RISK-0011` explicitly records that provider transport, authentication, timeouts, malformed responses, model alias drift, leakage and non-determinism remain unproven with local test doubles.

## Next gate
Connect exactly one authorized live AI/provider adapter through this boundary. Do not add live tools or material external side effects. A live candidate must still be rejectable by independent verification and enter the existing governed rework loop. If no authorized live provider is available, do not fake summit completion.
