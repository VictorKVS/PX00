# TF-0046 — Goal / Project / Task Graph

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0041

## Generation
Added the management layer above task routing: governed goals, bounded projects and dependency-aware task nodes.

## Surfaces
- `schemas/GOAL.yaml`
- `schemas/PROJECT.yaml`
- `schemas/TASK_NODE.yaml`
- `px00/work_management.py`
- `tests/test_work_management.py`
- `architecture/adr/ADR-0041-goal-project-task-graph.md`

## Management path
GOAL -> PROJECT -> TASK GRAPH -> READY TASK -> RESPONSIBILITY ROUTING -> ASSIGNMENT -> CONTEXT PACKAGE -> RUN.

## Next
Add PLAN/DECOMPOSITION records so FATHER can explain why it created each task and support governed replanning without rewriting the original plan.
