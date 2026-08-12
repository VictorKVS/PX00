# RISK-0004 — Concurrency, Idempotency and Transaction Semantics Undefined

Status: OPEN
Severity: S3
Category: SOFTWARE / GOVERNANCE
Source: ARGUS-SWE-002
Owner: ROLE-PRINCIPAL-ENGINEER

## Risk
Concurrent workers can race on assignment, task state, plan activation, handoff and risk updates because object revisions, compare-and-set preconditions, idempotency keys and atomic transition boundaries are not yet defined.

## Required mitigation
Introduce revision/etag semantics, idempotency keys, transition preconditions, transaction boundaries and race-condition tests before multi-worker execution.
