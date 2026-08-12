# TF-0022 — Pull request change-control rehearsal

**Date:** 2026-08-12  
**Status:** ACCEPTED WITH ACTIONS  
**Decision:** KEEP

## Trigger

`TF-0021` established tracked-file secret hygiene. Repository ruleset enforcement remains externally unverified, so the next smallest useful step was to prove the pull-request path itself before claiming enforcement.

## Structural delta

```text
security/CHANGE_CONTROL_BASELINE_0_1.md
Tree_F/TF-0022_2026-08-12_PULL_REQUEST_CHANGE_CONTROL_REHEARSAL.md
assurance/runs/PRGATE-0001_PULL_REQUEST_PASS_2026-08-12.md
assurance/records/ACCEPTANCE-PRGATE-0001.yaml
```

## Experiment

A material change was created on dedicated branch `gate/pr-change-control-rehearsal` and proposed through GitHub pull request `#1` to `main`.

Observed GitHub Actions evidence:

```text
run_id      31583857865
workflow    PX00 Contract Validation
event       pull_request
head_sha    014f40ad6af36a1c678e0fb2d9b3ef24405e60e2
base_sha    e73050bc1553d9dbc5a9713c1572e7835a677661
status      completed
conclusion  success
```

## Accepted claims

The rehearsal proves:

- a dedicated branch can carry a governed change;
- a PR to `main` triggers the existing validation workflow;
- the validation result is observable before merge;
- CI evidence can be preserved on the branch before acceptance.

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

`PASS_WITH_ACTIONS` for **PR workflow capability**.

The experiment intentionally distinguishes voluntary process from platform enforcement. A PASS here cannot be promoted to `main branch protection PASS`.

## Next gate

1. Verify the new PR run after the assurance evidence is committed.
2. Merge PR `#1` only after that successful validation.
3. Recheck repository rulesets separately; only actual enforcement can close the main-branch gate.