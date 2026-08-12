# TF-0068 — First Real Security Knowledge Snapshot Bridge

Date: 2026-08-12
Status: IMPLEMENTED
ADR: ADR-0061
Predecessor: TF-0067
Risk: RISK-0012 MITIGATING

## Objective
Move the cross-repository knowledge boundary from synthetic object references to the first real canonical Security Knowledge object without overstating its verification maturity.

## Real canonical slice
Selected from `VictorKVS/KNOWLEDGE_CORE`:

`security-knowledge/legislation/RU/regulators/FSB/117-2025/document.yaml`

Stable object ID:
`FSB-117-2025`.

The canonical source card states:
- official publication metadata is `VERIFIED_OFFICIAL`;
- full text ingestion is `PENDING_INGESTION`;
- atomization is `PENDING`.

Therefore TF-0068 imports the object as:
`SOURCE_VERIFIED`.

It explicitly does **not** claim a VERIFIED atomic requirement, applicability decision or compliance conclusion.

## KNOWLEDGE_CORE producer implementation
Added first real manifest:
`security-knowledge/corpus/snapshots/SEC-SNAPSHOT-0001.yaml`.

Pinned historical state:
- repository commit: `8f7e1cb7a5abec39e0432ce7a811591a5dcadc8d`;
- object content SHA-256: `5bdfd92728c6be35cdbffba5c57bb843bf1f3e48813c47fab2a755a5a3351710`;
- source locator: `publication.pravo.gov.ru:0001202503260008`;
- producer manifest digest: `8830d3aa51dab48586bdc96945f2e38182ced261eacef05fb10ef42ac9ce81d2`.

Added `tools/validate_security_snapshots.py` and strengthened `Knowledge Quality Gate` with full Git history (`fetch-depth: 0`).

Historical object verification is performed with:
`git show <pinned_commit>:<repository_relative_path>`.

The repository head advanced after the pinned commit, and CI still successfully verified the historical object bytes. This proves the snapshot does not silently follow current `main`.

## Pre-acceptance defect found and fixed
Initial manifest integrity did not include `classification` or `freshness_state`.

This was rejected before acceptance because either field can materially change consumer behavior.

The envelope now integrity-binds:
- schema version;
- repository/commit/root/request;
- object ID/version/type/path;
- exact content digest;
- knowledge state;
- source locator;
- freshness state;
- classification;
- selection reason.

## PX00 consumer implementation
Added `px00/knowledge_manifest_bridge.py`.

The bridge:
- independently recomputes producer manifest digest;
- verifies expected repository/knowledge-space/content-root boundary;
- preserves producer `knowledge_state` exactly;
- preserves classification/freshness/locator;
- builds a runtime `KNOWLEDGE_SNAPSHOT`;
- emits objects usable by `ContextPackageBuilder`;
- does not decide applicability or grant runtime authority.

Real regression proof pins:
- runtime snapshot digest: `04d5ec28431e8c13863dab9896533435dac735ceb36b6bf59e4f05eea1f7eac3`;
- ContextPackage hash: `9c09e6a4075f25ce2e341d1b0bd2fa4f59dedadf364019492be337893c220a2a`.

Added tampering tests for:
- knowledge-state escalation;
- source locator substitution;
- classification change;
- freshness change;
- wrong repository boundary.

Added route-only integration receipt:
`knowledge/integration/SEC-SNAPSHOT-0001_RECEIPT.yaml`.

The receipt is evidence of import, not a local copy of Security Knowledge truth.

## CI evidence
KNOWLEDGE_CORE:
- historical object SHA-256 validation: PASS;
- manifest integrity validation: PASS;
- normal knowledge-quality validation: PASS.

PX00:
- unit/repository integration tests: PASS;
- secret scan: PASS;
- contract validation: PASS.

## Architectural result
The first real canonical knowledge object has crossed:

`KNOWLEDGE_CORE historical object → producer manifest → PX00 manifest validation → KNOWLEDGE_SNAPSHOT → CONTEXT_PACKAGE`.

The state survived without semantic promotion.

## Important limitations
TF-0068 does not prove:
- FSB Order 117/2025 full text ingestion;
- atomic VERIFIED requirements from the order;
- organizational applicability;
- compliance;
- a completed FATHER RUN;
- RUN replay.

Thus:
`REAL KNOWLEDGE TRANSPORT PROVEN ≠ SECURITY EXPERT LOOP PROVEN`.

## Next narrow target
TF-0069 should carry this exact snapshot-bound ContextPackage through a bounded FATHER/RUN trace and replay path, preserving its knowledge references.

After that, repeat the same flow later with a true atomic VERIFIED Security requirement slice for the first evidence-backed professional reasoning loop.
