# TF-0028 — Policy Profile Registry and Run Pinning

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / CI VERIFIED  
**Lifecycle decision:** KEEP  
**Primary ADR:** `architecture/adr/ADR-0023-policy-profile-registry-and-run-pinning.md`

## Trigger

The Policy/Profile Engine can compute effective restrictions, but reproducibility requires each RUN to use exact immutable policy inputs rather than mutable profile names.

## Material change

This generation adds:

- `schemas/POLICY_SNAPSHOT.yaml` — run-pinned policy snapshot contract;
- `px00/profile_registry.py` — exact-version registry/resolver and deterministic SHA-256 snapshot hashing;
- `tests/test_profile_registry.py` — fail-closed resolution and reproducibility tests.

## Production chain

```text
Policy profiles
→ exact profile_id@version resolution
→ required-type completeness check
→ ACTIVE-state check
→ deterministic normalization
→ SHA-256 snapshot hash
→ immutable RUN policy snapshot
→ Policy Engine
→ Authority Decision
```

## Core invariants proven

1. Every required profile type is resolved exactly before snapshot creation.
2. Unknown version fails closed.
3. Inactive profile cannot enter a new snapshot.
4. Duplicate exact `(profile_id, version)` is rejected.
5. Profile input order does not affect snapshot hash.
6. Material policy change changes the hash.
7. Existing snapshot remains stable after a new version is registered.
8. A new RUN may explicitly pin the new version.
9. Snapshot identity is derived from normalized policy content, not executor claims.

## Algorithms / dependencies

Deterministic serialization uses Python standard-library `json` with sorted keys and stable normalization of set/tuple fields. Integrity fingerprint uses standard-library `hashlib.sha256`.

New third-party libraries: `NONE`.

The hash is evidence of exact normalized content. It is not a cryptographic signature or administrator-tamper proof.

## Security conclusion

`PASS_WITH_ACTIONS`.

This generation prevents silent policy drift for active RUNs and creates reproducible authority inputs. A future revocation mechanism may explicitly stop a RUN, but registry updates cannot silently migrate its pinned profile set.

Remaining work includes binding the snapshot reference/hash into canonical RUN and Authority Decision evidence and later protecting policy distribution/storage against unauthorized modification.

## CI evidence

GitHub Actions run `31588813999` completed the material validation steps successfully:

- unit and repository integration tests: PASS;
- secret hygiene: PASS;
- repository contract validation: PASS.

## Next gate

Bind `policy_snapshot_ref` and `policy_snapshot_hash` into RUN/Authority evidence so every material authority decision can be reproduced against the exact policy set used at execution time.
