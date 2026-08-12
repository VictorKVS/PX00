# ADR-0016 — Minimal CI Contract Validation Gate

**Status:** ACCEPTED  
**Date:** 2026-08-12

## Context

PX00's minimal validator has now passed in the owner's real repository and again in a fresh isolated `.venv`. The validation command chain is therefore stable enough to justify automation. Adding a broader CI/CD platform before this evidence would have violated the project's minimum-sufficient-architecture rule.

## Decision

Add one GitHub Actions workflow that runs only the existing validation chain on `push` and `pull_request` for `main`.

The workflow shall:

- use a GitHub-hosted `ubuntu-24.04` runner;
- use explicit Python `3.10`;
- grant only `contents: read` permission;
- pin GitHub Actions dependencies to full commit SHAs;
- disable persisted checkout credentials;
- install only `requirements-validator.txt`;
- execute `pip check`;
- execute the 13 unit/integration tests;
- execute the full repository validator;
- perform no deployment, release, network mutation, model call or customer-data processing.

Pinned action identities at acceptance time:

```text
actions/checkout
SHA d23441a48e516b6c34aea4fa41551a30e30af803
major line v6

actions/setup-python
SHA ece7cb06caefa5fff74198d8649806c4678c61a1
major line v6
```

These SHA values are canonical workflow dependencies. A future action update is a material supply-chain change and requires review/evidence rather than silent tag drift.

## Why not more

Not added:

- Docker;
- matrix across many OS/Python versions;
- coverage service;
- third-party test framework;
- artifact publication;
- deployment;
- workflow orchestration;
- dependency bot as a substitute for review;
- broad SAST/DAST.

None is needed to answer the current gate question: **does the checked-in PX00 contract baseline still validate in a clean disposable environment?**

## Security analysis

Controls:

- minimal token permission: `contents: read`;
- pinned action commits reduce tag-supply-chain drift;
- checkout credentials are not persisted;
- no repository write permission;
- no secrets are required;
- no untrusted production/customer data is consumed;
- job timeout bounds resource consumption;
- dependency set remains pinned and minimal.

Residual risks:

- GitHub-hosted runner and GitHub Actions service remain external trust dependencies;
- `ubuntu-24.04` image content evolves over time;
- Python `3.10` resolves within its patch line rather than pinning one exact patch;
- PyPI remains a dependency source during installation;
- repository secret scanning/branch protection are separate controls and are not proven by this workflow.

## Consequences

Positive:

- every push/PR to `main` gets the same deterministic contract gate;
- repository drift becomes visible before future acceptance;
- CI evidence can be compared with local evidence.

Negative:

- introduces two external GitHub Action dependencies and hosted-runner/PyPI reliance;
- requires future maintenance when action runtime generations or Python support change.

## Acceptance

The workflow is not considered validated merely because its YAML is committed. The next evidence must come from an actual GitHub Actions run. Until that run passes, CI state is `PENDING_EXECUTION`.

## Decision outcome

`KEEP / VERIFY IN GITHUB ACTIONS`.
