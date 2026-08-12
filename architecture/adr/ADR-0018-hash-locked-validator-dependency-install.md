# ADR-0018 — Hash-locked validator dependency install

**Date:** 2026-08-12  
**Status:** ACCEPTED

## Context

PX00 already had an exact direct dependency pin and a CycloneDX SBOM, with hosted and isolated-local agreement checks. The remaining supply-chain gap for the validator was that a package version could still be fetched from any distribution artifact accepted by the index/client path without a locally accepted artifact digest.

## Decision

For the currently verified validator environments, add a dedicated hashed requirements file and make CI install from it using pip hash-checking mode with binary-only installation.

The design is intentionally narrow:

```text
requirements-validator.txt
    = human/direct dependency declaration

requirements-validator-lock.txt
    = accepted package version + SHA256 artifact hashes

security/sbom/PX00-validator.cdx.json
    = component/dependency inventory

px00/dependency_provenance.py
    = cross-check of declaration, lock and SBOM
```

Supported artifact hashes are limited to CPython 3.10 Windows x86-64 and Linux manylinux x86-64 because those are the environments already used as acceptance evidence.

## Alternatives rejected

- New dependency manager solely to lock one package — rejected as unnecessary complexity.
- Accept version pin without artifact hashes — rejected because it leaves artifact-byte acceptance implicit.
- Hash every PyPI artifact for every platform — rejected because untested platforms are outside the current support boundary.
- Source distributions — rejected for this gate; CI uses binary-only installation.

## Verification

The first workflow edit failed before job creation because `--only-binary=:all:` was placed in a YAML plain scalar containing a colon followed by whitespace. The failure is preserved as run `31571384335`.

After changing the command to a folded block scalar, GitHub Actions run `31571447150` completed successfully with:

- hash-locked PyYAML installation;
- `pip check` PASS;
- 19 tests PASS;
- full PX00 validator PASS with 0 errors and 0 warnings.

## Consequences

Benefits:

- package version and accepted artifact bytes are both constrained;
- declaration/lock/SBOM drift becomes testable;
- CI proves the Linux artifact hash path;
- the Windows hash is ready for local isolated verification.

Remaining work:

- local Windows hash-install verification;
- repository main/ruleset enforcement;
- secret scanning/push protection verification;
- vulnerability monitoring and release signing only when justified by release scope.

## Decision

`KEEP`. This is the minimum useful artifact-integrity control for the current single-dependency validator.
