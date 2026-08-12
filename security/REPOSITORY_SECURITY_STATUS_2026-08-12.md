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
- A standard-library tracked-file secret-hygiene scanner is now executed in CI against the canonical `git ls-files` view.
- Accepted secret-hygiene run `31573355366` passed `24/24` tests, the explicit repository secret scan with `0 findings / 0 errors`, and PX00 contract validation with `0 errors / 0 warnings`.
- Failed runs `31573227207` and `31573246011` are preserved: literal generic-secret fixtures in the tracked test source were detected by the new scanner and were corrected by runtime fixture construction rather than suppressing the control.
- Failed workflow run `31571384335` is preserved as development evidence; it was caused by YAML scalar representation of the hash-locked install command and was corrected without disabling the security control.

## Not verified through the current GitHub integration

The following API reads previously returned `403 Resource not accessible by integration`:

- branch protection details for `main`;
- secret-scanning alert listing.

A `403` is **not** evidence that the feature is disabled and is **not** evidence that it is enabled. The correct state is `UNVERIFIED` until confirmed through an authorized API/UI path.

## Current control state

```text
CI contract validation                  PASS
Dependency provenance / SBOM gate       PASS
Local isolated SBOM reproduction        PASS
Hosted Linux artifact hash lock         PASS
Windows artifact hash execution         PASS
Two-target artifact hash baseline       PASS
Tracked-file secret hygiene             PASS_WITH_SCOPE_LIMITS
Tracked secret findings on accepted run 0
Workflow token permission                contents: read
Action identities pinned                 YES
Repository rulesets visible              NONE
main branch protection                   UNVERIFIED
GitHub Secret Scanning                   UNVERIFIED
GitHub Push Protection                   UNVERIFIED
Required status check enforcement        UNVERIFIED
Signed commit requirement                NOT REQUIRED BY CURRENT BASELINE
Release signing                          NOT IMPLEMENTED
External SBOM schema validation          NOT IMPLEMENTED
Vulnerability monitoring                 NOT IMPLEMENTED
```

## Security interpretation

The repository now detects contract regressions, direct dependency/SBOM drift, dependency-lock drift, missing SHA256 artifact hashes and selected high-signal credential leakage in current Git-tracked text files. The declared validator dependency installation paths on both hosted Linux x86-64 and local Windows x86-64 have been executed under exact version pinning, binary-only selection and recorded SHA256 allow-lists.

Artifact hashes prove that installed bytes match accepted distribution digests; they do not prove publisher identity, absence of future vulnerabilities or release authenticity. The internal secret-hygiene gate likewise does not prove universal secret absence: Git history, binary/encoded material, ignored/untracked files and credential formats outside its declared patterns remain outside this baseline.

A successful CI workflow still does not stop an administrator or other authorized writer from pushing a commit directly to `main` unless an appropriate branch/ruleset policy exists. Therefore CI **execution**, dependency artifact integrity and tracked-file secret detection are accepted, while CI **enforcement as a merge/push gate** remains unproven.

GitHub Secret Scanning and Push Protection must still be verified separately; the internal scanner is not recorded as a substitute for those platform controls.

## Required next controls

1. Verify or establish a `main` branch/ruleset policy appropriate to the project's current single-maintainer phase.
2. Require the `PX00 Contract Validation / Validate contracts` check before governed merges once PR-based change control becomes the normal workflow.
3. Verify GitHub Secret Scanning and Push Protection for the public repository.
4. Before a releasable distribution, decide the minimum justified vulnerability-monitoring and release-signing controls.

## Occam constraint

Do not add enterprise-grade approval bureaucracy or a large dependency/security stack merely for appearance. Current minimum useful controls are: exact dependency pin + SBOM + SHA256 artifact lock + deterministic tests + tracked-file secret detection + CI. Repository change-control enforcement remains the separate unresolved boundary that prevents these checks from being called non-bypassable.