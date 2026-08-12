# PRGATE-0001 — Pull request validation rehearsal

**Date:** 2026-08-12  
**Repository:** `VictorKVS/PX00`  
**Pull request:** `#1`  
**Branch:** `gate/pr-change-control-rehearsal`  
**Base:** `main`

## Purpose

Prove that a governed change proposed through a dedicated branch and pull request triggers the existing PX00 validation workflow before merge.

## Observed evidence

GitHub Actions run:

```text
run_id      31583857865
workflow    PX00 Contract Validation
event       pull_request
head_sha    014f40ad6af36a1c678e0fb2d9b3ef24405e60e2
base_sha    e73050bc1553d9dbc5a9713c1572e7835a677661
status      completed
conclusion  success
pull_request #1
```

The run was associated by GitHub with PR `#1` and the dedicated branch. This proves PR-triggered validation capability.

## Scope of conclusion

`PASS_WITH_ACTIONS` for **PR workflow capability** only.

This run does not prove platform enforcement. At the time of the rehearsal, repository rulesets were not visible through the available API path, so direct-push prevention, required-check enforcement, force-push blocking and branch-deletion protection remain unverified.

## Acceptance condition

The branch should receive this evidence, rerun the PR workflow successfully, and only then be merged. Repository enforcement must be assessed separately.