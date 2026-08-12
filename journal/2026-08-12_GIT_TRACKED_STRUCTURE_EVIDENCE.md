# 2026-08-12 — Canonical Git-tracked structure evidence

## Decision

PX00 repository structure is henceforth evidenced from Git-tracked paths rather than raw local filesystem enumeration.

## Trigger

A local `tree /F` included `.venv`, Python caches and package-manager internals. The subsequent owner-executed `git ls-files` returned only PX00-controlled tracked content.

## Evidence

- `assurance/runs/STRUCTURE-0001_GIT_TRACKED_FILES_2026-08-12.md`
- `Tree_F/TF-0016_2026-08-12_GIT_TRACKED_STRUCTURE_EVIDENCE.md`
- `.gitignore`

## Rule

```text
git ls-files                = canonical repository structure
physical tree /F            = supplementary workstation diagnostic
```

For structural deltas use `git diff --name-status <base>..<head>` and preserve material decisions in the next append-only `TF-xxxx` record.

## DevOps / security conclusion

No runtime or dependency change. The rule improves reproducibility and provenance by excluding ignored/generated workstation state from product architecture evidence.

**Decision:** KEEP.
