# ADR-0009 — Canonical Object Model and Governed Role Package Contract

**Status:** ACCEPTED FOR BASELINE 0.1  
**Date:** 2026-08-11

## Context

PX00 needs stable identities and typed production objects before role execution, event tracing, knowledge admission, automated evaluation or runtime implementation can be safely designed. Role behavior also needs a contract stricter than a prompt so that knowledge, authority, protocols, tools, evaluation and traceability can evolve independently of a chosen LLM provider.

## Decision

PX00 adopts:

1. `architecture/CANONICAL_OBJECT_MODEL.md` as the minimum canonical vocabulary for orchestration, evidence/knowledge, governance/assurance and traceability objects.
2. `schemas/CANONICAL_OBJECT_ENVELOPE.yaml` as the initial common metadata contract for material governed objects.
3. `roles/ROLE_PACKAGE_CONTRACT.md` as the normative baseline for governed professional roles.
4. `roles/ROLE_TEMPLATE.yaml` as the minimum declarative role-package template.

Canonical identifiers are immutable and brand-neutral. Display names may change without changing identity or provenance.

A role is defined by its governed package, not by a prompt or model. The provider/model is a replaceable processing dependency and never becomes legal, factual or organizational authority by itself.

The initial object vocabulary is deliberately constrained. New canonical object types require a demonstrated lifecycle, authority, retention or audit distinction that cannot be represented by existing types.

## Security and assurance

- Role authority is explicit; absent authority means no authority.
- Material role work requires task/run/trace linkage.
- Secrets and protected raw data are not stored in public role/governance files.
- LLM output alone cannot be admitted as evidence.
- Material decisions require explicit rationale and provenance.
- Hidden chain-of-thought is not an audit requirement; explicit evidence, rationale, protocol steps and decisions are.

## DevOps / dependencies

No runtime code, CI/CD pipeline or third-party library is introduced by this ADR. YAML and Markdown remain declarative contracts only. Runtime validation technology is intentionally not selected before schemas and acceptance tests justify it.

## Verification

The decision is considered provisionally valid when upcoming Authority/Autonomy, Event/Trace/Provenance and Knowledge Admission contracts can use the adopted object vocabulary without ambiguous reinterpretation or object proliferation.

## Reversibility

If a canonical type proves redundant or insufficient during contract validation, the baseline may be superseded by a later ADR. Existing IDs and historical records remain preserved; they are not silently repurposed.

## Decision

`KEEP — validate through next contracts before runtime implementation`.