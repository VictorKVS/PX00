# ADR-0036 — Corporate Management Model and Knowledge Binding

Date: 2026-08-12
Status: accepted

## Context
PX00/FATHER is evolving into a governed digital organization. Roles need explicit organizational placement, responsibilities and handoff protocols. Knowledge itself is being developed independently in `VictorKVS/KNOWLEDGE_CORE` and must not be copied into PX00 role definitions.

## Decision
Introduce ORGANIZATION, DEPARTMENT and KNOWLEDGE_BINDING contracts.

PX00 owns organizational structure, roles, responsibilities, protocols, authority and task execution. `KNOWLEDGE_CORE` owns domain knowledge, evidence structures and knowledge lifecycle. A role accesses a knowledge domain through an explicit binding constrained by purpose, protocol, access mode and optional object/classification limits.

Knowledge Binding is not runtime authority. Any material read/write/propose action remains governed by ActionRequest/Authority/Grant/Tool Boundary.

Cross-department handoff must be declared by protocol on both source and target departments.

## Architecture boundary
- PX00/FATHER = management and execution plane.
- KNOWLEDGE_CORE = corporate knowledge plane.
- Agent/model = replaceable executor.
- Role/protocol/knowledge bindings remain platform assets independent of model provider.

## Consequences
Agents can be replaced without losing organizational knowledge or responsibilities. One knowledge domain may serve multiple roles under different protocols, and one role may bind multiple knowledge domains without duplicating content.
