# RISK-0011 — Live Executor Provider Boundary Unproven

Status: MITIGATING
Severity: S3
Category: AI / PROVIDER / EXECUTION / ASSURANCE
Source: FFB-FP-0003 / MVP-EXEC-RUN-0001
Owner: FFB-ROLE-0006 Principal Software Engineer + FFB-ROLE-0007 Quality and Assurance Architect

## Risk
The governed executor boundary has not yet been exercised against an authorized live non-deterministic AI/provider interface. Real provider behavior may include transport/auth failures, rate limits, timeouts, malformed or oversized responses, output-shape instability, provider-side model alias drift, leakage and non-deterministic quality regressions.

## What is already proven
The local M1 executor boundary can:
- pin exact executor identity/version/provider/model metadata;
- bind invocation to the governed producer assignment and current stage;
- content-hash bounded input and candidate output;
- prevent structured authority/tool injection from becoming runtime authority;
- preserve a rejected candidate and exact worker version;
- replace the worker after verifier FAIL through governed rework;
- keep verifier and Socrates downstream and independent.

TF-0064 adds verified containment for the external provider boundary:
- HTTPS is mandatory;
- endpoint host must be explicitly allowlisted;
- endpoint userinfo is forbidden;
- live network use requires an explicit runtime enable flag;
- credential values are loaded only at runtime and are not stored in provider profiles/call records;
- request data classification must be explicitly permitted for provider egress;
- timeout and maximum response size are bounded;
- HTTP failure, invalid JSON and invalid response shape fail closed;
- request/response payload hashes, provider request ID and returned model ID are preserved when available;
- provider output remains candidate content and still flows through the existing governed executor/verifier/Socrates chain;
- secret-hygiene CI remains mandatory and was not weakened to accommodate the adapter.

## Why this risk remains open
A fake transport/driver can prove our boundary logic but cannot prove the external service itself. Remaining unknowns include:
- actual authentication/token lifecycle;
- provider rate limits and retry semantics;
- network timeout/error behavior;
- real response schema and provider error payloads;
- model alias/version behavior;
- prompt/context retention or provider data handling;
- real non-deterministic output quality;
- actual latency/cost behavior;
- live bad-output rejection and rework.

## Closure condition
Exercise exactly one bounded stage through an authorized live AI/provider driver while:
- pinning provider/model/version as far as the provider permits;
- preserving request/output hashes and provider call evidence;
- sending only explicitly allowed data classification;
- allowing no material external side effect beyond the provider inference call itself;
- keeping security-block regressions green;
- proving malformed/bad live output can be rejected and reworked;
- preventing provider response content from creating implicit authority;
- recording residual provider/version/data-handling limitations explicitly.

Until then, `SUMMIT-FFB-02 — FIRST GOVERNED LIVE EXECUTOR` remains OPEN.
