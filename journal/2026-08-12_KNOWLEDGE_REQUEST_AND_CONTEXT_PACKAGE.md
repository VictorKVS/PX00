# DJ-0033 — Knowledge Request and Context Package

Date: 2026-08-12
Tree_F: TF-0044
ADR: ADR-0039

## Completed
Introduced bounded KnowledgeRequest and immutable ContextPackage. Added a reference builder that validates role/binding/protocol scope, classification ceilings, object-type allowlists, maximum object count and stable logical knowledge IDs. The resulting package records exact route snapshots and a SHA-256 digest for the context delivered to the assigned agent.

## Architectural effect
A knowledge binding no longer implies that an agent receives a repository. The agent receives a bounded context package selected for one TASK/RUN. Physical KB migration can change route snapshots without changing stable `SRC-*`, `EVD-*`, `CLM-*` identities.

## Negative cases covered
- role/binding mismatch
- protocol not allowed for binding
- requested classification above binding ceiling
- physical URL used as knowledge identity
- object types outside the request/binding scope

## Next
Connect TASK responsibility routing to active agent assignments and pin exact assignment + model + ContextPackage to RUN creation.
