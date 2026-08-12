# TF-0027 — Policy/Profile Engine

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / CI VERIFIED  
**Lifecycle decision:** KEEP / EXPAND ONLY THROUGH PROFILE CONTRACTS  
**Primary ADR:** `architecture/adr/ADR-0022-policy-profile-engine.md`

## Trigger

The synthetic governed execution boundary proved `ActionRequest → Authority → Grant → Tool Boundary`, but its initial authority method still contained hardcoded capability and side-effect rules. PX00 requires `global by architecture, regional by policy`, so policy must be evaluated as explicit data rather than embedded executor logic.

## Material structural change

This generation adds:

- `schemas/POLICY_PROFILE.yaml` — common machine-readable restrictive policy profile contract;
- `px00/policy.py` — deterministic fail-closed policy intersection engine;
- `tests/test_policy.py` — positive, negative, order-independence and monotonic-restriction tests;
- integration of `SyntheticGovernedKernel.evaluate_authority()` with `PolicyEngine`;
- authority decisions now preserve policy references and the constraining profile where applicable.

The effective policy model is:

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
ALLOW | DENY | ESCALATE
```

## Intersection semantics

- capability sets intersect;
- explicit deny overrides allow;
- autonomy ceiling is the lowest A0..A4 ceiling;
- side-effect ceiling is the lowest S0..S4 ceiling;
- operation-count ceiling is the minimum positive limit;
- classification must be permitted by every applicable profile;
- target must match every profile that declares target prefixes;
- approval requirements accumulate;
- missing required profile fails closed;
- suspended/retired policy cannot authorize new execution.

## Security invariants

1. Adding a stricter profile cannot widen effective authority.
2. Reordering profiles cannot change the result.
3. Adapter hints and executor payload do not participate in policy computation.
4. Missing policy input does not default to allow.
5. A single restrictive layer can deny an action allowed by all other layers.
6. Approval absence produces `ESCALATE` where the policy requires approval.
7. Policy decision reasoning is represented through explicit reason codes/profile references rather than hidden chain-of-thought.

## CI evidence

The first isolated policy-test commit exposed integration mismatch while the kernel still used the previous assumptions. After routing synthetic authority through the Policy Engine and aligning the tests, GitHub Actions run `31588453074` completed successfully.

The successful run includes the repository unit/integration suite, tracked-file secret hygiene and contract validation workflow.

Failed intermediate evidence is intentionally preserved in GitHub Actions history; run `31588429464` records the pre-integration failure.

## Algorithms / dependencies

Algorithm: deterministic set intersection + ordered minimum ceilings + explicit deny/escalation rules.

New third-party dependencies: **NONE**.

## Evaluation

- authority consistency: 5/5;
- regional/profile extensibility: 5/5;
- deterministic reproducibility: 5/5;
- privilege-drift resistance: 5/5;
- implementation maturity: 3/5 — reference implementation is synthetic and policy schema has not yet been promoted to a full production profile registry.

Scores are coarse engineering decision aids, not statistical measurements.

## Next gate

Create a governed **Profile Registry / Resolver** that pins exact profile versions for a RUN/TRACE and prevents policy changes during an active run from silently changing its authority basis. Then add a dedicated validator rule for `POLICY_PROFILE.yaml` and profile-set completeness before considering any real external adapter.

## Supersession / rollback

This record is append-only. A future policy implementation may change storage or profile specialization, but restrictive-intersection, fail-closed, pinned-version and monotonic-authority invariants require explicit superseding evidence.
