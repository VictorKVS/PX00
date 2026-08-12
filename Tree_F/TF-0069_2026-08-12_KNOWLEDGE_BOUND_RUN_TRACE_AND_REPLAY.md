# TF-0069 — Knowledge-Bound RUN Trace and Replay

Date: 2026-08-12
Status: IMPLEMENTED
ADR: ADR-0062
Predecessor: TF-0068
Audit: ARGUS_AUDIT_0002 — PASS_WITH_RESTRICTIONS
Risk outcome: RISK-0012 RESOLVED for bounded M1 provenance/replay scope

## Objective
Carry the first real canonical Security Knowledge snapshot beyond ContextPackage construction into a governed RUN, persisted trace manifest and read-only replay without re-fetching current knowledge.

## Runtime changes
### `RUN_RECORD v0.5`
Adds explicit knowledge provenance:
- knowledge snapshot refs/digests;
- producer manifest refs/digests.

### `TRACE_MANIFEST v0.2`
A knowledge-bound trace may persist:
- ContextPackage ref/hash;
- knowledge snapshot refs/digests;
- producer manifest refs/digests.

### `TraceKnowledgeContext`
New immutable runtime object validates:
- ContextPackage hash;
- ref/digest cardinality;
- duplicate provenance refs;
- SHA-256 provenance digests.

### `RunKnowledgeBinder`
New pre-trace binder verifies:
- ContextPackage belongs to the RUN;
- role matches;
- assignment matches;
- imported snapshot set exactly matches ContextPackage snapshot refs;
- producer/snapshot digests are present and valid.

### Recorder/replay
`AppendOnlyEventRecorder` can persist and verify knowledge context together with the event-chain manifest.

`ReadOnlyReplayVerifier` accepts expected knowledge context and reports `knowledge_context_verified=true` only after persisted manifest equality is proven.

A trace that was persisted with knowledge context cannot be replayed while omitting that context; it fails closed with:
`TRACE_KNOWLEDGE_CONTEXT_EXPECTATION_REQUIRED`.

## First real knowledge-bound RUN proof
Input knowledge provenance comes from canonical:
`VictorKVS/KNOWLEDGE_CORE/security-knowledge/corpus/snapshots/SEC-SNAPSHOT-0001.yaml`.

Canonical object:
`FSB-117-2025`.

Producer knowledge state remains:
`SOURCE_VERIFIED`.

The governed RUN intentionally executes only a deterministic synthetic operation. This isolates the claim being tested:

> Can the runtime persist and replay the exact real external knowledge context alongside event/policy lineage?

Answer under the M1 reference harness: **YES**.

The test does not claim that the operation semantically reasons about FSB requirements.

## Negative evidence
Tests prove replay fails when:
- the recorded knowledge context is omitted;
- ContextPackage hash is changed;
- knowledge snapshot digest is changed;
- ContextPackage belongs to another RUN.

TF-0068 already proves producer manifest tampering is rejected for:
- knowledge-state escalation;
- source-locator substitution;
- classification change;
- freshness change;
- wrong repository boundary.

## Historical property
The producer snapshot is pinned to KNOWLEDGE_CORE commit:
`8f7e1cb7a5abec39e0432ce7a811591a5dcadc8d`.

KNOWLEDGE_CORE has advanced beyond that commit. Its CI still verifies the historical source bytes using full Git history.

PX00 replay does not fetch current knowledge; it verifies the persisted expected snapshot/context digests.

This establishes:
`HISTORICAL REPLAY != CURRENT REASSESSMENT`.

## ARGUS result
`ARGUS_AUDIT_0002_KNOWLEDGE_BOUND_REPLAY.md` returns `PASS_WITH_RESTRICTIONS`.

It permits the claim:
**bounded M1 cross-repository knowledge provenance/replay is proven**.

It explicitly prohibits promoting that claim into:
- full FSB source verification;
- VERIFIED atomic requirements;
- applicability/compliance;
- expert Security reasoning;
- production durability;
- live AI correctness;
- complete closed FATHER corporate loop.

## Risk decision
`RISK-0012` moves to `RESOLVED` for the bounded M1 provenance/replay scope.

Reopen if mutable routing re-enters historical replay, provenance is omitted, schema compatibility breaks, state is upgraded during transport, or future storage cannot reproduce pinned historical objects.

## CI evidence before generation close
Implementation tests passed:
- unit/repository integration tests;
- secret scan;
- PX00 repository contract validation.

KNOWLEDGE_CORE historical snapshot validation also passed on a head newer than the pinned source commit.

## What is now proven end to end

`REAL CANONICAL SOURCE METADATA`
`→ HISTORICAL PRODUCER MANIFEST`
`→ PRODUCER CI SHA-256`
`→ PX00 MANIFEST VALIDATION`
`→ KNOWLEDGE_SNAPSHOT`
`→ CONTEXT_PACKAGE`
`→ RUN KNOWLEDGE PIN`
`→ EVENT TRACE`
`→ PERSISTED TRACE MANIFEST`
`→ READ-ONLY REPLAY`

## Next narrow target
Do **not** confuse the next step with more snapshot plumbing.

Two independent useful tracks remain:
1. `SUMMIT-FFB-02` — first real governed live AI executor;
2. Security Knowledge corpus — continue FSTEC/FSB source and atomic requirement production.

The next integration milestone should wait for a genuinely atomic VERIFIED Security requirement slice, then use it in the first bounded professional Security reasoning task under independent review.
