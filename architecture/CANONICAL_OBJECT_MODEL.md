# PX00 Canonical Object Model — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1  
**Scope:** governance/control-plane contracts only; no runtime implementation.

## Purpose

PX00 needs one small, stable vocabulary so roles, projects, journals, knowledge, security, tests and releases can refer to the same objects without relying on product names, folder names or LLM wording.

The model follows the minimum-sufficient rule: add a new object type only when it has a distinct lifecycle, authority, retention or audit meaning.

## Common object envelope

Every material PX00 object SHALL expose or be traceable to these common fields where applicable:

- `id` — immutable canonical identifier;
- `type` — canonical object type;
- `schema_version` — contract version used to interpret the object;
- `status` — lifecycle state;
- `created_at` — UTC timestamp;
- `created_by` — human, role or system identity;
- `project_id` — owning project when applicable;
- `trace_id` — execution trace when produced by a run;
- `classification` — information/security classification;
- `provenance` — references to source objects, evidence or prior decisions;
- `supersedes` / `superseded_by` — explicit lifecycle linkage where replacement occurs.

Display names and customer brands are metadata. Canonical IDs do not change during rebranding.

## Canonical object types

### Orchestration

| Prefix | Object | Meaning |
|---|---|---|
| `PRJ-` | Project | Governed project/product context and capability boundary. |
| `ROLE-` | Role | Versioned governed professional role package. |
| `TASK-` | Task | Requested unit of work with objective, constraints and acceptance conditions. |
| `RUN-` | Run | One bounded execution attempt of a task/protocol by a role/system. |
| `PROTO-` | Protocol | Versioned procedure controlling how a class of work is performed. |

### Source, evidence and knowledge

| Prefix | Object | Meaning |
|---|---|---|
| `SRC-` | Source | Identified origin of information; source itself is not automatically evidence. |
| `ART-` | Artifact | Preserved file/message/document/data object with integrity metadata. |
| `EVD-` | Evidence | Artifact/source observation admitted for a defined claim or analysis purpose. |
| `FIND-` | Finding | Analyst/reviewer conclusion derived from evidence; may be disputed. |
| `KN-` | Knowledge | Governed knowledge object admitted through a knowledge gate. |

### Governance and assurance

| Prefix | Object | Meaning |
|---|---|---|
| `REQ-` | Requirement | Obligation or need from stakeholder, regulation, standard, policy or design. |
| `DEC-` | Decision | Material choice with rationale, alternatives, authority and evidence. |
| `CTRL-` | Control | Governed measure used to satisfy requirements or reduce risk. |
| `RISK-` | Risk | Explicit uncertainty/threat with impact, treatment and owner. |
| `EXC-` | Exception | Approved, time-bounded deviation from requirement/control/protocol. |
| `TEST-` | Test | Repeatable verification procedure with expected result. |
| `EVAL-` | Evaluation | Scored or qualitative assessment of an object, run, role or outcome. |
| `REL-` | Release | Controlled releasable baseline or customer distribution identity. |

### Traceability

| Prefix | Object | Meaning |
|---|---|---|
| `EVT-` | Event | One material recorded occurrence. |
| `TRACE-` | Trace | Correlation identity joining events/objects into one execution or decision chain. |

## Core relations

The initial relation vocabulary is deliberately small:

- `requested_by`
- `performed_by`
- `governed_by`
- `derived_from`
- `supported_by`
- `contradicted_by`
- `satisfies`
- `mitigates`
- `implements`
- `verified_by`
- `evaluated_by`
- `approved_by`
- `supersedes`
- `produces`
- `included_in`

A relation SHALL not be invented merely for nicer prose if an existing relation preserves the required meaning.

## Production-chain example

```text
REQ-0001
  ↓ governed_by
PROTO-0004
  ↓ produces
TASK-0012
  ↓ performed_by
ROLE-0201
  ↓ execution
RUN-0031 / TRACE-0088
  ↓ uses
EVD-0041 + EVD-0042
  ↓ produces
FIND-0018
  ↓ supported_by
DEC-0007
  ↓ implements
CTRL-0012 / change
  ↓ verified_by
TEST-0009
  ↓ evaluated_by
EVAL-0004
  ↓ included_in
REL-0002
```

## Lifecycle rules

1. IDs are immutable and never reused for another object.
2. Material objects are not silently overwritten; replacement uses lifecycle status and `supersedes` links.
3. `SOURCE`, `ARTIFACT`, `EVIDENCE`, `FINDING` and `KNOWLEDGE` are deliberately distinct.
4. LLM output alone cannot create `EVD-*`.
5. `KN-*` requires an admitted provenance chain.
6. Material `DEC-*` requires authority, rationale and evidence references.
7. `RUN-*` is bounded and belongs to one `TRACE-*`; retries create new runs unless a protocol explicitly defines continuation semantics.
8. `EVT-*` records material occurrences; debug noise is not promoted into permanent governance evidence by default.
9. Regional/customer display terminology may change without changing canonical IDs.

## Security and privacy

- Classification and retention are contract fields, not afterthoughts.
- Secrets and raw protected data are referenced through controlled storage identities rather than copied into public governance records.
- Provenance must preserve integrity without forcing confidential content into this repository.
- Access decisions shall be based on canonical object identity and classification, not display name.

## Verification

The object model is acceptable for Baseline 0.1 when:

- every planned Role Package input/output can map to these objects;
- the development production chain can be represented without ambiguous object meanings;
- no two object types have the same lifecycle purpose;
- future event/provenance schemas can reference canonical IDs without renaming them;
- a rebrand can change all display names while the canonical chain remains unchanged.

## Decision

**Current disposition:** `KEEP / VALIDATE IN NEXT CONTRACTS`.

Do not add additional canonical types until a real requirement demonstrates that the existing vocabulary is insufficient.