# ADR-0013 — First Governed Role Pilots: Analyst and Critical Reviewer

**Status:** ACCEPTED FOR PILOT VALIDATION  
**Date:** 2026-08-11

## Context

PX00 Baseline 0.1 now defines canonical objects, Role Package structure, authority/autonomy, event/trace/provenance, knowledge admission, decision evaluation, protocol execution and acceptance. The next gate is to prove these contracts can describe real professional roles without adding ad-hoc object types, hidden privileges or framework-specific assumptions.

## Decision

Instantiate two non-production pilot Role Packages:

- `ROLE-0201` — canonical name `analyst`, display name `Analyst`;
- `ROLE-0202` — canonical name `critical_reviewer`, initial display name `Socrates`.

Both pilots are limited to autonomy `A1` and remain `pilot_not_tested` until declared acceptance fixtures are executed with evidence.

The Analyst converts governed evidence into findings, knowledge candidates, open questions and decision recommendations. It cannot self-admit knowledge or execute material external side effects.

The Critical Reviewer challenges findings, knowledge candidates and decision proposals. It cannot directly mutate accepted knowledge, approve the reviewed decision or manufacture counter-evidence. Material dissent is preserved.

## Protocols

- `PROTO-0201` governs analytical classification, contradiction/gap detection, findings, proposals and evaluation.
- `PROTO-0202` governs evidence challenge, assumptions, alternatives, falsifiability, source independence, causal discipline, scope/temporal review and dissent.

Pilot loops for requesting additional evidence are bounded to three cycles. This is a pilot safety bound, not a permanent universal constant; later evidence may justify a different protocol version.

## Canonical-model restraint

No new canonical object type such as `CriticalReview` is introduced. Critical review is represented with existing `EVAL-*` and `FIND-*` objects. A follow-up evidence request is represented as a proposed `TASK-*`.

This decision follows the minimum-sufficient vocabulary rule.

## Acceptance

`assurance/fixtures/PILOT-0001_ANALYST_SOCRATES_ACCEPTANCE.yaml` defines blocking cases for authority, knowledge admission, provenance, dissent, missing evidence, trace separation and brand-independent canonical identity.

The pilots SHALL NOT be treated as production roles while the fixture state is `NOT_TESTED`, `FAIL` or `BLOCKED`.

## Security conclusion

`PASS_WITH_ACTIONS` at contract level.

Positive controls now include fail-closed A1 authority, read-only evidence access intent, no self-admission of knowledge, no direct knowledge mutation by reviewer, protected-data inheritance, cross-customer mixing prohibition and explicit trace/provenance requirements.

Runtime validation remains required for actual tool mediation, access-control enforcement, tenant isolation, event integrity, prompt-injection resistance, retrieval poisoning defenses and provider/data leakage controls.

## Consequences

The architecture can now be tested as a small production chain:

```text
TASK
→ ROLE-0201 / PROTO-0201
→ FIND / proposals / EVAL
→ ROLE-0202 / PROTO-0202
→ review EVAL / dissent FIND / follow-up TASK proposal
→ acceptance evidence
```

Runtime code remains blocked until these pilot packages and acceptance fixtures are reviewed/executed sufficiently to justify opening the implementation gate.
