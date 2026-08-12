# TF-0013 — Minimal CI Contract Validation Gate

**Date:** 2026-08-12  
**Status:** IMPLEMENTED / EXECUTION PENDING  
**Decision:** KEEP / VERIFY

## Trigger

`TF-0012` demonstrated that the validator passes in a clean local `.venv`. The next minimum-sufficient production control is one disposable CI execution of the same chain.

## Structural change

```text
.github/
└── workflows/
    └── contract-validation.yml

architecture/adr/
└── ADR-0016-minimal-ci-contract-validation-gate.md
```

The role, protocol, knowledge and runtime architecture did not change.

## File dossier

### `.github/workflows/contract-validation.yml`

**Why:** automatically detect contract/repository regression on `push` and `pull_request` to `main`.  
**Input:** repository checkout + `requirements-validator.txt`.  
**Processing:** checkout → setup Python 3.10 → install pinned dependency → `pip check` → 13 tests → full validator.  
**Output:** GitHub Actions PASS/FAIL signal and logs.  
**Libraries/actions:** `PyYAML==6.0.3`; `actions/checkout` and `actions/setup-python` pinned to full commit SHAs.  
**DevOps:** first automated quality gate; no build/deploy/release stage.  
**Security:** `contents: read`, no secrets, no write token, checkout credentials not persisted, five-minute timeout, no customer data or external mutation.

### `architecture/adr/ADR-0016-minimal-ci-contract-validation-gate.md`

**Why:** CI introduces external hosted-runner/action dependencies and therefore needs an explicit material architecture/supply-chain decision.  
**Input:** local shared-host PASS + isolated `.venv` PASS.  
**Processing:** compare automation value against added trust/maintenance cost.  
**Output:** constrained CI decision and residual-risk statement.  
**Libraries:** none; decision record.  
**Security:** records exact action SHAs and the limits of what CI proves.

## Action identities

At introduction time:

```text
actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803  # v6
actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6
```

These are pinned supply-chain dependencies; changing them is a reviewed material change.

## Algorithm

```text
Git push / PR to main
        ↓
clean GitHub-hosted Ubuntu 24.04 VM
        ↓
read-only checkout
        ↓
Python 3.10
        ↓
PyYAML==6.0.3
        ↓
pip check
        ↓
13 unit/integration tests
        ↓
python -m px00 .
        ↓
PASS / FAIL
```

## DevOps conclusion

This is the first justified automated gate. It duplicates the proven local sequence rather than inventing a second CI-specific validation path.

No artifact publishing, deployment, Docker, matrix build, coverage service or broad security scanner was added.

## Security conclusion

`PASS_WITH_ACTIONS`

Strong points: read-only token, pinned action identities, no secrets, bounded job, minimal dependency set and no external side effects.

Open points: actual workflow execution must still pass; hosted runner/PyPI are external trust dependencies; repository secret scanning/branch protection remain separately unverified; SBOM/signing remain release gates.

## Evaluation

- Correctness: 4/5 until first CI PASS
- Traceability: 5/5
- Security: 4/5
- Maintainability: 5/5
- Reproducibility: 4/5 until hosted-runner PASS
- Complexity / Cost: 1/5 added complexity

## Next gate

Observe the first real GitHub Actions run. On PASS, preserve CI run evidence and acceptance without widening runtime scope. On FAIL, record the failure and repair the smallest proven cause before any further feature work.
