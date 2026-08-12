# TF-0013 — Governed Action Validation Gate

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / REAL REPOSITORY EXECUTION PENDING  
**Decision:** KEEP / VERIFY LOCALLY

## Trigger

ADR-0016 and ADR-0017 introduced the minimal governed execution kernel design and the universal Action Request / Tool Boundary. Those contracts were not yet executable validation targets.

## Material change

This generation extends the existing deterministic PX00 validator so the new action/tool boundary contracts become machine-checked repository invariants before any synthetic kernel runtime is implemented.

Changed or added responsibilities:

- `px00/validator.py`
  - validates `schemas/ACTION_REQUEST.yaml`;
  - validates `schemas/TOOL_DEFINITION.yaml`;
  - validates `schemas/CAPABILITY_GRANT.yaml`;
  - enforces `ACTREQ-` canonical prefix;
  - enforces A0..A4 and S0..S4 enumerations where declared;
  - checks separation between action request and authority;
  - checks tool definitions do not become authority sources;
  - checks tool adapters cannot expand capabilities by contract;
  - checks capability-grant scope/replay/expiry/revocation invariants;
  - requires the three new schemas in whole-repository validation.
- `tests/test_validator.py`
  - adds positive and negative validator tests for governed action, tool and grant contracts.
- `assurance/fixtures/KERNEL-0001_GOVERNED_ACTION_BOUNDARY_ACCEPTANCE.yaml`
  - defines the first LLM-free, network-free, external-side-effect-free kernel/tool acceptance fixture;
  - covers authority absence, capability/target mismatch, grant expiry/revocation/replay, unauthorized adapter, side-effect/data-classification overflow and untrusted executor control attempts.

## Production-chain position

```text
ADR-0016 / ADR-0017
→ canonical schemas
→ executable validator rules
→ negative unit tests
→ KERNEL-0001 acceptance fixture
→ real checkout validation
→ smallest synthetic execution boundary
```

## Algorithms / dependencies

No new dependency. Existing Python deterministic rule evaluation, `PyYAML==6.0.3` and standard-library `unittest` remain sufficient.

The validator is intentionally schema-specific and fail-closed for declared critical invariants. It is not a generic YAML-schema framework and is not a production authorization engine.

## Security conclusion

`PASS_WITH_ACTIONS` at authoring level.

Security properties now explicitly guarded by tests/contracts include:

- request is not authority;
- adapter hint cannot expand permission;
- untrusted executor output cannot mutate control-plane state;
- tool definition does not grant authority;
- adapter cannot expand declared capability;
- capability grant must derive from ALLOW authority;
- replay/expiry/revocation and side-effect ceilings are material blocking conditions;
- first acceptance fixture prohibits network, shell, credentials, customer data and real external side effects.

No production security claim is made because runtime enforcement does not yet exist.

## Verification state

Repository modifications have been committed through GitHub. The authoritative test commands still need execution in the owner's real checkout:

```powershell
python -m unittest discover -s tests -v
python -m px00 .
python -m px00 . --json
```

A failed real-repository integration result blocks synthetic kernel implementation until corrected.

## Next gate

1. Execute the current validator and unit/integration tests in `G:\1\PX00`.
2. Preserve PASS/FAIL as assurance evidence.
3. If PASS, implement only the smallest deterministic `math.multiply` synthetic ActionRequest → Authority → Grant → Tool Boundary → Event/result path.
4. Keep live GitHub/mail/shell/database/network mutation adapters blocked.
