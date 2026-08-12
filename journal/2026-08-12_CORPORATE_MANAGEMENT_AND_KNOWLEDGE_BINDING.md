# DJ-0030 — Corporate Management and Knowledge Binding

Date: 2026-08-12
Tree_F: TF-0041
ADR: ADR-0036

## Completed
Introduced ORGANIZATION, DEPARTMENT and KNOWLEDGE_BINDING contracts plus a reference corporate organization model and tests. Roles can bind multiple external knowledge domains in `VictorKVS/KNOWLEDGE_CORE`, and cross-department handoff requires an explicitly shared protocol.

## Clarification
The previous OSINT-only mission realignment is superseded as a system-boundary decision. OSINT remains an important application/domain capability of PX00/FATHER, but PX00 itself is broader: a governed digital corporate management and execution system whose specialist roles can consume independent corporate knowledge bases.

## Architectural boundary
- PX00/FATHER owns organization, roles, responsibilities, protocols, task/execution governance and acceptance.
- KNOWLEDGE_CORE owns reusable domain knowledge and evidence structures.
- Agents/models are replaceable executors of roles.
- Knowledge bindings provide governed references and do not grant runtime action authority.

## Next
Define explicit ROLE_RESPONSIBILITY and HANDOFF_PACKAGE objects, then model assignment of concrete agent/model instances to roles.
