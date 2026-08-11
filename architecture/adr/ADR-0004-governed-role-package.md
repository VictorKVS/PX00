# ADR-0004 — Governed Role Package Architecture

Status: ACCEPTED FOR BASELINE 0.1

## Context

A role implemented only as a prompt is not sufficiently controllable, auditable, testable, or evolvable for material organizational work.

## Decision

Each governed role shall be packaged as a versioned Role Package containing or referencing:

- canonical role identity and display identity;
- purpose, responsibilities, authority, prohibitions, escalation rules;
- prompt/instruction set;
- role-specific knowledge base;
- allowed shared/domain/project knowledge bases;
- protocols and decision gates;
- tool permissions and access policy;
- input/output schemas;
- evaluation rubric, benchmark cases, and regression cases;
- journaling, traceability, provenance, and retention requirements;
- human-approval requirements;
- supported processing providers/models.

The LLM/provider is a replaceable processing component, not the identity or authority of the role.

## Consequences

- Role versions can be evaluated and compared.
- Weaknesses can be attributed to knowledge, protocol, prompt, model, tool policy, or evaluation design rather than treated as one opaque agent failure.
- Role evolution requires versioning and regression evidence.
- Significant role actions remain attributable and reviewable.
