# RISK-0012 — External Knowledge Snapshot Producer Gap

Status: MITIGATING
Severity: S3
Category: KNOWLEDGE / CROSS-REPOSITORY / REPRODUCIBILITY / INTEGRITY
Source: TF-0067 design pass; narrowed by TF-0068
Owner: FFB-ROLE-0004 Knowledge Architect + FFB-ROLE-0006 Principal Software Engineer

## Risk
A real Security Knowledge source-metadata slice now crosses the producer/consumer boundary with historical Git verification, manifest integrity, PX00 snapshot pinning and ContextPackage construction. The remaining gap is narrower: the pinned context has not yet been carried through an actual FATHER RUN and replay verifier after further canonical knowledge evolution.

Without RUN/replay evidence, we still cannot claim end-to-end historical decision reproducibility even though the external knowledge transport boundary itself is now materially proven.

## Proven in TF-0067
PX00:
- `KNOWLEDGE_SNAPSHOT` contract;
- immutable 40-hex Git commit pinning instead of `main/latest` for historical state;
- exact `object_id@version_id#sha256_content_digest` selection references;
- snapshot digest over repository, commit, route, content root and sorted selected object versions;
- `KB-SECURITY` route to `VictorKVS/KNOWLEDGE_CORE/security-knowledge/`;
- ContextPackage hashing of `knowledge_snapshot_refs`;
- fail-closed negative tests.

KNOWLEDGE_CORE:
- `security-knowledge/corpus/snapshot-export-schema.yaml` producer contract;
- selection remains distinct from verification;
- retrieval/model output cannot promote knowledge state.

## Additional evidence proven in TF-0068
### First real canonical object
Producer manifest `SEC-SNAPSHOT-0001` pins:
- object: `FSB-117-2025`;
- exact historical repository commit: `8f7e1cb7a5abec39e0432ce7a811591a5dcadc8d`;
- exact source-card content digest: `5bdfd92728c6be35cdbffba5c57bb843bf1f3e48813c47fab2a755a5a3351710`;
- state: `SOURCE_VERIFIED`;
- official publication locator: `publication.pravo.gov.ru:0001202503260008`.

The source record itself explicitly says full text and atomization remain pending. TF-0068 therefore preserves `SOURCE_VERIFIED` and does not promote the object to VERIFIED requirement knowledge.

### Historical producer validation
`Knowledge Quality Gate` now checks snapshots with full Git history using:
`git show <pinned_commit>:<path>`.

The repository head advanced beyond the pinned commit, yet CI successfully re-read the historical source card and verified its SHA-256. This proves the manifest does not silently follow current `main`.

### Manifest-envelope hardening
A pre-acceptance review found that classification and freshness were not initially inside the manifest digest. The envelope was strengthened before acceptance so the digest now covers:
- schema version;
- repository/commit/root/request;
- object/version/type/path/content digest;
- knowledge state;
- source locator;
- freshness state;
- classification;
- selection reason.

Tampering with state, locator, classification or freshness is rejected by PX00 consumer tests.

### PX00 real-manifest bridge
`px00/knowledge_manifest_bridge.py` independently recomputes the producer manifest digest and creates the runtime `KNOWLEDGE_SNAPSHOT` without changing knowledge state.

Regression evidence pins exact values:
- producer manifest digest: `8830d3aa51dab48586bdc96945f2e38182ced261eacef05fb10ef42ac9ce81d2`;
- PX00 runtime snapshot digest: `04d5ec28431e8c13863dab9896533435dac735ceb36b6bf59e4f05eea1f7eac3`;
- ContextPackage hash: `9c09e6a4075f25ce2e341d1b0bd2fa4f59dedadf364019492be337893c220a2a`.

PX00 stores only an integration receipt/reference, not a duplicate Security Knowledge truth object.

## Remaining evidence before closure
- carry the real snapshot-bound ContextPackage through an actual PX00/FATHER RUN;
- preserve the snapshot/package references in RUN/trace evidence;
- advance canonical Security Knowledge again;
- replay the historical RUN and prove it still verifies against the pinned snapshot/context rather than the new head;
- repeat later with a true atomic VERIFIED requirement slice, because TF-0068 proves source-metadata transport, not expert requirement reasoning.

## Immediate containment
- mutable branch resolution is never historical snapshot identity;
- no closed FATHER Security loop may claim reproducible knowledge context without immutable snapshot refs;
- canonical Security Knowledge remains in KNOWLEDGE_CORE and is not copied into PX00;
- knowledge state, classification and freshness are producer-signed-by-digest material and may not be silently altered by the consumer;
- `SOURCE_VERIFIED` is not `VERIFIED REQUIREMENT`.

## Closure condition
Prove:

`KNOWLEDGE_REQUEST → canonical selection → historical manifest → PX00 KNOWLEDGE_SNAPSHOT → CONTEXT_PACKAGE → RUN → TRACE/REPLAY`

and show the same historical RUN verifies after KNOWLEDGE_CORE head advances, without resolving knowledge from the newer head.
