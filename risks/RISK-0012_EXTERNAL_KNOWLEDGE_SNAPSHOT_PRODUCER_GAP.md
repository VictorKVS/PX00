# RISK-0012 — External Knowledge Snapshot Producer Gap

Status: OPEN
Severity: S3
Category: KNOWLEDGE / CROSS-REPOSITORY / REPRODUCIBILITY / INTEGRITY
Source: TF-0067 design pass
Owner: FFB-ROLE-0004 Knowledge Architect + FFB-ROLE-0006 Principal Software Engineer

## Risk
PX00 can now validate and pin an immutable external knowledge snapshot into a ContextPackage, but `VictorKVS/KNOWLEDGE_CORE` does not yet expose a canonical machine-readable snapshot/selection manifest that PX00 can consume for a real Security Knowledge request.

Without a producer-side manifest, an integration could accidentally reconstruct selected objects from mutable repository state, branch names, ad-hoc paths or retrieval output and thereby break historical reproducibility even though the PX00 consumer contract itself is correct.

## What is already proven
TF-0067 introduces:
- `KNOWLEDGE_SNAPSHOT` contract;
- immutable 40-hex Git commit pinning instead of `main/latest` for historical state;
- exact `object_id@version_id#sha256_content_digest` selection references;
- snapshot digest over repository, commit, route, content root and sorted selected object versions;
- `KB-SECURITY` route to `VictorKVS/KNOWLEDGE_CORE/security-knowledge/`;
- ContextPackage hashing of `knowledge_snapshot_refs`;
- tests showing commit/snapshot/object changes alter the resulting digest/hash;
- fail-closed rejection of branch names, repository URLs as logical identity, parent traversal, duplicate versions and cross-space objects.

## Why this risk remains open
The consumer side is synthetic-reference proven, not end-to-end repository proven. Missing producer evidence includes:
- canonical export/query manifest format in KNOWLEDGE_CORE;
- stable mapping from selected `SEC-*` objects to exact content digests;
- producer validation that exported object versions exist at the pinned commit;
- canonical query/selection evidence showing why each object was selected;
- cross-repository integration test using a real Security Knowledge slice;
- historical replay test after KNOWLEDGE_CORE `main` advances.

## Immediate containment
- PX00 must not treat mutable branch resolution as a historical knowledge snapshot.
- No first closed FATHER Security loop may claim reproducible Security Knowledge context unless an immutable snapshot ref is present.
- Existing Security Knowledge remains canonical in KNOWLEDGE_CORE; PX00 must not copy objects merely to simplify snapshotting.

## Closure condition
Create a producer-side snapshot/export contract in KNOWLEDGE_CORE and prove one real cross-repository flow:

`KNOWLEDGE_REQUEST → canonical KNOWLEDGE_CORE selection → commit/object/version/digest manifest → PX00 KNOWLEDGE_SNAPSHOT validation → CONTEXT_PACKAGE → RUN → replay verification`.

Then advance KNOWLEDGE_CORE `main` and prove that the historical RUN still resolves/verifies against its pinned commit and object versions without silently following the new head.
