# RISK-0011 — Live Executor Provider Boundary Unproven

Status: OPEN
Severity: S3
Category: AI / PROVIDER / EXECUTION / ASSURANCE
Source: FFB-FP-0003 / MVP-EXEC-RUN-0001
Owner: FFB-ROLE-0006 Principal Software Engineer + FFB-ROLE-0007 Quality and Assurance Architect

## Risk
The governed executor boundary is proven only with local test-double workers. It has not yet been exercised against a live non-deterministic AI/provider interface with real provider failure modes, variable outputs, timeouts, malformed responses, model/version drift or external service trust assumptions.

## What is already proven
The local M1 boundary can:
- pin exact executor identity/version/provider/model metadata;
- bind invocation to the governed producer assignment and current stage;
- content-hash bounded input and candidate output;
- prevent structured authority/tool injection from becoming runtime authority;
- keep external effects disabled;
- preserve a rejected candidate and exact worker version;
- replace the worker after verifier FAIL through governed rework;
- keep verifier and Socrates downstream and independent.

## Why this risk remains open
A test double cannot prove provider authentication, transport behavior, rate limits, retries, timeout semantics, output-shape instability, provider-side model alias changes, prompt/context leakage, or adversarial/non-deterministic response behavior.

## Closure condition
Exercise exactly one bounded stage through an authorized live AI/provider adapter while:
- pinning provider/model/version as far as the provider permits;
- preserving request/output hashes and invocation record;
- allowing no material external side effect;
- keeping security-block regressions green;
- proving malformed/bad live output can be rejected and reworked;
- preventing provider response content from creating implicit authority;
- recording all residual provider/version limitations explicitly.

Until then, `SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR` remains OPEN.
