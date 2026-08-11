# ADR-0014 — Pilot Dry Run and Minimal Runtime Opening

**Status:** ACCEPTED  
**Date:** 2026-08-11

## Context

`PILOT-0001` exercised the first governed Analyst/Critical Reviewer chain against synthetic/public-safe cases covering supported claims, unsupported model output, material contradiction, authority denial and distinct provenance for equal payloads.

All declared blocking contract semantics were representable without adding ad-hoc canonical object types or privileges. The result is `PASS_WITH_ACTIONS`, not production approval, because enforcement and security properties remain untested in executable runtime.

## Decision

PX00 Baseline 0.1 opens a deliberately narrow implementation scope:

**Allowed:**

- local contract/schema validation;
- local fixture execution and reporting;
- synthetic/public-safe test data;
- deterministic canonical-ID/reference checks;
- local read-only loading of repository contracts;
- generation of acceptance evidence files without external side effects.

**Still prohibited:**

- production AI agents;
- live customer/protected data;
- network collectors or external system mutation;
- autonomous material actions above `A1`;
- live knowledge admission based only on model output;
- claims of runtime security, conformity or certification not proven by evidence;
- large orchestration/framework infrastructure before the minimal validator demonstrates need.

## Technology-selection rule

Implementation SHALL begin with the smallest dependency surface that can validate the existing contracts. No database, vector store, broker, workflow engine, web framework or LLM SDK is justified by this gate.

Because the source contracts are YAML, the first implementation may either:

1. use one narrowly pinned YAML parser dependency; or
2. convert only the machine-validated subset to a standard-library-readable representation if that demonstrably reduces lifecycle/security cost.

The choice must be recorded with dependency, supply-chain and maintenance implications before broadening runtime.

## Required first runtime tests

The first implementation must prove at minimum:

- required role-package files exist;
- canonical role/protocol IDs and versions are consistent across manifests;
- referenced files resolve inside the repository boundary;
- pilot acceptance fixture can be loaded and blocking criteria enumerated;
- missing/invalid critical fields fail closed;
- `ROLE-0201` and `ROLE-0202` remain capped at `A1`;
- prohibited external-side-effect action classes cannot be declared as allowed by the pilot packages without a failing validation;
- no secret values are required by the validator;
- outputs are deterministic enough to compare in CI later.

## Security conclusion

Opening minimal local validation code is accepted because it reduces ambiguity without adding material external attack surface.

Security obligations before any live AI/runtime integration remain: dependency/SBOM controls, secret scanning, non-bypassable authorization, tenant isolation, prompt-injection/provider leakage controls, retrieval poisoning/freshness controls, event integrity, cancellation/retry/durability tests and separation-of-duties enforcement where applicable.

## Consequence

`NO CODE BEFORE CONTRACT` is satisfied for this narrow validation scope only.

The new rule is:

> No broad runtime before executable contract evidence.

Production approval remains blocked.
