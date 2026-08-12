# CI-0001 — GitHub Actions Contract Validation PASS

**Date:** 2026-08-12  
**Workflow:** `PX00 Contract Validation`  
**Run:** `31567474530`  
**Head commit:** `51312d4d067482067d777ef86fad6987e59b26c5`  
**Trigger:** push to `main`  
**Result:** PASS

## Purpose

Verify that the locally proven PX00 validation chain reproduces on a disposable GitHub-hosted runner with minimal permissions and pinned action identities.

## Workflow chain

```text
GitHub push
→ ubuntu-24.04 hosted runner
→ read-only checkout
→ Python 3.10
→ install requirements-validator.txt
→ pip check
→ 13 unit/integration tests
→ python -m px00 .
→ PASS
```

## Observed job evidence

Job: `Validate contracts`

All material steps completed successfully:

1. Checkout repository — success
2. Set up Python 3.10 — success
3. Show runtime — success
4. Install pinned validator dependency — success
5. Verify dependency consistency — success
6. Run unit and repository integration tests — success
7. Validate PX00 repository contracts — success

Workflow conclusion: `success`.

A prior first workflow run (`31567451236`) on the workflow-introduction commit also concluded `success`. The second successful run on the next material commit demonstrates that the gate is not a one-off authoring artifact.

## Supply-chain configuration

```text
actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803
actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1
PyYAML==6.0.3
```

Workflow token permission: `contents: read` only. Checkout credentials are not persisted. No repository secret, customer data, deployment key or external mutation is required.

## Interpretation

PX00 contract validation has now reproduced in three relevant environments:

```text
shared local host        PASS
isolated local .venv     PASS
GitHub hosted CI         PASS
```

This supports acceptance of the validator as the current automated architecture-contract gate. It does **not** authorize production agents or prove production runtime security.

## Security conclusion

`PASS_WITH_ACTIONS`

Proven at this gate:

- clean hosted execution succeeds;
- workflow has minimal repository permission;
- action dependencies are pinned to commit SHAs;
- current validator dependency graph installs and checks successfully;
- tests and repository validator succeed without secrets or side effects.

Still separate/unproven:

- repository secret-scanning and branch-protection settings;
- trusted publishing / release signing;
- full SBOM and transitive provenance for a releasable build;
- production authorization/tenant isolation/runtime event integrity;
- model-provider, RAG and customer-data threat controls.

## Decision

`KEEP` the CI gate. Do not widen runtime scope merely because CI passes.
