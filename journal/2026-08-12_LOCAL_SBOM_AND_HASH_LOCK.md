# 2026-08-12 — Local SBOM reproduction and dependency artifact hash lock

## Summary

The owner reproduced the accepted dependency provenance/SBOM gate in the isolated local PX00 `.venv`:

```text
pip check                    PASS
17 tests                     PASS
PX00 contract validation     PASS
errors                       0
warnings                     0
working tree                 clean
```

Evidence:

- `assurance/runs/SBOM-0002_LOCAL_ISOLATED_PASS_2026-08-12.md`
- `assurance/records/ACCEPTANCE-SBOM-LOCAL-0001.yaml`
- `Tree_F/TF-0018_2026-08-12_LOCAL_DEPENDENCY_PROVENANCE_PASS.md`

## Next hardening implemented

A hashed dependency lock was added for PyYAML 6.0.3 on the two currently verified validator targets. CI now installs with pip `--require-hashes` and `--only-binary=:all:`.

The first workflow representation failed before job creation (`31571384335`) because the command was written as an invalid YAML plain scalar around the `:all:` fragment. The failure was preserved; the workflow was corrected using a folded block scalar.

Accepted hosted run `31571447150` then produced:

```text
hash-locked install          PASS
pip check                    PASS
19 tests                     PASS
PX00 validator               PASS
errors                       0
warnings                     0
```

Evidence:

- `security/DEPENDENCY_ARTIFACT_HASH_BASELINE_0_1.md`
- `architecture/adr/ADR-0018-hash-locked-validator-dependency-install.md`
- `assurance/runs/HASHLOCK-0001_GITHUB_ACTIONS_PASS_2026-08-12.md`
- `assurance/records/ACCEPTANCE-HASHLOCK-0001.yaml`
- `Tree_F/TF-0019_2026-08-12_DEPENDENCY_ARTIFACT_HASH_LOCK_GATE.md`

## Security conclusion

`PASS_WITH_ACTIONS`.

Hosted Linux artifact integrity is enforced and evidenced. Windows artifact hash execution remains pending local verification. Main branch/ruleset enforcement and secret scanning/push protection also remain unverified and are not claimed as active controls.

## Decision

`KEEP`.
