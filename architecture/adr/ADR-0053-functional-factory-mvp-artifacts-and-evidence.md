# ADR-0053 — Functional Factory MVP artifacts and evidence

Date: 2026-08-12
Status: ACCEPTED FOR M1 REFERENCE MVP
Project: PROJECT-FFB-0001

## Context
The initial M1 control-flow harness proved that the Agent R&D Factory could enforce stage order and critical gates, but a state machine alone did not prove useful factory work. Each stage needed durable semantics: a concrete output, explicit producer, evidence lineage and a verifiable relation between review evidence and runtime state.

## Decision
The Factory Builder functional reference MVP shall require a typed immutable artifact for every workflow stage.

For the M1 reference MVP:
- each stage has one declared artifact type;
- artifact IDs are append-only;
- payloads are canonicalized and SHA-256 content-addressed;
- every non-initial artifact references the immediately preceding artifact;
- a stage cannot pass without a fresh artifact;
- verification artifacts must be produced by the pinned verifier assignment;
- Socrates artifacts must be produced by an assignment independent from producer and verifier;
- Security, Verification and Socrates declared verdicts must be consistent with the runtime outcome;
- successful governed delivery is terminal;
- artifact/evidence lineage grants no runtime authority.

The first functional reference case is a bounded deterministic engineering problem: design and verify a stable idempotency identity for retried synthetic delivery. The selected prototype hashes canonical JSON `[run_id, operation, target]`; the system explicitly does not claim that this creates exactly-once execution.

## Audit-driven corrections
During the functional audit cycle two defects were found and corrected before acceptance:
1. delimiter-based concatenation could ambiguously encode different idempotency tuples; canonical JSON tuple encoding replaced it;
2. assurance evidence could declare `FAIL` while runtime advanced with `PASS`; gated artifact verdicts are now checked against runtime outcomes.

## Maturity decision
`M1 FUNCTIONAL REFERENCE MVP — PASS_WITH_RESTRICTIONS` is accepted for synthetic/bounded execution only.

This decision does not authorize claims of:
- production readiness;
- live autonomous-agent competence;
- arbitrary external-content safety;
- material external tool execution;
- durable or recoverable operation;
- exactly-once execution.

## Risk consequences
- `RISK-0002` remains isolated, not closed;
- `RISK-0003` remains open because the reference stores are in-memory;
- `RISK-0004` remains open because durable transactional semantics are not implemented;
- `RISK-0009` is registered because current SHA-256 covers the payload, not the complete provenance envelope.

`RISK-0009` must be remediated before persistent evidence maturity by hashing a canonical envelope containing artifact/run/stage/type/producer/lineage metadata plus payload digest and verifying it across persistence/replay.

## Consequences
The project now changes mode from architecture expansion to evidence-driven iteration. The same artifact contract should be exercised on multiple bounded problems before introducing broader execution technology. A live executor, when introduced, should replace only one deterministic stage at a time while preserving the existing gates and evidence contracts.
