# TF-0018 — Local dependency provenance PASS

**Date:** 2026-08-12  
**Status:** ACCEPTED  
**Decision:** KEEP

## Trigger

The owner executed the accepted dependency provenance/SBOM gate in the isolated local PX00 `.venv` after pulling `TF-0017`.

## Structural delta

Added assurance evidence only:

```text
assurance/
├── runs/SBOM-0002_LOCAL_ISOLATED_PASS_2026-08-12.md
└── records/ACCEPTANCE-SBOM-LOCAL-0001.yaml
```

No runtime dependency or production capability was added by this evidence generation.

## Result

```text
pip check                     PASS
17 tests                      PASS
PX00 validator                PASS
errors                        0
warnings                      0
working tree                  clean
```

## Processing / algorithms / libraries

No new algorithm or library. Existing dependency-provenance validation was exercised against the real isolated Windows checkout.

## DevOps

Hosted CI evidence from `SBOM-0001` is now complemented by local isolated evidence. This increases reproducibility confidence without adding another test framework.

## Security conclusion

`PASS_WITH_ACTIONS`. Dependency declaration/SBOM agreement is reproduced locally. Artifact-byte integrity, vulnerability monitoring, repository branch enforcement and release signing remain separate controls.

## Verification

See:

- `assurance/runs/SBOM-0002_LOCAL_ISOLATED_PASS_2026-08-12.md`
- `assurance/records/ACCEPTANCE-SBOM-LOCAL-0001.yaml`

## Rollback

No runtime rollback is required. If later evidence invalidates this result, preserve this record and create a successor with the defect and corrected outcome.

## Next gate

Add the minimum artifact hash lock for the two currently verified execution targets: CPython 3.10 Windows x86-64 and GitHub-hosted Linux x86-64.
