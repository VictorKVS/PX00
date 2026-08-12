# PX00 Change Control Baseline 0.1

**Status:** PILOT / NOT ENFORCED  
**Scope:** changes targeting the default branch `main`

## Purpose

Define the smallest useful change-control path before repository ruleset enforcement is enabled.

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
4. The diff and CI result remain attributable to the pull request and commit identities.
5. Failed CI attempts remain visible; they are not rewritten as successful evidence.
6. Direct push capability is **not** treated as acceptable enforcement merely because maintainers follow this process voluntarily.

## Current enforcement state

This document defines a workflow convention and testable acceptance path. It does **not** claim repository-level enforcement.

Until GitHub branch protection or a repository ruleset is verified:

```text
PR workflow capability     TESTABLE
PR workflow enforcement    UNVERIFIED / NOT ESTABLISHED
required CI on merge       UNVERIFIED
force-push protection      UNVERIFIED
branch deletion protection UNVERIFIED
```

## Security rationale

The rehearsal proves that PX00's existing CI can act as a pre-merge signal on a pull request before that signal is made mandatory. This separates two claims that must not be confused:

- **capability:** a PR triggers and passes the accepted validation workflow;
- **enforcement:** GitHub prevents bypass of that workflow.

Only the second claim closes the repository change-control gate.

## Occam constraint

Do not introduce multi-reviewer bureaucracy, CODEOWNERS, signed-commit mandates, merge queues or additional CI systems until they solve an observed requirement. For the current single-maintainer phase, the minimum target is one PR path plus one required validation check and blocked destructive bypass.

## Acceptance

This baseline may be marked `PASS_WITH_ACTIONS` after a real pull request:

- is opened from a dedicated branch;
- triggers the existing workflow;
- receives a successful `Validate contracts` job;
- is merged without bypassing a failed check.

Repository enforcement remains a separate gate and cannot inherit PASS from the rehearsal.