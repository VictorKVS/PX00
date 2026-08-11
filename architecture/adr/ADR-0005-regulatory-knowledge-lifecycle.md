# ADR-0005 — Regulatory Knowledge Lifecycle and Regional Releases

Status: ACCEPTED FOR BASELINE 0.1

## Context

Laws, regulations, standards, regulator guidance, industry rules, and corporate policies change over time. Regional deployments must not rely on stale or silently overwritten normative knowledge.

## Decision

Normative objects shall carry at minimum:

- canonical identifier;
- authority and jurisdiction;
- document/edition/version identifier;
- publication and effective dates where applicable;
- lifecycle state (`DRAFT`, `ACTIVE`, `AMENDED`, `SUPERSEDED`, `REPEALED`, `UNKNOWN`);
- source class and provenance;
- applicability rules;
- licensing/access metadata where relevant;
- supersession relationships.

Regional releases shall be composed from versioned jurisdiction/industry/organization profiles. Historical decisions remain linked to the profile versions and normative objects that were active for that decision context.

## Consequences

- Regulatory change can trigger impact analysis rather than silent RAG replacement.
- Regional releases remain reproducible.
- A normative conflict becomes an explicit object requiring interpretation/escalation.
- Copyright/licensing constraints for standards are represented separately from technical applicability.
