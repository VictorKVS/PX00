# FATHER Product Scenario S1 — Task with Independent Verifier

Date: 2026-08-13
Scenario: S1
Status: PASS — contract/code evidence
Knowledge mode: SYNTHETIC_TEST_PACK — NOT VERIFIED PROFESSIONAL KNOWLEDGE
Prerequisite: S0 PASS

## Purpose
Prove the next product-production rung without claiming later rework/Socrates capability as part of this scenario: one bounded producer result is checked by an explicitly different verifier assignment, and self-review is rejected by the existing runtime contract.

## Scenario contract

- Goal: produce the same deterministic synthetic release-note summary as S0 and require an independent verifier before acceptance.
- Input: PUBLIC synthetic-safe fixture only: `ITEM-A`, `ITEM-B`, `ITEM-C`.
- Expected producer outcome: `ITEM-A | ITEM-B | ITEM-C`.
- Expected verifier outcome: `PASS` only when the produced identifiers exactly match the fixture in deterministic order and no extra identifier or professional claim is introduced.
- Materiality: D0 — local deterministic test transformation; verifier independence is an assurance property, not a claim of professional expertise.
- Authority boundary: local repository/runtime only; no network, credentials, provider call, production data, side effect or professional-knowledge admission.
- Evidence required: S0 PASS, runtime independence invariant, verifier-stage assignment invariant, positive verifier case, negative self-review case, negative incorrect-product case, repository CI.

## Assignments

- producer assignment: `S1-PRODUCER-001`
- verifier assignment: `S1-VERIFIER-001`

They are intentionally different assignments. The verifier does not inherit producer authority and the producer cannot submit the verifier-stage artifact.

## Positive execution

Synthetic producer artifact:
`ITEM-A | ITEM-B | ITEM-C`

Independent verifier assessment:
- expected identifiers: `ITEM-A`, `ITEM-B`, `ITEM-C`;
- observed identifiers: `ITEM-A`, `ITEM-B`, `ITEM-C`;
- extra identifiers: none;
- missing identifiers: none;
- VERIFIED professional/domain claims: none;
- verdict: `PASS`.

Scenario verdict: **PASS**.

## Runtime evidence

The existing `AgentRdFactoryMvp` contract already enforces the two invariants needed by S1:

1. `create_run(...)` rejects equal `producer_assignment_ref` and `verifier_assignment_ref` with `INDEPENDENCE_VIOLATION`.
2. At `VERIFY_AND_VALIDATE`, `submit_artifact(...)` requires the artifact producer to equal the run's `verifier_assignment_ref`; `advance(...)` rechecks independence.

S1 uses these already-proven bounded mechanisms as evidence. It does not claim the full factory pipeline was executed as S1, because that would silently include Socrates and later stages.

## Negative evidence retained

### N1 — self-review
Attempt:
`producer_assignment_ref == verifier_assignment_ref == S1-PRODUCER-001`

Expected runtime result:
`INDEPENDENCE_VIOLATION`

Verdict: **REJECTED BY CONTRACT**.

### N2 — producer impersonates verifier stage
Attempt: producer assignment submits `VERIFICATION_REPORT` at `VERIFY_AND_VALIDATE`.

Expected runtime result:
`VERIFIER_ASSIGNMENT_REQUIRED` / independence rejection.

Verdict: **REJECTED BY CONTRACT**.

### N3 — incorrect bounded product
Observed candidate:
`ITEM-A | ITEM-C`

Verifier result:
`FAIL — ITEM-B missing`.

This negative case is preserved as scenario evidence; the gate is not weakened to accept partial output.

### N4 — invented output
Observed candidate:
`ITEM-A | ITEM-B | ITEM-C | ITEM-D`

Verifier result:
`FAIL — ITEM-D absent from fixture`.

### N5 — synthetic knowledge promoted as professional truth
Any `VERIFIED professional knowledge` claim derived from this fixture => `FAIL`.

## What is proven

Within the bounded reference contract, producer and verifier identity are distinct and self-review fails closed. A deterministic synthetic product can therefore be accepted only after an explicitly independent verifier checks the expected bounded result.

## What is not proven

- verifier-forced rework and successful corrected rerun (S2);
- independent Socrates challenge (S3);
- multi-role handoff (S4);
- D2 alternatives/cost/risk/time decision (S5);
- dependent project replanning (S6);
- capability-based team assembly (S7);
- executor replacement/recovery (S8);
- authorized external/live execution (S9);
- full closed corporate loop (S10).

No live Gemini evidence is claimed. No runtime credential was inspected or invented for this offline rung.

## Next gate

S2 — deliberately submit a bounded product defect, require the independent verifier to return FAIL, preserve the failed artifact, invoke governed `request_rework(...)`, produce a corrected fresh artifact and prove the verifier can turn the corrected attempt into PASS without deleting the first failure.