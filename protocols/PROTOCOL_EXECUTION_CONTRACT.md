# PX00 Governed Protocol Execution Contract — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1  
**Scope:** control-plane contract; no runtime implementation.

## Purpose

A `PROTO-*` object defines how a governed class of work is executed. A protocol is not prose guidance that a role may ignore. It is a versioned execution contract with explicit inputs, steps, gates, bounds, outputs, failure paths, evidence requirements and authority constraints.

The objective is minimum sufficient control: enough structure to reproduce, audit, test and improve material work without encoding every trivial action.

## Required protocol blocks

Every material protocol SHALL define:

- immutable `protocol_id` and version;
- purpose and applicability scope;
- accepted role/capability classes;
- required input object types;
- preconditions;
- ordered or explicitly branched steps;
- authority and human-approval gates;
- retry/loop/time bounds;
- checkpoint/durability rules where state can be lost;
- required events/evidence;
- required output object types;
- failure, cancellation and escalation paths;
- completion/acceptance criteria;
- security/data-classification constraints.

## Execution model

```text
TASK
  ↓
select applicable PROTO version
  ↓
validate inputs + preconditions
  ↓
authority decision
  ↓
RUN starts / TRACE assigned
  ↓
STEP 1 → gate/evidence/event
  ↓
STEP 2 → gate/evidence/event
  ↓
...
  ↓
completion criteria
  ↓
outputs persisted
  ↓
RUN completed
  ↓
EVAL / acceptance evidence
```

A material step SHALL NOT be silently skipped. Optional steps must be declared optional and state the condition that makes them unnecessary.

## Step contract

Each governed step uses only fields that add decision value:

- `step_id` — stable within the protocol version;
- `purpose`;
- `actor_requirement` — role/capability/approval condition;
- `inputs`;
- `action_class`;
- `outputs`;
- `preconditions`;
- `success_condition`;
- `failure_transition`;
- `event_requirement`;
- `evidence_requirement`;
- `timeout` when time-bounded;
- `retry_policy` when retryable.

Free-form internal reasoning is not a protocol step. Material rationale is stored through explicit `DEC-*`, `FIND-*`, `EVAL-*` or event fields.

## Branching and loops

Branches must be explicit:

```text
condition A → step X
condition B → step Y
otherwise   → ESCALATE or FAIL
```

Loops must be bounded by at least one enforceable condition: maximum attempts, maximum elapsed time, maximum evidence requests, or an equivalent protocol-specific bound.

Unbounded autonomous loops are prohibited.

## Retry semantics

A retry normally creates a new `RUN-*` or an explicitly identified retry attempt while remaining linked to the same `TRACE-*` when it is still the same governed task.

Retries SHALL preserve failed-attempt evidence when material. They SHALL NOT overwrite prior outputs or events in place.

If an operation is non-idempotent, the protocol must define duplicate-prevention or reconciliation behavior before permitting automated retry.

## Checkpoint and durability

Where a protocol consumes external state or advances a cursor/checkpoint, durability order must be explicit.

General invariant:

> Do not advance a durable checkpoint before the material output/evidence that justifies the checkpoint is durably stored.

A duplicate caused by crash-before-checkpoint is generally preferable to permanent loss caused by checkpoint-before-save, unless a domain-specific contract states otherwise and proves safety.

## Authority integration

Every material action class is constrained by `AUTHORITY_AUTONOMY_CONTRACT.md`.

Protocol permission cannot expand role, project, organization, jurisdiction, tool or data-classification authority. Effective authority is the intersection of all applicable constraints.

A protocol step receiving `DENY` stops. `ESCALATE` follows the declared escalation path. Missing required approval is not equivalent to approval.

## Evidence and event requirements

Protocols reference, rather than duplicate, the Event/Trace/Provenance contract.

At minimum a material run must make reconstructable:

- task;
- protocol/version;
- role/version;
- authority decision(s);
- material inputs;
- material outputs;
- material step/gate outcomes;
- failures/retries;
- approval/escalation outcomes;
- completion state.

## Failure model

Permitted terminal run states:

- `COMPLETED`
- `FAILED`
- `DENIED`
- `ESCALATED`
- `CANCELLED`
- `BLOCKED`

A protocol must not translate failure into success merely to continue the chain.

## Versioning

A protocol version SHALL change when a material change affects:

- required step/order/branching;
- authority or approval gate;
- retry/loop/time bound;
- input/output contract;
- security/data handling;
- completion criteria;
- material evidence requirement.

Formatting-only edits do not require a protocol version increment.

An active run remains attributable to the version with which it started unless an explicit migration protocol safely transfers it.

## LLM policy

An LLM may execute reasoning/content tasks inside a protocol step, but it does not have authority to:

- remove required gates;
- invent new privileges;
- convert missing evidence into evidence;
- silently change protocol version;
- declare acceptance without required evidence.

## Security conclusion

The contract is designed to reduce privilege drift, unbounded loops, silent step skipping, duplicate side effects, lost evidence and unauditable retries.

Runtime acceptance must later prove non-bypassable gates, bounded loops, cancellation, idempotency handling where required, durable event/output ordering, secret minimization and safe failure behavior.

## Current disposition

`KEEP / VALIDATE WITH FIRST ROLE-PACKAGE PILOTS`.
