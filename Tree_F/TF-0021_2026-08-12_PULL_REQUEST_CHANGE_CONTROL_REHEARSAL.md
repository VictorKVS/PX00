# TF-0021 — Pull request change-control rehearsal

**Date:** 2026-08-12  
**Status:** PILOT / EXECUTION PENDING  
**Decision:** EXPERIMENT

## Trigger

The validator supply chain now has local and hosted evidence through Windows/Linux hash-locked dependency execution. The remaining repository-security weakness is not validator correctness but lack of verified enforcement on `main`.

Because GitHub repository rulesets are still not visible through the current API path, the next smallest useful step is to prove the pull-request path itself before claiming enforcement.

## Structural delta

```text
security/CHANGE_CONTROL_BASELINE_0_1.md
Tree_F/TF-0021_2026-08-12_PULL_REQUEST_CHANGE_CONTROL_REHEARSAL.md
```

## Experiment

Create this material change on a dedicated branch, open a pull request to `main`, observe the existing `PX00 Contract Validation` workflow on the pull-request event, preserve the result, then merge only after successful validation.

Expected path:

```text
gate/pr-change-control-rehearsal
→ pull request
→ Validate contracts
→ PASS
→ merge
```

## Claims allowed by a successful rehearsal

A successful run may prove:

- a dedicated branch can carry a governed change;
- a PR to `main` triggers the existing workflow;
- the exact validation job can be observed before merge;
- the merged commit remains attributable to PR/CI evidence.

It does **not** prove:

- GitHub blocks direct pushes to `main`;
- the check is required by ruleset/branch protection;
- force pushes or branch deletion are blocked;
- secret scanning or push protection are enabled.

## Algorithms / libraries

No new runtime algorithm or dependency. This is repository change-control evidence using existing GitHub branch, pull request and Actions mechanisms.

## Security conclusion

`NOT_TESTED` until the PR-triggered workflow completes.

The experiment intentionally distinguishes voluntary process from platform enforcement. A PASS here cannot be promoted to `main branch protection PASS`.

## Next gate

1. Open the pull request.
2. Verify PR-triggered `PX00 Contract Validation` success.
3. Record assurance evidence on the branch.
4. Merge after the successful check.
5. Recheck repository rulesets separately; only actual enforcement can close the main-branch gate.