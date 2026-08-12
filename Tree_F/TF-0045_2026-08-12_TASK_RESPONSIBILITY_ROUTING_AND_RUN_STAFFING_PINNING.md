# TF-0045 — Task-to-Responsibility Routing and RUN Staffing Pinning

Date: 2026-08-12
Status: implemented; final CI pending
ADR: ADR-0040

## Generation
FATHER can now route a task to a declared responsibility and select an eligible ACTIVE assignment without naming a model directly. The resulting RUN pins the exact responsibility, role, assignment, agent, executor/model and context package hash.

## Surfaces
- `schemas/TASK_ROUTING_DECISION.yaml`
- `schemas/RUN_RECORD.yaml` v0.4
- `px00/task_routing.py`
- `tests/test_task_routing.py`
- `architecture/adr/ADR-0040-task-responsibility-routing-and-run-staffing-pinning.md`

## Key invariants
- task routes by responsibility, not agent name
- selected assignment is ACTIVE and role/department aligned
- required role knowledge bindings are present
- context package matches RUN/ROLE/ASSIGNMENT
- model and context hash are pinned before execution
- later staffing changes do not rewrite history
- routing does not grant authority

## Next
Introduce GOAL/PROJECT/TASK contracts and a Task Graph so FATHER can decompose a user objective into governed responsibilities and dependencies before routing individual RUNs.
