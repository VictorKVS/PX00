# TF-0006 — Protocol Execution and Acceptance Model

**Date:** 2026-08-11  
**Status:** ACCEPTED FOR BASELINE VALIDATION  
**Decision:** KEEP / VALIDATE  
**Trigger:** Next PX00 architecture gate after authority/trace and knowledge/decision contracts.

## Structural change

Created:

```text
protocols/
└── PROTOCOL_EXECUTION_CONTRACT.md

assurance/
└── ACCEPTANCE_MODEL.md

schemas/
├── PROTOCOL_DEFINITION.yaml
├── RUN_RECORD.yaml
└── ACCEPTANCE_RECORD.yaml

architecture/adr/
└── ADR-0012-protocol-execution-and-acceptance-model.md

Tree_F/
└── TF-0006_2026-08-11_PROTOCOL_EXECUTION_AND_ACCEPTANCE.md
```

Updated separately in the same generation:

```text
PX00.yaml
README.md
DEVELOPMENT_JOURNAL.md
```

Prior `TF-0001..TF-0005` remain unchanged as development corpus history.

## Production-chain reason

The previous generation established who may act, how actions are traced, how evidence becomes knowledge and how decisions are evaluated. The missing production controls were:

1. a governed procedure defining how a task moves through required steps, gates, retries and failure paths;
2. an acceptance model defining when a material output can legitimately be called PASS.

Without these, a future runtime could technically follow canonical IDs while still skipping work or declaring success without evidence.

## File dossiers

### `protocols/PROTOCOL_EXECUTION_CONTRACT.md`

**Purpose:** Defines the contract for versioned `PROTO-*` execution.

**Trigger:** First Role Package pilots require one common execution semantics.

**Inputs / Outputs:** Consumes task, role, protocol, authority, canonical input objects; produces bounded run state, canonical outputs, events/evidence and terminal result.

**Processing:** Explicit preconditions → authority gate → bounded ordered/branched steps → retries/checkpoints where declared → completion criteria → outputs/evidence.

**Algorithms/rules:** fail-closed authorization; explicit branching; bounded loops; retry identity preservation; idempotency/reconciliation requirement for unsafe retries; durable-save-before-checkpoint invariant.

**Dependencies:** Existing PX00 contracts only. Runtime libraries: `NONE`.

**DevOps:** No workflow engine selected. Future runtime must demonstrate cancellation, bounds and durable execution semantics in tests.

**Security:** Reduces privilege drift, unbounded automation, unsafe duplicate effects and hidden failed attempts.

**Verification:** Pilot protocols must fit the contract without ad-hoc control semantics.

**Decision:** KEEP / VALIDATE.

### `schemas/PROTOCOL_DEFINITION.yaml`

**Purpose:** Declarative shape for protocol identity, scope, steps, bounds, authority, outputs and failures.

**Processing:** Contract metadata only.

**Dependencies/libraries:** `NONE` runtime.

**DevOps:** Candidate future validator input.

**Security:** Encodes authority/check/bounds and secret-storage prohibition.

**Verification:** Validate pilot protocol fixtures against fields/invariants after validator technology is selected.

**Decision:** KEEP / VALIDATE.

### `schemas/RUN_RECORD.yaml`

**Purpose:** Records one bounded execution instance without conflating task, trace or protocol identity.

**Processing:** Links role/protocol versions, authority decisions, attempts, material inputs/outputs, events, evidence and failure state.

**Dependencies/libraries:** `NONE` runtime.

**DevOps:** Future runtime persistence contract.

**Security:** Prevents silent overwriting of failed attempts and missing-authority reinterpretation.

**Verification:** Retry and failure fixtures must preserve separate identities and correct trace linkage.

**Decision:** KEEP / VALIDATE.

### `assurance/ACCEPTANCE_MODEL.md`

**Purpose:** Defines evidence-backed acceptance for contracts, schemas, roles, protocols, runs and releases.

**Processing:** Declared criteria → blocking/non-blocking classification → evidence → acceptance state.

**Algorithms/rules:** `NOT_TESTED | PASS | PASS_WITH_ACTIONS | FAIL | BLOCKED`; blocking failure prevents PASS; missing evidence is not success; A/B variants use comparable criteria where claims are comparable.

**Dependencies/libraries:** `NONE` runtime.

**DevOps:** Future CI/test evidence can satisfy acceptance criteria but CI product is not selected here.

**Security:** Prevents security/legal/control failures from being hidden under generic success when defined as blocking.

**Verification:** First pilot Role Packages must produce explicit acceptance cases.

**Decision:** KEEP / VALIDATE.

### `schemas/ACCEPTANCE_RECORD.yaml`

**Purpose:** Minimal machine-readable acceptance record.

**Processing:** Stores criteria, evidence references, per-criterion results and summary state.

**Dependencies/libraries:** `NONE` runtime.

**DevOps:** Future test runner/validator output target.

**Security:** Sensitive evidence is referenced rather than embedded when repository policy forbids storage.

**Verification:** Fixtures must prove blocking failures prevent PASS and PASS requires evidence.

**Decision:** KEEP / VALIDATE.

### `architecture/adr/ADR-0012-protocol-execution-and-acceptance-model.md`

**Purpose:** Records why protocol execution and acceptance are linked architecture gates.

**Processing/libraries:** Documentation only; `NONE` runtime.

**DevOps:** Explicitly defers workflow/test-framework choices.

**Security:** Records required runtime security proofs before production use.

**Verification:** Traceable to created contracts and next pilot-role gate.

**Decision:** KEEP.

## Data and algorithm flow

```text
TASK
  ↓
PROTO selection
  ↓
input/precondition validation
  ↓
AUTHORITY
  ↓
RUN / TRACE
  ↓
required bounded steps
  ↓
material EVT/EVD/outputs
  ↓
completion criteria
  ↓
acceptance criteria + evidence
  ↓
PASS / PASS_WITH_ACTIONS / FAIL / BLOCKED
  ↓
EVAL / improvement decision
```

## Libraries and runtime

Third-party application libraries introduced: `NONE`.

No workflow engine, schema validator, database, event broker, test framework or orchestration framework is selected at this stage.

## DevOps conclusion

Current effect is documentation/schema only. CI/CD remains intentionally minimal because there is still no executable runtime. The first pilot Role Packages should yield concrete fixtures from which validator/test-tool requirements can be selected.

## Security conclusion

`PASS_WITH_ACTIONS`.

Contract-level controls now address authority gating, bounded loops, retry safety, failed-attempt preservation, checkpoint ordering, blocking security criteria and evidence-backed PASS. Runtime evidence is still absent.

Required later runtime proofs:

- required steps/gates cannot be bypassed;
- loops/timeouts/cancellation are enforced;
- unsafe retry cannot duplicate side effects silently;
- event/output durability ordering is correct;
- acceptance evidence cannot be forged by the executing role without required separation/approval;
- sensitive data is minimized in logs and test evidence.

## Evaluation

- Correctness: 4/5 — coherent contract, not runtime-proven.
- Traceability: 5/5 — task/protocol/run/trace/acceptance linkage explicit.
- Security: 4/5 — design controls strong, enforcement untested.
- Maintainability: 4/5 — minimal contracts, no framework coupling.
- Reproducibility: 4/5 — acceptance semantics defined; executable fixtures pending.
- Complexity/Cost: 4/5 — added only controls required before pilot roles.

## Rollback

If pilot roles show the model is too heavy or incomplete, supersede this TF/ADR with a new generation. Do not delete `TF-0006`; preserve it as evidence of the evaluated design.

## Next gate

Create governed pilot Role Packages for `Analyst` and `Socrates/Critical Reviewer`, including their role knowledge manifests, protocols, authority boundaries, I/O schemas, evaluation rubrics and baseline acceptance fixtures.
