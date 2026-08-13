# Cross-repository protected sections index

Status: ACTIVE
Purpose: human-readable map for any future GitHub/repository restructuring.

Machine-readable authorities:
- `VictorKVS/PX00/governance/REPOSITORY_STRUCTURE_PROTECTION.yaml`
- `VictorKVS/KNOWLEDGE_CORE/REPOSITORY_STRUCTURE_PROTECTION.yaml`

## Rule

**Protected does not mean frozen content.** These areas continue to be edited and filled normally.
Protection applies to repository structure: generic cleanup must not rename, relocate, merge or delete
canonical paths. Structural migration requires a governed migration record and green CI.

## PX00 — runtime / governance / history

### DO_NOT_MOVE
- `PX00.yaml`
- `governance/FATHER_CONSTITUTION.md`
- `governance/DECISION_MATERIALITY_STANDARD.md`
- `governance/ARCHITECT_FORESIGHT_LOOP.md`
- `governance/REPOSITORY_STRUCTURE_PROTECTION.yaml`
- `Tree_F/`
- `journal/`
- `DEVELOPMENT_JOURNAL.md`
- `architecture/adr/`
- `PROJECT_PROGRESS.md`
- `projects/FATHER_FACTORY_BUILDER/`

### MIGRATION_ONLY
- `px00/`
- `schemas/`
- `tests/`
- `protocols/`
- `knowledge/`
- `father/`
- `assurance/`
- `audit/`
- `.github/workflows/contract-validation.yml`

## KNOWLEDGE_CORE — canonical professional knowledge

### DO_NOT_MOVE
- `REPOSITORY_STRUCTURE_PROTECTION.yaml`
- `security-knowledge/`
- `security-knowledge/corpus/snapshots/`
- `security-knowledge/audits/`
- `father/domain-knowledge/`
- `father/domain-knowledge/domain-registry.yaml`
- `father/domain-knowledge/PROFESSIONAL_EVIDENCE_DOCTRINE.md`
- `father/domain-knowledge/PROFESSIONAL_KB_MATURITY_MODEL.yaml`
- `father/domain-knowledge/PROFESSIONAL_KB_REVIEW_PROTOCOL.yaml`
- `father/domain-knowledge/professional-decision-schema.yaml`
- `father/domain-knowledge/DOMAIN_BOOTSTRAP_TEMPLATE.yaml`
- `father/product-roadmap/`
- `father/product-roadmap/master-product-roadmap.yaml`
- `father/product-roadmap/security-products.yaml`
- `professional-knowledge/`
- every materialized domain under `professional-knowledge/` (prefix protection)

### MIGRATION_ONLY
- `tools/`
- `.github/workflows/`

## Reorganizable candidate material

The following KNOWLEDGE_CORE topical/legacy roots are not automatically canonical professional truth
and may be reorganized after checking inbound references and admission status:
`algorithms/`, `architecture/`, `benchmarks/`, `build-and-packaging/`, `concurrency/`,
`data-structures/`, `application-security/`, `claims/`.

PX00 `legacy/` is likewise reorganizable after checking protected references.

## Ownership boundary that restructuring must preserve

`PX00` owns organizational/runtime authority, execution, trace/replay, governance and Factory Builder.
`KNOWLEDGE_CORE` owns canonical professional/domain/product knowledge. Security truth remains in
`KNOWLEDGE_CORE/security-knowledge/`; PX00 may pin/consume it but must not create a competing corpus.

## Migration procedure

PX00 migration records: `governance/repository-migrations/`.
KNOWLEDGE_CORE migration records: `father/repository-migrations/`.

Every protected-path migration requires at minimum: rationale, affected IDs, `old → new` map,
inbound-reference inventory, provenance/history impact, compatibility plan, rollback plan, reviewer
and CI evidence. Historical ADR/Tree_F/journal/snapshot/audit records are not rewritten to make a new
layout look retroactively canonical.
