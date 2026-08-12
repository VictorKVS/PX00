# ADR-0037 — Role Responsibility, Handoff and Agent Assignment

Date: 2026-08-12
Status: accepted

## Context
PX00/FATHER now has Organization, Department and Knowledge Binding. To operate as a digital enterprise, it must distinguish the permanent organizational role from the replaceable executor/model and formalize the transfer of work between roles.

## Decision
Introduce three governed contracts:

1. ROLE_RESPONSIBILITY — what a role is accountable for, required outputs, allowed protocols, knowledge bindings and escalation conditions.
2. HANDOFF_PACKAGE — bounded transfer of work product, evidence, assumptions, unresolved questions and blocking findings between roles.
3. AGENT_ASSIGNMENT — time-bounded binding of a concrete executor/model configuration to a role.

## Core invariants
- role is organizational identity; agent/model is replaceable executor
- assignment cannot expand role knowledge bindings or authority
- role responsibility does not itself grant runtime authority
- handoff does not transfer sender authority to receiver
- handoff protocol must be declared for both participating roles
- blocking findings prevent READY handoff
- replacing a model does not rewrite role or execution history
- RUN will eventually pin exact assignment/model version

## Knowledge architecture
Domain knowledge remains external to PX00 in KNOWLEDGE_CORE. PX00 stores only governed knowledge bindings and uses authority/tool boundaries for actual access.

## Consequences
FATHER can begin treating agents as staff positions in a corporate management system: duties are stable, executors are replaceable, work products have formal transfer boundaries, and organizational history remains reproducible.
