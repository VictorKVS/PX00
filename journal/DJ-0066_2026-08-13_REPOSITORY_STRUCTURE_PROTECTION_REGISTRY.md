# DJ-0066 — Repository Structure Protection Registry

Date: 2026-08-13
Generation: `TF-0078`
Status: COMPLETE

## Decision
Future GitHub/repository restructuring must distinguish active content evolution from structural relocation. Canonical FATHER/PX00 and KNOWLEDGE_CORE surfaces are now inventoried as `DO_NOT_MOVE`, `MIGRATION_ONLY` or reorganizable candidate material.

## Implemented
PX00:
- `governance/REPOSITORY_STRUCTURE_PROTECTION.yaml`;
- `governance/CROSS_REPOSITORY_PROTECTED_SECTIONS.md`;
- `governance/repository-migrations/MIGRATION_RULES.md`;
- `px00.repository_structure_guard` integrated into Contract Validation.

KNOWLEDGE_CORE:
- root `REPOSITORY_STRUCTURE_PROTECTION.yaml`;
- `father/repository-migrations/MIGRATION_RULES.md`;
- repository protection validator integrated into Knowledge Quality Gate;
- every activated non-Security professional domain must have its canonical `professional-knowledge/<domain>` root explicitly registered `DO_NOT_MOVE`.

## Core invariant
`PROTECTED STRUCTURE != FROZEN CONTENT`.

Protected knowledge/runtime sections continue to evolve normally. Generic cleanup may not silently rename, relocate, merge or delete them.

## Ownership preserved
- PX00 owns organization/runtime/authority/execution/trace/replay/Factory Builder.
- KNOWLEDGE_CORE owns canonical professional/domain/product knowledge.
- Security remains canonical at `KNOWLEDGE_CORE/security-knowledge/`.

## Failed evidence
The first strengthened KNOWLEDGE_CORE Quality Gate failed on invalid YAML in the newly added protection registry. The YAML structure was repaired; the gate was not weakened. The following run passed.

## Migration rule
Any approved protected-path relocation requires a migration record with `old → new` mapping, inbound-reference inventory, history/provenance impact, compatibility/rollback plan, reviewer and CI evidence. Historical ADR/Tree_F/journal/snapshot/audit records remain historical and are not rewritten to match the new layout.

## Maturity impact
No FATHER/FFB maturity promotion. This is a repository-governance safety rail for future restructuring.
