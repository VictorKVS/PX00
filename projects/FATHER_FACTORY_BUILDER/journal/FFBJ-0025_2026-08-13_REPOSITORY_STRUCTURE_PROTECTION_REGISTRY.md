# FFBJ-0025 — Repository Structure Protection Registry

Date: 2026-08-13
Generation: `TF-0078`
Status: COMPLETE

Factory Builder now has an explicit repository-structure safety boundary for future GitHub cleanup/reorganization.

Protected PX00 surfaces include the Factory Builder project root, role/contracts/risk/journal history, governance, Tree_F/ADR history, runtime/contracts/tests and knowledge-consumer boundary according to their `DO_NOT_MOVE` or `MIGRATION_ONLY` class.

Canonical professional knowledge remains owned by KNOWLEDGE_CORE. Security Knowledge, professional domain governance, product roadmaps and every activated `professional-knowledge/<domain>` root are protected from generic structural relocation.

Key invariant:
`PROTECTED != FROZEN`.

Factory Builder and professional KB content continue to be edited and matured. Structural identity changes require an explicit migration record, compatibility/rollback plan and green CI rather than a generic cleanup commit.

The first KNOWLEDGE_CORE protection-gate attempt exposed invalid YAML in the new registry. The failure was retained and repaired without weakening validation; the next Quality Gate passed.

No summit promotion is claimed. This generation protects provenance, references and canonical ownership while future product/scenario work continues.
