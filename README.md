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
- No material PASS without declared criteria and evidence.
- Material decisions are evaluated before execution and after outcome.
- Customer differentiation is implemented through controlled profiles and extensions, not uncontrolled source forks.

## Target architecture

PX00 provides the governance layer for roles, protocols, project registries, knowledge governance, decision records, audit/event traceability, jurisdiction/industry/organization profiles, assurance, and distribution composition.

Managed projects such as OSINT collection, analytics, engineering, security, and other domain products remain independently evolvable systems connected through explicit contracts.

## Baseline contracts

- [`architecture/CANONICAL_OBJECT_MODEL.md`](architecture/CANONICAL_OBJECT_MODEL.md) — stable canonical vocabulary and production-chain object distinctions.
- [`schemas/CANONICAL_OBJECT_ENVELOPE.yaml`](schemas/CANONICAL_OBJECT_ENVELOPE.yaml) — initial common metadata contract for material PX00 objects.
- [`roles/ROLE_PACKAGE_CONTRACT.md`](roles/ROLE_PACKAGE_CONTRACT.md) and [`roles/ROLE_TEMPLATE.yaml`](roles/ROLE_TEMPLATE.yaml) — governed professional-role contract and template.
- [`governance/AUTHORITY_AUTONOMY_CONTRACT.md`](governance/AUTHORITY_AUTONOMY_CONTRACT.md) and [`schemas/AUTHORITY_DECISION.yaml`](schemas/AUTHORITY_DECISION.yaml) — fail-closed authority, autonomy `A0..A4` and `ALLOW | DENY | ESCALATE` decisions.
- [`architecture/EVENT_TRACE_PROVENANCE_CONTRACT.md`](architecture/EVENT_TRACE_PROVENANCE_CONTRACT.md), [`schemas/EVENT_ENVELOPE.yaml`](schemas/EVENT_ENVELOPE.yaml) and [`schemas/TRACE_MANIFEST.yaml`](schemas/TRACE_MANIFEST.yaml) — material execution history and lineage.
- [`knowledge/KNOWLEDGE_ADMISSION_CONTRACT.md`](knowledge/KNOWLEDGE_ADMISSION_CONTRACT.md) and [`schemas/KNOWLEDGE_RECORD.yaml`](schemas/KNOWLEDGE_RECORD.yaml) — evidence/provenance-based knowledge admission.
- [`assurance/DECISION_EVALUATION_CONTRACT.md`](assurance/DECISION_EVALUATION_CONTRACT.md), [`schemas/DECISION_RECORD.yaml`](schemas/DECISION_RECORD.yaml) and [`schemas/EVALUATION_RECORD.yaml`](schemas/EVALUATION_RECORD.yaml) — material decision records plus ex-ante/ex-post evaluation.
- [`protocols/PROTOCOL_EXECUTION_CONTRACT.md`](protocols/PROTOCOL_EXECUTION_CONTRACT.md), [`schemas/PROTOCOL_DEFINITION.yaml`](schemas/PROTOCOL_DEFINITION.yaml) and [`schemas/RUN_RECORD.yaml`](schemas/RUN_RECORD.yaml) — bounded, authority-gated protocol execution with explicit retry/failure semantics.
- [`assurance/ACCEPTANCE_MODEL.md`](assurance/ACCEPTANCE_MODEL.md) and [`schemas/ACCEPTANCE_RECORD.yaml`](schemas/ACCEPTANCE_RECORD.yaml) — evidence-backed acceptance states and blocking/non-blocking criteria.
- [`architecture/adr/ADR-0012-protocol-execution-and-acceptance-model.md`](architecture/adr/ADR-0012-protocol-execution-and-acceptance-model.md) — current baseline decision linking governed execution with acceptance.

## Development evidence

PX00 development is treated as an auditable production chain, not only as Git history.

- [`DEVELOPMENT_JOURNAL.md`](DEVELOPMENT_JOURNAL.md) — chronological index: what changed, why, evidence, algorithms/dependencies, DevOps/security conclusion, evaluation and next gate.
- [`Tree_F/`](Tree_F/README.md) — append-only material repository-structure history and per-file engineering dossiers.
- `Tree_F/TF-0001..TF-0006` — accumulated structural generations; accepted historical records are not deleted during normal evolution.
- [`architecture/adr/ADR-0008-development-production-chain-and-structure-history.md`](architecture/adr/ADR-0008-development-production-chain-and-structure-history.md) — governing decision for the development evidence model.

Git remains the byte-level source of truth. The journal and `Tree_F` explain the production chain and support future `KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT` decisions, including controlled A/B comparisons.

## Current phase

`Architecture Baseline 0.1` — core contracts are now defined through protocol execution and acceptance. Runtime code remains blocked until the first governed `Analyst` and `Socrates/Critical Reviewer` Role Package pilots, their protocols and acceptance fixtures validate the architecture without ad-hoc semantics.

The repository does **not** claim conformity or certification to any standard merely because a standard is referenced or mapped. Formal conformance/certification requires the applicable assessment process.
