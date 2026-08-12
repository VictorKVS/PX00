# HASHLOCK-0001 — GitHub Actions hash-lock PASS

**Date:** 2026-08-12  
**Status:** PASS

## Scope

Verification of the validator dependency artifact hash lock on the GitHub-hosted Linux x86-64 runner.

## Preserved failed attempt

Run `31571384335` failed before jobs were created after the hash-install command was placed in a YAML plain scalar containing `:all:` followed by whitespace. This was a workflow syntax/representation defect, not a package hash mismatch.

The defect was corrected by expressing the command as a folded block scalar.

## Accepted run

GitHub Actions run: `31571447150`  
Commit: `ad810f2fc292864beae1e882c1c7d728dae8506f`

Observed accepted sequence:

```text
Install hash-locked validator dependency   PASS
PyYAML 6.0.3 manylinux x86-64 wheel        installed
pip check                                  PASS
19 tests                                   PASS
PX00 contract validation                   PASS
errors                                     0
warnings                                   0
```

The install command used both `--require-hashes` and `--only-binary=:all:` with `requirements-validator-lock.txt`.

## Interpretation

The Linux CI path now proves that the declared PyYAML version can only install from an artifact matching one of the locally accepted SHA256 values in the lock file.

The Windows artifact hash is declared but requires a separate local isolated hash-install run before its execution path is accepted.

## Decision

`KEEP`. Artifact hash enforcement is accepted for the hosted Linux validator path.
