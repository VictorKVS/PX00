# ADR-0060 — Cross-Repository Knowledge Snapshot Pinning

Status: Accepted
Date: 2026-08-12

## Context
`SEC-PROD-0001 Security Knowledge Base` is canonical in `VictorKVS/KNOWLEDGE_CORE/security-knowledge/`, while PX00/FATHER is the governed runtime that consumes selected knowledge through roles, bindings, ContextPackages and RUNs.

The existing ContextPackage contract already pins each selected knowledge object as:

`object_id@version_id#sha256_content_digest`.

That is necessary but insufficient for a long-lived cross-repository boundary. An active `KNOWLEDGE_ROUTE` may legitimately resolve to a mutable branch such as `main`, while a historical RUN must never silently follow that branch after KNOWLEDGE_CORE evolves.

## Decision
Introduce an immutable `KNOWLEDGE_SNAPSHOT` between route resolution and ContextPackage delivery.

For external Git-backed knowledge, the snapshot pins:
- stable `knowledge_space_id`;
- canonical repository slug;
- exact 40-hex repository commit SHA;
- route snapshot reference;
- content root;
- exact selected `object_id@version_id#sha256_content_digest` references;
- deterministic SHA-256 snapshot digest.

`ContextPackage` now carries `knowledge_snapshot_refs` and includes those references in `package_hash`.

## Resolution model

```text
KNOWLEDGE_REQUEST
        ↓
active KNOWLEDGE_ROUTE
(may resolve through main/current endpoint)
        ↓
canonical producer selection
        ↓
IMMUTABLE KNOWLEDGE_SNAPSHOT
(repo commit + exact object versions/digests)
        ↓
CONTEXT_PACKAGE
        ↓
RUN
```

The active route is operational routing state. The snapshot is historical evidence. They are intentionally different objects.

## Canonical Security route
`KB-SECURITY` resolves to:
- repository: `VictorKVS/KNOWLEDGE_CORE`;
- content root: `security-knowledge/`;
- product: `SEC-PROD-0001`.

PX00 stores route/snapshot references, not a duplicate Security Knowledge truth store.

## Producer/consumer boundary
`KNOWLEDGE_CORE` owns knowledge truth and must produce a machine-readable export manifest containing commit, stable object/version identity, exact content digest, knowledge state and selection reason.

PX00 owns runtime validation and must reject mutable revision identifiers or malformed/mismatched snapshots before context delivery.

The producer-side contract is defined in:
`VictorKVS/KNOWLEDGE_CORE/security-knowledge/corpus/snapshot-export-schema.yaml`.

## Security and authority invariant
Snapshot validity means only:
> “this is the exact knowledge state/context supplied to the RUN.”

It does **not** mean:
- the content is true merely because it is pinned;
- the content is legally applicable;
- a control is implemented;
- a compliance decision is approved;
- an executor receives tool/action authority.

Knowledge verification state and runtime authority remain separate dimensions.

## Rejected alternatives
### Pin only `main` or another branch
Rejected because historical replay changes when the branch advances.

### Copy Security Knowledge into PX00
Rejected because it creates competing truth stores and divergent regulatory history.

### Pin only per-object digests
Rejected as incomplete repository provenance: object identity can be reproduced, but the exact producer repository state and selection boundary are lost.

### Pin only repository commit
Rejected because a commit does not state which exact objects were supplied to a specific assignment/RUN.

## Consequences
Positive:
- KNOWLEDGE_CORE may evolve independently without rewriting historical FATHER context;
- exact external knowledge context is replayable in principle;
- migration from GitHub to another store can preserve logical IDs and historical provenance;
- multiple domain KBs can reuse the same pattern later.

Costs:
- producer must generate an export manifest;
- consumer must validate it;
- storage/retention must preserve enough historical repository/object state for replay;
- freshness and reproducibility must be managed separately.

## Remaining gap
`RISK-0012` remains MITIGATING until one real `SEC-*` slice is exported from KNOWLEDGE_CORE, validated by PX00, included in a ContextPackage, used in a RUN and successfully replayed after KNOWLEDGE_CORE `main` advances.
