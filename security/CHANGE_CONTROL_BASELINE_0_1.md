# PX00 Change Control Baseline 0.1

**Status:** PASS_WITH_ACTIONS / NOT ENFORCED  
**Scope:** changes targeting the default branch `main`

## Purpose

Define and exercise the smallest useful change-control path before repository ruleset enforcement is enabled.

## Baseline path

```text
change
→ dedicated branch
→ pull request to main
→ PX00 Contract Validation
→ review of diff + CI evidence
→ merge
```

## Required properties

1. Material changes targeting `main` should be proposed through a dedicated branch and pull request.
2. The pull request must trigger `PX00 Contract Validation`.
3. The validation job must complete successfully before the change is accepted.
4. The diff and CI result remain attributable to pull request and commit identities.
5. Failed CI attempts remain visible; they are not rewritten as successful evidence.
6. Direct push capability is **not** treated as acceptable enforcement merely because maintainers follow this process voluntarily.

## Rehearsal evidence

Pull request `#1` from `gate/pr-change-control-rehearsal` triggered GitHub Actions run `31583857865` with event `pull_request`. The run completed successfully for head commit `014f40ad6af36a1c678e0fb2d9b3ef24405e60e2` against base `e73050bc1553d9dbc5a9713c1572e7835a677661`.

This proves the PR workflow is technically usable as a pre-merge validation path.

## Current enforcement state

```text
PR workflow capability     PASS
PR workflow enforcement    UNVERIFIED / NOT ESTABLISHED
required CI on merge       UNVERIFIED
force-push protection      UNVERIFIED
branch deletion protection UNVERIFIED
```

## Security rationale

The rehearsal separates two claims that must not be confused:

- **capability:** a PR triggers and passes the accepted validation workflow;
- **enforcement:** GitHub prevents bypass of that workflow.

Only the second claim closes the repository change-control gate.

## Occam constraint

Do not introduce multi-reviewer bureaucracy, CODEOWNERS, signed-commit mandates, merge queues or additional CI systems until they solve an observed requirement. For the current single-maintainer phase, the minimum target is one PR path plus one required validation check and blocked destructive bypass.

## Acceptance

Current state is `PASS_WITH_ACTIONS` for PR workflow capability. Repository enforcement remains a separate gate and cannot inherit PASS from this rehearsal.