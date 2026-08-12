# TF-0026 — Synthetic Governed Execution Boundary

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / CI PASS  
**Decision:** KEEP / NEXT: POLICY EXTRACTION

## Trigger

TF-0025 established executable validation for ActionRequest, Tool Definition and Capability Grant contracts. GitHub Actions then passed after Tree_F sequence correction, opening the explicitly bounded next gate: one deterministic, side-effect-free execution path.

## Material change

The first executable governed action path now exists:

```text
ActionRequest
→ AuthorityDecision
→ CapabilityGrant
→ Deterministic Tool Boundary
→ MaterialEvent
→ GovernedResult
```

Implemented files:

- `px00/kernel/__init__.py`
- `px00/kernel/synthetic.py`
- `px00/tools/__init__.py`
- `px00/tools/deterministic.py`
- `tests/test_synthetic_kernel.py`

## Scope

The runtime supports exactly one synthetic capability:

```text
math.multiply
```

with target:

```text
synthetic://math.multiply
```

The capability is `S0`, `PUBLIC`, `A1` and has no network, filesystem mutation, subprocess, connector, model or external side effect.

## Proven invariants

The executable tests verify:

- valid scoped multiply completes;
- absent authority returns `DENIED` and issues no grant;
- capability mismatch is denied before execution;
- side-effect overflow is denied before execution;
- privileged adapter hints do not expand execution privilege;
- executor payload fields claiming authority or control transitions have zero control-plane effect;
- target mismatch blocks at the Tool Boundary;
- consumed grants cannot be replayed;
- data-classification overflow blocks;
- grant/request identity mismatch blocks.

## Algorithms / dependencies

No new third-party dependency.

The implementation uses Python standard-library dataclasses and UUID identifiers plus the existing PX00 package. Boundary validation is explicit and fail-closed.

The code is intentionally not a generic workflow engine. It is a proof that control-plane authority can remain separate from execution mechanics.

## CI evidence

GitHub Actions run `31588037787` completed successfully on commit `3f6d31f446db9d23e0f8fd8f128a919d428c1e9f`.

All workflow stages passed:

- dependency installation/consistency;
- unit + repository integration tests;
- secret hygiene scan;
- full PX00 repository contract validation.

## Security conclusion

`PASS_WITH_ACTIONS`.

The synthetic path proves several non-bypass properties in executable form, but it is not production authorization. Authority logic is still deliberately hardcoded to the synthetic capability and must be extracted into a governed Policy/Profile Engine before real tools are introduced.

Live GitHub, mail, shell, database, filesystem mutation and network adapters remain blocked.

## Evaluation

- control/execution separation: 5/5;
- deterministic reproducibility: 5/5;
- external attack surface: 5/5 for current synthetic scope;
- policy maturity: 2/5 because synthetic authority rules are hardcoded;
- production readiness: 1/5 by design.

Scores are coarse engineering decision aids, not statistical measurements.

## Next gate

Define and validate the Policy/Profile Engine that resolves effective policy from project, organization, jurisdiction, tool, data classification and explicit approvals. Replace hardcoded synthetic authorization with policy-derived decisions while keeping the synthetic tool as the only executable adapter until policy tests pass.
