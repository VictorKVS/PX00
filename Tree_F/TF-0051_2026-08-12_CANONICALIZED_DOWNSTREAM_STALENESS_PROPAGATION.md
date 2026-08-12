# TF-0051 — Canonicalized Downstream Staleness Propagation

Date: 2026-08-12
Status: implemented
ADR: ADR-0036
Historical note: this capability was originally recorded under a duplicate TF-0041 identifier. The implementation/content is preserved; this generation canonicalizes its Tree_F identity without erasing history.

## Generation
A directed downstream dependency graph and immutable impact records allow claim-assessment changes to mark dependent knowledge, decisions, and plans for review without deleting or autonomously reversing them.

## Surfaces
- `schemas/DOWNSTREAM_IMPACT.yaml`
- `px00/downstream.py`
- `tests/test_downstream.py`
- `architecture/adr/ADR-0036-downstream-staleness-propagation.md`

## Status propagation
`CLMA changed -> KN STALE -> DEC REASSESSMENT_REQUIRED -> PLAN REVIEW_REQUIRED`

## Boundary
Propagation is informative/governance state, not authority to revoke or cancel.

## Identity repair
The former duplicate Tree_F file is removed only after this canonical record exists. Git history preserves the original commit; this new stable ID is the canonical forward reference.

## Next
Create governed reassessment queues/work items and bind them to role/protocol execution so stale objects become actionable tasks rather than passive flags.
