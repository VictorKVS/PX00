# FFBJ-0018 — Professional Decision Trace and Replay

Date: 2026-08-13
Tree_F: `TF-0071`
ADR: `ADR-0064`
Norm: `PX00-NORM-DM-0001`

## Why this matters to Factory Builder

A factory blueprint must not create roles that can make material professional decisions while leaving the justification as prompt text or personal preference.

TF-0071 proves the runtime side of the Factory Builder obligation introduced by TF-0070: material professional decisions can be gated by D0–D3 evidence depth and then pinned into RUN trace/replay as immutable provenance.

## Proven behavior

`REQUIREMENTS / CONSTRAINTS → MATERIALITY → OPTIONS / EVIDENCE → REVIEW / APPROVAL → PROFESSIONAL DECISION → TRACE → REPLAY`

The runtime rejects:
- insufficient D2 evidence;
- RUN/role/assignment identity mismatch;
- selected option not present in the declared option set;
- replay that omits persisted decision context;
- replay with substituted decision digest.

Decision provenance is stored as stable references/digests/materiality, not hidden chain-of-thought.

## Factory Builder consequence

New or revised Role Packages must increasingly specify:
- which professional decisions the role owns;
- typical D0–D3 range;
- promotion triggers;
- admissible domain evidence classes;
- independent-review/approval requirements;
- expected verification/outcome feedback.

Factory Builder does not need a separate profession-specific truth store. It designs the organizational contract; `KNOWLEDGE_CORE` supplies canonical domain evidence.

## Maturity restraint

This proves a bounded reference control. It does not prove that an AI is a competent architect, analyst, programmer or Security expert merely because the decision record is structurally valid.

## Next useful summit evidence

No more decision-provenance plumbing unless a real run exposes a failure.

Priority remains:
1. `SUMMIT-FFB-02` real governed live executor;
2. real canonical professional knowledge slice at sufficient verification state;
3. first closed FATHER loop combining professional evidence, decision, execution, independent review and replay.
