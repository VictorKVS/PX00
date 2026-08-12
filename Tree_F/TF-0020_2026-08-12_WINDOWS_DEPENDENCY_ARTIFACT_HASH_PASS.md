# TF-0020 — Windows dependency artifact hash PASS

**Date:** 2026-08-12  
**Status:** ACCEPTED  
**Decision:** KEEP

## Trigger

`TF-0019` introduced the SHA256 artifact lock and proved the hosted Linux path. The remaining declared verification target was the owner's isolated Windows x86-64 environment.

## Structural delta

Added:

```text
assurance/runs/HASHLOCK-0002_WINDOWS_LOCAL_PASS_2026-08-12.md
assurance/records/ACCEPTANCE-HASHLOCK-WINDOWS-0001.yaml
Tree_F/TF-0020_2026-08-12_WINDOWS_DEPENDENCY_ARTIFACT_HASH_PASS.md
journal/2026-08-12_WINDOWS_HASH_LOCK_PASS.md
```

Modified:

```text
PX00.yaml
security/REPOSITORY_SECURITY_STATUS_2026-08-12.md
```

No runtime dependency, framework, service, network capability or production-agent behavior is added by this generation.

## Executed evidence

Owner executed the hash-locked install in the isolated Windows environment after synchronizing the repository.

Observed:

```text
pyyaml-6.0.3-cp310-cp310-win_amd64.whl downloaded
PyYAML 6.0.3 installed under --require-hashes and --only-binary=:all:
pip check: No broken requirements found.
19 tests: PASS
PX00 validator: PASS
errors=0
warnings=0
git status: clean
```

## Production-chain interpretation

The validator dependency path is now evidenced on both currently declared targets:

```text
exact dependency pin
→ CycloneDX SBOM
→ requirements/SBOM agreement
→ SHA256 artifact allow-list
→ hosted Linux hash-enforced install PASS
→ local Windows hash-enforced install PASS
→ deterministic tests PASS
→ repository contract validator PASS
```

## Algorithms / libraries

No algorithm or library change. Existing pip hash-checking mode and the previously implemented deterministic provenance validator are exercised against the Windows artifact.

## DevOps

No new CI workflow is added. Hosted Linux remains automated; Windows is currently a controlled local acceptance target. A Windows CI matrix is deliberately deferred until repeated Windows-specific regression value justifies the cost and complexity.

## Security conclusion

`PASS_WITH_ACTIONS` for the broader repository assurance state; `PASS` for the two-target validator artifact hash-lock control.

Improved / now evidenced:

- exact version pin;
- SBOM agreement;
- SHA256 artifact lock;
- binary-only install;
- Linux hosted execution;
- Windows isolated execution.

Still unresolved:

- repository ruleset / branch protection enforcement;
- required CI status check enforcement;
- secret scanning / push protection verification;
- vulnerability monitoring policy before release;
- release provenance/signing when a releasable artifact exists.

## Rollback

Do not remove accepted hashes merely to bypass an installation failure. If a supported wheel changes, requires another platform, or is replaced by a newer dependency version, update the pin/SBOM/hash baseline as one governed change and preserve the old TF records.

## Next gate

Establish or verify the `main` repository change-control boundary. Production runtime remains blocked.
