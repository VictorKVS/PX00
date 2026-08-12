# TF-0071 — Professional Decision Trace and Replay

Date: 2026-08-13
Status: COMPLETE — M1 REFERENCE CONTRACT
ADR: `ADR-0064`
Norm: `PX00-NORM-DM-0001`

## Why this generation exists

TF-0070 made decision materiality a project norm. TF-0071 makes that norm operational inside historical RUN evidence.

Before this generation PX00 could replay:
- governed events;
- policy snapshot;
- pinned knowledge context.

The remaining gap was the professional derivation itself: **which formal decision was relied on, under which materiality class, and whether that decision had passed the evidence/review floor before being attached to the RUN.**

## Implemented chain

`REQUIREMENTS / CONSTRAINTS → MATERIALITY → OPTIONS / EVIDENCE → REVIEW / APPROVAL → PROFESSIONAL DECISION → DECISION DIGEST → RUN TRACE → READ-ONLY REPLAY`

Implemented:
- `GovernedProfessionalDecision` canonical record in the PX00 reference runtime;
- `DecisionContextBinder` bound to exact RUN/role/assignment;
- materiality gate before decision binding;
- D1/D2/D3 evidence obligations enforced proportionally;
- D2/D3 requirements, constraints, options and review obligations;
- D3 approval obligation;
- selected option must belong to the declared option set;
- decision SHA-256 + materiality class persisted in TRACE manifest;
- replay requires persisted decision context and fails closed on omission/substitution;
- previous knowledge-only replay semantics preserved.

## Acceptance criteria

1. D2 with incomplete evidence cannot bind — PASS.
2. Decision from another RUN cannot bind — PASS.
3. Role/assignment identity is pinned by the binder — PASS.
4. Undeclared selected option is rejected — PASS.
5. Decision reference, digest and D0–D3 class persist in TRACE — PASS.
6. Replay cannot silently omit persisted decision context — PASS.
7. Digest substitution is detected — PASS.
8. Existing knowledge-only replay compatibility is preserved — PASS.
9. Unit/integration, secret scan and repository contract validation pass — PASS on implementation head; final generation head is revalidated after journals/records.

## Important restraint

This is **formal rationale provenance, not hidden chain-of-thought capture**.

TRACE carries stable references and digests. Professional decision records carry requirements, constraints, alternatives, evidence references, formal rationale, assumptions, uncertainty and verification plans. Private model reasoning is neither required nor treated as audit evidence.

## What this proves

PX00 can now preserve four different things without conflating them:

`POLICY ≠ KNOWLEDGE ≠ PROFESSIONAL DECISION ≠ RUNTIME AUTHORITY`.

A historical reviewer can establish:
- what policy governed the RUN;
- what knowledge snapshot was available;
- which evidence-backed professional decision was relied on;
- its materiality class and immutable digest;
- which governed material events happened.

## What is NOT proven

- production durable decision storage;
- enterprise approval workflow;
- live AI professional judgment;
- expert Security reasoning over a truly atomic VERIFIED requirement;
- correctness of a domain decision merely because its trace is intact.

Integrity proves history, not truth.

## Next high-value evidence

Do not extend decision/snapshot plumbing unless real use breaks it.

Next product-value targets:
1. `SUMMIT-FFB-02` — first governed real AI provider inference through the existing boundary;
2. first professional Security decision using a truly atomic VERIFIED Security requirement from canonical `KNOWLEDGE_CORE`, when such a slice is ready;
3. combine real knowledge + professional decision + real executor + independent verifier in the first closed FATHER professional loop.
