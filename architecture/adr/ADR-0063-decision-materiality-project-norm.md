# ADR-0063 — Decision Materiality as Project-Wide Governance Norm

Date: 2026-08-13
Status: ACCEPTED

## Context
Across multiple design discussions the same principle repeatedly emerged: not every decision deserves the same evidentiary burden, but decisions with higher consequence, irreversibility, uncertainty or risk require stronger evidence, independent review and accountable approval.

Without a project-wide norm this principle would remain informal, be rediscovered per role/domain, or be applied inconsistently. That creates two opposite failure modes:
- bureaucracy for trivial/local decisions;
- intuition-based acceptance for architecture, regulated, safety or critical decisions.

## Decision
Adopt `PX00-NORM-DM-0001` in `governance/DECISION_MATERIALITY_STANDARD.md` as a project-wide governance norm.

Use four materiality classes:
- `D0_LOCAL_CONVENTIONAL`;
- `D1_IMPLEMENTATION`;
- `D2_ARCHITECTURE_PRODUCT`;
- `D3_REGULATED_SAFETY_CRITICAL`.

Materiality is determined from consequence/cost of error, reversibility, uncertainty, blast radius, regulatory/contractual criticality, security/safety criticality, lock-in and material external effects.

The highest material dimension sets a floor; dimensions are not averaged down.

Existing risk severity remains independent but can raise the floor:
- S2 → at least D1 when behavior is affected;
- S3 → at least D2;
- S4 → D3 and existing veto semantics.

## Enforcement
- Constitution now contains the materiality invariant.
- `schemas/DECISION_MATERIALITY.yaml` defines machine-readable semantics.
- `px00/decision_materiality.py` implements a fail-closed reference gate.
- tests cover under-classification, S3/S4 floors, missing evidence and independent review/approval requirements.
- Factory Builder Role Packages must declare typical materiality range and promotion triggers.
- KNOWLEDGE_CORE `PROFESSIONAL_DECISION_RECORD` is aligned to the same norm while retaining domain-specific evidence semantics.

## Key separation
`DECISION MATERIALITY != RISK SEVERITY != SYSTEM MATURITY != DELIVERY STAGE`.

PX00 owns the governance depth required by materiality. KNOWLEDGE_CORE professional domains define what counts as valid evidence for the profession.

## Consequences
Positive:
- material decisions become consistently explainable and auditable;
- assurance effort scales with consequence instead of being uniformly heavy;
- role/agent cannot silently downgrade a critical decision to avoid evidence/review;
- Security evidence-first design becomes a reusable pattern for every professional domain.

Costs:
- D2/D3 decisions require explicit evidence categories and independent review;
- role/protocol design must include materiality behavior;
- future decision records need historical evidence snapshots for replay/reassessment.

## Non-goal
This ADR does not require full D3 ceremony for local coding conventions or other D0 decisions. Proportionality is part of the norm.
