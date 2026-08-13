# S6 — dependent tasks + replanning

Status: VERIFY
Date: 2026-08-14
Predecessor gate: S5 GREEN (`PX00 Contract Validation` #610 SUCCESS)
Materiality: D1 execution; D2 if scope/cost/risk/time acceptance is changed
Knowledge profile: SYNTHETIC / TEST ONLY — MUST NOT be promoted to VERIFIED professional knowledge.
External execution: NONE. Gemini/live executors are out of scope.

## One-step complexity increment

S6 adds exactly one capability over S5: execute a small project of dependent tasks and replan after a deterministic failed attempt without weakening acceptance or deleting failed evidence.

## Synthetic project pack

Goal fixture: package exactly `{ITEM-A, ITEM-B, ITEM-C}`.

Dependency graph:
- T1 SPEC: freeze exact set `{A,B,C}` and acceptance contract.
- T2 BUILD: depends on T1 PASS.
- T3 VERIFY: depends on a fresh T2 attempt; independently compares output to T1.
- T4 PACKAGE: depends on T3 PASS.

Deterministic first attempt:
- T2-A1 produces `{A,C}`.
- T3-A1 MUST record FAIL because `B` is missing.
- failed T2-A1 and T3-A1 remain append-only evidence.
- explicit replan keeps the T1 acceptance contract unchanged and creates T2-A2.
- T2-A2 produces `{A,B,C}`.
- fresh T3-A2 verifies T2-A2 and MUST PASS.
- only then may T4 package the accepted result.

## Expected outcome

1. Dependencies prevent T2 before T1 PASS, T3 before a T2 attempt, and T4 before T3 PASS.
2. First build attempt fails verification and is preserved.
3. Replanning records reason, affected tasks and lineage; it does not rewrite history.
4. Replan creates a fresh build attempt rather than mutating T2-A1.
5. Fresh verifier evidence is required for T2-A2; T3-A1 cannot be reused.
6. T4 contains exactly `{A,B,C}` and traces through T3-A2 -> T2-A2 -> T1.
7. Any material change to scope/cost/risk/time requires D2 authority rather than being hidden inside replanning.

## Failure conditions

FAIL/REWORK/BLOCK if any occurs:
- a dependent task starts before its predecessor gate;
- T3-A1 missing-item failure is ignored and T4 proceeds;
- T2-A1 or T3-A1 is overwritten/deleted;
- T2-A1 is edited in place instead of creating T2-A2;
- stale T3-A1 is reused to accept T2-A2;
- replanning weakens exact-set acceptance or silently removes ITEM-B;
- replanning changes material scope/cost/risk/time without D2 authority;
- attempt identity or lineage is lost;
- verifier is not independent;
- rejected/failed evidence disappears from replay;
- synthetic fixtures are represented as VERIFIED professional knowledge;
- external/live execution occurs.

## Authority boundary

- PLANNER may sequence/resequence tasks within the frozen contract; cannot weaken acceptance.
- PRODUCER may execute T2 attempts; cannot self-verify or rewrite failed attempts.
- VERIFIER independently evaluates each fresh attempt; cannot repair producer output.
- D2 AUTHORITY is required for material scope/cost/risk/time contract changes.
- PACKAGE may run only after fresh verification PASS.
- No role may promote this synthetic pack to VERIFIED professional knowledge.

## Evidence required

- immutable T1 contract and dependency graph;
- T2-A1 `{A,C}` artifact;
- T3-A1 FAIL artifact identifying missing B;
- explicit replan artifact with reason and affected-task lineage;
- fresh T2-A2 `{A,B,C}` artifact;
- fresh independent T3-A2 PASS artifact;
- T4 package artifact linked to accepted attempt;
- append-only failed/rejected evidence sufficient for replay;
- PX00 Contract Validation GREEN for repository state containing S6.

## Negative test pack

N1 start T2 before T1 PASS -> FAIL dependency gate.
N2 start T4 after T3-A1 FAIL -> FAIL gate bypass.
N3 delete T2-A1 after replan -> FAIL evidence loss.
N4 mutate T2-A1 from `{A,C}` to `{A,B,C}` -> FAIL history rewrite.
N5 reuse T3-A1 as verification for T2-A2 -> FAIL stale evidence.
N6 replan acceptance from `{A,B,C}` to `{A,C}` -> FAIL gate weakening.
N7 change material scope/cost/risk/time during replan without D2 -> FAIL authority violation.
N8 omit attempt IDs/lineage -> FAIL non-replayable execution.
N9 producer performs T3-A2 -> FAIL independence violation.
N10 package `{A,B,C,D}` -> FAIL exact-set acceptance.
N11 label fixtures VERIFIED professional requirements -> FAIL provenance violation.
N12 invoke Gemini/network/live executor -> FAIL for this scenario profile.

## Acceptance

S6 is GREEN only when the deterministic failed attempt forces an explicit append-only replan, the second attempt receives fresh independent verification, dependency gates remain fail-closed, material authority is preserved, replay contains both failed and accepted paths, and PX00 Contract Validation is green.

Until then S7 is BLOCKED.
