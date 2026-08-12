# TF-0042 — Governed Staffing and Handoff

Date: 2026-08-12
Status: implemented; final CI pending
ADR: ADR-0037

## Generation
PX00/FATHER now models stable role duties, replaceable agent/model assignments and protocol-governed inter-role handoffs.

## Surfaces
- `schemas/ROLE_RESPONSIBILITY.yaml`
- `schemas/HANDOFF_PACKAGE.yaml`
- `schemas/AGENT_ASSIGNMENT.yaml`
- `px00/staffing.py`
- `tests/test_staffing.py`
- `architecture/adr/ADR-0037-role-responsibility-handoff-agent-assignment.md`

## Critical distinctions
- ROLE != AGENT != MODEL
- KNOWLEDGE_BINDING != AUTHORITY
- HANDOFF != AUTHORITY_TRANSFER

## Next
Bind exact AGENT_ASSIGNMENT to RUN and add responsibility-based task assignment/routing.
