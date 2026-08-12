# PX00 Repository Security Status — 2026-08-12

**Scope:** GitHub repository-level controls for `VictorKVS/PX00`  
**Status:** PARTIALLY VERIFIED

## Verified facts

- Repository visibility: `public`.
- Default branch: `main`.
- Connected account has administrative repository permission.
- Repository rulesets endpoint has repeatedly returned an empty set (`[]`): no repository ruleset is currently visible through the API used for this verification.
- Minimal GitHub Actions contract-validation workflow exists and has successful hosted runs.
- Minimal dependency provenance / CycloneDX SBOM gate is implemented and accepted in hosted CI and reproduced in the owner's isolated local `.venv`.
- Local isolated dependency-provenance result: `17/17 PASS`, `pip check` clean, repository validator `PASS`, `0 errors`, `0 warnings`.
- Dependency artifact hash locking is implemented for the two currently verified execution targets: CPython 3.10 Windows x86-64 and Linux manylinux x86-64.
- Hosted Linux hash-lock execution passed in GitHub Actions run `31571447150`.
- Hosted hash-lock test result: `19/19 PASS`, `pip check` clean, repository validator `PASS`, `0 errors`, `0 warnings`.
- Local Windows hash-lock execution passed after a forced binary-only reinstall under `--require-hashes`; the selected artifact was `pyyaml-6.0.3-cp310-cp310-win_amd64.whl`.
- Local Windows result: `19/19 PASS`, `pip check` clean, repository validator `PASS`, `0 errors`, `0 warnings`, clean Git working tree.
- Failed workflow run `31571384335` is preserved as development evidence; it was caused by YAML scalar representation of the new install command and was corrected without disabling the security control.

## Not verified through the current GitHub integration

The following API reads previously returned `403 Resource not accessible by integration`:

- branch protection details for `main`;
- secret-scanning alert listing.

A `403` is **not** evidence that the feature is disabled and is **not** evidence that it is enabled. The correct state is `UNVERIFIED` until confirmed through an authorized API/UI path.

## Current control state

```text
CI contract validation                 PASS
Dependency provenance / SBOM gate      PASS
Local isolated SBOM reproduction       PASS
Hosted Linux artifact hash lock        PASS
Windows artifact hash execution        PASS
Two-target artifact hash baseline      PASS
Workflow token permission               contents: read
Action identities pinned                YES
Repository rulesets visible             NONE
main branch protection                  UNVERIFIED
Secret scanning                         UNVERIFIED
Push protection                         UNVERIFIED
Required status check enforcement       UNVERIFIED
Signed commit requirement               NOT REQUIRED BY CURRENT BASELINE
Release signing                         NOT IMPLEMENTED
External SBOM schema validation         NOT IMPLEMENTED
Vulnerability monitoring                NOT IMPLEMENTED
```

## Security interpretation

The repository now detects contract regressions, direct dependency/SBOM drift, dependency-lock drift and missing SHA256 artifact hashes. The declared validator dependency installation paths on both hosted Linux x86-64 and local Windows x86-64 have been executed under exact version pinning, binary-only selection and recorded SHA256 allow-lists.

Artifact hashes prove that the installed bytes match an accepted distribution digest. They do not by themselves prove publisher identity, absence of future vulnerabilities or release authenticity.

A successful CI workflow still does not stop an administrator or other authorized writer from pushing a commit directly to `main` unless an appropriate branch/ruleset policy exists. Therefore CI **execution** and dependency artifact integrity are accepted while CI **enforcement as a merge/push gate** remains unproven.

Secret-scanning controls must also be verified separately before PX00 can claim repository-level secret prevention/detection coverage.

## Required next controls

1. Verify or establish a `main` branch/ruleset policy appropriate to the project's current single-maintainer phase.
2. Require the `PX00 Contract Validation / Validate contracts` check before governed merges once PR-based change control becomes the normal workflow.
3. Verify secret scanning and push protection for the public repository.
4. Before a releasable distribution, decide the minimum justified vulnerability-monitoring and release-signing controls.

## Occam constraint

Do not add enterprise-grade approval bureaucracy or a large dependency-management stack merely for appearance. Current minimum useful supply-chain controls are: exact pin + SBOM + SHA256 artifact lock + deterministic tests + CI enforcement of the lock. Repository change-control enforcement remains a separate unresolved gate.
