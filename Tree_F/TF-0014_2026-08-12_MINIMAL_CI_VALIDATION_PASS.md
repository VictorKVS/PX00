# TF-0014 — Minimal CI Validation PASS

**Date:** 2026-08-12  
**Status:** ACCEPTED  
**Decision:** KEEP

## Trigger

The first automated PX00 contract-validation workflow completed successfully, followed by a second successful run on the next material commit.

## Structural effect

New assurance evidence:

```text
assurance/
├── runs/
│   └── CI-0001_GITHUB_ACTIONS_PASS_2026-08-12.md
└── records/
    └── ACCEPTANCE-CI-0001.yaml
```

No production runtime, role authority or external-action scope was widened.

## File dossier

### `assurance/runs/CI-0001_GITHUB_ACTIONS_PASS_2026-08-12.md`

**Why:** preserve actual hosted execution evidence rather than treating committed workflow YAML as proof.  
**Input:** repository commit `51312d4...`, pinned workflow dependencies and validator dependency.  
**Processing:** hosted checkout → Python → dependency check → tests → validator.  
**Output:** reproducibility evidence from GitHub Actions.  
**Libraries/actions:** PyYAML plus two GitHub actions pinned to full SHAs.  
**DevOps:** proves the local quality gate is reproducible on a disposable CI runner.  
**Security:** confirms no write token, secrets, deployment or customer data are required.

### `assurance/records/ACCEPTANCE-CI-0001.yaml`

**Why:** machine-readable CI acceptance.  
**Input:** successful workflow run and step conclusions.  
**Processing:** compare to ADR-0016 acceptance conditions.  
**Output:** `PASS` for CI contract-validation scope.  
**Libraries:** none; declarative YAML.  
**Security:** keeps production/runtime/release claims explicitly outside scope.

## Production-chain result

```text
contract design
    ↓
local validator
    ↓
shared-host PASS
    ↓
isolated .venv PASS
    ↓
minimal CI workflow
    ↓
GitHub Actions PASS
    ↓
second CI PASS
    ↓
automated contract gate accepted
```

## Algorithms and dependencies

No algorithm changed. The same deterministic validator and same 13-test suite are executed in CI.

Current direct runtime dependency remains:

```text
PyYAML==6.0.3
```

CI supply-chain dependencies:

```text
actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803
actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1
```

## DevOps conclusion

The first automated gate is justified and functioning. The project now has a minimum useful continuous validation loop without introducing deployment or orchestration complexity.

## Security conclusion

`PASS_WITH_ACTIONS`

Proven: minimal permissions, pinned action identities, dependency consistency, passing tests and passing contract validator on a hosted disposable runner.

Still not proven: repository secret-scanning/branch-protection configuration, releasable-build SBOM/signing, production authorization, tenant isolation, event tamper resistance, LLM/RAG/provider security.

## Evaluation

- Correctness: 5/5
- Traceability: 5/5
- Security: 4/5
- Maintainability: 5/5
- Reproducibility: 5/5 for current contract-validator gate
- Complexity / Cost: 1/5 added complexity

## Next gate

Do not add more CI features yet. Verify repository security controls next, then decide the smallest SBOM/dependency provenance control required before any releasable distribution.
