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
- [`roles/ROLE_PACKAGE_CONTRACT.md`](roles/ROLE_PACKAGE_CONTRACT.md) — governed professional-role contract.
- [`governance/AUTHORITY_AUTONOMY_CONTRACT.md`](governance/AUTHORITY_AUTONOMY_CONTRACT.md) — fail-closed authority and autonomy `A0..A4`.
- [`architecture/EVENT_TRACE_PROVENANCE_CONTRACT.md`](architecture/EVENT_TRACE_PROVENANCE_CONTRACT.md) — material execution history and lineage.
- [`knowledge/KNOWLEDGE_ADMISSION_CONTRACT.md`](knowledge/KNOWLEDGE_ADMISSION_CONTRACT.md) — evidence/provenance-based knowledge admission.
- [`assurance/DECISION_EVALUATION_CONTRACT.md`](assurance/DECISION_EVALUATION_CONTRACT.md) — ex-ante/ex-post evaluation.
- [`protocols/PROTOCOL_EXECUTION_CONTRACT.md`](protocols/PROTOCOL_EXECUTION_CONTRACT.md) — bounded, authority-gated protocol execution.
- [`assurance/ACCEPTANCE_MODEL.md`](assurance/ACCEPTANCE_MODEL.md) — evidence-backed acceptance states and blocking criteria.

Shared machine-readable contracts are kept under [`schemas/`](schemas/).

## First governed role pilots

Baseline 0.1 now has two concrete non-production Role Packages:

- [`ROLE-0201 Analyst`](roles/ROLE-0201-analyst/ROLE.yaml) — evidence-bound analysis, findings, knowledge/decision proposals and bounded evidence requests; maximum pilot autonomy `A1`.
- [`ROLE-0202 Critical Reviewer`](roles/ROLE-0202-critical-reviewer/ROLE.yaml) — display name `Socrates`; challenges evidence support, assumptions, contradictions, alternatives, falsifiability, source independence and scope without directly mutating accepted knowledge; maximum pilot autonomy `A1`.

Their governed protocols are [`PROTO-0201`](protocols/pilots/PROTO-0201_ANALYSIS.yaml) and [`PROTO-0202`](protocols/pilots/PROTO-0202_CRITICAL_REVIEW.yaml).

The declared pilot acceptance fixture is [`PILOT-0001`](assurance/fixtures/PILOT-0001_ANALYST_SOCRATES_ACCEPTANCE.yaml). Its current state is `NOT_TESTED`; these roles are not approved for production work.

Architecture decision: [`ADR-0013`](architecture/adr/ADR-0013-first-governed-role-pilots-analyst-and-critical-reviewer.md).

## Development evidence

PX00 development is treated as an auditable production chain, not only as Git history.

- [`DEVELOPMENT_JOURNAL.md`](DEVELOPMENT_JOURNAL.md) — chronological index: what changed, why, evidence, algorithms/dependencies, DevOps/security conclusion, evaluation and next gate.
- [`Tree_F/`](Tree_F/README.md) — append-only material repository-structure history and per-file engineering dossiers.
- `Tree_F/TF-0001..TF-0007` — accumulated structural generations; accepted historical records are not deleted during normal evolution.
- [`TF-0007`](Tree_F/TF-0007_2026-08-11_FIRST_GOVERNED_ROLE_PILOTS.md) — first concrete Role Package generation.

Git remains the byte-level source of truth. The journal and `Tree_F` explain the production chain and support future `KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT` decisions, including controlled A/B comparisons.

## Current phase

`Architecture Baseline 0.1` — core contracts and first pilot roles are defined. Runtime code remains blocked until `PILOT-0001` is executed as a controlled dry-run, acceptance evidence is recorded, contract gaps are assessed, and a decision is made on opening only the smallest justified runtime implementation.

The repository does **not** claim conformity or certification to any standard merely because a standard is referenced or mapped. Formal conformance/certification requires the applicable assessment process.
