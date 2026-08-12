# TF-0016 — Git-tracked structure becomes canonical development evidence

**Date:** 2026-08-12  
**Status:** ACCEPTED  
**Decision:** KEEP

## Trigger

A local `tree /F` snapshot included `.venv`, Python caches, pip/setuptools internals and other generated workstation state. The owner then executed `git ls-files`, producing a clean inventory of PX00-controlled repository paths only.

## Decision

For future PX00 structure baselines:

```text
Canonical product structure = Git-tracked repository paths
Diagnostic local structure  = physical filesystem tree
```

Primary commands:

```powershell
git ls-files
git status --short
git diff --name-status <base>..<head>
```

`tree /F` remains useful for troubleshooting the workstation but SHALL NOT be treated as the canonical architecture inventory.

## Why

Physical trees contain environment-specific and generated files. Treating them as product structure would create false architecture changes whenever a virtual environment, package manager, cache or local tool changes. Git-tracked structure is deterministic, reviewable, reproducible in CI and directly comparable between commits.

## Structural observation

The tracked inventory contains the PX00 governance, architecture, assurance, roles, protocols, schemas, validator, tests, security documents and accumulated `Tree_F` records through `TF-0015`. `.venv/` and `__pycache__/` are absent from the tracked inventory as intended by `.gitignore`.

## Processing / algorithms / libraries

No runtime algorithm and no new library. The evidence method is Git index enumeration plus optional commit-to-commit name-status comparison.

## DevOps

Future structure evidence can be generated consistently on Windows, Linux and GitHub-hosted CI without depending on local filesystem noise.

## Security conclusion

`PASS`. This reduces provenance confusion and prevents local third-party/generated files from being misclassified as PX00-owned source. It does not replace dependency provenance or SBOM controls.

## Verification

Owner-executed `git ls-files` output confirmed that local `.venv` contents were not tracked while the intended PX00 source/evidence files were present.

## Rollback

If Git-tracked paths become insufficient for a future deployment topology, add a successor TF record defining an additional governed structure source. Do not rewrite this accepted record.

## Next gate

Establish/verify repository change-control enforcement and then add the minimum dependency provenance/SBOM evidence required before releasable distribution.
