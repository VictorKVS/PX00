# ADR-0006 — Universal Event, Traceability and Provenance Model

Status: ACCEPTED FOR BASELINE 0.1

## Context

PX00 must be able to reconstruct who or what acted, when, under which role/protocol/context, using which evidence and knowledge, producing which decisions/artifacts, and what happened afterward.

## Decision

PX00 shall distinguish three related concerns:

- **Log** — technical/operational record of what happened;
- **Trace** — linked execution path of one operation/task/process;
- **Provenance** — lineage of an artifact, knowledge object, decision, release, or distribution.

Material events shall use a canonical event envelope containing at least event identity, timestamp, actor/role identity and version, action type, object identity, project/context, protocol identity/version, input/output references, result, trace identifier, provenance references, security classification, and retention class.

PX00 shall support durable lineage from source/evidence through analysis/decision/implementation/release/distribution where applicable.

The core shall not depend on blockchain. Integrity may use append-only storage, hashes, signatures, immutable/WORM storage for selected classes, and signed checkpoints/manifests.

## Consequences

- Significant AI actions are not detached from their history.
- Decision quality can later be correlated with role/protocol/knowledge/model versions.
- Rebranding does not break lineage.
- Retention is significance/classification-driven; PX00 does not require permanent storage of every debug/token-level event.
