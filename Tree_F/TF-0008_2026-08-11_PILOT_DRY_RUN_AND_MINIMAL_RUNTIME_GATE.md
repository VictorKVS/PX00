# TF-0008 — Pilot Dry Run and Minimal Runtime Gate

**Date:** 2026-08-11  
**Status:** ACCEPTED  
**Decision:** KEEP / OPEN MINIMAL VALIDATION RUNTIME  
**Trigger:** `PILOT-0001` contract dry-run completed with `PASS_WITH_ACTIONS`.

## Structural delta

Added:

```text
assurance/
├── runs/
│   └── PILOT-0001_DRY_RUN_2026-08-11.md
└── records/
    └── ACCEPTANCE-PILOT-0001.yaml

architecture/adr/
└── ADR-0014-pilot-dry-run-and-minimal-runtime-opening.md
```

Updated:

```text
assurance/fixtures/PILOT-0001_ANALYST_SOCRATES_ACCEPTANCE.yaml
```

The append-only history `TF-0001..TF-0007` remains unchanged.

## Why this generation exists

The previous generation defined the first two Role Packages and their protocols. This generation answers the next manufacturing question: can the declared chain survive representative cases without hidden semantics before code is written?

The dry-run covered:

1. supported bounded claim;
2. unsupported LLM statement;
3. contradictory evidence;
4. unauthorized external side effect;
5. equal payload with distinct provenance.

All declared blocking contract rules passed at manual contract level. Remaining implementation/security actions prevent unconditional production PASS.

## File dossiers

### `assurance/runs/PILOT-0001_DRY_RUN_2026-08-11.md`

**Purpose:** Human-reviewable execution evidence for the first contract-level pilot.  
**Inputs:** Role Packages, pilot protocols and PILOT-0001 fixture.  
**Outputs:** Case-by-case evidence and blocking-criteria matrix.  
**Algorithm:** deterministic scenario walkthrough against declared authority, knowledge, provenance and review rules.  
**Libraries:** NONE.  
**DevOps:** no executable test runner yet.  
**Security:** synthetic/public-safe objects only; no network or side effects.  
**Verification:** compare cases against fixture expected outcomes and role/protocol contracts.  
**Decision:** KEEP.

### `assurance/records/ACCEPTANCE-PILOT-0001.yaml`

**Purpose:** Machine-readable acceptance summary separated from narrative evidence.  
**Inputs:** dry-run evidence and declared blocking criteria.  
**Outputs:** `PASS_WITH_ACTIONS`, remaining action list and allowed next scope.  
**Algorithm:** all blocking contract criteria must pass; unresolved runtime controls are recorded as actions rather than hidden.  
**Libraries:** NONE.  
**Security:** explicitly forbids treating this record as production approval.  
**Verification:** compare with dry-run matrix and Acceptance Model.  
**Decision:** KEEP.

### Updated `PILOT-0001` fixture

**Purpose:** Bind test definition to its execution evidence while preserving original acceptance criteria.  
**Change:** status moves from `NOT_TESTED` to `PASS_WITH_ACTIONS`; execution/evidence references and limitations added.  
**Security:** contract PASS does not imply runtime enforcement.  
**Decision:** KEEP.

### `ADR-0014-pilot-dry-run-and-minimal-runtime-opening.md`

**Purpose:** Formally open only the minimum implementation scope justified by evidence.  
**Allowed:** local validator/fixture runner and synthetic tests.  
**Prohibited:** production agents, customer data, network side effects, A2+ autonomous actions, large infrastructure and unsupported assurance claims.  
**Decision:** KEEP.

## Production-chain consequence

Before:

```text
Contracts
→ Pilot role definitions
→ Acceptance fixture
```

Now:

```text
Contracts
→ Pilot role definitions
→ Acceptance fixture
→ Manual dry-run evidence
→ Acceptance record
→ narrow implementation authorization
```

The next generation may add code, but only to make these existing rules executable.

## Algorithms / technology

No runtime algorithm or third-party library has been selected yet.

The first implementation must evaluate two minimal choices:

- narrowly pinned YAML parser dependency; or
- standard-library-readable machine representation for the subset that truly needs validation.

No broader stack is currently justified.

## DevOps conclusion

The next implementation should be CI-friendly and deterministic but need not introduce CI itself until a local validator exists and has useful tests.

Expected first DevOps artifacts after implementation:

```text
validator
→ unit tests
→ synthetic negative fixtures
→ dependency/SBOM evidence if a third-party parser is selected
→ minimal CI check
```

## Information-security conclusion

**PASS_WITH_ACTIONS.**

Risk is still low because no executable runtime, external connectivity or customer data was introduced in this generation.

Before live runtime, evidence is still required for:

- dependency/supply-chain controls;
- secret scanning;
- non-bypassable authorization;
- tenant/project isolation;
- prompt-injection/provider leakage controls;
- retrieval poisoning/freshness controls;
- event integrity;
- retry/cancellation/durability;
- separation of duties.

## Evaluation

- Correctness: 4/5 — all declared contract cases are representable; executable enforcement absent.
- Traceability: 5/5 — fixture → dry-run → acceptance record → ADR → TF chain exists.
- Security: 4/5 — minimal scope remains isolated; runtime controls not yet proven.
- Maintainability: 5/5 — no framework added; acceptance record separates machine state from narrative.
- Reproducibility: 4/5 — manual cases are explicit; machine runner remains next step.
- Complexity/Cost: 5/5 — no technology added before need is demonstrated.

**Decision:** `OPEN MINIMAL VALIDATION RUNTIME`.

**Next gate:** select the smallest parser/representation approach, implement local contract validator + synthetic negative tests, then produce `TF-0009` with actual libraries, DevOps chain and security evidence.
