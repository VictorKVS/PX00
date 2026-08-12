# Governed Action Validation Gate — 2026-08-12

**Development journal entry:** `DJ-0014`  
**Status:** IMPLEMENTED / CI RE-VERIFICATION IN PROGRESS  
**Decision:** KEEP / VERIFY CI

## Why

The Minimal Governed Execution Kernel and Universal Tool Boundary were already accepted as contracts, but their critical action/authority/tool/grant boundaries were not yet protected by executable validator rules or a dedicated acceptance fixture.

## Evidence / files

- `px00/validator.py`
- `tests/test_validator.py`
- `schemas/ACTION_REQUEST.yaml`
- `schemas/TOOL_DEFINITION.yaml`
- `schemas/CAPABILITY_GRANT.yaml`
- `assurance/fixtures/KERNEL-0001_GOVERNED_ACTION_BOUNDARY_ACCEPTANCE.yaml`
- `Tree_F/TF-0023_2026-08-12_MINIMAL_GOVERNED_EXECUTION_KERNEL.md`
- `Tree_F/TF-0024_2026-08-12_GOVERNED_ACTION_REQUEST_TOOL_BOUNDARY.md`
- `Tree_F/TF-0025_2026-08-12_GOVERNED_ACTION_VALIDATION_GATE.md`
- `architecture/adr/ADR-0016-minimal-governed-execution-kernel.md`
- `architecture/adr/ADR-0017-governed-action-request-and-tool-boundary.md`

## Data & processing

The existing deterministic repository validator now loads and validates the three governed action/tool schemas. It checks the `ACTREQ-` identity boundary, A0..A4 autonomy values, S0..S4 side-effect values, action-request/authority separation, tool non-authority semantics, adapter capability limits and capability-grant replay/scope/revocation invariants.

`KERNEL-0001` defines the first deterministic acceptance boundary with no LLM, network, shell, customer data, credentials or real external side effects. Its negative cases cover missing authority, capability/target mismatch, expired/revoked/replayed grants, unauthorized adapters, side-effect/data-classification overflow and attempts by executor/tool output to alter the control plane.

## Algorithms / libraries

No new dependency. Existing Python deterministic validation, `PyYAML==6.0.3` and standard-library `unittest` remain sufficient.

During implementation the first validator draft was found to use field names that differed from the already committed schemas. The validator was corrected to treat the schemas as the source of truth rather than changing contracts to fit code. This correction is part of the material development evidence.

## DevOps

Changes were written directly to the GitHub `main` branch as discrete commits. Existing GitHub Actions immediately executed the test suite.

The first CI run after this generation produced a useful integration failure: all new governed-action unit tests passed, but `RepositoryIntegrationTests.test_current_repository_contracts` detected duplicate `Tree_F` sequence numbers. The repository already contained material generations through `TF-0022`; the new work had initially reused `TF-0011..TF-0013` based on stale context.

The correction preserves the validator and renumbers the new material generations to the next free sequence:

```text
TF-0023 — Minimal Governed Execution Kernel
TF-0024 — Governed Action Request / Tool Boundary
TF-0025 — Governed Action Validation Gate
```

The duplicate files were removed after their correctly numbered replacements were committed. This is a correction of invalid identifiers, not deletion of accepted unique historical generations.

## Security conclusion

`PASS_WITH_ACTIONS` at authoring level. Contract guards now cover key privilege-boundary invariants. The CI failure demonstrated that the repository integration gate is actively detecting governance-history defects rather than merely checking isolated unit rules.

## Tests / evaluation

CI evidence from the failed run:

- dependency provenance tests: PASS;
- secret hygiene tests: PASS;
- governed action schema tests: PASS;
- role/protocol/acceptance tests: PASS;
- repository integration: FAIL due only to duplicate Tree_F identifiers;
- total: 30 tests, 1 integration failure.

Tree_F identifiers have been corrected and CI re-verification is the current gate.

## Next gate

1. Confirm GitHub Actions PASS on the corrected `TF-0023..TF-0025` sequence.
2. Preserve the successful run as assurance evidence.
3. Implement only the smallest synthetic `math.multiply` ActionRequest → Authority → Capability Grant → Tool Boundary → Event/result path.
4. Keep live GitHub/mail/shell/database/network mutation adapters blocked.
