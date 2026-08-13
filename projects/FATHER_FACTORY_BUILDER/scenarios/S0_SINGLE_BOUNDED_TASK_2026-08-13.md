# FATHER Product Scenario S0 — Single Bounded Task

Date: 2026-08-13
Scenario: S0
Status: PASS
Knowledge mode: SYNTHETIC_TEST_PACK — NOT VERIFIED PROFESSIONAL KNOWLEDGE

## Purpose
Prove the lowest product-production rung before adding verifier/rework/Socrates complexity: one bounded task enters with explicit limits and produces one deterministic bounded result without external side effects.

## Scenario contract

- Goal: normalize a synthetic three-item release note into a deterministic delivery summary.
- Input: PUBLIC synthetic-safe fixture only.
- Expected outcome: exactly one bounded result containing the three supplied item identifiers in deterministic order and no invented professional claims.
- Failure conditions:
  - output adds an item absent from the fixture;
  - output drops a supplied item;
  - output crosses the declared PUBLIC/no-network boundary;
  - output claims VERIFIED professional knowledge;
  - task expands into a project, multi-role workflow, external executor, or side effect.
- Materiality: D0 — local deterministic transformation with no regulated/safety/financial/external effect.
- Authority boundary: A0/A1-equivalent bounded local computation; no network, credentials, tools with side effects, production data, or autonomous material action.
- Evidence required: immutable scenario contract, deterministic expected result, negative cases, repository CI.

## Synthetic fixture

Input items:
1. `ITEM-A` — validator documentation updated.
2. `ITEM-B` — synthetic fixture added.
3. `ITEM-C` — negative test added.

Expected deterministic product:
`ITEM-A | ITEM-B | ITEM-C`

No statement above is admitted as professional domain knowledge. The fixture exists only to exercise the production mechanism.

## Execution result

Observed bounded product:
`ITEM-A | ITEM-B | ITEM-C`

Verdict: PASS.

The scenario intentionally does **not** invoke the full `AgentRdFactoryMvp` chain, because that chain already includes later-rung verifier and Socrates semantics. Using it here would falsely claim S0 isolation. S0 proves only the atomic production premise; S1 will add an independent verifier explicitly.

## Negative evidence

The following are defined as rejection cases for this rung:
- extra `ITEM-D` => FAIL: invented output;
- missing `ITEM-B` => FAIL: incomplete output;
- any network/provider call => FAIL: authority expansion;
- any `VERIFIED` domain claim => FAIL: synthetic-pack boundary violation.

These rejection conditions are retained even though the positive fixture passes.

## What is proven

A single bounded product task can be specified with expected outcome, failure conditions, D0 materiality, authority boundary and evidence before execution, and can produce a deterministic result without depending on unfinished professional KB or live providers.

## What is not proven

- independent verification;
- verifier-forced rework;
- Socrates challenge;
- multi-role handoff;
- D2 alternatives/cost/risk/time trade-off;
- project replanning;
- capability-based team assembly;
- executor replacement/failure recovery;
- live external executor;
- closed project lifecycle.

Those remain later scenario rungs and must not be inferred from S0 PASS.

## Next gate

S1 — run a bounded task with an explicitly independent verifier and preserve both producer output and verifier verdict.