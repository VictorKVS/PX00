# Policy/Profile Engine — 2026-08-12

**Development journal entry:** `DJ-0016`  
**Status:** IMPLEMENTED / CI VERIFIED  
**Decision:** KEEP / CONTINUE WITH PROFILE REGISTRY

## Why

The first synthetic governed runtime proved the Action Request / Authority / Capability Grant / Tool Boundary chain, but authority still contained hardcoded synthetic policy rules. That would not scale to project, organization, jurisdiction, tool and data-classification differences and would violate the intended `global core / regional policy` architecture.

## What changed

- Corrected duplicate ADR numbering introduced during rapid development:
  - Minimal Governed Execution Kernel moved to `ADR-0020`.
  - Governed Action Request / Tool Boundary moved to `ADR-0021`.
  - duplicate `ADR-0016`/`ADR-0017` files were removed because those identifiers were already occupied by established repository-assurance ADRs.
  - `TF-0023` and `TF-0024` references were corrected to the new ADR identities.
- Added `ADR-0022 — Policy/Profile Engine`.
- Added `schemas/POLICY_PROFILE.yaml`.
- Added `px00/policy.py` with deterministic restrictive policy intersection.
- Added `tests/test_policy.py`.
- Modified `px00/kernel/synthetic.py` so policy evaluation is no longer hardcoded in the kernel.
- Modified synthetic runtime tests to assert policy-backed authority behavior.
- Added `TF-0027_2026-08-12_POLICY_PROFILE_ENGINE.md`.

## Policy algorithm

```text
ROLE
∩ PROTOCOL
∩ PROJECT
∩ ORGANIZATION
∩ JURISDICTION
∩ TOOL
∩ DATA
∩ APPROVAL
        ↓
Effective Policy
        ↓
ALLOW | DENY | ESCALATE
```

Capabilities and classifications are restrictive intersections. A0..A4 and S0..S4 use the lowest applicable ceiling. Operation counts use the minimum positive limit. Explicit deny overrides allow. Required approvals accumulate. Missing required profile fails closed.

## Verification

The first policy-test-only commit produced GitHub Actions failure `31588429464`, which is retained as development evidence. After integration into the synthetic kernel and test alignment, run `31588453074` completed successfully.

The successful workflow verifies unit/integration tests, dependency consistency, tracked-file secret hygiene and repository contract validation.

## Security conclusion

`PASS_WITH_ACTIONS`.

The material improvement is removal of authorization facts from execution code. A role, tool adapter or model cannot widen authority by changing its own implementation. The effective policy is now reproducible from explicit profile inputs and yields reason codes/profile references.

Remaining actions before any real external adapter:

- add profile registry/resolver and immutable run-time version pinning;
- add dedicated repository-validator rules for `POLICY_PROFILE.yaml` and complete profile sets;
- preserve effective policy snapshot/hash in RUN/TRACE evidence;
- keep network, shell, mail, database and production mutation adapters blocked.

## Next gate

Implement a minimal Profile Registry / Resolver that resolves exact versions for all eight profile layers and binds them to a run before authority evaluation. A profile update after run start must not silently change the run's authority basis.
