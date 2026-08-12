# DJ-0019 — Durable Execution Event Lineage

Date: 2026-08-12
Tree_F: TF-0030
ADR: ADR-0025

## Work completed
Extended the canonical EVENT_ENVELOPE with ActionRequest, AuthorityDecision, PolicySnapshot and CapabilityGrant lineage. Updated the synthetic governed kernel so emitted material events carry RUN/TASK context, exact authority decision, snapshot ref/hash and the grant used for execution. Added runtime assertions for the successful tool event and denied authority event.

## Engineering observation
The repository already had `EVENT_ENVELOPE.yaml`; no second event schema was introduced. The existing canonical event contract was extended instead, preserving one event model.

## Current proof chain
`EVT -> ACTREQ -> AUTH -> POLSNAP -> exact PolicyProfile versions`

Granted execution additionally preserves:
`EVT -> GRANT -> Tool Boundary`

## Next gate
After green CI on the complete generation, implement a durable append-only event recorder/trace manifest boundary so lineage is not only present in in-memory dataclasses but persisted as verifiable execution evidence.
