# VALIDATOR-0003 — Isolated `.venv` Validation Run

**Date:** 2026-08-12  
**Environment:** owner local clone `G:\1\PX00`, Windows PowerShell, isolated Python `.venv`  
**Result:** PASS

## Why this run exists

The previous real-repository run passed, but installation into the shared host Python environment surfaced an unrelated pre-existing dependency conflict outside PX00. This run isolates PX00 so its dependency and validation result can be evaluated without contamination from unrelated packages.

## Executed chain

```text
fresh .venv
→ install requirements-validator.txt
→ pip check
→ 13 unittest cases
→ repository integration test
→ full PX00 validator
→ JSON validator output
```

## Observed evidence

Dependency installation:

```text
PyYAML==6.0.3 installed successfully
```

Dependency consistency:

```text
No broken requirements found.
```

Unit and integration tests:

```text
Ran 13 tests in 0.093s
OK
```

The test set included `RepositoryIntegrationTests.test_current_repository_contracts` and all declared negative cases.

Full repository validation:

```text
PX00 contract validation: PASS
errors=0 warnings=0
```

JSON result:

```json
{
  "status": "PASS",
  "errors": 0,
  "warnings": 0,
  "issues": []
}
```

## Interpretation

The same validator that passed in the shared host environment also passed in an isolated environment with a consistent dependency graph. The earlier `chromadb`/`bcrypt` conflict is therefore confirmed as external to the PX00 validator dependency graph.

This is evidence of **local environment reproducibility for the current validator gate**. It is not evidence of production runtime security, customer-data isolation, authorization enforcement or release supply-chain integrity.

## Security conclusion

`PASS_WITH_ACTIONS`

Positive evidence:

- isolated dependency graph is consistent;
- only the pinned direct dependency is required by the validator;
- all 13 tests pass;
- full repository validation has zero errors and warnings;
- no network or external side effects are required by the validator.

Remaining actions:

- reproduce the same gate on a disposable GitHub-hosted runner;
- preserve action dependency identities and minimal workflow permissions;
- verify repository secret-scanning/branch-protection state separately;
- generate SBOM/dependency evidence before any releasable distribution.

## Decision

`KEEP` the minimal validator and open the next gate: **minimal CI validation only**.
