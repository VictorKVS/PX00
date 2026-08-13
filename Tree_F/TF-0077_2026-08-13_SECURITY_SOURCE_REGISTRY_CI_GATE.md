# TF-0077 — Security Source Registry CI Gate

Status: IMPLEMENTED_PENDING_PX00_CI
Date: 2026-08-13

## Goal
Close the repository-level acceptance gap for newly registered Security Knowledge P0 source registries without promoting their maturity beyond available evidence.

## Canonical trigger
KNOWLEDGE_CORE scorecard `SEC-COVERAGE-2026-08-13-R04` recorded all 12 P0 families as REGISTERED at a conservative overall maturity of 10%, while explicitly leaving `GAP-P0-009`: no repository-level validator/CI acceptance for the new registries.

## Change in KNOWLEDGE_CORE
PR #1 introduced `Security Source Registry Gate` plus regression tests. The gate checks:
- registry family IDs resolve in `master-source-inventory.yaml`;
- priority and family status match the canonical inventory;
- source IDs remain unique;
- evidence-bearing official metadata keeps required fields and HTTPS authoritative hosts;
- acquired dynamic sources require snapshot semantics;
- dynamic VERIFIED observations carry `observed_at`;
- explicit red-team limitations remain present.

The first gate run failed and was retained as evidence. It found `GOST_R_ISO_IEC_27001_2021` marked `STATUS_VERIFIED_METADATA_ONLY` without `status_observed`. The implementation also exposed three existing VERIFIED dynamic BDU observations without `observed_at`, contrary to the registry's own red-team rule. Both defects were repaired; the gate and repository CI then passed. The implementation was squash-merged as KNOWLEDGE_CORE commit `63caabd66a880fb6af2017642982c55507b4e5c3`.

## Maturity effect
`GAP-P0-009` is closed, but no family is promoted by validator acceptance alone. Conservative Security Knowledge maturity remains 10% and `expert_ready` remains false.

## Cross-repository effect
PX00 does not copy the professional knowledge. It records the governance milestone and corrects its dashboard drift: all 12 P0 families are now REGISTERED or better, not four families NOT_REGISTERED.

## Next proof
Promote one P0 family beyond REGISTERED with family-wide evidence. Current first choice is `CLASSIFICATION_AND_CATEGORIZATION_METHODS`: establish current PP 1119 and PP 127 version chains, then extract decision logic with explicit inputs, provenance, reassessment triggers and effective dates.

`SUMMIT-FFB-02` remains OPEN until a real authorized Gemini run exists.
