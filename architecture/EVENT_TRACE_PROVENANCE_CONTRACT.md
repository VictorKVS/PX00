# PX00 Event, Trace and Provenance Contract — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1  
**Parent decision:** ADR-0006

## Purpose

PX00 must reconstruct material activity without storing indiscriminate internal model reasoning or an unlimited technical event dump.

Three concerns remain distinct:

- **Log** — technical/operational record;
- **Trace** — linked execution path for one governed task/run;
- **Provenance** — lineage of a material result back to inputs, evidence, decisions and producing actors.

## Trace hierarchy

```text
TASK-*
  ↓
RUN-*
  ↓
TRACE-*
  ├─ EVT-*
  ├─ EVT-*
  └─ EVT-*
       ↓
material outputs
```

A task may have multiple runs. A run may fail and be retried. Independent runs are never collapsed merely because their payloads match.

## Material event rule

An event is material when it changes or materially evaluates at least one of:

- governed object lifecycle/state;
- authority/approval;
- evidence/knowledge admission;
- decision/risk/control/exception;
- external system state;
- security/compliance posture;
- release/distribution;
- acceptance/evaluation result.

Routine debug noise may remain in operational logs and does not automatically enter the durable provenance corpus.

## Event significance classes

- `T0 DEBUG` — short-lived troubleshooting telemetry;
- `T1 OPERATION` — routine execution/health activity;
- `T2 BUSINESS` — material process step;
- `T3 DECISION_KNOWLEDGE` — governed decision, finding or knowledge event;
- `T4 ASSURANCE` — security, compliance, audit, approval, exception;
- `T5 RELEASE_LEGAL` — release, delivery, acceptance or legally significant record.

Retention is controlled by jurisdiction/organization/project policy; these classes do not prescribe a universal duration.

## Canonical event requirements

A material event SHALL record or reference:

- immutable event ID;
- UTC timestamp;
- trace/run/task context;
- actor identity, role and version where applicable;
- action type;
- target/object reference;
- protocol and version when governed by a protocol;
- authority-decision reference for material tool/actions;
- input/output object references;
- concise rationale/reason code when decision-bearing;
- result/status;
- knowledge/evidence versions materially relied upon;
- model/provider/tool identity when relevant to reproducibility;
- classification and retention class;
- provenance parents/children where known.

## Provenance rule

Material outputs must preserve lineage by references rather than copying protected content unnecessarily.

Typical chain:

```text
SRC → ART → EVD → FIND → KN/DEC → REQ/ADR → implementation → TEST → REL → distribution
```

A downstream object may have multiple parents. Contradictory evidence remains represented rather than being silently removed.

## Integrity rule

PX00 core does not require blockchain.

Integrity mechanisms may include:

- append-only event storage;
- content hashes for artifacts;
- signed manifests/checkpoints;
- immutable/WORM storage for selected classes;
- repository/commit identity;
- release signatures.

The actual storage/signature technology is deferred until runtime and deployment requirements justify it.

## Sensitive-data rule

Traceability does not justify uncontrolled retention.

Events SHALL NOT contain secrets, credentials, private keys or unnecessary personal/protected data. Sensitive inputs are referenced by controlled ID/hash/location where possible. Redaction must preserve enough metadata to prove that a governed event occurred without retaining prohibited content.

## AI reasoning rule

Hidden chain-of-thought is not part of the audit contract. Decision-bearing events preserve explicit rationale summaries, evidence references, alternatives/constraints where required, protocol steps and outcome data.

## Failure and retry rule

Failures are explicit. A retry creates a distinguishable run/event sequence. Durable material save must precede any checkpoint whose advancement would otherwise make missing data unrecoverable.

## Minimum future acceptance tests

1. every material action links to one `TRACE-*`;
2. retry produces a new distinguishable run/sequence;
3. equal payload from independent observations preserves separate provenance;
4. material authority action links to an authority decision;
5. output lineage can be traversed to material inputs/evidence;
6. protected values are not leaked into public trace records;
7. retention/classification are populated for T3–T5 events;
8. release/distribution lineage survives display-name rebranding.

## Current disposition

`KEEP / runtime storage and cryptographic implementation deferred until deployment requirements exist`.
