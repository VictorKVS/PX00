# ADR-0062 — Knowledge-Bound RUN Trace and Replay

Status: Accepted
Date: 2026-08-12
Related: ADR-0060, ADR-0061, TF-0069, RISK-0012

## Context
PX00 already replay-verifies material event lineage and policy snapshots. TF-0067/0068 added immutable external knowledge snapshots and a real Security Knowledge producer/consumer bridge.

Without binding knowledge provenance into RUN trace evidence, replay could still answer:
> “these events and policy decisions are internally consistent”

while silently ignoring:
> “which exact knowledge context was supplied to the worker.”

For a knowledge-driven system that omission is material.

## Decision
A knowledge-bound RUN persists the expected knowledge provenance inside its trace manifest and requires the same expected provenance during read-only replay.

The trace knowledge context contains:
- `context_package_ref` and exact hash;
- ordered knowledge snapshot refs/digests;
- ordered producer manifest refs/digests.

`RUN_RECORD v0.5` exposes corresponding knowledge-provenance fields.

`RunKnowledgeBinder` verifies before trace persistence that:
- ContextPackage belongs to the intended RUN;
- ContextPackage role matches the intended role;
- ContextPackage assignment matches the intended assignment;
- the snapshot set in ContextPackage exactly matches imported canonical slices;
- snapshot and producer manifest digests are valid and paired with their refs.

## Replay rule
If a persisted trace contains knowledge context, replay without the expected knowledge context fails closed.

Replay also fails when the expected:
- ContextPackage hash changes;
- knowledge snapshot digest changes;
- producer manifest/snapshot set differs.

The replay verifier performs no tool execution and no fresh knowledge retrieval.

## Why replay must not fetch current knowledge
Historical replay is verification of what happened, not reassessment using today's knowledge.

Therefore replay must not:
- query current `main`;
- retrieve latest regulator data;
- substitute a newer knowledge snapshot;
- ask an LLM to reconstruct missing context.

A later reassessment is a new governed evaluation/RUN that may supersede prior conclusions while preserving history.

## First real proof
The first knowledge-bound replay uses canonical Security Knowledge manifest `SEC-SNAPSHOT-0001` and source metadata object `FSB-117-2025`.

The bounded RUN itself uses a deterministic synthetic action. This deliberately proves provenance/replay mechanics only.

It does not claim that the synthetic action semantically used FSB regulatory content or that FATHER has completed a professional Security reasoning task.

## Important invariants
- `EVENT REPLAY WITHOUT KNOWLEDGE CONTEXT ≠ COMPLETE REPLAY` for a knowledge-bound RUN.
- `HISTORICAL REPLAY ≠ CURRENT REASSESSMENT`.
- `KNOWLEDGE SNAPSHOT ≠ ACTION AUTHORITY`.
- `SOURCE_VERIFIED ≠ VERIFIED REQUIREMENT`.
- `RUN CONTEXT PINNING ≠ PROFESSIONAL EXPERTISE`.

## Backward compatibility
Traces created without governed knowledge context remain replayable under the prior event/policy rules. Knowledge context is optional for non-knowledge-bound traces but mandatory when it was persisted originally.

## Consequences
Positive:
- historical decisions can retain exact knowledge provenance;
- current knowledge evolution cannot silently rewrite prior RUN context;
- knowledge tampering becomes part of replay failure;
- the pattern can generalize beyond Security Knowledge.

Costs:
- trace manifests carry additional references/digests;
- caller must retain the expected knowledge context for replay;
- durable storage and long-term artifact retention remain separate production concerns.

## Risk decision
With executable real-manifest RUN/replay evidence and ARGUS Audit 0002, `RISK-0012` is resolved for the bounded M1 cross-repository provenance/replay scope.

Reopen conditions remain attached to the risk record.
