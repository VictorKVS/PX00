# TF-0007 — First Governed Role Pilots

**Date:** 2026-08-11  
**Status:** ACCEPTED FOR PILOT VALIDATION  
**Decision:** KEEP / VALIDATE  
**Trigger:** Baseline contracts reached the first Role Package instantiation gate.

## Structural delta

Added two complete pilot Role Packages plus their governed protocols and one cross-role acceptance fixture:

```text
roles/
├── ROLE-0201-analyst/
│   ├── ROLE.yaml
│   ├── PROMPT.md
│   ├── AUTHORITY.md
│   ├── knowledge/manifest.yaml
│   ├── protocols/manifest.yaml
│   ├── schemas/manifest.yaml
│   └── evals/rubric.yaml
└── ROLE-0202-critical-reviewer/
    ├── ROLE.yaml
    ├── PROMPT.md
    ├── AUTHORITY.md
    ├── knowledge/manifest.yaml
    ├── protocols/manifest.yaml
    ├── schemas/manifest.yaml
    └── evals/rubric.yaml

protocols/pilots/
├── PROTO-0201_ANALYSIS.yaml
└── PROTO-0202_CRITICAL_REVIEW.yaml

assurance/fixtures/
└── PILOT-0001_ANALYST_SOCRATES_ACCEPTANCE.yaml

architecture/adr/
└── ADR-0013-first-governed-role-pilots-analyst-and-critical-reviewer.md
```

## Production-chain purpose

This generation converts abstract governance contracts into the first concrete professional chain:

```text
TASK
→ Analyst
→ FIND / EVAL / KN candidate / DEC candidate / follow-up TASK candidate
→ Critical Reviewer
→ EVAL / dissent FIND / bounded follow-up TASK candidate
→ Acceptance
```

No runtime framework, database, message broker, vector store or LLM SDK is introduced.

## File dossiers

### `roles/ROLE-0201-analyst/ROLE.yaml`

**Purpose:** Canonical pilot identity and complete role declaration for `ROLE-0201`.  
**Inputs/Outputs:** Declares accepted governed objects and outputs `FIND/EVAL`, with proposals for `KN/DEC/TASK`.  
**Processing:** Declarative only; runtime algorithm `NONE`.  
**Dependencies:** PX00 Role, Authority, Protocol, Knowledge, Trace and Evaluation contracts.  
**DevOps:** No build/deploy effect.  
**Security:** A1 cap; no external side effects; no self-admission of knowledge; provenance mutation prohibited.  
**Verification:** Validate against Role Package acceptance fixture and shared schemas later.  
**Decision:** KEEP / VALIDATE.

### `roles/ROLE-0201-analyst/PROMPT.md`

**Purpose:** Governed behavioral instruction set separated from authority.  
**Processing:** Analytical behavior rules: fact/inference/hypothesis separation, evidence binding, contradiction/gap handling, qualitative confidence.  
**Libraries:** NONE.  
**Security:** Prompt cannot override authority/protocol/security; fabrication and silent privilege expansion prohibited.  
**Verification:** Pilot cases CASE-01..CASE-05.  
**Decision:** KEEP / VALIDATE.

### `roles/ROLE-0201-analyst/AUTHORITY.md`

**Purpose:** Human-readable authority boundary.  
**Processing:** Fail-closed intersection of applicable constraints; maximum A1.  
**Security:** Material external side effects blocked.  
**Decision:** KEEP.

### Analyst manifests and rubric

**Purpose:** Keep knowledge, protocols, schemas and evaluation independently versionable without duplicating shared contracts.  
**Processing:** Declarative references and blocking evaluation rules.  
**Libraries:** NONE.  
**Security:** Cross-customer knowledge mixing prohibited; classification inherited; fabricated evidence and prohibited disclosure are blocking failures.  
**Decision:** KEEP / VALIDATE.

### `roles/ROLE-0202-critical-reviewer/ROLE.yaml`

**Purpose:** Canonical pilot identity for independent critical-review function. `Socrates` is display metadata only.  
**Inputs/Outputs:** Reviews `FIND/KN/DEC/EVAL/EVD`; produces `EVAL/FIND` and may propose bounded follow-up `TASK`.  
**Processing:** Declarative only.  
**Security:** A1; cannot mutate active knowledge or reviewed decisions; cannot manufacture counter-evidence or suppress dissent.  
**Verification:** Cross-role acceptance fixture.  
**Decision:** KEEP / VALIDATE.

### `roles/ROLE-0202-critical-reviewer/PROMPT.md`

**Purpose:** Defines challenge method without making the prompt the source of authority.  
**Processing:** claim/evidence support, assumptions, contradictions, alternatives, falsifiability, source independence, causal discipline, scope and time.  
**Libraries:** NONE.  
**Security:** No fabricated counter-evidence; no artificial consensus.  
**Decision:** KEEP / VALIDATE.

### `roles/ROLE-0202-critical-reviewer/AUTHORITY.md`

**Purpose:** Human-readable A1 review boundary and separation-of-duties condition.  
**Security:** If independence cannot be satisfied where required, review is BLOCKED/ESCALATED rather than falsely labelled independent.  
**Decision:** KEEP.

### Critical Reviewer manifests and rubric

**Purpose:** Versionable knowledge/protocol/schema/evaluation controls.  
**Processing:** Declarative references and critical-review quality criteria.  
**Libraries:** NONE.  
**Security:** Active knowledge mutation, provenance alteration and dissent suppression are blocking failures.  
**Decision:** KEEP / VALIDATE.

### `protocols/pilots/PROTO-0201_ANALYSIS.yaml`

**Purpose:** Bounded Analyst production procedure.  
**Algorithm:** validate → classify claims → detect contradictions/gaps → produce findings → optional proposals → evaluation. Evidence request cycle max 3.  
**Dependencies:** PX00 Protocol Execution, Authority, Trace and Acceptance contracts.  
**Security:** no raw secrets, no cross-customer mixing, no provenance mutation.  
**Verification:** Pilot acceptance fixture plus future executable fixtures.  
**Decision:** KEEP / VALIDATE.

### `protocols/pilots/PROTO-0202_CRITICAL_REVIEW.yaml`

**Purpose:** Bounded evidence-disciplined review procedure.  
**Algorithm:** validate target/independence → test evidence support → assumptions/alternatives → validity checks → persist evaluation/dissent → optional follow-up task. Max 3 additional-evidence cycles.  
**Security:** no artificial independence claim, no knowledge mutation, no provenance mutation.  
**Decision:** KEEP / VALIDATE.

### `assurance/fixtures/PILOT-0001_ANALYST_SOCRATES_ACCEPTANCE.yaml`

**Purpose:** Predeclare success/failure before runtime implementation.  
**Algorithm:** deterministic blocking criteria over role/package/protocol behavior; no runtime code yet.  
**Security:** synthetic/public-safe data only; no secrets/customer data/side effects.  
**Decision:** KEEP / EXECUTE NEXT.

### `architecture/adr/ADR-0013-first-governed-role-pilots-analyst-and-critical-reviewer.md`

**Purpose:** Architectural record for why these are the first two roles and why no new `CriticalReview` canonical object was added.  
**Security:** Records role boundaries and remaining runtime security obligations.  
**Decision:** KEEP.

## Algorithmic analysis

The current chain intentionally uses a two-role separation:

1. Analyst creates an evidence-bound proposition layer.
2. Critical Reviewer attacks its support and assumptions without having mutation authority.
3. Knowledge admission remains a separate gate.

This reduces self-confirmation and keeps the reviewer from silently becoming the owner of the reviewed state.

The pilot evidence-request bound of three cycles is chosen as a conservative test limit to prove bounded execution. It may be changed only through a new protocol version with evidence.

## Libraries and runtime

**Third-party libraries:** NONE.  
**Runtime framework:** NONE.  
**Database/vector store/message broker:** NONE.  
**LLM provider SDK:** NONE.

Reason: contracts and fixtures are being validated before technology selection.

## DevOps conclusion

No executable CI is added yet. The next generation should execute schema/fixture validation with the smallest justified validator/tooling once the pilot dry-run exposes the exact machine-validation needs.

## Information-security conclusion

**PASS_WITH_ACTIONS.**

Contract-level controls now cover authority caps, non-mutation, provenance preservation, cross-customer separation intent, classification inheritance, dissent preservation and no external side effects.

Still unproven at runtime:

- non-bypassable tool authorization;
- prompt-injection resistance;
- provider data leakage controls;
- tenant/project KB isolation;
- retrieval poisoning/freshness controls;
- tamper-evident event writes;
- actual separation of reviewer execution where required.

## Acceptance / tests

Next required evidence is execution of `PILOT-0001` as a controlled dry-run using synthetic/public-safe objects. No broad runtime implementation is justified before the fixture reveals whether the contracts are sufficient.

## Rollback

Do not delete this TF record or role history. If the pilot fails, mark the relevant package/protocol version superseded and create a new Role/Protocol version plus a new `TF-*` generation.

## Evaluation

- Correctness: 4/5 — contracts are coherent but not executed.
- Traceability: 5/5 — canonical IDs and production chain are explicit.
- Security: 4/5 — strong contract boundaries, runtime enforcement absent.
- Maintainability: 4/5 — shared contracts minimize duplication; pilot role packages remain compact.
- Reproducibility: 4/5 — fixture exists; execution evidence absent.
- Complexity/Cost: 4/5 — two roles and two protocols only; no framework inflation.

**Decision:** `KEEP / VALIDATE`.

**Next gate:** Execute Pilot-0001 as a paper/machine-readable dry-run, record acceptance evidence, then decide whether Baseline 0.1 permits the first minimal runtime validator/orchestrator code.
