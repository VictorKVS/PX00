# ADR-0007 — Canonical Identity and White-Label Distribution

Status: ACCEPTED FOR BASELINE 0.1

## Context

PX00 products may be distributed under customer-specific or regional commercial names. Branding must remain flexible without breaking technical identity, traceability, licensing obligations, security records, upgrade paths, or product lineage.

## Decision

Every product/module/role/protocol/control/event/release shall have a stable canonical identifier independent from display branding.

For PX00 itself:

- canonical product id: `PX-00`;
- repository: `VictorKVS/PX00`;
- package namespace: `px00`;
- architecture codename: `FATHER`;
- customer-facing display name: distribution/profile controlled.

Rebranding may change approved presentation-layer and distribution metadata such as product display name, logo, icon, visual theme, terminology, installer display name, document covers, support contacts, and approved customer profile configuration.

Rebranding shall not mutate canonical identifiers, database schema identifiers, event identifiers, protocol/control identifiers, migration identities, provenance, commit references, security identities, licenses/notices, SBOM identity, or audit history.

Customer differentiation shall use governed brand/customer/regional/industry profiles and explicit extensions rather than uncontrolled source forks.

## Consequences

- One maintained technical lineage can support many branded distributions.
- A distribution can be uniquely traced to core version, commit, profiles, SBOM, licenses, security evidence, and approvals.
- Customer-specific forks require an explicit architecture exception rather than being the default customization method.
