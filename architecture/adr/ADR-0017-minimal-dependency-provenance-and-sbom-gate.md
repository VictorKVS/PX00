# ADR-0017 — Minimal Dependency Provenance and SBOM Gate

**Date:** 2026-08-12  
**Status:** ACCEPTED

## Context

PX00 now has one executable third-party dependency, `PyYAML==6.0.3`, a reproducible isolated environment and a passing GitHub Actions contract gate. The next release-assurance need is to make dependency provenance machine-readable and make dependency drift detectable without adding an oversized software-supply-chain platform.

Repository branch/ruleset enforcement is still not evidenced, so this decision does not treat CI execution as non-bypassable change control.

## Decision

Adopt a minimal dependency-provenance baseline consisting of:

- exact direct version pins in `requirements-validator.txt`;
- a tracked CycloneDX 1.7 JSON SBOM for the validator;
- deterministic standard-library validation of requirement/SBOM agreement;
- positive and negative unit tests automatically executed by the existing CI workflow;
- explicit recording of package source and license metadata;
- no new runtime dependency solely for SBOM generation or validation at this phase.

## Rationale

The current dependency graph contains one direct library and no declared transitive runtime dependency. A separate package manager, container scanner, SBOM generator service or vulnerability platform would add more software than the dependency surface being governed.

The selected mechanism gives immediate value: any version change in `requirements-validator.txt` must be accompanied by a corresponding SBOM change or CI fails.

## Consequences

Positive:

- dependency inventory becomes machine-readable;
- requirement/SBOM drift becomes testable;
- package source and license metadata have a governed location;
- CI automatically evaluates the new gate;
- no new third-party runtime dependency is introduced.

Limitations:

- package artifact hashes are not yet pinned;
- full CycloneDX schema validation is not yet part of CI;
- vulnerability monitoring, attestations, signing and release provenance are deferred;
- repository change-control enforcement remains a separate unresolved gate.

## Security decision

`PASS_WITH_ACTIONS`.

This gate is sufficient for the current architecture-baseline validator. Any releasable distribution must revisit artifact integrity, vulnerability status, signing/attestation and full release SBOM requirements.
