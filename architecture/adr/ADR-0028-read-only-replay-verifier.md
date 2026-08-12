# ADR-0028 — Read-only Replay Verifier

Status: Accepted
Date: 2026-08-12

## Context
PX00 now persists policy snapshots, authority lineage, material events, an append-only hash chain, and a trace manifest. A verifier is needed to reconstruct and assess that evidence later without re-executing tools or creating side effects.

## Decision
Introduce a read-only Replay Verifier with no Tool Boundary dependency. It verifies request/run identity, AuthorityDecision lineage, PolicySnapshot ref/hash, event lineage, persisted trace manifest integrity and event-set consistency.

Replay outcomes are classified as:
- VERIFIED_RECORD
- BROKEN_LINEAGE
- TAMPER_DETECTED
- POLICY_MISMATCH
- INSUFFICIENT_EVIDENCE

## Epistemic rule
`VERIFIED_RECORD` means that the recorded governed lineage and integrity checks passed. It does not assert that the underlying real-world claim is true. Factual truth remains a higher-level evidence/provenance/evaluation question.

## Consequences
- replay cannot itself create a new material external effect;
- historical verification becomes possible without privileged tool access;
- broken lineage is distinguished from tampering and from insufficient evidence;
- future Acceptance can require a successful replay verification result before promotion.
