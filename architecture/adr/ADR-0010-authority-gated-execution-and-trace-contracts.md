# ADR-0010 — Authority-Gated Execution and Trace Contracts

**Status:** ACCEPTED FOR BASELINE 0.1  
**Date:** 2026-08-11

## Context

PX00 already requires governed roles and universal traceability, but those principles are not sufficient until execution is formally gated by authority and every material action can be reconstructed from durable event/trace/provenance records.

A capable model/tool must not gain permission merely because it can technically perform an action. Likewise an action record without the authority decision that permitted it is incomplete assurance evidence.

## Decision

PX00 adopts two coupled baseline contracts:

1. **Authority/Autonomy Contract** — explicit fail-closed authority with levels `A0..A4`, effective-authority intersection, approval gates, revocation and `ALLOW | DENY | ESCALATE` decisions.
2. **Event/Trace/Provenance Contract** — material actions use canonical event envelopes linked to `TASK`, `RUN`, `TRACE`, authority decisions, inputs/outputs, evidence/knowledge, classification and retention.

Material execution SHALL follow this conceptual gate:

```text
requested action
→ resolve applicable authority constraints
→ authority decision
   ├─ DENY → no execution
   ├─ ESCALATE → approval/review path
   └─ ALLOW → bounded execution
                ↓
             material EVT
                ↓
             TRACE update
                ↓
             output provenance
```

## Key invariants

- authority is explicit and fail-closed;
- effective autonomy cannot exceed the strictest applicable cap;
- provider/model capability is not authority;
- approval must match the action and scope;
- material tool/action events reference their authority decision;
- retries/failures remain distinct and reconstructable;
- equal payload does not collapse independent observations;
- hidden chain-of-thought is not an audit requirement;
- secrets/unnecessary protected values are not retained merely for traceability;
- display-name rebranding does not alter canonical lineage.

## Deferred implementation choices

Baseline 0.1 does not yet select:

- schema validation library;
- event database;
- queue/broker;
- WORM/immutable storage product;
- signature/PKI technology;
- observability stack.

Those choices require runtime and deployment requirements first.

## Security conclusion

`PASS_WITH_ACTIONS`.

The contracts reduce privilege-escalation and non-repudiation gaps by forcing explicit authorization and trace links. Residual implementation risks include TOCTOU between approval and execution, forged/altered events, sensitive-data leakage, broken revocation propagation, excessive retention and incomplete tool mediation. These require runtime controls and tests before autonomous production execution.

## Consequences

Positive:

- role authority becomes testable rather than descriptive;
- every material action can be tied to the decision that allowed it;
- autonomy can be capped by project/jurisdiction/organization policy;
- role/model versions can be compared against outcomes;
- later audit and rollback have a durable execution lineage.

Cost:

- material actions require an authority check plus structured trace evidence.

The cost is accepted because the system is intended for accountable organizational use.

## Next gate

Define Knowledge Admission and Decision Evaluation contracts. No production role instantiation or autonomous runtime execution before those gates and acceptance-model completion.
