# HASHLOCK-0002 — Windows local artifact hash-lock PASS

**Date:** 2026-08-12  
**Environment:** owner local isolated `.venv`, Windows x86-64, CPython 3.10  
**Status:** PASS

## Purpose

Close the Windows execution side of ADR-0018 by proving that the recorded PyYAML 6.0.3 Windows wheel hash is accepted by pip hash-checking mode and that the complete PX00 validation suite remains green after the forced reinstall.

## Executed controls

```text
pip install --force-reinstall --no-cache-dir --no-input --only-binary=:all: --require-hashes -r requirements-validator-lock.txt
pip check
python -m unittest discover -s tests -v
python -m px00 .
git status
```

## Observed result

```text
Downloaded artifact: pyyaml-6.0.3-cp310-cp310-win_amd64.whl
Hash-locked install: PASS
Installed version: PyYAML 6.0.3
pip check: No broken requirements found.
Tests: 19/19 PASS
PX00 contract validation: PASS
errors: 0
warnings: 0
Git working tree: clean and synchronized with origin/main at execution time
```

The install used both `--require-hashes` and `--only-binary=:all:`. Therefore the executed Windows dependency artifact had to match one of the SHA256 digests recorded in `requirements-validator-lock.txt`; otherwise pip would have rejected the installation.

## Security interpretation

This proves the currently supported Windows x86-64 validator path at the dependency-artifact level. Together with hosted Linux run `31571447150`, both declared verification targets now have executed hash-lock evidence.

This does **not** prove package publisher identity, future vulnerability absence, repository branch protection, secret-scanning enforcement, or release signing.

## Evidence source

Owner-provided PowerShell execution output from `G:\1\PX00`, preserved as a governed run summary without copying local secrets or unrelated machine state.

## Decision

`KEEP / PASS` for the current two-target validator artifact hash-lock baseline.

## Next gate

Return to repository change-control enforcement: establish/verify protection of `main`, required CI status enforcement, and secret scanning / push protection before widening runtime or producing a releasable distribution.
