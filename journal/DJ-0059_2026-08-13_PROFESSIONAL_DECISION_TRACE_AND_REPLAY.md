# DJ-0059 — Professional Decision Trace and Replay

Date: 2026-08-13
Tree_F: `TF-0071`
ADR: `ADR-0064`

## Change

Operationalized `PX00-NORM-DM-0001` inside the governed RUN evidence path.

PX00 can now bind an evidence-backed professional decision only after the decision materiality gate passes, pin it to exact RUN/role/assignment identity, persist its canonical digest and D0–D3 class in the TRACE manifest, and require the same decision context during read-only replay.

## Why

Historical audit requires more than `what happened`. For professional work FATHER must preserve the formal answer to `why was this option selected under the requirements, constraints and evidence that existed then?`

The auditable object is a governed professional decision record and its provenance — not hidden model chain-of-thought.

## Cross-project boundary

`KNOWLEDGE_CORE` remains authoritative for profession-specific evidence semantics and source corpora.

PX00 owns:
- decision materiality floor;
- fail-closed runtime binding;
- RUN/role/assignment identity checks;
- decision digest trace persistence;
- replay integrity.

Knowledge/evidence still does not grant runtime authority.

## Evidence

Negative and positive tests prove:
- incomplete D2 evidence blocks binding;
- cross-RUN decision substitution blocks;
- undeclared selected options block;
- decision digest is persisted;
- omitted decision context blocks replay;
- digest substitution is detected;
- knowledge-only replay backward compatibility remains intact.

## Maturity statement

This is a bounded M1 reference runtime proof. It is not a production decision repository and does not yet prove expert Security reasoning or a live AI professional executor.

## Next

Stop meta-expanding this layer. Move evidence generation back to product value:
1. governed live AI executor;
2. atomic VERIFIED Security requirement;
3. first closed professional FATHER loop combining both.
