# PX00 DevSecOps Baseline 0.1 — Minimal Validator

**Status:** ACTIVE / VALIDATOR GATE PASSED  
**Scope:** contract validation only; no production runtime.

## Why this exists

PX00 contains executable Python, so documentation-only controls are insufficient. The baseline adds only the smallest testable software-supply-chain controls justified by the current validator.

## Runtime and dependencies

- Direct third-party runtime dependency: `PyYAML==6.0.3`.
- Purpose: parse PX00 YAML contracts and fixtures.
- Parser policy: `yaml.safe_load` only; unsafe object-construction loaders are prohibited.
- Tests: Python standard-library `unittest`.
- Validator network access: none required.
- Validator external side effects: prohibited.
- Production runtime: not approved.

## Proven execution environments

The validator now passes in three relevant contexts:

```text
shared local host        PASS
isolated local .venv     PASS
GitHub-hosted CI         PASS
```

Owner-observed isolated result:

```text
pip check: No broken requirements found.
13/13 tests: PASS
repository validation: PASS
errors=0 warnings=0
```

CI result:

```text
workflow: PX00 Contract Validation
runner: ubuntu-24.04
Python: 3.10
accepted run: 31567474530
conclusion: success
```

Evidence:

- `assurance/runs/VALIDATOR-0003_ISOLATED_VENV_RUN_2026-08-12.md`
- `assurance/records/ACCEPTANCE-VALIDATOR-ISOLATED-0001.yaml`
- `assurance/runs/CI-0001_GITHUB_ACTIONS_PASS_2026-08-12.md`
- `assurance/records/ACCEPTANCE-CI-0001.yaml`

## Environment isolation

The first owner run in the shared host Python environment exposed an unrelated pre-existing `chromadb`/`bcrypt` conflict. PX00 validation itself passed. The isolated `.venv` then produced `No broken requirements found`, proving the conflict was outside the PX00 validator dependency graph.

Preferred local sequence:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-validator.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m px00 .
.\.venv\Scripts\python.exe -m px00 . --json
```

Rules:

- do not repair unrelated global packages as part of PX00 validation;
- do not call a host dependency conflict a PX00 defect unless it belongs to the PX00 dependency graph;
- use isolated `.venv` or disposable CI for dependency evidence;
- containers remain deferred until a requirement justifies them.

## Controls enforced by validator

1. Canonical `PX-00` identity remains immutable.
2. Production runtime gate remains false.
3. Role/protocol IDs follow canonical formats.
4. A0/A1 pilot roles prohibit external side effects.
5. Retrieval cannot be evidence by itself.
6. Required role-package references resolve to files.
7. Pilot protocols prohibit unbounded loops and expose positive bounds.
8. Required protocol steps include core success/failure/event fields.
9. Optional protocol steps require explicit conditions.
10. Acceptance PASS requires blocking criteria plus evidence rule.
11. Pilot fixture runtime side effects remain prohibited.
12. `Tree_F` numbering remains contiguous from `TF-0001`.
13. Conservative YAML-key scanning rejects obvious embedded secret values in selected high-risk fields.

## Minimal CI gate

Workflow: `.github/workflows/contract-validation.yml`.

Security controls:

```text
permissions: contents: read
checkout credentials persisted: false
job timeout: 5 minutes
secrets required: none
customer data: none
repository mutation: none
```

Pinned GitHub Action identities:

```text
actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803
actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1
```

Changing an action SHA is a material supply-chain change requiring review/evidence.

## Threat view

Current relevant threats:

- unsafe YAML deserialization;
- contract bypass by malformed/missing fields;
- role privilege drift;
- removal of protocol bounds;
- acceptance without evidence;
- accidental secrets in public governance YAML;
- silent gap/deletion in `Tree_F` history;
- dependency compromise/drift;
- shared-environment contamination;
- CI action/tag supply-chain drift;
- CI running successfully but being bypassable because branch/ruleset enforcement is absent or unverified.

## Repository-level security status

See `security/REPOSITORY_SECURITY_STATUS_2026-08-12.md`.

Current evidence:

```text
CI execution                    PASS
Repository rulesets visible     NONE
main branch protection          UNVERIFIED
Secret scanning                 UNVERIFIED
Push protection                 UNVERIFIED
Required CI enforcement         UNVERIFIED
```

Branch-protection and secret-scanning API reads returned `403 Resource not accessible by integration`. A 403 is recorded as `UNVERIFIED`, never interpreted as enabled or disabled.

## Controls deliberately deferred

Not justified yet:

- web/API service;
- database or broker;
- Docker/Kubernetes;
- vector DB/RAG runtime;
- live LLM provider integration;
- production PKI/WORM;
- broad SAST/DAST stack;
- deployment/release workflow.

Each requires its own requirement, threat view and acceptance case before introduction.

## Dependency and supply-chain policy

- Direct dependencies are explicit and pinned.
- A new dependency requires purpose, owner, license/source review, security impact and Tree_F/journal evidence.
- Prefer removal over addition when stdlib is sufficient.
- CI action dependencies are pinned by full commit SHA.
- Full SBOM becomes mandatory before a releasable distribution.
- Release signing/provenance is separate from validator CI and remains unimplemented.

## Security acceptance status

`PASS_WITH_ACTIONS`

The validator itself is accepted as a reproducible local + CI contract gate. This does **not** prove production authorization, tenant isolation, tamper resistance, secret scanning, protected-branch enforcement, release integrity or model/RAG security.

## Required next evidence

Before any releasable distribution or wider runtime scope:

1. verify or establish minimum `main` branch/ruleset enforcement;
2. verify secret scanning and push protection;
3. decide and implement the minimum SBOM/dependency provenance control;
4. preserve CI regression evidence without logging every routine successful run into `Tree_F`;
5. threat-model any future network, provider, database or customer-data integration before code.
