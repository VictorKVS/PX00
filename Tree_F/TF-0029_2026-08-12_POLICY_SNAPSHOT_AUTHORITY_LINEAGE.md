# TF-0029 — Policy Snapshot Authority Lineage

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / CI VERIFICATION IN PROGRESS  
**Lifecycle decision:** KEEP / VERIFY  
**Primary ADR:** `architecture/adr/ADR-0024-policy-snapshot-authority-lineage.md`

## Trigger

TF-0028 introduced exact-version policy resolution and immutable RUN-bound policy snapshots. The remaining gap was that `RUN_RECORD` and `AUTHORITY_DECISION` did not require the same snapshot identity/hash, leaving authority reconstruction ambiguous.

## Material structural change

The authority production chain is now explicitly bound:

```text
PolicyProfile exact versions
→ PolicySnapshot
→ RUN_RECORD policy ref/hash
→ AuthorityDecision policy ref/hash
→ ACTREQ
→ CapabilityGrant
→ Tool Boundary
→ Event / Artifact
```

## Changed artifacts

- `schemas/RUN_RECORD.yaml` — adds pinned policy snapshot ref/hash and matching-decision invariant.
- `schemas/AUTHORITY_DECISION.yaml` — adds run/action request identity plus mandatory policy snapshot ref/hash/algorithm and exact profile refs.
- `schemas/POLICY_SNAPSHOT.yaml` — separates runtime snapshot identity from policy-content hash semantics.
- `px00/profile_registry.py` — snapshot runtime identity is now derived from RUN + policy content hash while `snapshot_hash` remains content-only SHA-256.
- `px00/kernel/synthetic.py` — authority evaluation and grant issuance enforce active RUN policy lineage.
- `tests/test_profile_registry.py` — proves equal policy content can share hash but not runtime snapshot identity across RUNs.
- `tests/test_synthetic_kernel.py` — proves run/ref/hash mismatch blocks grant/execution.
- `tests/test_policy_lineage_contracts.py` — schema-regression tests for lineage invariants.

## Core invariants

1. `snapshot_id` identifies one runtime snapshot bound to one RUN.
2. `snapshot_hash` identifies normalized policy content and may be equal across different RUNs.
3. AuthorityDecision must match the active RUN snapshot identity and hash.
4. Snapshot run mismatch denies authority.
5. Snapshot ref/hash mismatch prevents capability grant issuance.
6. New policy versions never mutate a previously pinned RUN snapshot.
7. Executor/tool/source output cannot change policy lineage.

## Algorithms / dependencies

No new dependency. Runtime identity uses SHA-256 over `run_id:policy_content_hash`; policy-content hashing remains deterministic JSON normalization + SHA-256. Existing PyYAML is reused only in contract tests.

## Security conclusion

`PASS_WITH_ACTIONS` pending final CI state for the complete generation. The change closes a policy TOCTOU/reconstruction gap by making the policy state used for authority both identifiable and content-verifiable.

## Next gate

After CI PASS, propagate the pinned policy snapshot lineage into durable RUN/Event evidence and ensure every material event can trace to the exact AuthorityDecision and policy snapshot that authorized it.
