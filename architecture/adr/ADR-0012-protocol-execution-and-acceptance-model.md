# ADR-0012 — Governed Protocol Execution and Acceptance Model

**Status:** ACCEPTED FOR BASELINE 0.1 VALIDATION  
**Date:** 2026-08-11

## Context

PX00 already defines canonical objects, governed roles, authority/autonomy, event/provenance, knowledge admission and decision evaluation. Runtime must remain blocked until the system also defines how governed work executes step-by-step and how a result becomes accepted.

Without a protocol execution contract, roles can silently skip gates, loop indefinitely, retry unsafe actions or redefine workflow semantics. Without an acceptance model, “looks correct” can be mistaken for evidence-backed PASS.

## Decision

PX00 adopts two linked controls:

1. `protocols/PROTOCOL_EXECUTION_CONTRACT.md` — versioned, bounded, authority-gated execution of `PROTO-*` work.
2. `assurance/ACCEPTANCE_MODEL.md` — evidence-backed acceptance states and criteria for contracts, schemas, roles, protocols, runs and future releases.

Supporting schema contracts:

- `schemas/PROTOCOL_DEFINITION.yaml`
- `schemas/RUN_RECORD.yaml`
- `schemas/ACCEPTANCE_RECORD.yaml`

## Protocol invariants

- material required steps cannot be silently skipped;
- branches and loops are explicit;
- autonomous loops are bounded;
- authority is checked fail-closed;
- protocol permission cannot expand external authority;
- retry identity and material failed attempts are preserved;
- non-idempotent retries require duplicate-prevention/reconciliation semantics;
- checkpoints do not advance before the corresponding material output/evidence is durably saved unless a domain-specific contract proves another ordering safe;
- terminal states remain explicit.

## Acceptance invariants

- no material PASS without declared criteria and linked evidence;
- blocking failures prevent PASS;
- missing evidence is not success;
- `PASS_WITH_ACTIONS` records remaining actions;
- a completed run may still fail acceptance;
- comparable A/B variants preserve evidence for both variants;
- implementation does not silently redefine acceptance criteria after the fact.

## Dependencies

No runtime library, workflow engine, event broker, database, test framework or schema validator is selected by this ADR.

This is deliberate: implementation technology remains deferred until pilot Role Packages demonstrate the minimum runtime requirements.

## Security

This decision reduces risks from privilege bypass, infinite loops, unsafe retries, lost evidence, silent control bypass, false PASS and post-hoc acceptance criteria.

Runtime security must later prove non-bypassable gates, safe cancellation, retry/idempotency behavior, event/output durability, evidence integrity, protected test data handling and separation of duties where required.

## Consequences

Positive:

- the first pilot roles can execute under one shared production contract;
- test design can precede implementation where useful;
- failures/retries become measurable production evidence;
- A/B experiments can compare implementations without erasing losing variants;
- runtime technology can now be selected from observed requirements instead of speculation.

Cost:

- material protocols require explicit bounds, gates and acceptance criteria.

This cost is accepted as necessary governance, while trivial internal operations remain outside permanent material evidence unless promoted by risk/requirement.

## Next gate

Instantiate the first two governed Role Package pilots — `Analyst` and `Socrates/Critical Reviewer` — with their knowledge manifests, protocols, authority, I/O contracts, evaluation rubrics and acceptance fixtures. Use those pilots to validate Baseline 0.1 before opening the first minimal runtime implementation.
