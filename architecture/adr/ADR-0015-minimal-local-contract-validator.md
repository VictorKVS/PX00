# ADR-0015 — Minimal Local Contract Validator

**Status:** ACCEPTED FOR EXECUTABLE VALIDATION GATE  
**Date:** 2026-08-12

## Context

Baseline 0.1 contracts, pilot roles and dry-run acceptance are now explicit enough to justify the first executable code. The runtime opening remains deliberately narrow: local, read-only contract validation with synthetic/public-safe tests and no production agents or external side effects.

A hand-written YAML parser would create unnecessary complexity and parsing risk. A broad validation framework would also be premature.

## Decision

PX00 introduces one minimal Python validation package:

```text
px00/
├── __init__.py
├── __main__.py
└── validator.py
```

It validates the current material invariants of:

- root PX00 identity/runtime gate;
- governed Role Packages;
- pilot protocols;
- acceptance fixture gates;
- canonical role/protocol references;
- `Tree_F` contiguous append-only numbering;
- conservative obvious-secret fields in public YAML.

The validator is local and read-only. It performs no network requests, external writes, model calls, knowledge admission or production actions.

## Dependency choice

One direct dependency is accepted: `PyYAML==6.0.3`.

Reason: PX00 already uses YAML as its machine-readable contract representation. Reimplementing YAML parsing is higher complexity and risk than using a mature dedicated parser. The implementation uses `yaml.safe_load` and does not enable arbitrary Python object construction.

Tests use Python standard-library `unittest`; no additional test framework is introduced at this gate.

## Execution

```powershell
python -m pip install -r requirements-validator.txt
python -m unittest discover -s tests -v
python -m px00 .
python -m px00 . --json
```

Exit code `0` means the currently encoded blocking invariants passed; non-zero means validation failed.

## What PASS does not mean

Validator PASS is not production approval, certification, legal conformity or proof that future authorization/runtime controls are non-bypassable. It only proves the repository state satisfies the executable checks currently defined for this gate.

## DevSecOps

The dependency is explicitly pinned and documented. New dependencies require a material-change review. CI is deferred until the local commands are proven stable against the real repository. Full SBOM becomes mandatory before a releasable distribution.

## Security conclusion

`PASS_WITH_ACTIONS`.

The validator reduces configuration drift, privilege drift, unsafe-loop regression, false acceptance, obvious public-YAML secret insertion and Tree_F sequence damage. Remaining work includes real local repository evidence, CI, repository security-setting verification, dependency/SBOM automation and later runtime-enforcement tests.

## Consequences

Positive:

- first executable architecture proof exists;
- negative cases become regression tests;
- machine checks remain aligned with governed contracts;
- implementation remains small and local.

Cost:

- one third-party YAML dependency;
- every new executable invariant must be maintained with its contract and tests.

## Disposition

`KEEP / RUN AGAINST REAL LOCAL REPOSITORY BEFORE WIDENING RUNTIME SCOPE`.
