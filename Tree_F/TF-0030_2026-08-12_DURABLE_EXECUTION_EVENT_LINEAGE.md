# TF-0030 — Durable Execution Event Lineage

Date: 2026-08-12
Status: implemented; CI validation pending on generation head
ADR: ADR-0025

## Material generation
PX00 material events now preserve governed execution lineage across ActionRequest, AuthorityDecision, PolicySnapshot and CapabilityGrant.

## Changed surfaces
- `schemas/EVENT_ENVELOPE.yaml`
- `px00/kernel/synthetic.py`
- `tests/test_synthetic_kernel.py`
- `architecture/adr/ADR-0025-durable-execution-event-lineage.md`

## Resulting trace
`EVT -> ACTREQ -> AUTH -> POLSNAP -> PolicyProfile@version`

For granted execution:
`EVT -> GRANT -> ACTREQ/AUTH -> Tool Boundary`

## Acceptance
CI must prove unit/integration tests, dependency consistency, secret hygiene and repository contract validation on the complete generation state.
