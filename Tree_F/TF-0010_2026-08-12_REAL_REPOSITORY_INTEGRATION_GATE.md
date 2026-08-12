# TF-0010 — Real Repository Integration Gate

**Date:** 2026-08-12  
**Status:** DEFINED / EXECUTION PENDING  
**Decision:** KEEP  
**Parent:** TF-0009

## Trigger

TF-0009 introduced the validator and synthetic negative tests. The next required evidence is not another synthetic unit case but proof that the complete current repository satisfies the same contracts.

## Structural delta

```text
tests/test_validator.py
└── RepositoryIntegrationTests.test_current_repository_contracts  NEW
```

No prior TF record was modified or removed.

## Why

A validator can pass isolated unit tests while failing on the real repository because of missing references, inconsistent IDs, malformed YAML, role/protocol mismatch or a broken `Tree_F` sequence. The integration test binds the validator to the actual clone without adding a separate framework.

## Processing

```text
repository root
→ validate_repository(root)
→ root/manifest checks
→ Role Package checks
→ protocol checks
→ acceptance fixture checks
→ cross-reference checks
→ Tree_F sequence check
→ PASS only when issue list is empty
```

## Libraries

No new dependency. Uses existing `PyYAML==6.0.3` plus Python standard-library `unittest` and `pathlib`.

## DevOps

The same command now contains both unit and repository integration coverage:

```powershell
python -m unittest discover -s tests -v
```

CI remains deferred until this command passes in the owner's real clone.

## Security conclusion

`PASS_WITH_ACTIONS`.

The integration test strengthens detection of configuration/contract drift but does not turn the validator into a production security boundary. The authoritative result is still pending local execution in `G:\1\PX00`.

## Acceptance

Expected local evidence:

- all unit tests PASS;
- repository integration test PASS;
- `python -m px00 .` returns PASS and exit code 0;
- JSON output contains zero errors.

Any failure blocks CI introduction and broader runtime scope until analyzed.

## Next gate

Execute the commands in the real local clone and preserve the resulting evidence as a new run/acceptance record. Do not rewrite TF-0009 or TF-0010 to hide a failure; record the result separately.
