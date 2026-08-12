# TF-0019 — Dependency artifact hash-lock gate

**Date:** 2026-08-12  
**Status:** ACCEPTED WITH ACTIONS  
**Decision:** KEEP

## Trigger

`TF-0017` established exact dependency pins and SBOM agreement. `TF-0018` reproduced that gate locally. The next smallest unresolved supply-chain control was artifact-byte integrity for the one validator dependency.

## Structural delta

```text
requirements-validator-lock.txt
security/DEPENDENCY_ARTIFACT_HASH_BASELINE_0_1.md
architecture/adr/ADR-0018-hash-locked-validator-dependency-install.md
assurance/runs/HASHLOCK-0001_GITHUB_ACTIONS_PASS_2026-08-12.md
assurance/records/ACCEPTANCE-HASHLOCK-0001.yaml
```

Modified:

```text
.github/workflows/contract-validation.yml
px00/dependency_provenance.py
tests/test_dependency_provenance.py
PX00.yaml
```

## File dossier

### `requirements-validator-lock.txt`

**Purpose:** locally record accepted SHA256 distribution hashes for the exact direct dependency.  
**Inputs:** PyYAML 6.0.3 release file metadata.  
**Outputs:** pip hash-checking input for supported validator targets.  
**Processing:** exact pin + SHA256 allow-list.  
**Dependencies:** pip hash-checking mode.  
**Security:** constrains accepted package bytes.  
**Verification:** hosted Linux install passed; Windows execution remains pending.

### `px00/dependency_provenance.py`

**Purpose:** detect drift among direct requirements, hash lock and SBOM.  
**Processing:** parse exact pins, parse SHA256 hashes, compare normalized name/version sets, retain SBOM checks.  
**Dependencies:** Python standard library only.  
**Security:** rejects missing hashes and lock/version drift.

### `.github/workflows/contract-validation.yml`

**Purpose change:** dependency install is now hash-enforced and binary-only.  
**Security:** `--require-hashes` + `--only-binary=:all:`; workflow token remains read-only.  
**Verification:** GitHub run `31571447150` PASS.

## Failed attempt retained

GitHub run `31571384335` failed before any job started. Cause: the first workflow command used a YAML plain scalar in which the `:all:` fragment was followed by whitespace, making the workflow representation invalid. The command was changed to a folded block scalar. The failure is preserved as production-chain evidence instead of being erased.

## Accepted result

```text
hash-locked dependency install   PASS
pip check                        PASS
19 tests                         PASS
PX00 validator                   PASS
errors                           0
warnings                         0
```

Accepted run: `31571447150`.

## Algorithms / libraries

No new runtime library. Added deterministic parsing/comparison logic in the existing validator support package. PyYAML remains the only direct third-party runtime dependency.

## DevOps

CI now validates both dependency metadata and actual accepted artifact hashes for its Linux x86-64 wheel path.

## Security conclusion

`PASS_WITH_ACTIONS`.

Improved:

- exact version pin;
- CycloneDX component inventory;
- declaration/SBOM agreement;
- local SHA256 artifact allow-list;
- CI hash enforcement;
- source-distribution fallback blocked in CI.

Still open:

- execute the Windows hash-lock install in the isolated local `.venv`;
- main branch/ruleset enforcement;
- secret scanning/push protection verification;
- vulnerability monitoring;
- release signing/attestation when a releasable distribution exists.

## Rollback

Revert the hash-lock workflow/install changes only if they block a declared supported target and preserve this record plus failed/successful run IDs. Prefer adding a justified artifact hash over disabling hash checking.

## Next gate

Verify the Windows hash-locked install locally. Repository ruleset enforcement remains a separate externally controlled gate and must not be marked PASS until actually observable.
