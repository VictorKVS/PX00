# TF-0067 — Cross-Repository Knowledge Snapshot Pinning

Date: 2026-08-12
Status: IMPLEMENTED
ADR: ADR-0060

## Objective
Make the boundary between `VictorKVS/PX00` and canonical `VictorKVS/KNOWLEDGE_CORE` historically reproducible without copying Security Knowledge into PX00.

## Problem discovered
`CONTEXT_PACKAGE v0.2` pinned exact selected object versions/digests and route refs, but an external knowledge repository could still advance after the RUN. A mutable active route such as `main` is appropriate for new requests but cannot be historical evidence.

## Implemented in PX00
### `schemas/KNOWLEDGE_SNAPSHOT.yaml`
New immutable cross-repository snapshot contract pins:
- stable knowledge space;
- canonical repository slug;
- exact Git commit SHA;
- route snapshot;
- content root;
- exact object/version/SHA-256 refs;
- deterministic snapshot digest.

### `px00/knowledge_snapshots.py`
Fail-closed runtime builder rejects:
- branch/tag names in place of a 40-hex commit;
- repository URLs where a canonical repository slug is required;
- invalid/path-traversal content roots;
- invalid SHA-256 object digests;
- duplicate object versions;
- objects from another knowledge space;
- empty snapshots.

### `CONTEXT_PACKAGE v0.3`
`knowledge_snapshot_refs` are now preserved and participate in `package_hash`.
Changing only the external repository snapshot changes the ContextPackage hash even when selected object IDs/version refs remain identical.

### Canonical route
Added `knowledge/routes/KB-SECURITY.yaml`:

`KB-SECURITY → VictorKVS/KNOWLEDGE_CORE/security-knowledge/`.

The active route may resolve current state; every historical RUN must pin an immutable snapshot before context delivery.

## Implemented in KNOWLEDGE_CORE
Added:
`security-knowledge/corpus/snapshot-export-schema.yaml`.

The producer-side manifest requires:
- repository commit;
- stable object/version IDs;
- exact content SHA-256;
- knowledge state;
- repository-relative path;
- selection reason.

Selection and verification remain separate. Retrieval rank, RAG output or model output cannot promote knowledge to VERIFIED.

## Tests / evidence
New tests cover:
- deterministic snapshot construction;
- commit change → snapshot digest change;
- object digest change → snapshot digest change;
- invalid mutable revision rejection;
- repository identity validation;
- path traversal rejection;
- cross-space rejection;
- duplicate version rejection;
- empty snapshot rejection;
- ContextPackage snapshot preservation;
- snapshot change → ContextPackage hash change.

PX00 Contract Validation passed on the implementation head before generation documentation.
KNOWLEDGE_CORE Knowledge Quality Gate passed with the producer schema.

## Risk
Created `RISK-0012 — External Knowledge Snapshot Producer Gap`, now `MITIGATING`.

Consumer and producer contracts exist, but the first real exported Security Knowledge slice and historical replay after repository head advancement are not yet proven.

## Architectural result
The cross-repository knowledge flow is now explicitly:

`REQUEST → ROUTE → PRODUCER SELECTION → IMMUTABLE SNAPSHOT → CONTEXT PACKAGE → RUN`.

This preserves the permanent invariant:

`LOGICAL KNOWLEDGE IDENTITY != PHYSICAL REPOSITORY LOCATION`.

## Next narrow target
Implement the first executable producer export in KNOWLEDGE_CORE for a small real VERIFIED `SEC-*` slice, validate it in PX00, construct a ContextPackage and prove historical replay after KNOWLEDGE_CORE changes.

This is a direct prerequisite for the first closed FATHER Security-domain loop, but it does not block ongoing Security Knowledge corpus population or SUMMIT-FFB-02 live-provider work.
