# DJ-0034 — Task-to-Responsibility Routing and RUN Staffing Pinning

Date: 2026-08-12
Tree_F: TF-0045
ADR: ADR-0040

## Completed
Added responsibility-based task routing, exact active assignment selection, context-package lineage checks and RUN staffing pinning. RUN_RECORD v0.4 now preserves responsibility, assignment, agent, executor/model and context package digest alongside the existing policy and trace lineage.

## Design consequence
FATHER now routes work as an organization: first determine which governed duty/role is accountable, then choose a currently ACTIVE digital employee. The model is an implementation detail of an assignment, not the identity of the role.

## Historical reproducibility
If `ROLE-ANALYST` is reassigned tomorrow from `MODEL-A@1` to `MODEL-B@2`, an old RUN remains pinned to its original assignment/model/context hash. Staffing changes create new assignments; they do not rewrite execution history.

## Next
Build the objective/work graph above routing: GOAL -> PROJECT -> TASK GRAPH -> responsibility routing -> RUN. This is the next step toward the FATHER orchestration loop.
