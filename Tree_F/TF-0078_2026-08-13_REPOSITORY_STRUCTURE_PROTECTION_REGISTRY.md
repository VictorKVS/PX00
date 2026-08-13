# TF-0078 — Repository Structure Protection Registry

Date: 2026-08-13
Status: COMPLETE — CROSS-REPOSITORY STRUCTURE PROTECTION
ADR: none; canonical ownership did not change
Summit: no maturity/summit promotion by this generation

## Trigger
The owner requested an explicit registry of GitHub sections that are actively populated by FATHER/Professional KB work and must not be accidentally moved, renamed, merged or deleted during future repository restructuring.

## Principle
`PROTECTED != FROZEN CONTENT`.

Protected sections remain actively editable. Protection applies to structural identity during generic cleanup/reorganization.

Three classes are explicit:
- `DO_NOT_MOVE` — canonical identity/history surface;
- `MIGRATION_ONLY` — structural relocation only through a governed migration record;
- `CAN_REORGANIZE` — ordinary cleanup rules may apply.

## PX00 implementation
Added:
- `governance/REPOSITORY_STRUCTURE_PROTECTION.yaml`;
- `governance/CROSS_REPOSITORY_PROTECTED_SECTIONS.md`;
- `governance/repository-migrations/MIGRATION_RULES.md`;
- `px00/repository_structure_guard.py`;
- CI step in `PX00 Contract Validation`.

The protected PX00 set includes canonical root contract, constitution/materiality/foresight governance, Tree_F, journals, ADR history, PROJECT_PROGRESS, Factory Builder root, and migration-only runtime/schema/test/protocol/knowledge/father/assurance/audit/CI surfaces.

## KNOWLEDGE_CORE implementation
Added:
- root `REPOSITORY_STRUCTURE_PROTECTION.yaml`;
- `father/repository-migrations/MIGRATION_RULES.md`;
- `tools/validate_repository_structure_protection.py`;
- CI integration in `Knowledge Quality Gate`.

The protected knowledge set includes Security Knowledge, Security snapshots/audits, professional domain governance, canonical product roadmaps, `professional-knowledge/`, activated professional domain roots, validators and workflows.

Every activated non-Security domain under `professional-knowledge/` must receive an explicit `DO_NOT_MOVE` registry entry. This prevents the registry from becoming stale as new professional KBs are materialized.

## Ownership boundary
Repository restructuring must preserve:
- PX00 = organization/runtime/authority/execution/trace/replay/Factory Builder;
- KNOWLEDGE_CORE = canonical professional/domain/product knowledge;
- Security truth remains in `KNOWLEDGE_CORE/security-knowledge/` and is consumed/pinned by PX00 rather than duplicated there.

## Governed migration
A protected structural move requires an explicit migration record containing at least rationale, affected protected IDs, old-to-new path mapping, inbound-reference inventory, provenance/history impact, compatibility plan, rollback plan, independent/relevant reviewer and CI evidence.

Historical Tree_F/ADR/journal/snapshot/audit records are not rewritten to pretend a new layout always existed.

## Failed evidence retained
The first strengthened KNOWLEDGE_CORE gate failed because the newly created protection registry contained an invalid YAML list/note indentation. The validator failure was inspected and the YAML was repaired; the gate was not weakened.

## Evidence
- PX00 Contract Validation on the protected-registry implementation completed SUCCESS.
- KNOWLEDGE_CORE Knowledge Quality Gate run #478 on commit `b666e36ea42e3e3928f2caeb26a9f0aeea4753a4` completed SUCCESS after the YAML repair.

## What is proven
Canonical repository surfaces are now explicitly inventoried and CI checks that registered paths still exist with the expected structural kind. Activated professional domains cannot silently exist outside the explicit protected inventory.

## What is not proven
This is repository-level guardrail, not an administrator-proof control. A privileged actor can still bypass CI, rewrite Git history or alter branch protection outside repository code. Such platform controls remain separate operational governance.
