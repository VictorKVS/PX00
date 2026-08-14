# S8 — Replaceable Executor and Failure Recovery

Date: 2026-08-14
Project: `PROJECT-FFB-0001`
Scenario rung: S8
Predecessor gate: S7 generation GREEN (`PX00 Contract Validation #616`, commit `eb1cc09fdd6c95686bf5c80f872fd2de3c0f4348`)
Knowledge profile: PUBLIC-safe synthetic/test professional pack only. This scenario is NOT VERIFIED professional knowledge.
Live executor: forbidden for this scenario.

## One new complexity

S8 adds exactly one capability over S7: an assigned executor may fail and be replaced by another eligible executor without changing task acceptance, authority, lineage, or independent review requirements.

## Synthetic capability registry

- `EXEC-A`: capabilities `[bounded_transform]`; eligible producer; primary assignment.
- `EXEC-B`: capabilities `[bounded_transform]`; eligible producer; replacement candidate.
- `VERIFY-C`: capabilities `[bounded_verify]`; verifier only.
- `SOCRATES-D`: capabilities `[bounded_challenge]`; Socrates only.

Registry entries are synthetic fixtures. Capability match does not prove real professional competence and does not grant authority.

## Bounded task

Input: `{A,B,C}`.
Acceptance result: exactly `{A,B,C}`; no missing or extra item.
Primary executor: `EXEC-A`.
Replacement executor: `EXEC-B` only after explicit failure evidence for the primary attempt.

## Expected outcome

1. Assignment `T1-A1` is issued to `EXEC-A` with immutable acceptance `{A,B,C}`.
2. `EXEC-A` produces deterministic failure evidence `EXECUTOR_FAILURE` before an acceptable result is produced.
3. Failure evidence and the failed assignment remain append-only and replayable.
4. Recovery decision explicitly records why replacement is allowed and selects `EXEC-B` from the same pre-existing capability requirements.
5. A fresh assignment `T1-A2` is issued to `EXEC-B`; it does not inherit hidden authority from `EXEC-A`.
6. `EXEC-B` produces fresh result `{A,B,C}` linked to `T1-A2` and the recovery decision.
7. `VERIFY-C` independently verifies the fresh result; stale verification from A1 cannot be reused.
8. `SOCRATES-D` independently challenges recovery, lineage, unchanged acceptance and authority boundaries.
9. Delivery is allowed only after fresh verifier PASS and Socrates PASS.

Expected scenario verdict: PASS only if all nine conditions hold.

## Failure conditions

Any of the following is scenario FAIL/BLOCK:

- replacement occurs without recorded primary failure;
- failed/rejected A1 evidence is deleted, overwritten or hidden;
- acceptance is weakened or scope is changed to make replacement pass;
- replacement candidate lacks the original required capability;
- replacement selection mutates the registry after failure;
- `EXEC-B` reuses A1 result/artifact identity instead of creating fresh evidence;
- stale A1 verification is reused for A2;
- producer performs its own verification or Socrates review;
- replacement implicitly acquires D1/D2 authority;
- retry loop is unbounded or silently repeats the same failed executor;
- output contains missing/extra items;
- synthetic capability evidence is promoted to VERIFIED professional competence;
- any external/live executor is invoked.

## Materiality

D0 bounded synthetic execution. Executor replacement is operational recovery only. Any change to scope, acceptance, cost/risk/time thresholds, external execution permission, or D2 decision is outside this scenario and must BLOCK/escalate rather than be hidden as recovery.

## Authority boundary

- Executor may execute only its explicit assignment.
- Recovery controller may replace a failed executor only with a candidate satisfying the unchanged explicit capability requirement.
- Verifier may accept/reject evidence but may not rewrite producer output.
- Socrates may challenge recovery and evidence but may not silently change acceptance.
- No role gains D2 authority through capability match, failure, replacement, or handoff.

## Evidence required for replay

Preserve append-only:

- original task and acceptance contract;
- capability requirements and registry snapshot used before A1;
- `T1-A1` assignment;
- A1 failure/rejected evidence and reason;
- explicit recovery/replacement decision;
- rejected replacement candidates, if any;
- fresh `T1-A2` assignment;
- fresh A2 result and lineage to recovery decision;
- fresh independent verifier verdict;
- fresh independent Socrates verdict;
- final delivery/acceptance decision.

## Negative tests

1. `replace_without_failure` → BLOCK.
2. `delete_failed_A1_evidence` → BLOCK.
3. `weaken_acceptance_during_recovery` → BLOCK.
4. `replacement_missing_capability` → BLOCK.
5. `post_failure_registry_mutation` → BLOCK.
6. `reuse_A1_artifact_as_A2` → BLOCK.
7. `reuse_stale_A1_verification` → BLOCK.
8. `producer_self_verification` → BLOCK.
9. `producer_or_verifier_as_socrates` → BLOCK unless independently assigned and independence contract is still satisfied; default fixture rejects it.
10. `implicit_D2_escalation` → BLOCK.
11. `unbounded_retry_same_executor` → BLOCK.
12. `extra_ITEM_D_or_missing_ITEM_B` → FAIL.
13. `synthetic_to_VERIFIED_promotion` → BLOCK.
14. `external_live_executor_call` → BLOCK.

Rejected and failed evidence must remain in the replay set; a PASS that depends on erasing it is invalid.

## Acceptance

S8 PASS proves only the bounded product mechanism: an eligible executor can fail, the failure remains evidence, another eligible executor can be explicitly substituted, and fresh independent verification/challenge can accept the recovered result without weakening gates or authority boundaries.

It does NOT prove real professional competence, production-grade fault tolerance, authorized live-provider execution, or S9/S10.

Next rung is permitted only after this S8 repository generation receives green `PX00 Contract Validation`: **S9 — bounded external/live executor when explicitly authorized**.