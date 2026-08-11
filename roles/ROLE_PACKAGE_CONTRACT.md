# PX00 Governed Role Package Contract — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1  
**Parent decision:** ADR-0004

## Purpose

A PX00 role is not a prompt and not an LLM instance. It is a versioned professional contract that defines what the role knows, may do, must do, must not do, how it is evaluated, and how every material action is traced.

## Minimum Role Package

```text
roles/<role-id>/
├── ROLE.yaml
├── PROMPT.md
├── AUTHORITY.md
├── knowledge/
│   └── manifest.yaml
├── protocols/
│   └── manifest.yaml
├── schemas/
│   └── manifest.yaml
└── evals/
    └── rubric.yaml
```

The package may reference shared files instead of duplicating them. New files are added only when they carry distinct decision value.

## Required contract blocks

### Identity

- immutable `role_id`;
- canonical name;
- mutable display name;
- package version;
- lifecycle status;
- owner/maintainer.

### Mission and responsibility

The role SHALL state:

- purpose;
- responsibilities;
- required outputs;
- boundaries with other roles;
- escalation conditions.

### Authority

The role SHALL state:

- allowed action classes;
- prohibited actions;
- human-approval gates;
- tool permissions;
- data/classification limits;
- project/jurisdiction scope.

Absence of authority means no authority.

### Knowledge

Each role SHALL have a role-specific knowledge manifest and MAY reference:

1. constitutional/governance knowledge;
2. role-method knowledge;
3. domain knowledge;
4. jurisdiction/industry knowledge;
5. organization/project knowledge;
6. task evidence.

Knowledge access SHALL be versioned and traceable. RAG retrieval is an access mechanism, not proof that retrieved content is correct.

### Prompt/instruction set

`PROMPT.md` defines role behavior, but cannot override:

- Constitution;
- authority;
- protocol;
- security policy;
- applicable human approval requirements.

Changing a model/provider does not change role identity.

### Protocols

The role SHALL reference approved `PROTO-*` objects for material work. Protocols define required steps, gates, inputs, outputs, retry/loop bounds and escalation.

### Inputs and outputs

Every material role action SHALL consume and produce canonical PX00 objects. Free text may be present inside those objects, but the execution boundary remains typed and traceable.

### Evaluation

Every role SHALL have an evaluation rubric covering, where applicable:

- correctness;
- evidence/provenance discipline;
- protocol compliance;
- security/compliance;
- uncertainty handling;
- completeness without unnecessary complexity;
- reproducibility;
- outcome quality after implementation.

Scores are decision aids, not claims of statistical precision.

### Journaling and traceability

Every material execution SHALL identify at minimum:

- `role_id` and role version;
- `TASK-*`;
- `RUN-*`;
- `TRACE-*`;
- protocol/version;
- knowledge package versions used;
- tool/action classes used;
- material input/output object IDs;
- approval/escalation outcome;
- evaluation references when available.

Internal hidden chain-of-thought is not required. Auditability is provided by explicit rationale, evidence, protocol steps and recorded decisions.

## Role versioning

A new role version is required when a material change affects any of:

- authority;
- prohibited actions;
- required protocol;
- knowledge admission/access policy;
- prompt behavior with decision impact;
- input/output contract;
- evaluation rubric;
- security or human-approval rule.

Typos and non-semantic formatting changes do not require a role version increment.

## Provider/model policy

A provider/model is declared as a processing dependency with capability constraints. It SHALL NOT become the source of legal, regulatory, organizational or factual authority merely because it generated an answer.

Role evaluation SHALL make it possible to compare provider/model variants under the same role contract when useful.

## Failure policy

A role must fail or escalate explicitly when:

- required evidence is missing;
- authority is insufficient;
- applicable protocols conflict;
- a security/compliance gate blocks the action;
- required human approval is absent;
- output cannot satisfy the declared schema;
- uncertainty exceeds the role/protocol's permitted threshold.

Silent fabrication, silent privilege expansion and silent conversion of hypothesis into fact are prohibited.

## Acceptance gate

Before a role may perform material production work, the package must have:

- valid identity/version;
- mission/responsibility;
- explicit authority and prohibitions;
- knowledge manifest;
- protocol manifest;
- I/O contract references;
- evaluation rubric;
- trace/journal requirements;
- security review status.

## Current decision

**Disposition:** `KEEP / instantiate only after authority and event contracts are completed`.