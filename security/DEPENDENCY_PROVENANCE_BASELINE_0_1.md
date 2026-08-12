# PX00 Dependency Provenance Baseline 0.1

**Date:** 2026-08-12  
**Scope:** minimal validator runtime only  
**Status:** IMPLEMENTED / CI ACCEPTANCE PENDING

## Goal

Keep the first PX00 executable dependency set explicit, reproducible and reviewable without introducing a package-management framework that the project does not yet need.

## Current dependency surface

The validator has one direct third-party runtime dependency:

```text
PyYAML==6.0.3
```

The authoritative install input is [`../requirements-validator.txt`](../requirements-validator.txt).

The dependency inventory is represented as a CycloneDX 1.7 JSON SBOM in [`sbom/PX00-validator.cdx.json`](sbom/PX00-validator.cdx.json). The package component is identified by Package URL and its source registry reference.

Package registry evidence used for this baseline:

- PyPI release metadata: `https://pypi.org/pypi/PyYAML/6.0.3/json`
- PyPI project release page: `https://pypi.org/project/PyYAML/6.0.3/`

The recorded package license identifier is `MIT`, matching the release metadata available from PyPI at baseline creation.

## Enforcement

[`../px00/dependency_provenance.py`](../px00/dependency_provenance.py) performs deterministic checks using only the Python standard library:

1. Every active requirement must be an exact `name==version` pin.
2. Every pinned PyPI requirement must have one matching SBOM component.
3. SBOM name/version and Package URL must agree.
4. Every component must retain license metadata and an external provenance reference.
5. The root SBOM dependency graph must include the same components.
6. Dependency drift fails the test suite.

[`../tests/test_dependency_provenance.py`](../tests/test_dependency_provenance.py) contains positive and negative checks. The existing GitHub Actions workflow discovers these tests automatically, so no additional CI action or third-party SBOM tool is required at this phase.

## What this baseline proves

- the direct dependency set is explicit;
- the version is pinned;
- the SBOM and install input cannot silently drift while CI is passing;
- package provenance and license metadata have a machine-readable location;
- the control adds no new runtime dependency.

## What this baseline does not yet prove

- downloaded wheel/sdist bytes are hash-pinned;
- the SBOM has been externally validated against the complete CycloneDX JSON schema;
- artifact signatures or package attestations have been verified;
- release artifacts are signed;
- a release SBOM includes operating-system/container components;
- vulnerability status is continuously monitored.

These omissions are intentional. PX00 currently has one direct Python library and no releasable production runtime. Adding a large SBOM/security toolchain now would exceed the demonstrated need.

## Security conclusion

`PASS_WITH_ACTIONS`.

The baseline materially improves software-supply-chain traceability and drift detection. Before a releasable distribution, evaluate hash-locked installation, schema validation, vulnerability scanning, release provenance/signing and full release SBOM generation.

Repository `main` gate enforcement, secret scanning and push protection remain separate controls and must not be inferred from this SBOM baseline.
