# TF-0009 — Minimal Contract Validator

**Date:** 2026-08-12  
**Status:** ACCEPTED FOR LOCAL EXECUTABLE VALIDATION  
**Decision:** KEEP / VERIFY LOCALLY  
**Parent:** TF-0008

## Trigger

Baseline 0.1 contracts and the Analyst/Socrates pilot dry run reached the previously declared gate for a minimal executable validator. Runtime scope remains local, read-only and non-production.

## Structural delta

```text
PX00/
├── requirements-validator.txt                  NEW
├── px00/                                       NEW
│   ├── __init__.py                             NEW
│   ├── __main__.py                             NEW
│   └── validator.py                            NEW
├── tests/                                      NEW
│   └── test_validator.py                       NEW
├── security/                                   NEW
│   └── DEVSECOPS_BASELINE_0_1.md               NEW
├── architecture/adr/
│   └── ADR-0015-minimal-local-contract-validator.md  NEW
└── Tree_F/
    └── TF-0009_2026-08-12_MINIMAL_CONTRACT_VALIDATOR.md NEW
```

Existing TF-0001..TF-0008 remain unchanged and addressable.

## Production-chain position

```text
Contracts
→ Pilot Role Packages
→ Pilot Protocols
→ Dry-run Acceptance
→ ADR-0014 minimal runtime opening
→ TF-0009 executable validator
→ local repository test evidence
→ decide CI / next runtime scope
```

## File dossiers

### `requirements-validator.txt`

**Purpose:** declare the one direct runtime dependency needed to safely parse existing YAML contracts.  
**Trigger:** first machine validation of YAML.  
**Input / Output:** package requirement only.  
**Processing:** NONE.  
**Dependency:** `PyYAML==6.0.3`.  
**DevOps:** deterministic direct dependency for local install.  
**Security:** dependency drift is reduced by exact pin; full transitive/SBOM evidence remains a later release gate.  
**Verification:** clean environment can install it and execute validator/tests.  
**Decision:** KEEP.

### `px00/__init__.py`

**Purpose:** establish the minimum `px00` Python package namespace already declared by PX00 identity policy.  
**Processing:** NONE.  
**Dependencies:** Python standard library only.  
**Security:** no attack surface beyond package import.  
**Verification:** `import px00`.  
**Decision:** KEEP.

### `px00/__main__.py`

**Purpose:** allow `python -m px00` without a packaging/build framework.  
**Processing:** delegates to `validator.main`.  
**Dependencies:** package-local only.  
**Security:** no network/write behavior.  
**Verification:** CLI returns deterministic exit code.  
**Decision:** KEEP.

### `px00/validator.py`

**Purpose:** executable enforcement of the first small set of Baseline 0.1 invariants.  
**Inputs:** repository paths and YAML contract files.  
**Outputs:** PASS/FAIL report, optional JSON report, process exit code.  
**Processing:** safe YAML parse; canonical ID checks; role authority/trace checks; protocol bound/step checks; acceptance gate checks; cross-reference checks; Tree_F sequence check; conservative high-risk secret-field scan.  
**Algorithms:** deterministic rule evaluation; no ML/LLM; no probabilistic score.  
**Libraries:** Python stdlib + PyYAML.  
**DevOps:** intended first as local gate; CI deferred until local value and command stability are proven.  
**Security:** read-only; no network; `yaml.safe_load`; no production side effects. Main residual risks are incomplete rule coverage, false-positive/false-negative secret heuristics, dependency compromise and future validator bypass if enforcement is not wired into delivery gates.  
**Verification:** unit tests plus full repository invocation.  
**Decision:** KEEP / EXPAND ONLY BY PROVEN CONTRACT REQUIREMENT.

### `tests/test_validator.py`

**Purpose:** negative regression evidence for the validator itself.  
**Inputs:** synthetic in-memory contract objects and temporary Tree_F directories.  
**Outputs:** unittest PASS/FAIL.  
**Processing:** deliberately breaks authority, retrieval-evidence, secret, loop-bound, optional-step, acceptance-evidence and Tree_F invariants and checks that validation rejects them.  
**Libraries:** Python stdlib `unittest`, `tempfile`, `pathlib`.  
**DevOps:** command is stable without pytest dependency.  
**Security:** tests use synthetic/public-safe values only.  
**Verification:** `python -m unittest discover -s tests -v`.  
**Decision:** KEEP.

### `security/DEVSECOPS_BASELINE_0_1.md`

**Purpose:** state executable-gate dependency, parser, testing, threat and deferred-control policy.  
**Processing:** NONE.  
**Libraries:** documents PyYAML and stdlib testing choice.  
**DevOps:** defines when CI/SBOM/dependency automation become justified.  
**Security:** prevents the first code from silently expanding runtime/security scope.  
**Verification:** compare implementation/dependencies to the documented baseline.  
**Decision:** KEEP.

### `architecture/adr/ADR-0015-minimal-local-contract-validator.md`

**Purpose:** make the first code and the PyYAML dependency an explicit architectural decision rather than accidental implementation drift.  
**Processing / Libraries:** NONE runtime; documents selection.  
**Security:** preserves the local/read-only runtime cap.  
**Verification:** repository implementation must remain consistent with ADR until superseded.  
**Decision:** KEEP.

## Test design

Current synthetic tests cover:

- valid A1 role baseline;
- missing A1 external-side-effect prohibition;
- retrieval incorrectly treated as evidence;
- obvious secret-like YAML value;
- valid bounded protocol;
- unbounded-loop policy regression;
- missing positive `max_*` bound;
- optional step without condition;
- acceptance without evidence gate;
- pilot side effects incorrectly enabled;
- contiguous Tree_F sequence;
- Tree_F numbering gap.

These tests verify blocking rules, not business intelligence quality.

## Authoring verification

During implementation, the validator source compiled successfully and 12 isolated `unittest` cases passed in a Python 3.13.5 environment with PyYAML 6.0.3.

This is authoring evidence only. The authoritative next step is execution against the owner's real local clone `G:\1\PX00` after `git pull`.

## DevOps conclusion

No CI added yet. This is intentional. The local command must first prove stable and useful; then one minimal CI gate can be added rather than designing a pipeline around unproven code.

## Information-security conclusion

`PASS_WITH_ACTIONS`.

Positive controls now exist in executable form, but the validator is not a security boundary for production. Before runtime scope expands, prove full-repository PASS, add CI, verify repository-level secret/branch controls, and add dependency/SBOM evidence appropriate to release scope.

## Rollback

If the validator design is rejected, remove the executable validator package and dependency in a new governed change, preserve TF-0009, and record the superseding decision. Do not delete TF-0009 from development history.

## Evaluation

- Correctness: 4/5 — deterministic checks exist; full local repository run pending.
- Traceability: 5/5 — ADR, Tree_F, tests and dependency are linked.
- Security: 4/5 — local/read-only scope and safe loader; production enforcement not claimed.
- Maintainability: 4/5 — one module, one direct dependency, stdlib tests.
- Reproducibility: 4/5 — pinned direct dependency; CI/lock/SBOM not yet added.
- Complexity/Cost: 4/5 — deliberately avoids packaging framework, pytest and CI until justified.

Scores are coarse comparison aids, not statistical measurements.

## Next gate

Run the real local clone:

```powershell
python -m pip install -r requirements-validator.txt
python -m unittest discover -s tests -v
python -m px00 .
python -m px00 . --json
```

Then preserve the result as acceptance evidence and decide whether to add minimal CI.
