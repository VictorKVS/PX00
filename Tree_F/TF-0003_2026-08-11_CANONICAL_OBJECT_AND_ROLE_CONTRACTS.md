# TF-0003 — Canonical Object and Role Contracts

**Date:** 2026-08-11  
**Status:** ACCEPTED  
**Decision:** KEEP / VALIDATE  
**Trigger:** Next gate after append-only development corpus: define the canonical object vocabulary and governed Role Package before runtime code.

## Structural delta

Added:

```text
architecture/
├── CANONICAL_OBJECT_MODEL.md
└── adr/
    └── ADR-0009-canonical-object-model-and-role-package-contract.md

roles/
├── ROLE_PACKAGE_CONTRACT.md
└── ROLE_TEMPLATE.yaml

schemas/
└── CANONICAL_OBJECT_ENVELOPE.yaml
```

No existing structural-history record was removed or overwritten.

## Production-chain purpose

```text
Constitution / ADR baseline
        ↓
Canonical object vocabulary
        ↓
Common object envelope
        ↓
Governed Role Package contract
        ↓
Role template
        ↓
NEXT: Authority + Event/Trace + Knowledge Admission contracts
        ↓
only later: runtime schemas/validators/tests/code
```

## File dossiers

### `architecture/CANONICAL_OBJECT_MODEL.md`

**Purpose:** Define one minimal stable vocabulary for Project, Role, Task, Run, Protocol, Source, Artifact, Evidence, Finding, Knowledge, Requirement, Decision, Control, Risk, Exception, Test, Evaluation, Release, Event and Trace.

**Why now:** All later schemas and role protocols need common IDs before implementation.

**Inputs:** Constitution, ADR-0003/0004/0006/0007/0008 and current production-chain requirements.

**Outputs:** Canonical prefixes, object distinctions, core relations, lifecycle/security invariants.

**Processing:** Classification by distinct lifecycle/authority/retention/audit meaning; redundancy-minimization by Occam rule.

**Libraries:** NONE.

**DevOps:** NONE now. Later becomes source for schema validation and contract tests.

**Security:** Positive. Prevents display-name/brand identity from becoming access-control identity; separates evidence from unverified source/model output.

**Verification:** Upcoming contracts must represent their flows without ambiguous or duplicate object types.

**Decision:** KEEP / VALIDATE.

### `schemas/CANONICAL_OBJECT_ENVELOPE.yaml`

**Purpose:** Machine-readable initial common metadata contract.

**Why now:** Prevent every future object/schema from inventing incompatible identity, lifecycle and provenance fields.

**Inputs:** Canonical Object Model.

**Outputs:** Required/conditional fields and invariants.

**Processing:** Declarative contract only; no executable validation.

**Libraries:** NONE; runtime validator deliberately not selected.

**DevOps:** Future CI may validate objects against a formal schema derived from this contract.

**Security:** Classification and provenance are first-class fields; protected content may be referenced rather than copied.

**Verification:** Compare future schemas against envelope invariants.

**Decision:** KEEP / formalize only when concrete schemas exist.

### `roles/ROLE_PACKAGE_CONTRACT.md`

**Purpose:** Define what a governed professional role is and what must exist before material production use.

**Why now:** Prevent role = prompt/model coupling and uncontrolled autonomy.

**Inputs:** ADR-0004 plus canonical object model and prior requirements for KB, RAG, protocols, journals, evaluations, traceability and human approval.

**Outputs:** Required identity, mission, authority, KB, prompt, protocols, schemas, evaluation, traceability, provider and failure contracts.

**Processing:** Contract decomposition; fail-closed authority model; version-on-material-change rule.

**Libraries:** NONE.

**DevOps:** Later enables lint/validation/regression gates for role packages.

**Security:** Positive. Explicit authority, prohibited actions, classification ceiling, human approval, tool scope and fail/escalate conditions.

**Verification:** Instantiate first real role only after Authority/Autonomy and Event contracts are defined.

**Decision:** KEEP.

### `roles/ROLE_TEMPLATE.yaml`

**Purpose:** Minimum declarative skeleton for future role packages.

**Why now:** Turn prose contract into repeatable fields without implementing runtime logic.

**Inputs:** Role Package Contract.

**Outputs:** Versioned role-manifest template.

**Processing:** NONE; declarative metadata.

**Libraries:** NONE.

**DevOps:** Future schema/lint target.

**Security:** Defaults are intentionally restrictive: no implicit authority, no secrets, provider not authority, retrieval not evidence.

**Verification:** First instantiated role must fill required fields without adding ad-hoc authority semantics.

**Decision:** KEEP.

### `architecture/adr/ADR-0009-canonical-object-model-and-role-package-contract.md`

**Purpose:** Make the object/role contracts an explicit architecture decision.

**Processing / libraries:** Documentation only / NONE.

**Security:** Records fail-closed authority and evidence/provenance rules.

**Decision:** KEEP.

## Algorithmic conclusion

No application algorithm exists yet. The only active design algorithms are:

1. **Materiality filter:** create distinct canonical types only for distinct lifecycle/authority/retention/audit meaning.
2. **Fail-closed authority:** absent permission is not permission.
3. **Provenance separation:** source → artifact/evidence → finding → knowledge/decision are not collapsed.
4. **Version-on-material-change:** semantic role contract changes create a new role version.

These are contractual algorithms/rules, not executable code.

## DevOps conclusion

No CI/CD or package dependency should be introduced yet. Selecting JSON Schema/Pydantic/other validation technology before concrete Event, Decision, Knowledge and Protocol schemas would create premature coupling.

## Security conclusion

**PASS_WITH_ACTIONS.** New files reduce architectural risk and introduce no runtime attack surface.

Required before first executable role:

- Authority/Autonomy contract;
- Event/Trace/Provenance schema;
- Knowledge Admission contract;
- data classification/retention rules;
- contract tests and security acceptance cases.

## Evaluation

| Criterion | Score | Basis |
|---|---:|---|
| Correctness | 4/5 | Internally coherent; must be validated by next contracts. |
| Traceability | 5/5 | Canonical IDs and production relationships are explicit. |
| Security | 5/5 | Fail-closed authority and evidence separation are baseline rules. |
| Maintainability | 4/5 | Small shared vocabulary; avoid adding types without evidence. |
| Reproducibility | 4/5 | Declarative templates exist; formal validator not yet chosen. |
| Complexity / Cost | 4/5 | Adds only five contract files; no runtime dependency. |

## Rollback / change path

Do not delete TF-0003. If the model is changed, create a new TF/ADR that explicitly supersedes affected contracts and preserves prior IDs/history.

## Next gate

Define **Authority/Autonomy Levels + Universal Event/Trace/Provenance contract**, then validate the Role Package against them before creating the first production role.