# PX00

**Canonical technical identity:** `PX-00`  
**Repository:** `VictorKVS/PX00`  
**Architecture codename:** `FATHER`

PX00 is the governance and control-plane project for a family of traceable, auditable, policy-driven AI-assisted systems.

The project is intentionally brand-neutral. Customer-facing product names, regional names, logos, terminology, and distribution identities are configuration layers. Canonical technical identifiers, provenance, audit records, security identities, licenses, SBOM data, and traceability records are not changed by rebranding.

## Core principles

- No code before contract.
- Reliability > performance.
- Security and compliance by design.
- Global by architecture, regional by policy.
- LLM output is never evidence by itself.
- No material knowledge without provenance.
- No material decision without traceability.
- No autonomous action without explicit authority.
- Material decisions are evaluated before execution and after outcome.
- Customer differentiation is implemented through controlled profiles and extensions, not uncontrolled source forks.

## Target architecture

PX00 provides the governance layer for roles, protocols, project registries, knowledge governance, decision records, audit/event traceability, jurisdiction/industry/organization profiles, assurance, and distribution composition.

Managed projects such as OSINT collection, analytics, engineering, security, and other domain products remain independently evolvable systems connected through explicit contracts.

## Development evidence

PX00 development is treated as an auditable production chain, not only as Git history.

- [`DEVELOPMENT_JOURNAL.md`](DEVELOPMENT_JOURNAL.md) — chronological index: what changed, why, evidence, algorithms/dependencies, DevOps/security conclusion, evaluation and next gate.
- [`Tree_F/`](Tree_F/README.md) — material repository-structure history and per-file engineering dossiers.
- [`Tree_F/TF-0001_2026-08-11_DOCUMENTATION_BASELINE.md`](Tree_F/TF-0001_2026-08-11_DOCUMENTATION_BASELINE.md) — first complete structure baseline.
- [`architecture/adr/ADR-0008-development-production-chain-and-structure-history.md`](architecture/adr/ADR-0008-development-production-chain-and-structure-history.md) — governing decision for this evidence model.

Git remains the byte-level source of truth. The journal and `Tree_F` explain the production chain and support future `KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT` decisions, including controlled A/B comparisons.

## Current phase

`Architecture Baseline 0.1` — contract and governance definition only.

The repository does **not** claim conformity or certification to any standard merely because a standard is referenced or mapped. Formal conformance/certification requires the applicable assessment process.
