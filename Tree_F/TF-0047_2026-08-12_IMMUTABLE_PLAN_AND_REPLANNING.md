# TF-0047 — Immutable Plan and Governed Replanning

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0042

## Generation
Added PLAN revisions and explicit REPLAN_TRIGGER lineage above the GOAL/PROJECT/TASK graph.

## Flow
GOAL -> PROJECT -> PLAN-v1 -> TASK GRAPH -> observation/challenge/change -> REPLAN_TRIGGER -> PLAN-v2 -> revised task graph.

## Surfaces
- `schemas/PLAN.yaml`
- `schemas/REPLAN_TRIGGER.yaml`
- `px00/planning.py`
- `tests/test_planning.py`
- `architecture/adr/ADR-0042-immutable-plan-and-replanning-lineage.md`

## Next
Add FATHER management-cycle state machine: observe project/task state, choose dispatch/wait/replan/escalate/close actions, and emit auditable management decisions without executing specialist work itself.
