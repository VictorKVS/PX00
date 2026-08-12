# 2026-08-12 — Windows hash-lock acceptance

## Result

The owner reproduced the validator dependency artifact lock on the isolated Windows x86-64 environment.

```text
PyYAML 6.0.3 Windows wheel selected
hash-enforced binary-only reinstall PASS
pip check PASS
19/19 tests PASS
PX00 contract validation PASS
errors=0 warnings=0
git working tree clean
```

## Decision

The current two-target artifact hash-lock baseline is accepted:

- hosted Linux x86-64: PASS;
- local Windows x86-64: PASS.

This closes the execution action left open by `TF-0019` without changing the dependency set or widening runtime authority.

## Evidence

- `assurance/runs/HASHLOCK-0002_WINDOWS_LOCAL_PASS_2026-08-12.md`
- `assurance/records/ACCEPTANCE-HASHLOCK-WINDOWS-0001.yaml`
- `Tree_F/TF-0020_2026-08-12_WINDOWS_DEPENDENCY_ARTIFACT_HASH_PASS.md`

## Security state

Dependency artifact-byte integrity is now executed on both declared validator targets. Repository ruleset/branch enforcement and secret scanning / push protection remain separate unresolved controls.

## Next

Return to the repository change-control gate. Do not widen production runtime merely because the dependency hash-lock gate passed.
