# S7 — Capability-Based Team Assembly

Date: 2026-08-14
Project: `PROJECT-FFB-0001`
Scenario rung: S7
Predecessor: S6 GREEN (`PX00 Contract Validation #611`)
Knowledge profile: PUBLIC-safe SYNTHETIC/TEST ONLY
Live executor: FORBIDDEN in this scenario

## Claim boundary

This scenario proves only bounded capability-based team assembly and governed handoff selection over synthetic fixtures. It does **not** prove professional expertise, VERIFIED professional knowledge, production readiness, live-provider execution, or autonomous hiring/staffing.

## One new complexity over S6

S6 proved dependent tasks plus explicit replanning. S7 adds exactly one new complexity: executors are selected from an explicit synthetic capability registry according to task requirements instead of being hard-coded by identity.

## Synthetic capability registry

- `AGENT-ANALYST-01`: capabilities `{scope_analysis, dependency_mapping}`; authority `D0`.
- `AGENT-BUILDER-01`: capabilities `{bounded_build, lineage_emit}`; authority `D0`.
- `AGENT-VERIFY-01`: capabilities `{independent_verification, acceptance_check}`; authority `D0`; independence class `VERIFY`.
- `AGENT-SOCRATES-01`: capabilities `{socratic_challenge, assumption_attack}`; authority `D0`; independence class `SOCRATES`.
- `AGENT-GENERALIST-01`: capabilities `{scope_analysis, bounded_build}`; authority `D0`; intentionally lacks independent verification and Socrates capabilities.

Registry entries are test fixtures, not claims about real people, models, vendors, or professional competence.

## Task requirements

- `T1 ANALYZE` requires `{scope_analysis, dependency_mapping}`.
- `T2 BUILD` requires `{bounded_build, lineage_emit}` and depends on T1 PASS.
- `T3 VERIFY` requires `{independent_verification, acceptance_check}`, depends on T2, and executor must differ from T2 executor.
- `T4 SOCRATES` requires `{socratic_challenge, assumption_attack}`, depends on T3 PASS, and executor must differ from T2 and T3 executors.
- `T5 PACKAGE` depends on T4 PASS.

Expected assembly:
`T1→AGENT-ANALYST-01`, `T2→AGENT-BUILDER-01`, `T3→AGENT-VERIFY-01`, `T4→AGENT-SOCRATES-01`.

## Expected outcome

1. Assembly is derived from declared task requirements and registry capabilities.
2. Every assignment records required capabilities, selected executor, matched capabilities, authority boundary, predecessor evidence and selection reason.
3. T1 PASS unlocks T2; T2 emits the bounded synthetic result and lineage.
4. T3 independently verifies the exact current T2 artifact.
5. T4 independently challenges the accepted assumptions and returns PASS for this fixture.
6. T5 packages only after T3 and T4 PASS.
7. Replay reconstructs requirements → candidate evaluation → assignments → artifacts → verification → Socrates → package.
8. Rejected candidates and rejected assignment attempts remain evidence.

Scenario acceptance: PASS only if all eight conditions hold without weakening any predecessor gate.

## Failure conditions

FAIL/BLOCK if any task is assigned to an executor missing a required capability; capability requirements are changed after candidate evaluation merely to obtain a match; an executor self-verifies its own build; Socrates independence collapses; stale capability declarations or stale verification are reused after an assignment/artifact change; rejected candidates disappear; authority grows implicitly through assignment; synthetic capability declarations are presented as VERIFIED professional competence; or an external/live executor is invoked.

## Materiality

`D0` for the bounded synthetic fixture and deterministic team assembly. Any change to project scope, acceptance, material cost/risk/time, external execution, credential use, professional assertion, or authority escalation is outside S7 and requires the applicable higher authority/gate. Capability matching never grants authority by itself.

## Authority boundary

The assembler may select only among declared eligible synthetic executors and only for D0 tasks. It may not invent capabilities, infer professional qualifications, weaken independence, grant D1/D2 authority, authorize external execution, or convert a capability match into a professional-knowledge claim.

## Evidence required

Preserve append-only:
- scenario input and capability registry version/digest;
- task requirement set/digest;
- candidate evaluation for each task, including rejected candidates and reasons;
- assignment records and authority boundary;
- T1/T2 artifacts and lineage;
- T3 verification evidence bound to current T2 artifact;
- T4 Socrates evidence bound to accepted chain;
- T5 package evidence;
- negative/rejected attempts;
- replay ordering and final acceptance verdict;
- PX00 Contract Validation result for this scenario generation.

## Negative tests

1. Assign `AGENT-GENERALIST-01` to T3 → REJECT: missing `{independent_verification, acceptance_check}`.
2. Assign `AGENT-BUILDER-01` to T3 after it produced T2 → REJECT: independence violation even if a capability is later claimed.
3. Add `independent_verification` to an executor after candidate evaluation solely to force a match → REJECT: post-hoc capability mutation.
4. Assign T4 to T3 verifier → REJECT: Socrates independence collapse.
5. Remove a rejected candidate from evidence → REJECT: incomplete replay.
6. Start T2 before T1 PASS → REJECT: predecessor gate bypass.
7. Reuse T3 PASS after replacing/revising T2 artifact → REJECT: stale verification.
8. Let capability match implicitly grant D2 decision authority → REJECT: authority escalation.
9. Select an executor using identity/preference while a required capability is absent → REJECT: non-capability assignment.
10. Promote synthetic registry claims to VERIFIED professional competence → REJECT.
11. Invoke Gemini or another live/external executor in S7 → REJECT.
12. Package before T4 PASS → REJECT.

Rejected/failed evidence is retained; gates are not weakened to obtain PASS.

## Acceptance verdict

`S7 PASS` is permitted only when predecessor S6 is green, capability matching is explicit and replayable, independence and authority boundaries remain fail-closed, negative evidence is preserved, and PX00 Contract Validation for the S7 generation is green.

Until that CI result is green, status is `S7 VERIFY`; S8 remains blocked.

## Architectural impact

No Tree_F/ADR update is justified by this bounded scenario alone. Capability matching is exercised as a product-level selection contract; it becomes an architectural primitive only if later implementation requires a durable cross-system schema/protocol decision.