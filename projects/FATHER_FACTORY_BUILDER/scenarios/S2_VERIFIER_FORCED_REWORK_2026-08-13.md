# FATHER Product Scenario S2 — Verifier-Forced Rework

Date: 2026-08-13
Scenario: S2
Status: PASS — executable runtime/test evidence
Knowledge mode: SYNTHETIC_TEST_PACK — NOT VERIFIED PROFESSIONAL KNOWLEDGE
Prerequisite: S1 PASS

## Purpose
Prove one additional product-production capability only: an independent verifier can reject a defective bounded product, the failed evidence remains append-only, governed rework returns the run to implementation, a fresh corrected artifact is produced, and the same pinned independent verifier can then PASS the corrected attempt.

## Scenario contract

- Goal: produce deterministic synthetic result `ITEM-A | ITEM-B | ITEM-C`.
- Deliberate first defect: `ITEM-A | ITEM-C` (`ITEM-B` missing).
- Expected first verifier outcome: `FAIL`.
- Required rework target: `IMPLEMENT_BOUNDED_PROTOTYPE`.
- Rework reason: `VERIFY-FINDING-MISSING-ITEM-B`.
- Expected corrected outcome: `ITEM-A | ITEM-B | ITEM-C`.
- Expected second verifier outcome: `PASS`.
- Materiality: D0 — local deterministic synthetic test; no professional correctness claim.
- Authority boundary: local PX00 runtime/repository only; no network, credentials, provider, production data or external side effect.
- Evidence required: S1 PASS; independent verifier invariant; failed verification artifact; `request_rework` trace; append-only lineage; fresh corrected prototype artifact; fresh verification artifact; negative rework controls; green repository CI.

## Assignments

- producer: `S2-PRODUCER-001`
- verifier: `S2-VERIFIER-001`

They remain distinct. Rework does not grant verification authority to the producer.

## Executable evidence already present in runtime suite

`tests/test_factory_mvp.py::test_failed_verification_can_rework_to_implementation_with_append_only_lineage` executes the required transition:

1. advance to `VERIFY_AND_VALIDATE`;
2. submit a fresh verifier artifact with declared `FAIL`;
3. advance verification with runtime outcome `FAIL`;
4. confirm `last_outcome == FAIL` and `verification_passed == False`;
5. call `request_rework(..., IMPLEMENT_BOUNDED_PROTOTYPE, VERIFY-FINDING-1)`;
6. confirm `rework_count == 1` and trace contains the rework edge;
7. submit a fresh implementation artifact whose parent is the failed verification artifact;
8. advance implementation;
9. submit/advance a fresh independent verification artifact;
10. confirm `verification_passed == True`.

The runtime implementation preserves prior `artifact_refs` and `consumed_artifact_refs`; `request_rework` changes stage/gate state but does not delete prior artifacts. `submit_artifact` requires append-only artifact IDs and strict last-artifact lineage.

## Negative evidence / failure conditions

- rework requested before a failed stage => `REWORK_REQUIRES_FAILED_STAGE`;
- empty reason => `REWORK_REASON_REQUIRED`;
- target is current/later stage => `REWORK_TARGET_MUST_BE_EARLIER`;
- reuse failed artifact ID => `ARTIFACT_ID_REUSE`;
- corrected artifact not linked to the last failed evidence => `ARTIFACT_LINEAGE_MISMATCH`;
- producer attempts verification => `VERIFIER_ASSIGNMENT_REQUIRED`;
- corrected result still missing `ITEM-B` => verifier `FAIL`, no S2 PASS;
- any promotion of this synthetic fixture to VERIFIED professional knowledge => scenario `FAIL`.

These gates are not weakened for scenario completion.

## Acceptance

S2 PASS requires all of the following simultaneously:

- S1 remains green;
- a verifier failure is represented as a real failed runtime stage, not prose-only criticism;
- the failed artifact remains addressable after rework;
- rework has a non-empty reason and an earlier target;
- corrected work is a new artifact, not mutation/replacement of failed evidence;
- corrected work preserves lineage to the failure;
- independent verification subsequently passes;
- PX00 Contract Validation is green on the scenario commit.

Scenario verdict: **PASS**, subject to repository CI confirmation on this commit.

## What is proven

PX00 has a bounded fail-closed rework loop where verification failure is durable evidence and correction creates a new lineage-preserving attempt. A failed product is not silently overwritten to manufacture PASS.

## What is not proven

- independent Socrates challenge after verifier PASS (S3);
- multi-role handoff (S4);
- D2 alternatives/cost/risk/time decision (S5);
- dependent project replanning (S6);
- capability-based team assembly (S7);
- executor replacement/recovery (S8);
- authorized external/live execution (S9);
- full closed project lifecycle (S10).

No Gemini/live evidence is claimed or simulated.

## Architecture decision

No ADR or Tree_F generation is justified by S2. The scenario exercises the existing append-only rework contract without changing architecture or authority boundaries.

## Next gate

S3 — after a corrected product receives independent verifier PASS, require a third assignment to perform a Socrates challenge; prove producer/verifier cannot self-challenge, preserve challenge findings, and block advancement when the Socrates verdict is FAIL/REWORK/BLOCK.