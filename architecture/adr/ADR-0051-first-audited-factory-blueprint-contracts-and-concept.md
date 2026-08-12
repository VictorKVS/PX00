# ADR-0051 — First Audited Factory Blueprint Contracts and Concept

Date: 2026-08-12
Status: accepted

## Context
Factory Builder had a charter, specialist roles and a synthesis protocol, but had not yet proven that it could turn an authorized need into a factory design and then accept criticism without weakening its own maturity rules.

## Decision
Adopt three explicit Factory Builder design objects:
- `FACTORY_REQUIREMENT` for an authorized qualified need;
- `CAPABILITY` for technology-neutral outcome capabilities;
- `FACTORY_BLUEPRINT` for an immutable reviewable factory design before FATHER operation.

Exercise those objects on `FFB-REQ-0001 Agent R&D Factory` and require Socrates, ARGUS and a declared acceptance matrix before any summit/maturity claim.

## First exercise result
Candidate `FFB-BP-0001 v0.1` was rejected for M1 because it:
- conflicted with the S4 maturity gate through unresolved `RISK-0002`;
- duplicated FATHER management through a local R&D Manager;
- referenced undefined operational protocols;
- lacked sufficient measurable acceptance and runtime independence evidence.

The candidate remains preserved. New revision `FFB-BP-0001-V2 v0.2` resolves the concept-level management/reference issues and intentionally targets only `M0_CONCEPT`.

`FFB-ACC-0001` makes M0 and M1 acceptance separate evidence gates. Socrates and ARGUS independently accept v0.2 only for M0, while M1 remains blocked.

## Invariants
- failed blueprint history is never rewritten to manufacture a clean record;
- maturity is evidence-gated, not author-declared;
- unresolved S4 cannot be bypassed by architectural enthusiasm or majority vote;
- Factory Builder designs; FATHER manages/operates;
- local coordination cannot become a second FATHER;
- undefined contracts are future requirements, not executable dependencies;
- role and capability identities remain independent of agents/models/vendors/devices;
- concept acceptance grants no runtime authority.

## Consequences
Factory Builder now has its first demonstrated learning loop:

`AUTHORIZED NEED → CAPABILITIES → BLUEPRINT v0.1 → SOCRATES/ARGUS FAIL → REWORK → BLUEPRINT v0.2 → INDEPENDENT RE-REVIEW → M0 PASS_WITH_ACTIONS`.

The next architectural gate is operational M1 evidence: complete `PROTO-RD-*` contracts, runtime producer/reviewer separation, adversarial trust controls for `RISK-0002`, reproducible bounded execution and executor snapshotting.
