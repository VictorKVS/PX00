# DJ-0018 — Policy Snapshot Authority Lineage

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / CI VERIFICATION IN PROGRESS  
**Decision:** KEEP / VERIFY

## Why

Exact policy versions were already pinned into a RUN-specific PolicySnapshot, but authority records were not yet contractually required to prove that the same snapshot was used when an action was allowed, denied or escalated.

## Evidence / files

- `architecture/adr/ADR-0024-policy-snapshot-authority-lineage.md`
- `schemas/RUN_RECORD.yaml`
- `schemas/AUTHORITY_DECISION.yaml`
- `schemas/POLICY_SNAPSHOT.yaml`
- `px00/profile_registry.py`
- `px00/kernel/synthetic.py`
- `tests/test_profile_registry.py`
- `tests/test_synthetic_kernel.py`
- `tests/test_policy_lineage_contracts.py`
- `Tree_F/TF-0029_2026-08-12_POLICY_SNAPSHOT_AUTHORITY_LINEAGE.md`

## Material findings during implementation

A real identity-model defect was found: `PolicySnapshot.snapshot_id` used only the policy-content hash. That meant two different RUNs using identical policy content could receive the same runtime snapshot identity. The implementation was corrected so runtime identity is derived from `run_id + policy_content_hash`, while the content hash remains stable across equivalent policy sets.

This preserves two distinct semantics:

```text
snapshot_id   = identity of this RUN's immutable policy snapshot
snapshot_hash = digest of normalized policy content
```

## Runtime behavior

The synthetic governed kernel now creates a policy snapshot for the request RUN, evaluates policy only against the profiles carried by that snapshot, stores snapshot ref/hash in AuthorityDecision, and refuses to issue a capability grant when RUN, snapshot identity or snapshot hash lineage does not match.

## Tests

New negative cases cover:

- policy snapshot from another RUN;
- tampered policy snapshot reference;
- tampered policy snapshot hash;
- equal policy content across two RUNs producing equal content hash but distinct runtime snapshot identity;
- schema regression that removes policy lineage fields/invariants.

## Dependencies / DevOps

No new dependency or external side-effect path. Existing GitHub Actions contract-validation workflow remains the acceptance gate.

## Security conclusion

This generation strengthens TOCTOU resistance and post-event audit reconstruction. A material action can no longer be treated as correctly authorized merely because some compatible policy existed; the AuthorityDecision must match the exact snapshot pinned to the RUN.

## Next gate

Bind AuthorityDecision and policy snapshot lineage into durable Event/Trace evidence so an event can reconstruct `EVT → AUTH → POLSNAP → exact PolicyProfile versions` without relying on current mutable configuration.
