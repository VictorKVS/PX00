# PX00 DevSecOps Baseline 0.1 — Minimal Validator

**Status:** ACTIVE FOR EXECUTABLE VALIDATION GATE  
**Scope:** local contract validator only; no production runtime.

## Why this exists

PX00 now contains executable Python. The security boundary must therefore move from documentation-only controls to a minimal, testable software supply-chain baseline without introducing a large tool stack before value is proven.

## Runtime and dependencies

- Python: local interpreter; production runtime is not approved.
- Direct third-party runtime dependency: `PyYAML==6.0.3`.
- Purpose: parse PX00 YAML contracts and fixtures.
- Parser policy: use `yaml.safe_load` only for repository-controlled or reviewed YAML; do not use unsafe object construction loaders.
- Unit-test framework: Python standard-library `unittest`; no test framework dependency is added yet.
- Network access: validator requires none.
- External side effects: prohibited.

## Execution-environment isolation

The first owner-executed real repository run passed all 13 tests and the full validator, but installation into the shared host Python environment surfaced an unrelated pre-existing package conflict (`chromadb` vs `bcrypt`).

Therefore the validation baseline now requires an isolated environment for reproducible local runs:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-validator.txt
python -m unittest discover -s tests -v
python -m px00 .
```

The repository already ignores `.venv/`.

Rules:

- do not repair unrelated global Python packages as part of PX00 validation;
- do not treat a global-environment package conflict as a PX00 defect unless the conflicting package is in PX00's dependency graph;
- future dependency evidence should be collected from the isolated PX00 environment or a disposable CI environment;
- containers remain deferred until requirements justify them; stdlib `venv` is sufficient for the current gate.

## Minimal controls now enforced in code

1. Canonical `PX-00` identity remains immutable.
2. Production runtime gate must remain false.
3. Role IDs and protocol IDs follow canonical formats.
4. A0/A1 pilot roles must explicitly prohibit external side effects.
5. Retrieval cannot be declared evidence by itself.
6. Required role package references must resolve to files.
7. Pilot protocols must prohibit unbounded loops and expose a positive `max_*` bound.
8. Required protocol steps cannot omit core success/failure/event fields.
9. Optional protocol steps require an explicit condition.
10. Acceptance PASS requires blocking criteria plus evidence rule.
11. Pilot fixture runtime side effects remain prohibited.
12. `Tree_F` numbering must remain contiguous from `TF-0001`.
13. Conservative YAML key scanning rejects obvious embedded secret values in selected high-risk fields.

## Threat view

Primary threats at this phase:

- unsafe YAML deserialization;
- contract bypass by malformed or missing fields;
- privilege drift in role definitions;
- removal of loop bounds;
- acceptance without evidence;
- accidental secret insertion into public governance YAML;
- silent deletion/gap in accumulated `Tree_F` development history;
- dependency compromise or unexpected dependency drift;
- non-reproducible results caused by unrelated state in a shared Python environment.

## Controls deliberately deferred

Not added yet because the validator has no network or production side effects:

- web/API service;
- database;
- broker/queue;
- container runtime;
- Kubernetes;
- vector database/RAG runtime;
- live LLM provider integration;
- production PKI/WORM storage;
- broad SAST/DAST platform.

These require a separate requirement and acceptance case before introduction.

## Dependency and supply-chain policy

- Direct dependencies are explicitly listed and pinned for this gate.
- New dependency requires purpose, owner, license/source review, security impact and Tree_F/journal evidence.
- Dependency removal is preferred over addition when standard-library functionality is sufficient.
- A full SBOM becomes mandatory before any releasable distribution; the current validator gate records direct dependency provenance only.
- Local acceptance evidence should come from an isolated `.venv` or equivalent disposable environment.
- CI is intentionally deferred until local repository validation produces value and stable commands. When CI is added, action dependencies and permissions must be minimized and reviewed.

## Test commands

Preferred isolated local sequence:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-validator.txt
python -m unittest discover -s tests -v
python -m px00 .
python -m px00 . --json
```

The validator returns exit code `0` on PASS and non-zero on FAIL.

## Security acceptance status

`PASS_WITH_ACTIONS`

Current design is appropriate for a local, read-only contract validator. It is **not** evidence that production authorization, tenant isolation, tamper resistance, secret scanning, dependency integrity or runtime enforcement are solved.

The first real local repository run is preserved in `assurance/runs/VALIDATOR-0002_REAL_LOCAL_RUN_2026-08-12.md`; validator acceptance is recorded in `assurance/records/ACCEPTANCE-VALIDATOR-0001.yaml`.

## Required next evidence

Before widening runtime scope:

- reproduce validator PASS in an isolated local `.venv`;
- prove negative tests fail for intended contract violations;
- add minimal CI only after the isolated commands remain stable;
- add dependency/SBOM automation before a releasable build;
- verify repository secret scanning / branch protection state separately;
- threat-model any network, model-provider, database or customer-data integration before implementation.
