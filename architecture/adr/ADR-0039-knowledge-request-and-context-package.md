# ADR-0039 — Knowledge Request and Context Package

Date: 2026-08-12
Status: accepted

## Context
PX00 roles bind to stable logical knowledge spaces while physical KB locations may migrate. Agents must not receive unrestricted repository contents or treat a knowledge binding as runtime authority.

## Decision
Introduce KnowledgeRequest and immutable ContextPackage.

A KnowledgeRequest is scoped to TASK, RUN, ROLE, PROTOCOL and one or more KnowledgeBindings. It declares query intent, allowed object types, classification ceiling and maximum object count.

A ContextPackage contains only the selected stable logical knowledge object IDs plus the exact route snapshot references used to resolve them for that RUN. Its SHA-256 covers the material selection metadata.

## Invariants
- assignment_receives_context_not_whole_repository
- physical_repository_path_is_not_knowledge_identity
- context_selection_must_be_subset_of_declared_role_bindings
- context_package_does_not_grant_action_authority
- historical_context_preserves_route_snapshot_used_at_selection_time
- KB relocation does not rewrite logical object IDs or historical lineage

## Consequences
FATHER can later move `KB-SECURITY` from `KNOWLEDGE_CORE/security-core` to a dedicated `SECURITY_KB` repository while preserving stable `SRC-*`, `EVD-*`, `CLM-*` identities and the exact context previously delivered to an agent.
