# TF-0004 — Authority and Trace Contracts

**Date:** 2026-08-11  
**Status:** ACCEPTED FOR BASELINE VALIDATION  
**Trigger:** DJ-0004 next gate; ADR-0004/0006/0009 required concrete authority and trace contracts before role instantiation.  
**Decision:** KEEP / VALIDATE

## Structural delta

New material files:

```text
governance/
└── AUTHORITY_AUTONOMY_CONTRACT.md

architecture/
├── EVENT_TRACE_PROVENANCE_CONTRACT.md
└── adr/
    └── ADR-0010-authority-gated-execution-and-trace-contracts.md

schemas/
├── AUTHORITY_DECISION.yaml
├── EVENT_ENVELOPE.yaml
└── TRACE_MANIFEST.yaml
```

Existing cumulative `TF-0001..TF-0003` records remain unchanged and addressable.

## Production chain introduced

```text
Role/Protocol requests action
        ↓
resolve authority constraints
        ↓
ALLOW / DENY / ESCALATE
        ↓              \
    execution         review/stop
        ↓
      EVT
        ↓
     TRACE
        ↓
output + provenance
        ↓
later EVAL / audit / improvement
```

## File dossiers

### `governance/AUTHORITY_AUTONOMY_CONTRACT.md`

**Purpose:** Defines who/what may perform which action, under what autonomy level and approval constraints.  
**Trigger:** Governed roles had authority fields but no shared enforcement contract.  
**Inputs:** Role authority, protocol, project, organization/jurisdiction policy, tool permission, data classification, approvals.  
**Outputs:** Effective authority semantics and `A0..A4` execution boundaries.  
**Processing:** Intersection/strictest-cap rule; fail-closed decision; deny/escalate conditions; revocation.  
**Dependencies:** Existing ADR-0004/0009 and canonical IDs only. No runtime library.  
**DevOps:** None yet; later becomes a policy gate before tool execution.  
**Security:** Positive control against silent privilege expansion. Key future risks: stale approvals, TOCTOU, revocation propagation.  
**Verification:** Negative tests must deny missing/ambiguous authority and missing approval.  
**Decision:** KEEP / VALIDATE.

### `schemas/AUTHORITY_DECISION.yaml`

**Purpose:** Machine-readable contract for an authority decision.  
**Trigger:** Authority must become testable and traceable, not prose-only.  
**Inputs:** Actor/role/action/context/constraint references.  
**Outputs:** `ALLOW | DENY | ESCALATE` plus effective autonomy and rationale reference.  
**Processing:** Declarative invariants; no executable validator selected.  
**Dependencies:** YAML only; canonical object vocabulary.  
**DevOps:** Future schema lint/validation candidate.  
**Security:** Ensures material execution has an explicit permission record; must not contain sensitive payloads unnecessarily.  
**Verification:** Contract tests against allowed/denied fixtures when validator exists.  
**Decision:** KEEP / VALIDATE.

### `architecture/EVENT_TRACE_PROVENANCE_CONTRACT.md`

**Purpose:** Defines durable material execution lineage and separates logs, traces and provenance.  
**Trigger:** ADR-0006 required a concrete material-event contract before runtime.  
**Inputs:** Task/run/actor/action/authority/input/output/evidence/knowledge/security context.  
**Outputs:** Event/trace/provenance requirements and significance classes T0–T5.  
**Processing:** Materiality classification; parent/child lineage; explicit retry/failure preservation; protected-data reference rule.  
**Dependencies:** ADR-0006, canonical object model. No storage/observability library selected.  
**DevOps:** Later drives event persistence, observability and audit pipeline acceptance.  
**Security:** Avoids both missing audit evidence and indiscriminate sensitive logging. Integrity technology deferred.  
**Verification:** Traverse output back to inputs/evidence; prove retry separation and rebranding-stable lineage.  
**Decision:** KEEP / VALIDATE.

### `schemas/EVENT_ENVELOPE.yaml`

**Purpose:** Canonical machine-readable fields for a material event.  
**Trigger:** Event traceability needed a shared envelope before implementation.  
**Inputs:** Actor/action/context/authority/provenance/security metadata.  
**Outputs:** Structured `EVT-*` record.  
**Processing:** Declarative required/conditional field rules.  
**Dependencies:** YAML and canonical IDs only.  
**DevOps:** Future schema validator and event pipeline input.  
**Security:** Classification/retention fields are mandatory; secrets and hidden reasoning dumps are prohibited.  
**Verification:** Fixture-based schema tests plus sensitive-value negative tests.  
**Decision:** KEEP / VALIDATE.

### `schemas/TRACE_MANIFEST.yaml`

**Purpose:** Compact manifest for one governed execution trace.  
**Trigger:** Events need an addressable execution container that survives retries/failures.  
**Inputs:** Task/run/event references and material inputs/outputs.  
**Outputs:** `TRACE-*` lifecycle/status manifest.  
**Processing:** Reference aggregation, ordered/sequence-addressable events, explicit retry/failure separation.  
**Dependencies:** YAML/canonical IDs only.  
**DevOps:** Future trace storage/index contract.  
**Security:** References protected values instead of copying them.  
**Verification:** Failed trace remains discoverable after successful retry; no history overwrite.  
**Decision:** KEEP / VALIDATE.

### `architecture/adr/ADR-0010-authority-gated-execution-and-trace-contracts.md`

**Purpose:** Makes authority-gated execution plus trace evidence an architectural baseline decision.  
**Trigger:** Coupled contracts materially constrain all future runtime/tool execution.  
**Inputs:** ADR-0004, ADR-0006, ADR-0009 and the new contracts.  
**Outputs:** Accepted invariants and deferred implementation choices.  
**Processing:** Architectural decision record; no runtime algorithm.  
**Dependencies:** None beyond repository contracts.  
**DevOps:** Prevents premature selection of event DB/broker/validator/PKI.  
**Security:** Records residual risks and blocks autonomous runtime until controls/tests exist.  
**Verification:** Future implementation must map back to this ADR and pass negative authority/trace tests.  
**Decision:** KEEP.

## Algorithms and libraries

Runtime algorithm: `NONE` implemented.

Contract algorithms/rules defined:

1. effective authority = intersection of applicable grants/caps;
2. absence/ambiguity of authority → deny/escalate;
3. material action → authority decision → event → trace → provenance;
4. retries/failures remain distinct;
5. retention uses significance/classification rather than unlimited capture.

Third-party libraries introduced: `NONE`.

Deferred candidates such as JSON Schema/Pydantic, event stores, OpenTelemetry, message brokers, WORM products and PKI are intentionally not selected yet.

## DevOps conclusion

No executable CI/CD change. The contracts now define what future schema validation and runtime test gates must prove. Selecting infrastructure now would violate `NO CODE BEFORE CONTRACT` and create premature coupling.

## Security / privacy conclusion

**Result:** `PASS_WITH_ACTIONS`.

Improved controls:

- explicit fail-closed authority;
- bounded autonomy;
- approval linkage;
- revocation requirement;
- material event traceability;
- classification/retention metadata;
- protected-data minimization;
- durable failure/retry lineage.

Required before runtime autonomy:

- authorization mediation cannot be bypassed by tools;
- TOCTOU protection between approval and action;
- authenticated/tamper-evident event writes;
- revocation propagation tests;
- data-redaction/retention tests;
- runtime secret scanning and supply-chain controls.

## Evaluation

Coarse baseline score (0–5, evidence aid only):

- Correctness/contract coherence: 4/5
- Traceability: 5/5
- Security-by-design: 5/5
- Maintainability: 4/5
- Reproducibility: 4/5
- Complexity/cost: 4/5

Main uncertainty: contracts are not yet exercised by executable roles/runtime.

## Rollback

Do not delete this accepted TF record. If contracts prove unsuitable, create successor ADR/TF records that explicitly supersede the affected contracts and preserve this generation for comparison.

## Next gate

Define:

1. Knowledge Admission Contract;
2. Decision Evaluation Contract;
3. acceptance fixtures sufficient to instantiate the first governed Role Package without ad-hoc semantics.
