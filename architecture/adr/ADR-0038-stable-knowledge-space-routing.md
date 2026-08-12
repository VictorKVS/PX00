# ADR-0038 — Stable Knowledge Space Routing

Date: 2026-08-12
Status: accepted

## Context
Knowledge domains currently live in VictorKVS/KNOWLEDGE_CORE, but future scale may require splitting physical storage into PROGRAMMING_KB, SECURITY_KB, ARCHITECTURE_KB, DEVSECOPS_KB, PRODUCT_KB, RESEARCH_KB, OSINT_KB and AI_AGENTS_KB. Physical moves must not invalidate role bindings, claim/evidence lineage, graph edges or historical references.

## Decision
PX00 binds roles and protocols to stable logical `knowledge_space_id` values plus logical domains. Physical repositories, paths, databases or APIs are resolved through versioned KNOWLEDGE_ROUTE records.

A physical migration changes only the route. It MUST NOT change stable knowledge identities or rewrite historical graph lineage.

## Core invariant
`logical identity != physical locator`

Examples:
- `KB-SECURITY/security-core` may initially resolve to `VictorKVS/KNOWLEDGE_CORE/security-core`.
- Later the same logical identity may resolve to `VictorKVS/SECURITY_KB`.
- Existing role bindings and evidence/claim references remain unchanged.

## Consequences
- Knowledge storage can be split or migrated without changing FATHER role definitions.
- Routing/index infrastructure becomes the integration boundary between PX00 and distributed KB repositories.
- Route versions are immutable historical records.
- Suspended/retired routes are not selected for new requests.
- KnowledgeBinding does not grant runtime tool authority; tool access remains governed by ActionRequest/Authority/Grant.
