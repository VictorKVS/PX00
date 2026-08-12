# DJ-0032 — Stable Knowledge Space Routing

Date: 2026-08-12
Tree_F: TF-0043
ADR: ADR-0038

## Completed
Introduced stable logical knowledge-space identifiers and a versioned route registry that resolves them to physical endpoints. Updated KnowledgeBinding so roles reference `knowledge_space_id + logical_domain` rather than repository/path identities.

## Why
KNOWLEDGE_CORE is currently a convenient monorepository, but future scale may split it into PROGRAMMING_KB, SECURITY_KB, ARCHITECTURE_KB, DEVSECOPS_KB, PRODUCT_KB, RESEARCH_KB, OSINT_KB and AI_AGENTS_KB. FATHER must continue to see one governed knowledge system across such moves.

## Verified scenario
`KB-SECURITY/security-core` is first routed to `VictorKVS/KNOWLEDGE_CORE/security-core`, then migrated to `VictorKVS/SECURITY_KB` without modifying the role binding or stable logical identity.

## Design boundary
Physical storage is replaceable infrastructure. Stable IDs and graph lineage are part of the knowledge contract and are not rewritten by migration.

## Next
Define KnowledgeRequest and ContextPackage so FATHER can retrieve a bounded, purpose-specific set of knowledge objects for an assigned role without exposing whole repositories or relying on agent-local hidden knowledge.
