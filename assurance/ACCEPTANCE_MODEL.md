# PX00 Acceptance Model — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1  
**Scope:** governance, contracts, role packages, runs and releases.

## Purpose

PX00 must distinguish an assertion from a verified result. A component, role, protocol, decision, run or release is not accepted because an author, reviewer or LLM says it looks correct. Acceptance requires predefined criteria and evidence.

The model follows one rule:

> No material PASS without declared acceptance criteria and linked evidence.

## Acceptance states

- `NOT_TESTED` — criteria/evidence have not yet been executed or collected.
- `PASS` — all blocking criteria satisfied with evidence.
- `PASS_WITH_ACTIONS` — blocking criteria satisfied; non-blocking actions remain.
- `FAIL` — one or more blocking criteria failed.
- `BLOCKED` — acceptance cannot be completed because required input, authority, environment or evidence is unavailable.

`PASS_WITH_ACTIONS` must list owners/conditions for unresolved actions. It is not a synonym for “probably fine”.

## Acceptance layers

### 1. Contract acceptance

Used for architecture/governance contracts.

Minimum evidence:

- purpose and scope are explicit;
- terms map to canonical objects;
- contradictions with accepted contracts are resolved or explicitly recorded;
- security/compliance consequences are stated;
- verification method exists;
- no unjustified runtime dependency is introduced.

### 2. Schema acceptance

Minimum evidence:

- required/optional fields are explicit;
- lifecycle/identity invariants are represented;
- invalid/missing critical fields have defined failure behavior;
- secrets/protected-data policy is represented where applicable;
- round-trip/validation fixtures exist once runtime validation begins.

### 3. Role Package acceptance

Minimum evidence:

- identity/version;
- mission and boundaries;
- authority/prohibitions;
- knowledge manifest;
- protocol manifest;
- I/O contracts;
- evaluation rubric;
- trace requirements;
- security review;
- benchmark/regression cases appropriate to the role.

A role cannot perform material production work while its package is `NOT_TESTED` or `FAIL`.

### 4. Protocol acceptance

Minimum evidence:

- bounded execution;
- explicit authority gates;
- no silent required-step skipping;
- declared retry/idempotency behavior;
- failure/cancellation/escalation paths;
- output and completion criteria;
- event/provenance requirements;
- tests for blocking failure conditions.

### 5. Run acceptance

A run can be technically completed yet fail acceptance.

Minimum evidence where applicable:

- correct task/protocol/role versions;
- authority decisions present;
- material inputs/outputs preserved;
- blocking protocol steps completed;
- failures/retries recorded;
- expected output contract satisfied;
- security/compliance gates passed;
- evaluation completed when required.

### 6. Release/distribution acceptance

Minimum evidence later includes:

- source/build identity;
- tests;
- security checks;
- dependency/SBOM evidence;
- license/attribution evidence;
- configuration/profile identity;
- known risks/exceptions;
- approval/signature requirements;
- reproducible provenance from source to distribution.

## Blocking vs non-blocking criteria

Every acceptance case identifies criteria as:

- `BLOCKING` — failure prevents PASS;
- `NON_BLOCKING` — failure creates an action/risk but may permit PASS_WITH_ACTIONS.

Security, legal/regulatory, authority and data-protection constraints default to blocking when the applicable contract says the action is prohibited or approval is mandatory.

## Test design before implementation

For material runtime work, acceptance tests SHOULD be designed before implementation whenever the expected behavior can be stated independently of the implementation.

This supports:

```text
Requirement
→ Acceptance Criteria
→ Test/Fixture
→ Implementation
→ Evidence
→ Acceptance
```

The purpose is not test-first dogma. The purpose is to stop implementation from silently redefining success after the fact.

## Comparative and A/B evaluation

Alternative implementations use the same acceptance criteria where they claim to solve the same requirement.

Variant evidence is preserved:

```text
A → TEST/EVAL → outcome
B → TEST/EVAL → outcome
            ↓
        DECISION
```

A losing variant is not deleted from the development corpus if it produced material learning.

## Assurance case

Critical acceptance may be summarized as:

```text
CLAIM
  ↓
ARGUMENT
  ↓
EVIDENCE
```

This is an explanation layer over canonical objects, not a substitute for them.

## Baseline 0.1 exit gate

Application runtime remains blocked until at minimum:

1. canonical object model exists;
2. Role Package contract exists;
3. authority/autonomy contract exists;
4. event/trace/provenance contract exists;
5. knowledge admission contract exists;
6. decision evaluation contract exists;
7. protocol execution contract exists;
8. acceptance model exists;
9. first pilot Role Packages and protocols are reviewable;
10. acceptance fixtures prove the contracts can be instantiated without ad-hoc semantics.

Opening runtime code does not mean production approval. It only means the contract-first architecture gate has been crossed.

## Security conclusion

The acceptance model reduces false PASS, silent waiver of controls, post-hoc success criteria and unauditable production claims.

Future runtime must additionally provide trustworthy test execution, evidence integrity, separation of duties where required, protected test data handling and non-bypassable blocking gates.

## Current disposition

`KEEP / VALIDATE WITH PILOT ROLES AND PROTOCOLS`.
