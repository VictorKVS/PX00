# FFBJ-0014 — Cross-Repository Knowledge Snapshot Pinning

Date: 2026-08-12
Related: TF-0067 / ADR-0060 / RISK-0012

## Factory Builder impact
A reusable factory role can now consume canonical knowledge from an external domain repository without binding its historical work to a mutable branch or copying the domain corpus into PX00.

New reusable pattern:

`ROLE KNOWLEDGE BINDING → ACTIVE ROUTE → IMMUTABLE KNOWLEDGE SNAPSHOT → CONTEXT PACKAGE → RUN`.

This is required for the long-term Factory Builder objective because future knowledge domains may live in different repositories/storage systems while Role Packages continue to reference stable logical spaces.

## Security domain proof target
`KB-SECURITY` now routes to canonical:
`VictorKVS/KNOWLEDGE_CORE/security-knowledge/`.

A real Security role is not yet proven end-to-end through the new snapshot boundary. Producer and consumer contracts exist; executable export/replay remains open under `RISK-0012`.

## Important separation
Snapshot integrity proves exactly which knowledge was supplied.
It does not prove:
- truth;
- applicability;
- control implementation;
- acceptance;
- authority.

Those remain governed by Security Knowledge verification/applicability/review and PX00 authority/acceptance controls.

## Reusable lesson
For every future domain KB:
`mutable discovery route` and `immutable RUN context` must remain separate concepts.

Do not solve reproducibility by copying knowledge into the consuming factory.

## Next Factory Builder evidence
Use one real VERIFIED Security Knowledge slice in the first Security-domain factory/FATHER loop after producer export is executable.
