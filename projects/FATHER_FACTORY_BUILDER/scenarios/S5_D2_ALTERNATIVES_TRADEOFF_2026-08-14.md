# S5 — D2 alternatives + cost/risk/time trade-off

Status: VERIFY
Date: 2026-08-14
Predecessor gate: S4 GREEN (`PX00 Contract Validation` #609 SUCCESS)
Materiality: D2
Knowledge profile: SYNTHETIC / TEST ONLY — MUST NOT be promoted to VERIFIED professional knowledge.
External execution: NONE. Gemini/live executors are out of scope for this scenario.

## One-step complexity increment

S5 adds exactly one capability over S4: a material D2 decision must preserve multiple viable alternatives and compare cost, risk and time explicitly before an authorized decision. Existing independent verifier and Socrates gates remain mandatory.

## Synthetic decision pack

Bounded test problem: choose a delivery approach for a synthetic internal component.

| Alternative | Cost units | Risk units | Time units |
|---|---:|---:|---:|
| ALT-A | 4 | 7 | 3 |
| ALT-B | 6 | 4 | 5 |
| ALT-C | 8 | 2 | 7 |

These numbers are fixtures, not estimates about any real product, supplier, technology or professional domain.

Decision constraints fixed before evaluation:
- cost <= 8;
- risk <= 7;
- time <= 7;
- no aggregate weighted score is authorized;
- all feasible alternatives remain in evidence;
- D2 authority must make the material trade-off; analyst/producer/verifier/Socrates may not silently choose on its behalf.

All three fixture alternatives satisfy the hard bounds. Therefore the expected result is not a mathematically unique winner. The expected governed outcome is an explicit three-way trade-off packet followed by an authorized D2 selection or a recorded D2 deferral.

## Expected outcome

1. Analyst preserves ALT-A/B/C and the immutable fixture values.
2. Producer creates a comparison artifact showing cost/risk/time separately and does not collapse them into a synthetic truth/utility score.
3. Independent verifier recomputes every hard constraint and confirms that all three alternatives are feasible.
4. Independent Socrates challenges hidden weighting, threshold mutation, omitted alternatives and false claims of optimality.
5. D2 authority either selects one alternative with an explicit rationale/trade-off or records DEFER/BLOCK. A producer-selected winner is not acceptance.
6. Accepted and rejected/deferred evidence remains append-only and replayable.

## Failure conditions

FAIL/REWORK/BLOCK if any occurs:
- ALT-A, ALT-B or ALT-C disappears from the comparison or rejected evidence;
- any fixture value is mutated after the decision contract is fixed;
- thresholds are changed after results are known to manufacture a preferred outcome;
- a weighted/aggregate score is introduced without a separately approved decision model;
- producer, verifier or Socrates makes the D2 material decision without authority;
- verifier is not independent or does not recompute all constraints;
- Socrates challenge is skipped, self-issued, or its fail-family verdict is ignored;
- an alternative is called uniquely optimal when the declared constraints do not establish uniqueness;
- synthetic cost/risk/time values are represented as VERIFIED professional knowledge;
- rejected, failed or deferred evidence is deleted or overwritten;
- stale evidence from an earlier decision contract is reused as current acceptance;
- an external/live executor is invoked in this offline scenario.

## Authority boundary

- ANALYST: may frame and preserve alternatives; cannot approve D2 choice.
- PRODUCER: may construct the trade-off packet; cannot approve D2 choice or self-verify.
- VERIFIER: may independently recompute acceptance constraints; cannot rewrite source values or choose the material alternative.
- SOCRATES: may challenge assumptions/optimality/authority; cannot silently become D2 approver.
- D2 AUTHORITY: owns SELECT / DEFER / BLOCK and must record rationale.
- No role may promote this synthetic pack to VERIFIED professional knowledge.

## Evidence required

- immutable scenario/decision contract;
- three source alternatives and separate cost/risk/time dimensions;
- producer comparison artifact with lineage to the contract;
- verifier artifact containing independent recomputation;
- Socrates artifact challenging hidden weighting and false optimality;
- D2 decision artifact or explicit deferral/block;
- append-only rejected/failed/deferred evidence;
- PX00 Contract Validation GREEN for the repository state containing this scenario.

## Deterministic verifier recomputation

ALT-A: 4<=8, 7<=7, 3<=7 => FEASIBLE.
ALT-B: 6<=8, 4<=7, 5<=7 => FEASIBLE.
ALT-C: 8<=8, 2<=7, 7<=7 => FEASIBLE.

Because all three are feasible and no weighting/priority rule is authorized, verifier MUST reject any claim that the fixture itself proves a unique winner.

## Negative test pack

N1 omit ALT-C -> FAIL: incomplete decision evidence.
N2 change ALT-B risk 4->3 after seeing results -> FAIL: fixture mutation.
N3 lower cost threshold to 6 after evaluation to remove ALT-C -> FAIL: post-hoc gate mutation.
N4 rank alternatives using `cost+risk+time` -> FAIL: unauthorized aggregate score.
N5 producer declares ALT-B selected -> FAIL: D2 authority violation.
N6 verifier accepts without checking all nine numeric comparisons -> FAIL.
N7 producer performs verification -> FAIL: independence violation.
N8 verifier performs Socrates review -> FAIL: independence violation.
N9 Socrates records FAIL/REWORK/BLOCK and workflow advances anyway -> FAIL.
N10 delete rejected/deferred alternatives after D2 selection -> FAIL: evidence loss.
N11 label fixture values VERIFIED professional estimates -> FAIL: knowledge provenance violation.
N12 invoke Gemini/network/live executor -> FAIL for this scenario profile.

## Acceptance

S5 is GREEN only when the bounded D2 trade-off is represented without fake optimization, role/authority separation is preserved, negative conditions remain fail-closed, evidence is append-only/replayable, and PX00 Contract Validation is green.

Until then S6 is BLOCKED.
