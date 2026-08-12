# TF-0022 — Pull request change-control rehearsal

**Date:** 2026-08-12  
**Status:** PILOT / EXECUTION PENDING  
**Decision:** EXPERIMENT

## Trigger

`TF-0021` established tracked-file secret hygiene. Repository ruleset enforcement remains externally unverified, so the next smallest useful step is to prove the pull-request path itself before claiming enforcement.

## Structural delta

```text
security/CHANGE_CONTROL_BASELINE_0_1.md
Tree_F/TF-0022_2026-08-12_PULL_REQUEST_CHANGE_CONTROL_REHEARSAL.md
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
- GitHub Secret Scanning or Push Protection are enabled.

## Numbering correction retained in Git

The first branch-only draft used `TF-0021` before the latest `main` history was inspected. `main` already contained `TF-0021` for the secret-hygiene gate, so the draft was removed and this experiment was correctly assigned `TF-0022`. The transient branch commits remain in Git history; accepted Tree_F numbering stays contiguous and unique.

## Algorithms / libraries

No new runtime algorithm or dependency. This is repository change-control evidence using existing GitHub branch, pull request and Actions mechanisms.

## Security conclusion

`NOT_TESTED` until the PR-triggered workflow completes.

The experiment intentionally distinguishes voluntary process from platform enforcement. A PASS here cannot be promoted to `main branch protection PASS`.

## Next gate

1. Verify the pull-request-triggered `PX00 Contract Validation` run.
2. Preserve assurance evidence on the branch.
3. Merge after successful validation.
4. Recheck repository rulesets separately; only actual enforcement can close the main-branch gate.