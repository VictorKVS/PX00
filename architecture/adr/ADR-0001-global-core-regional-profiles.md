# ADR-0001 — Global Core + Regional Profiles

Status: ACCEPTED FOR BASELINE 0.1

## Context

PX00 is intended to support deployments in multiple jurisdictions, industries, organizations, and customer environments without creating country-specific source forks.

## Decision

PX00 shall use a stable global governance/runtime core with layered policy/context profiles:

`Global Core -> Global Standards -> Jurisdiction -> Industry -> Organization -> Project -> Task`.

Country, industry, customer branding, terminology, applicability, and policy differences shall be represented through governed profiles, mappings, extensions, or adapters rather than scattered conditional logic throughout the core.

## Consequences

- Regional releases are compositions, not forks.
- Applicability must be explicit and versioned.
- Conflicting rules produce explicit conflict objects and escalation.
- Historical decisions remain bound to the profile versions used at decision time.
- UI localization and legal/regulatory regionalization are separate mechanisms.
