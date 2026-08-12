# RISK-0012 — External Knowledge Snapshot Producer Gap

Status: MITIGATING
Severity: S3
Category: KNOWLEDGE / CROSS-REPOSITORY / REPRODUCIBILITY / INTEGRITY
Source: TF-0067 design pass
Owner: FFB-ROLE-0004 Knowledge Architect + FFB-ROLE-0006 Principal Software Engineer

## Risk
PX00 can validate and pin an immutable external knowledge snapshot into a ContextPackage, and `VictorKVS/KNOWLEDGE_CORE` now defines the producer-side snapshot/export manifest contract. However, a real Security Knowledge slice has not yet been exported, validated cross-repository and replayed after the KNOWLEDGE_CORE head changes.

Without executable producer/export evidence, an integration could still accidentally reconstruct selected objects from mutable repository state, branch names, ad-hoc paths or retrieval output and thereby break historical reproducibility even though both sides now agree on the contract.

## What is already proven
TF-0067 introduces in PX00:
- `KNOWLEDGE_SNAPSHOT` contract;
- immutable 40-hex Git commit pinning instead of `main/latest` for historical state;
- exact `object_id@version_id#sha256_content_digest` selection references;
- snapshot digest over repository, commit, route, content root and sorted selected object versions;
- `KB-SECURITY` route to `VictorKVS/KNOWLEDGE_CORE/security-knowledge/`;
- ContextPackage hashing of `knowledge_snapshot_refs`;
- tests showing commit/snapshot/object changes alter the resulting digest/hash;
- fail-closed rejection of branch names, repository URLs as logical identity, parent traversal, duplicate versions and cross-space objects.

Producer containment now exists in KNOWLEDGE_CORE:
- `security-knowledge/corpus/snapshot-export-schema.yaml` defines the canonical export manifest;
- the manifest separates selection from verification;
- each selected object must carry stable object/version identity, repository-relative path, SHA-256 digest, knowledge state and selection reason;
- VERIFIED remains dependent on source/locator lineage rather than retrieval rank or model output;
- manifest generation is required to pin the repository commit and preserve stale/disputed/contradictory material when material to scope;
- KNOWLEDGE_CORE Knowledge Quality Gate passes with the new producer contract.

## Why this risk remains open
The contract exists on both sides, but the flow is not end-to-end proven. Missing evidence includes:
- executable producer/export implementation in KNOWLEDGE_CORE;
- stable mapping from a real selected `SEC-*` slice to exact content digests;
- producer validation that exported object versions exist at the pinned commit;
- canonical query/selection evidence showing why each object was selected;
- cross-repository integration test using a real Security Knowledge slice;
- historical replay test after KNOWLEDGE_CORE `main` advances.

## Immediate containment
- PX00 must not treat mutable branch resolution as a historical knowledge snapshot.
- No first closed FATHER Security loop may claim reproducible Security Knowledge context unless an immutable snapshot ref is present.
- Existing Security Knowledge remains canonical in KNOWLEDGE_CORE; PX00 must not copy objects merely to simplify snapshotting.
- Producer-side retrieval or LLM output remains candidate selection material and cannot upgrade `knowledge_state` by itself.

## Closure condition
Implement the producer/export path in KNOWLEDGE_CORE and prove one real cross-repository flow:

`KNOWLEDGE_REQUEST → canonical KNOWLEDGE_CORE selection → commit/object/version/digest manifest → PX00 KNOWLEDGE_SNAPSHOT validation → CONTEXT_PACKAGE → RUN → replay verification`.

Then advance KNOWLEDGE_CORE `main` and prove that the historical RUN still resolves/verifies against its pinned commit and object versions without silently following the new head.
