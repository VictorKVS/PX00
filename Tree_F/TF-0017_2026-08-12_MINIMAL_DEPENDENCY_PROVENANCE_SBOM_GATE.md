# TF-0017 — Minimal Dependency Provenance and SBOM Gate

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / CI ACCEPTANCE PENDING  
**Decision:** KEEP / VERIFY

## Trigger

PX00 has reached the point where executable code depends on one external Python package. The dependency is pinned, but a production-development corpus also needs an explicit machine-readable dependency inventory and a deterministic drift check.

The repository ruleset endpoint was rechecked before this change and still returned an empty set, so branch-gate enforcement remains unresolved and is not falsely marked complete.

## Structural delta

```text
PX00/
├── architecture/adr/
│   └── ADR-0017-minimal-dependency-provenance-and-sbom-gate.md
├── px00/
│   └── dependency_provenance.py
├── security/
│   ├── DEPENDENCY_PROVENANCE_BASELINE_0_1.md
│   └── sbom/
│       └── PX00-validator.cdx.json
├── tests/
│   └── test_dependency_provenance.py
└── Tree_F/
    └── TF-0017_2026-08-12_MINIMAL_DEPENDENCY_PROVENANCE_SBOM_GATE.md
```

## File dossiers

### `px00/dependency_provenance.py`

- **Purpose:** deterministic dependency/SBOM drift validator.
- **Inputs:** `requirements-validator.txt`, tracked CycloneDX SBOM.
- **Outputs:** list of validation errors.
- **Processing:** exact-pin parsing, normalized package-name comparison, PURL consistency, license/provenance presence, dependency-graph comparison.
- **Dependencies:** Python standard library only.
- **DevOps:** exercised by `unittest` discovery in the existing CI workflow.
- **Security:** fails on unpinned requirements or install/SBOM mismatch; no network access and no secret processing.
- **Verification:** positive repository test plus negative drift/unpinned/graph tests.
- **Decision:** KEEP / VERIFY.

### `security/sbom/PX00-validator.cdx.json`

- **Purpose:** machine-readable software bill of materials for the current validator scope.
- **Inputs:** accepted direct dependency pin and official package-registry metadata.
- **Outputs:** CycloneDX 1.7 JSON inventory.
- **Processing:** declarative only.
- **Dependencies:** none at runtime.
- **DevOps:** tracked and compared by the dependency-provenance tests.
- **Security:** improves supply-chain visibility but does not yet provide artifact hash verification or vulnerability monitoring.
- **Verification:** requirement/SBOM agreement test; full external schema validation deferred.
- **Decision:** KEEP / IMPROVE before release.

### `tests/test_dependency_provenance.py`

- **Purpose:** enforce positive and fail-closed dependency provenance behavior.
- **Processing:** verifies current repository agreement and rejects version drift, non-exact pins and missing root dependency graph.
- **Dependencies:** standard-library `unittest`.
- **DevOps:** automatically included by the existing GitHub Actions test discovery.
- **Security:** turns dependency metadata drift into a blocking CI failure.
- **Decision:** KEEP.

### `security/DEPENDENCY_PROVENANCE_BASELINE_0_1.md`

- **Purpose:** defines scope, proof level and explicit limitations of the dependency-provenance control.
- **Processing:** documentation only.
- **Security:** prevents overclaiming; records missing hash pinning, full schema validation, vulnerability monitoring and signing as future release actions.
- **Decision:** KEEP.

### `architecture/adr/ADR-0017-minimal-dependency-provenance-and-sbom-gate.md`

- **Purpose:** records why a small deterministic SBOM gate was selected instead of a larger supply-chain toolchain.
- **Decision:** ACCEPTED.

## Production-chain effect

```text
requirements-validator.txt
        ↓
exact pins
        ↓
CycloneDX SBOM
        ↓
dependency_provenance.py
        ↓
positive + negative tests
        ↓
existing GitHub CI
        ↓
PASS / FAIL
```

A dependency version change without a matching SBOM update is intended to fail the gate.

## Libraries

No new third-party runtime or test library. Existing `PyYAML==6.0.3` remains the only direct third-party validator dependency.

## Security conclusion

`PASS_WITH_ACTIONS`.

The change reduces dependency drift and provenance ambiguity. It does not prove artifact-byte integrity, package signing, vulnerability status, release signing, or non-bypassable branch enforcement.

## Rollback

Revert the introduced files and ADR in Git if the approach is replaced. Preserve this TF record as historical evidence and create a successor record for the replacement mechanism.

## Acceptance

Pending successful GitHub Actions execution with the new tests. Production runtime remains blocked regardless of this gate result.

## Next gate

1. Preserve CI acceptance evidence for this gate.
2. Verify or establish `main` change-control enforcement.
3. Verify secret scanning and push protection.
4. Before releasable distribution, evaluate artifact hashes, schema validation, vulnerability scanning and release provenance/signing.
