# Policy Profile Registry and Run Pinning — 2026-08-12

**Development journal entry:** `DJ-0017`  
**Status:** IMPLEMENTED / CI VERIFIED  
**Decision:** KEEP

## Why

Policy intersection alone is insufficient for reproducible governed execution. A RUN must preserve the exact policy versions used when authority was evaluated, even if newer policy versions are registered later.

## Evidence / files

- `architecture/adr/ADR-0023-policy-profile-registry-and-run-pinning.md`
- `schemas/POLICY_SNAPSHOT.yaml`
- `px00/profile_registry.py`
- `tests/test_profile_registry.py`
- `Tree_F/TF-0028_2026-08-12_POLICY_PROFILE_REGISTRY_AND_RUN_PINNING.md`

## Data & processing

The new registry resolves explicit `(profile_id, version)` pairs for all required policy layers and fails closed on missing types, unknown versions, type mismatch or inactive profiles. A resolved set is normalized deterministically and hashed with SHA-256. The resulting immutable `PolicySnapshot` carries the RUN ID, exact profile references, normalization identifier and content hash.

A later registry update does not mutate an existing snapshot. New RUNs can explicitly request a newer profile version.

## Algorithms / libraries

Python standard library only: `json` deterministic serialization and `hashlib.sha256`. No new dependency.

## Security conclusion

`PASS_WITH_ACTIONS`. Silent policy drift during an active RUN is blocked by exact-version pinning. The snapshot hash is a reproducibility/integrity fingerprint, not a signature; policy storage/distribution tamper resistance remains a later control.

## Tests / evaluation

Tests cover complete resolution, missing layer, unknown version, inactive profile, duplicate exact version, order-independent hashing, hash change on material policy change, old-snapshot stability after registry updates and explicit new-version pinning.

GitHub Actions run `31588813999` passed unit/integration tests, secret hygiene and repository contract validation material steps.

## Next gate

Bind policy snapshot identity/hash into `RUN_RECORD` and `AUTHORITY_DECISION` contracts and then into the synthetic runtime event chain so any authority decision can be reproduced from exact pinned policy input.
