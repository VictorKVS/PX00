# TF-0041 — Downstream Staleness Propagation

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0036

## Generation
Added a directed downstream dependency graph and immutable impact records so claim-assessment changes can mark dependent knowledge, decisions, and plans for review without deleting or autonomously reversing them.

## Surfaces
- `schemas/DOWNSTREAM_IMPACT.yaml`
- `px00/downstream.py`
- `tests/test_downstream.py`
- `architecture/adr/ADR-0036-downstream-staleness-propagation.md`

## Status propagation
`CLMA changed -> KN STALE -> DEC REASSESSMENT_REQUIRED -> PLAN REVIEW_REQUIRED`

## Boundary
Propagation is informative/governance state, not authority to revoke or cancel.

## Next
Create governed reassessment queues/work items and bind them to role/protocol execution so stale objects become actionable tasks rather than passive flags.
