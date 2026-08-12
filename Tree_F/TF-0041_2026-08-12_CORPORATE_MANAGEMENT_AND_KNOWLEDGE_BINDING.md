# TF-0041 — Corporate Management and Knowledge Binding

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0036

## Generation
PX00/FATHER now has an explicit corporate management layer above governed execution. Departments, mandates, role placement and cross-department protocols are modeled separately from external knowledge domains.

## Surfaces
- `schemas/ORGANIZATION.yaml`
- `schemas/DEPARTMENT.yaml`
- `schemas/KNOWLEDGE_BINDING.yaml`
- `px00/organization.py`
- `tests/test_organization.py`
- `architecture/adr/ADR-0036-corporate-management-and-knowledge-binding.md`

## Boundary
PX00 manages the digital organization. `VictorKVS/KNOWLEDGE_CORE` remains the external corporate knowledge plane and is referenced, not duplicated.

## Next
Define ROLE RESPONSIBILITY and HANDOFF PACKAGE contracts, then connect agent identity/model assignment to organizational roles.
