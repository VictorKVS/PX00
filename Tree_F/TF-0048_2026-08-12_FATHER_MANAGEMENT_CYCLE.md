# TF-0048 — FATHER Management Cycle

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0043

## Generation
Added the first explicit management loop for FATHER over project/task/plan state.

## Actions
DISPATCH / WAIT / REQUEST_REVIEW / REPLAN / ESCALATE / CLOSE_PROJECT.

## Surfaces
- `schemas/FATHER_MANAGEMENT_DECISION.yaml`
- `px00/father_cycle.py`
- `tests/test_father_cycle.py`
- `architecture/adr/ADR-0043-father-management-cycle.md`

## Boundary
FATHER manages; specialist roles execute. Management decisions never bypass Authority/Grant/Tool Boundary.

## Next
Build governed review routing for SOCRATES and specialist reviewers, including review mandate, independence constraints, findings, disposition and return-to-work protocol.
