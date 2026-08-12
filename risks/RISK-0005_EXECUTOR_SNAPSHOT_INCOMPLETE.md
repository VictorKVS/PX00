# RISK-0005 — Executor Snapshot Incomplete for Reproducibility

Status: OPEN
Severity: S3
Category: ARCHITECTURE / SOFTWARE
Source: ARGUS-ARCH-001
Owner: ROLE-ARCHITECT

## Risk
RUN pinning records model/executor identity but not a complete immutable runtime profile: provider/model build, role/system prompt version, adapter version, tool profile version and decoding/runtime parameters.

## Required mitigation
Introduce EXECUTOR_SNAPSHOT / AGENT_RUNTIME_PROFILE and pin its digest in RUN.
