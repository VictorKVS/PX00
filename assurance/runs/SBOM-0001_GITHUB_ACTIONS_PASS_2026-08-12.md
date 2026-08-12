# SBOM-0001 — GitHub Actions Dependency Provenance PASS

**Date:** 2026-08-12  
**Workflow:** `PX00 Contract Validation`  
**Run ID:** `31570702457`  
**Commit:** `cbcd866a99be0f2b0a74cbdfd8adaac45b912418`  
**Result:** PASS

## Environment

- GitHub-hosted runner: Ubuntu 24.04.4 LTS
- Runner image: `ubuntu-24.04`
- Python: CPython 3.10.20
- pip: 26.1.2
- workflow token permission: `contents: read` plus GitHub metadata read

## Dependency installation

The clean runner installed:

```text
PyYAML==6.0.3
```

`python -m pip check` returned:

```text
No broken requirements found.
```

## Tests

The test suite executed the new dependency-provenance cases plus the existing contract tests:

```text
Ran 17 tests
OK
```

Dependency-provenance tests passed for:

- current repository requirements/SBOM agreement;
- rejection of missing SBOM root dependency graph;
- rejection of requirement version drift;
- rejection of non-exact requirement pins.

## Repository validation

The existing full repository validator also remained green:

```text
PX00 contract validation: PASS
errors=0 warnings=0
```

## Acceptance interpretation

The minimal dependency provenance/SBOM gate is accepted at CI level for the current validator scope.

This does not establish branch/ruleset enforcement, secret scanning, push protection, package artifact hash locking, external CycloneDX schema validation, vulnerability monitoring, or release signing.
