# Repository structure migration rules

Status: ACTIVE
Registry: `governance/REPOSITORY_STRUCTURE_PROTECTION.yaml`

This directory exists only for explicit structural migrations of protected repository surfaces.
Ordinary cleanup, deduplication, naming normalization, documentation reshuffling or repository
reorganization is not sufficient justification to move a protected path.

A migration record must preserve canonical ownership, historical references, replay/provenance links
and cross-repository routes. It must contain the fields declared in the registry, including an
`old_to_new_path_map`, inbound-reference inventory, compatibility/redirect plan, rollback plan,
reviewer and CI evidence.

`DO_NOT_MOVE` surfaces additionally require an explicit owner decision and architecture decision
before replacement or relocation. Historical Tree_F, ADR and journal records are never rewritten to
make a new layout look as if it had always existed.
