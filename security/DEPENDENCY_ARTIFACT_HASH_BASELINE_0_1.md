# PX00 Dependency Artifact Hash Baseline 0.1

**Date:** 2026-08-12  
**Status:** ACCEPTED FOR VALIDATOR SCOPE

## Purpose

Pinning `PyYAML==6.0.3` prevents version drift but does not by itself prove that the downloaded distribution bytes match an explicitly accepted artifact. This baseline adds a small hash-checking layer for the two environments PX00 currently verifies.

## Scope

Supported verification targets for this baseline:

- CPython 3.10, Windows x86-64;
- CPython 3.10, Linux manylinux x86-64 on the GitHub-hosted validator runner.

The hash lock is stored in `requirements-validator-lock.txt`.

## Accepted artifacts

```text
PyYAML 6.0.3

Windows x86-64 wheel
pyyaml-6.0.3-cp310-cp310-win_amd64.whl
SHA256 bdb2c67c6c1390b63c6ff89f210c8fd09d9a1217a465701eac7316313c915e4c

Linux x86-64 wheel
pyyaml-6.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
SHA256 9c7708761fccb9397fe64bbc0395abcae8c4bf7b0eac081e12b809bf47700d0b
```

Source of file identities and digests: PyPI release file metadata for PyYAML 6.0.3.

## Install rule

CI uses:

```text
python -m pip install --no-input --only-binary=:all: --require-hashes -r requirements-validator-lock.txt
```

`--require-hashes` makes the locally recorded hashes mandatory, while `--only-binary=:all:` prevents an unlisted source distribution from becoming an alternate installation path.

Reference: pip Secure Installs / Hash-checking Mode.

## Machine validation

`px00/dependency_provenance.py` now validates:

1. direct requirements remain exact `name==version` pins;
2. the hash-lock file contains the same dependency names and versions;
3. each lock entry contains at least one SHA256 artifact hash;
4. requirements and CycloneDX SBOM remain aligned;
5. the SBOM dependency graph still contains the declared component.

The gate intentionally does not try to model every PyPI platform artifact. New supported execution targets require an explicit successor update with their accepted hashes.

## Failure preserved

The first workflow edit placed `--only-binary=:all:` in a plain YAML scalar. The trailing colon followed by whitespace made the workflow invalid, producing GitHub Actions run `31571384335` with failure before jobs were created. The workflow was corrected by using a folded YAML block scalar; run `31571447150` then passed.

This failed attempt remains part of the development evidence rather than being hidden.

## Security conclusion

`PASS_WITH_ACTIONS` for validator dependency artifact integrity on the two declared targets.

Still not claimed:

- vulnerability absence or continuous vulnerability monitoring;
- signing/attestation of upstream PyPI artifacts;
- release signing of PX00;
- branch/ruleset enforcement;
- production-agent supply-chain readiness.

## Occam constraint

Do not introduce a full package-management stack while PX00 has one runtime dependency. Exact pin + SBOM + locally recorded SHA256 hashes + CI hash enforcement is the minimum useful control at this stage.
