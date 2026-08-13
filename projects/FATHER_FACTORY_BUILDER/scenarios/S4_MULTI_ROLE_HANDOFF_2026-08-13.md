# S4 — Bounded multi-role handoff

Date: 2026-08-13
Status: VERIFY — bounded offline scenario
Depends on: S3 green (`PX00 Contract Validation #606`)

## Purpose

Prove exactly one additional capability over S3: bounded work can be handed from one role to another without transferring hidden authority, losing required context, breaking artifact lineage, or allowing the receiving role to rewrite upstream evidence.

This scenario uses only synthetic/test professional material. It is NOT VERIFIED professional knowledge and creates no professional truth claim.

## Scenario

Synthetic PUBLIC-safe task: transform the fixed input set `ITEM-A`, `ITEM-B`, `ITEM-C` into the canonical result `ITEM-A | ITEM-B | ITEM-C`.

Role chain:

`ASSIGN-ANALYST -> ASSIGN-PRODUCER -> ASSIGN-VERIFIER -> ASSIGN-SOCRATES`

The Analyst creates a bounded handoff artifact containing the task boundary, expected output, permitted synthetic context and upstream lineage. The Producer may implement only that handed-off scope. The independent Verifier evaluates the produced result without becoming its producer. The independent Socrates assignment challenges the verified result before governed delivery.

## Expected outcome

1. Analyst handoff preserves the exact three-item scope and synthetic-only classification.
2. Producer consumes the handoff without receiving Analyst authority.
3. Producer emits a fresh result artifact linked to the handoff lineage.
4. Independent verifier checks exact equality with `ITEM-A | ITEM-B | ITEM-C`.
5. Independent Socrates challenge remains required after verifier PASS.
6. Rejected/failed attempts remain append-only evidence.
7. No role may rewrite or relabel an upstream artifact as its own evidence.

## Materiality

`D0` for the synthetic product result. S4 validates orchestration and handoff governance only. It does not authorize a D2/D3 professional decision.

## Authority boundary

Allowed:
- offline bounded PX00/FATHER reference harness;
- synthetic PUBLIC-safe fixtures;
- distinct Analyst, Producer, Verifier and Socrates assignments;
- explicit handoff/context artifacts;
- append-only lineage and trace;
- fail-closed rejection.

Forbidden:
- external/live executor or network call;
- runtime credentials;
- promotion of synthetic material to VERIFIED professional knowledge;
- authority inheritance merely because an artifact was handed off;
- producer/verifier/Socrates identity collapse;
- mutation or deletion of rejected upstream evidence;
- expansion beyond the three-item scope.

## Required evidence

PASS evidence must show:
- S3 predecessor CI green;
- distinct role/assignment identities across the chain;
- a bounded handoff artifact/context boundary;
- fresh downstream artifact lineage rather than upstream mutation;
- independent verifier and Socrates gates remain fail-closed;
- negative cases are represented by executable repository controls/tests or explicit rejected evidence;
- PX00 Contract Validation green for this scenario head.

## Negative tests / failure conditions

S4 is FAIL if any of the following succeeds:

1. Producer changes handed-off scope by adding `ITEM-D`.
2. Producer drops `ITEM-B` without a recorded failure/rework path.
3. Receiving role gains upstream role authority implicitly.
4. Producer self-verifies.
5. Verifier rewrites the producer result instead of issuing independent evidence.
6. Producer or verifier performs the Socrates review.
7. A downstream artifact substitutes unrelated lineage.
8. A consumed/stale artifact is reused as fresh stage evidence.
9. Rejected/failed evidence disappears after handoff/rework.
10. Synthetic fixture content is labelled VERIFIED professional knowledge.
11. Any external call occurs in this offline scenario.

Any missing authority, context, lineage or independence proof is fail-closed; the gate must not be weakened merely to obtain PASS.

## Acceptance

S4 may be declared PASS only when the repository evidence supports the bounded handoff invariants above and Contract Validation for this head is green. Until then status remains VERIFY/FAIL/REWORK as observed.

No Tree_F or ADR update is justified by creation of this scenario alone: it exercises the existing organization/assignment/context/lineage architecture rather than changing it. If implementation reveals that a new handoff primitive or authority rule is required, that architectural change must be handled separately and S4 must remain non-green until revalidated.

## What this scenario does not prove

- semantic competence of real professional roles;
- VERIFIED professional knowledge;
- external/live executor reliability;
- capability-based team assembly (S7);
- replaceable executor recovery (S8);
- full project closure/replay (S10).

Next allowed level after green acceptance: **S5 — alternatives + cost/risk/time trade-off under D2**.
