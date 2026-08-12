# SBOM-0002 — Local isolated dependency provenance PASS

**Date:** 2026-08-12  
**Environment:** owner workstation, `G:\1\PX00`, project `.venv`  
**Status:** PASS

## Trigger

The owner pulled the accepted minimal dependency provenance/SBOM gate and executed it in the isolated PX00 virtual environment.

## Observed commands and results

```text
.venv Python -> pip check
No broken requirements found.

python -m unittest discover -s tests -v
Ran 17 tests
OK

python -m px00 .
PX00 contract validation: PASS
errors=0 warnings=0

git status
working tree clean
```

The test set included the four dependency-provenance checks for current repository agreement, SBOM root dependency graph, exact pin enforcement and requirement/SBOM drift detection.

## Interpretation

This is independent local evidence that the accepted `requirements-validator.txt` ↔ CycloneDX SBOM relationship works outside the hosted CI runner and does not break the isolated PX00 environment.

It does not prove artifact-byte integrity, vulnerability absence, repository branch enforcement or production runtime readiness.

## Decision

`KEEP`. Promote the dependency provenance gate from hosted-CI-only evidence to hosted + isolated-local evidence. Continue with artifact hash locking as the next independent supply-chain hardening step while repository ruleset enforcement remains externally unresolved.
