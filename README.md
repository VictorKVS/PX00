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

- [`ROLE-0201 Analyst`](roles/ROLE-0201-analyst/ROLE.yaml) — evidence-bound analysis, findings, knowledge/decision proposals and bounded evidence requests; maximum pilot autonomy `A1`.
- [`ROLE-0202 Critical Reviewer`](roles/ROLE-0202-critical-reviewer/ROLE.yaml) — display name `Socrates`; challenges evidence support, assumptions, contradictions, alternatives, falsifiability, source independence and scope without directly mutating accepted knowledge; maximum pilot autonomy `A1`.

Their protocols are [`PROTO-0201`](protocols/pilots/PROTO-0201_ANALYSIS.yaml) and [`PROTO-0202`](protocols/pilots/PROTO-0202_CRITICAL_REVIEW.yaml).

## Pilot acceptance

[`PILOT-0001`](assurance/fixtures/PILOT-0001_ANALYST_SOCRATES_ACCEPTANCE.yaml) has now been executed as a manual contract dry-run with synthetic/public-safe objects.

- Dry-run evidence: [`PILOT-0001_DRY_RUN_2026-08-11.md`](assurance/runs/PILOT-0001_DRY_RUN_2026-08-11.md)
- Acceptance record: [`ACCEPTANCE-PILOT-0001.yaml`](assurance/records/ACCEPTANCE-PILOT-0001.yaml)
- Result: `PASS_WITH_ACTIONS`
- Production approval: **NO**

The dry-run verified the declared contract behavior for supported claims, unsupported model statements, contradictions, A1 authority denial and distinct provenance. It does not prove runtime enforcement or production security.

Architecture decisions: [`ADR-0013`](architecture/adr/ADR-0013-first-governed-role-pilots-analyst-and-critical-reviewer.md) and [`ADR-0014`](architecture/adr/ADR-0014-pilot-dry-run-and-minimal-runtime-opening.md).

## Minimal executable validator

The first code is intentionally narrow and local:

```text
requirements-validator.txt
px00/
├── __init__.py
├── __main__.py
└── validator.py

tests/
└── test_validator.py
```

Purpose: verify current PX00 contracts, pilot Role Packages, protocol bounds, acceptance gates, references, obvious high-risk secret fields and contiguous `Tree_F` numbering. It performs no network requests, model calls or external side effects.

Run locally:

```powershell
python -m pip install -r requirements-validator.txt
python -m unittest discover -s tests -v
python -m px00 .
python -m px00 . --json
```

Direct dependency: `PyYAML==6.0.3`. Tests use Python standard-library `unittest` rather than adding another framework dependency.

Evidence and controls:

- [`ADR-0015`](architecture/adr/ADR-0015-minimal-local-contract-validator.md)
- [`TF-0009`](Tree_F/TF-0009_2026-08-12_MINIMAL_CONTRACT_VALIDATOR.md)
- [`DEVSECOPS_BASELINE_0_1.md`](security/DEVSECOPS_BASELINE_0_1.md)
- [`VALIDATOR-0001 authoring verification`](assurance/runs/VALIDATOR-0001_AUTHORING_VERIFICATION_2026-08-12.md)

Authoring unit tests: `12/12 PASS`. Full validation against the owner's real local clone is the next acceptance gate; production runtime remains blocked.

## Development evidence

PX00 development is treated as an auditable production chain, not only as Git history.

- [`DEVELOPMENT_JOURNAL.md`](DEVELOPMENT_JOURNAL.md) — chronological index: what changed, why, evidence, algorithms/dependencies, DevOps/security conclusion, evaluation and next gate.
- [`Tree_F/`](Tree_F/README.md) — append-only material repository-structure history and per-file engineering dossiers.
- `Tree_F/TF-0001..TF-0009` — accumulated structural generations; accepted historical records are not deleted during normal evolution.
- [`TF-0007`](Tree_F/TF-0007_2026-08-11_FIRST_GOVERNED_ROLE_PILOTS.md) — first concrete Role Package generation.
- [`TF-0008`](Tree_F/TF-0008_2026-08-11_PILOT_DRY_RUN_AND_MINIMAL_RUNTIME_GATE.md) — pilot dry-run evidence and narrow runtime gate.
- [`TF-0009`](Tree_F/TF-0009_2026-08-12_MINIMAL_CONTRACT_VALIDATOR.md) — first executable validation generation.

Git remains the byte-level source of truth. The journal and `Tree_F` explain the production chain and support future `KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT` decisions, including controlled A/B comparisons.

## Current phase

`Architecture Baseline 0.1 — Executable Validation Gate`.

The contract-first gate is open **only** for a minimal local validator/fixture runner using synthetic/public-safe data and no external side effects. Production agents, live customer data, network mutation and broad orchestration infrastructure remain blocked.

The repository does **not** claim conformity or certification to any standard merely because a standard is referenced or mapped. Formal conformance/certification requires the applicable assessment process.
