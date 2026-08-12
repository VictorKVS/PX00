# ADR-0047 — Architect Foresight and Risk Radar

Date: 2026-08-12
Status: accepted

## Context
A long-lived system cannot rely on the owner already knowing every architectural, security, operational, organizational or cyber-physical risk. Unknown risks must be actively searched for before they become embedded in higher maturity levels.

## Decision
Introduce a mandatory Architect Foresight Loop and immutable `ARCHITECTURE_RADAR_ENTRY` records. Material decisions are reviewed for assumptions, reversibility, lock-in, blast radius, future-horizon conflicts and maturity deadlines.

The architect function must proactively propose `KEEP`, `EXPERIMENT`, `ABSTRACT_NOW`, `DEFER_WITH_GUARD`, `REPLACE` or `STOP`. Radar findings can create or modify durable `RISK-*` records and maturity gates.

## Consequences
- The project does not wait for the owner to name a risk before investigating it.
- Shortcuts remain visible as shortcuts with explicit replacement deadlines.
- Decisions that are expensive or practically irreversible receive earlier scrutiny.
- Future physical/cyber-physical expansion automatically raises safety and external-blast-radius review requirements.
- Architectural foresight becomes an auditable project function rather than an informal conversational habit.
