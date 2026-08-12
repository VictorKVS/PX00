# TF-0012 — Isolated Environment Reproducibility PASS

**Date:** 2026-08-12  
**Status:** ACCEPTED  
**Decision:** KEEP / OPEN MINIMAL CI GATE

## Trigger

The owner reran PX00 validation inside a fresh local `.venv` after the shared host Python environment exposed an unrelated package conflict. The purpose was to distinguish PX00 dependency behavior from host-environment contamination.

## Structural effect

New assurance evidence was added:

```text
assurance/
├── runs/
│   └── VALIDATOR-0003_ISOLATED_VENV_RUN_2026-08-12.md
└── records/
    └── ACCEPTANCE-VALIDATOR-ISOLATED-0001.yaml
```

No runtime architecture, role package or protocol structure changed.

## File dossier

### `assurance/runs/VALIDATOR-0003_ISOLATED_VENV_RUN_2026-08-12.md`

**Why:** preserve owner-observed execution evidence from an isolated environment.  
**Input:** clean `.venv`, pinned `requirements-validator.txt`, current repository.  
**Processing:** install → `pip check` → tests → full validator → JSON validator.  
**Output:** reproducibility evidence.  
**Libraries:** `PyYAML==6.0.3`; tests use stdlib `unittest`.  
**DevOps:** proves the local command chain is stable enough to move to disposable CI.  
**Security:** isolates dependency state and removes unrelated global-package contamination from the acceptance basis.

### `assurance/records/ACCEPTANCE-VALIDATOR-ISOLATED-0001.yaml`

**Why:** machine-readable acceptance result.  
**Input:** `VALIDATOR-0003`.  
**Processing:** compare observed results to declared blocking criteria.  
**Output:** `PASS` for local isolated validator scope only.  
**Libraries:** none; declarative YAML.  
**DevOps:** becomes the acceptance predecessor for CI introduction.  
**Security:** explicitly prevents local validator PASS from being misrepresented as production-runtime or release-security approval.

## Observed production-chain result

```text
shared host run
  PASS + unrelated dependency conflict observed
          ↓
isolated .venv
          ↓
PyYAML==6.0.3
          ↓
pip check PASS
          ↓
13/13 tests PASS
          ↓
full repository validator PASS
          ↓
errors=0 warnings=0
```

## Algorithm / dependency assessment

The architecture still needs only deterministic Python validation plus YAML parsing. No evidence justifies adding Poetry, tox, Docker, a workflow framework, database, broker, LLM SDK or additional test framework.

`PyYAML==6.0.3` remains the only direct third-party validator dependency.

## DevOps conclusion

The local commands now have two successful execution contexts:

1. real shared host environment;
2. isolated `.venv` environment.

This is sufficient evidence to justify one minimal CI workflow using the same command chain on a disposable GitHub-hosted runner.

## Security conclusion

`PASS_WITH_ACTIONS`

Local reproducibility is demonstrated. Production authorization, tenant isolation, prompt/model security, tamper-evident event persistence, repository security settings and releasable-build SBOM/signing remain outside this acceptance scope.

## Evaluation

- Correctness: 5/5
- Traceability: 5/5
- Security: 4/5
- Maintainability: 5/5
- Reproducibility: 5/5 local scope
- Complexity / Cost: 1/5 added complexity

These are coarse engineering comparison scores, not statistical quality claims.

## Next gate

Introduce exactly one minimal GitHub Actions contract-validation workflow with read-only repository permission, pinned action identities, explicit Python version and the same `pip check → tests → validator` chain. Record it separately in the next `Tree_F` generation.
