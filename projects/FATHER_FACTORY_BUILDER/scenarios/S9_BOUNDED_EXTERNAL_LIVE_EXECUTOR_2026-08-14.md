# S9 — Bounded external/live executor when authorized

Date: 2026-08-14
Project: `PROJECT-FFB-0001`
Scenario rung: S9
Predecessor: S8 GREEN (`PX00 Contract Validation #619`)
Status: BLOCKED — authorization/runtime credential preconditions not proven in this run

## Purpose

Add exactly one complexity over S8: permit a bounded external/live executor only when both runtime authorization and an actually available runtime credential are proven. This scenario does not simulate a provider call and does not treat offline/synthetic output as live evidence.

## Knowledge profile

- fixture/professional material: PUBLIC-safe synthetic/test only;
- professional KB status: NOT VERIFIED by this scenario;
- synthetic capability/knowledge MUST NOT be promoted to VERIFIED professional knowledge;
- no secret, credential value, private payload or credential-derived data may be committed as evidence.

## Expected outcome fixed before execution

If all live preconditions are proven, one PUBLIC-only bounded request may be delegated to the authorized external executor and must return a fresh provider/runtime evidence chain that is independently verified and Socrates-challenged before acceptance.

If any live precondition is absent or unproven, expected outcome is `BLOCKED` and no external call occurs. BLOCKED is the correct fail-closed acceptance outcome, not a reason to weaken the gate.

## Materiality

D2.

External execution changes the trust boundary and may create cost, disclosure, provider and availability risk. Authorization to perform the live call is therefore not inherited from an executor assignment or from earlier offline scenario success.

## Authority boundary

The executor may execute only the explicitly authorized PUBLIC-only bounded request. It may not broaden scope, change data classification, choose a different provider, expose credentials, alter acceptance criteria, approve its own result, or convert synthetic/test knowledge into VERIFIED professional knowledge.

D2 authority must explicitly authorize the live boundary. Verifier and Socrates remain independent from the external executor.

## Mandatory preconditions / evidence

Before any live call, append-only evidence must prove all of:

1. S8 predecessor generation is GREEN;
2. external/live execution is explicitly authorized for this bounded scenario;
3. payload classification is PUBLIC-only;
4. provider/profile is explicitly allowed;
5. runtime credential is actually available to the runtime without revealing its value;
6. request scope, expected result shape, timeout/retry ceiling and cost boundary are fixed before execution;
7. executor assignment identifies the live boundary and cannot self-verify;
8. failure/rejection evidence will be retained;
9. fresh independent verifier and Socrates evidence are required after the provider result.

For Gemini specifically, absence of an explicitly available runtime credential or PUBLIC-only authorized profile means `BLOCKED`; no mock response may be labelled Gemini/live evidence.

## Current execution result

This run proves S8 predecessor GREEN via Contract Validation #619, but does not have evidence that an authorized PUBLIC-only Gemini/live profile and runtime credential are explicitly available to this execution context. Therefore the live branch is not executed.

Verdict: `S9 BLOCKED`.

This is a scenario-gate result, not a provider failure and not a professional-KB verdict.

## Negative tests / rejected conditions

The following must remain fail-closed and retained as rejected evidence:

1. live call without explicit D2 authorization;
2. live call when credential availability is merely assumed;
3. exposing or committing a credential/secret as evidence;
4. non-PUBLIC or ambiguously classified payload;
5. provider/profile substitution after authorization;
6. mock/stub/offline output labelled as live provider evidence;
7. executor self-verification;
8. stale verifier/Socrates evidence reused for a fresh live result;
9. retry beyond the predeclared bound;
10. post-hoc weakening of acceptance, timeout, cost or scope limits;
11. provider result treated as VERIFIED professional knowledge solely because it is live;
12. failed/rejected provider evidence deleted or overwritten;
13. live result accepted without fresh lineage/digest binding;
14. external executor granted authority not present in the explicit assignment.

## Acceptance

`PASS` requires actual authorized live evidence satisfying every precondition plus fresh independent verifier and Socrates PASS evidence.

`BLOCKED` is mandatory when authorization/profile/credential evidence is absent. A BLOCKED S9 does not unlock S10.

## Replay

Replay must distinguish at least: `PRECONDITION_CHECK -> AUTHORIZATION -> LIVE_ASSIGNMENT -> PROVIDER_ATTEMPT -> RESULT/FAILURE -> VERIFIER -> SOCRATES -> ACCEPT/BLOCK`, preserving rejected/failed evidence append-only.

## Architecture impact

No Tree_F/ADR change is justified by this blocked run. If an authorized live execution later proves a new provider-neutral trust-boundary primitive that is not already represented by existing executor/authority/evidence contracts, record that architectural decision then rather than speculatively now.
