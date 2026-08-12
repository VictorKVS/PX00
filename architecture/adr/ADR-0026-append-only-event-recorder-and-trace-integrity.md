# ADR-0026 — Append-only Event Recorder and Trace Integrity

Status: Accepted
Date: 2026-08-12

## Context
PX00 material events now carry durable governance lineage, but synthetic runtime still returns them only in memory. The next proof must persist events without allowing silent rewrite and must make trace sequence tampering detectable before introducing a database or observability platform.

## Decision
PX00 SHALL implement a minimal filesystem-backed append-only event recorder for test/runtime proof. Events are serialized deterministically and appended as JSON Lines. Each recorded envelope SHALL include `previous_event_hash` and `event_hash`, where `event_hash = SHA256(previous_event_hash || canonical_event_payload)`. The trace manifest records ordered event refs/hashes, event_count, algorithm and chain head.

The recorder SHALL fail closed on trace/run/task mismatch and SHALL verify the full chain before reporting trace integrity PASS.

## Non-goals
No database, message broker, distributed consensus, WORM appliance or production log platform is authorized by this ADR.

## Security invariants
- append is the only normal event mutation operation;
- event identity cannot be reused within a trace;
- payload tampering changes the chain;
- deletion, insertion and reordering are detectable;
- trace/run/task lineage must remain consistent;
- recorder persists references and explicit summaries, not hidden chain-of-thought or unnecessary secrets.
