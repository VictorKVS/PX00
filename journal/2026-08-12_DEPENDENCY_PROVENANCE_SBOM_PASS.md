# 2026-08-12 — Dependency Provenance / SBOM Gate PASS

PX00 added the first machine-readable dependency provenance gate for the minimal validator runtime.

## Result

- direct dependency remains `PyYAML==6.0.3`;
- CycloneDX 1.7 SBOM added at `security/sbom/PX00-validator.cdx.json`;
- standard-library dependency/SBOM validator added;
- four dependency-provenance tests added;
- GitHub Actions run `31570702457` completed successfully;
- clean-runner `pip check`: PASS;
- total tests: `17/17 PASS`;
- repository contract validation: `PASS`, `0 errors`, `0 warnings`.

## Decision

`KEEP` for the current architecture-baseline validator scope.

No new third-party runtime dependency was introduced to implement the gate.

## Remaining security gates

Repository ruleset/main enforcement, secret scanning and push protection remain unverified. Artifact hash locking, external CycloneDX schema validation, vulnerability monitoring and release signing remain future release controls.

Production runtime remains blocked.
