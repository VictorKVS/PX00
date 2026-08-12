# RISK-0003 — Reference Stores Are Not Durable System-of-Record Implementations

Status: OPEN
Severity: S3
Category: SOFTWARE / OPERATIONS
Source: ARGUS-SWE-001
Owner: ROLE-PRINCIPAL-ENGINEER

## Risk
Core registries are executable in-memory specifications, not crash-consistent multi-process persistence suitable for years of operation.

## Required mitigation
Define durable storage contracts, transaction semantics, schema migrations, backup/restore, recovery objectives and explicit labeling of reference implementations as non-production.
