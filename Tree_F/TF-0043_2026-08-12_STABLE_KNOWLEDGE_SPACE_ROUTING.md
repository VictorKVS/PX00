# TF-0043 — Stable Knowledge Space Routing

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0038

## Generation
Separated stable logical knowledge identity from mutable physical storage location.

## Surfaces
- `schemas/KNOWLEDGE_ROUTE.yaml`
- `schemas/KNOWLEDGE_BINDING.yaml` v0.2
- `px00/knowledge_routing.py`
- `tests/test_knowledge_routing.py`
- `architecture/adr/ADR-0038-stable-knowledge-space-routing.md`

## Proven migration scenario
`KB-SECURITY/security-core`

v1 physical route:
`VictorKVS/KNOWLEDGE_CORE/security-core`

v2 physical route:
`VictorKVS/SECURITY_KB`

The role binding remains `KB-SECURITY/security-core` throughout.

## Invariants
- stable IDs survive physical moves
- graph lineage is not rewritten by storage migration
- endpoint paths are not identities
- suspended/retired endpoints fail closed for new resolution
- knowledge bindings do not confer tool authority

## Next
Add a Knowledge Request / Context Package protocol so an assigned role can request a bounded subset of one or more knowledge spaces through routing/index resolution.
