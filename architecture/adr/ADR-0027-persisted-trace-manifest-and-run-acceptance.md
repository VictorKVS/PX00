# ADR-0027 — Persisted Trace Manifest and RUN Acceptance

Status: Accepted
Date: 2026-08-12

## Context
Hash-chained events detect local sequence tampering, but a terminal RUN needs a durable summary artifact that can be independently referenced and verified later.

## Decision
Persist the verified TRACE_MANIFEST as canonical JSON with its own SHA-256 digest. A terminal RUN containing material events is not accepted as reproducibly complete unless its persisted manifest exists, its digest verifies, its RUN/TASK/TRACE context matches, and the manifest still matches the live event hash chain.

## Epistemic boundary
PX00 deliberately distinguishes integrity from truth. A valid hash proves that recorded evidence has not changed under the defined canonicalization and hash model; it does not prove that the original observation was factually true. Truth claims require provenance, independent evidence and evaluation layers above recorder integrity.

## Consequences
- RUN_RECORD gains trace_manifest_ref/hash linkage.
- Event-chain mutation after manifest persistence invalidates verification.
- Manifest mutation is independently detectable.
- Replay verification can be implemented without executing tools.
