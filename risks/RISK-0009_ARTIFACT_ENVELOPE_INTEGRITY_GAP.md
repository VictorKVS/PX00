# RISK-0009 — Artifact Envelope Integrity Gap

Status: OPEN
Severity: S3
Category: EVIDENCE / PROVENANCE / SOFTWARE
Source: ARGUS-FFB-FUNC-001
Owner: FFB-ROLE-0004 / FFB-ROLE-0007

## Risk
The functional MVP currently hashes the canonical artifact payload, but the digest does not yet cover the complete evidence envelope: run identity, stage, artifact type, producer assignment and parent-lineage references.

For the current frozen in-memory dataclass MVP this is an acceptable restriction. Once artifacts are persisted, exchanged or replayed across processes, metadata tampering could preserve a valid payload digest while changing provenance semantics.

## Immediate containment
- keep the functional MVP synthetic, local and in-memory;
- do not treat the current digest as a production evidence signature;
- preserve explicit producer/stage/lineage checks in runtime;
- do not advance this evidence path beyond M2 without remediation.

## Required remediation
Create a canonical immutable artifact envelope and compute an envelope digest over identity + provenance metadata + payload digest. Persist and replay-verify the complete envelope.

## Exit evidence
- canonical envelope serialization tests;
- metadata tamper negative tests;
- persisted round-trip/replay verification;
- ARGUS re-review.
