# TF-0053 — Architect Foresight and Risk Radar

Date: 2026-08-12
Status: governance architecture accepted
ADR: ADR-0047

## Generation
Made proactive architectural foresight an explicit governed function rather than an informal expectation.

## New surfaces
- `schemas/ARCHITECTURE_RADAR_ENTRY.yaml`
- `governance/ARCHITECT_FORESIGHT_LOOP.md`
- `architecture/adr/ADR-0047-architect-foresight-and-risk-radar.md`

## Core rule
The project must actively search for unknown architectural/security/operational/organizational risks. The owner is not expected to know their names in advance.

## Mandatory dimensions
Assumption, failure mode, reversibility, lock-in, blast radius, future horizon, maturity trigger and recommended treatment.

## Outcome classes
KEEP / EXPERIMENT / ABSTRACT_NOW / DEFER_WITH_GUARD / REPLACE / STOP.

## Next
Use the radar during each major generation and SUMMIT; feed material findings into the durable risk matrix and ARGUS audit loop.
