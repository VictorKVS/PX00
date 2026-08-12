# STRUCTURE-0001 — Git-tracked repository structure run

**Date:** 2026-08-12  
**Status:** PASS

## Command

```powershell
cd G:\1\PX00
git ls-files
```

## Result

The owner-executed command returned the expected PX00-controlled paths: governance, architecture, assurance, roles, protocols, schemas, validator, tests, security documentation, CI workflow and accumulated `Tree_F` history through `TF-0015`.

Local `.venv/`, `__pycache__/`, pip/setuptools internals and other generated workstation files were absent from the Git-tracked inventory.

## Interpretation

This proves that the physical workstation tree and the product/repository tree must be treated as different evidence classes:

- `git ls-files` = canonical repository structure evidence;
- `tree /F` = supplementary workstation diagnostic evidence.

The distinction avoids false architectural deltas caused by virtual environments, caches and package-manager internals.

## Security conclusion

`PASS` for structure-evidence hygiene. Generated/local dependencies are not misclassified as PX00-owned source. Dependency provenance and SBOM remain separate controls.

## Linked decision

See `Tree_F/TF-0016_2026-08-12_GIT_TRACKED_STRUCTURE_EVIDENCE.md`.
