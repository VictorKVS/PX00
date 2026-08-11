# ADR-0008 — Development Production Chain and Structure History

**Status:** ACCEPTED  
**Date:** 2026-08-11

## Context

PX00 must be improvable as an engineering production system, not only as a codebase. It must remain possible to reconstruct what changed, why it changed, what files appeared, what data and algorithms are involved, which dependencies are used, which security controls apply, how the result was tested, and whether a later decision should keep, modify, replace, or roll back the change.

A complete event dump would create noise and unnecessary retention risk. The required control is therefore material-change traceability, not indiscriminate logging.

## Decision

PX00 establishes two linked evidence layers:

1. `DEVELOPMENT_JOURNAL.md` — root-level chronological production journal and index.
2. `Tree_F/` — immutable-by-convention structural snapshots and file dossiers for material repository-structure changes.

Every material structural change SHALL receive a `TF-xxxx` record linked from the development journal.

Accepted `TF-xxxx` records form an append-only development corpus. During normal engineering evolution they SHALL NOT be deleted, overwritten, renamed for convenience, or reused. New material states receive new monotonically increasing identifiers. A successor may supersede a prior decision but SHALL reference rather than erase the prior record.

The accumulated corpus is an intentional engineering dataset for architecture comparison, production-chain analysis, regression design, A/B and alternative evaluation, security/DevOps retrospectives, lessons learned and rollback.

The only destructive exception is an authorized security/legal sanitation event where retaining content would itself be unsafe or unlawful. Such action SHALL preserve a non-sensitive tombstone/incident reference and SHALL NOT reproduce the removed secret or protected data.

Each `TF-xxxx` record SHALL state, as applicable:

- trigger and decision basis;
- structure before/after or structural delta;
- purpose of each created/moved/removed material file;
- inputs, outputs and data flow;
- algorithms or processing rules;
- libraries, runtimes and external dependencies;
- DevOps/CI/CD implications;
- security and privacy implications;
- tests and acceptance evidence;
- rollback path;
- evaluation result and improvement decision.

Documentation-only files MUST explicitly state when no runtime algorithm or software library is involved instead of inventing implementation details.

## Evaluation model

A material change may be evaluated before and after implementation on a simple 0–5 rubric:

- correctness;
- traceability;
- security;
- maintainability;
- reproducibility;
- operational cost/complexity.

The score is evidence for comparison, not a claim of statistical precision.

Permitted lifecycle decisions:

`KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT`

A/B or alternative experiments SHALL identify variants explicitly (`A`, `B`, ...), use the same acceptance criteria where comparable, preserve evidence for both variants, and record the selected decision. Experiments MUST NOT silently overwrite the baseline.

## Security rule

The journal and `Tree_F` SHALL never contain secrets, credentials, private keys, raw session material, unnecessary personal data, or confidential customer content. Sensitive evidence is referenced by controlled identifier/hash/location rather than copied into the public repository.

## Consequences

Positive:

- development becomes auditable as a production chain;
- structural drift is visible;
- decisions can be compared and reversed;
- tests and future role evaluations can use historical baselines;
- knowledge about why a file exists is not lost;
- historical structural states accumulate into a reusable development evidence corpus.

Cost:

- every material structural change requires a short evidence record;
- retained history grows over time and therefore requires disciplined materiality, classification and later retention controls.

This cost is accepted. Records SHALL remain concise and materiality-driven in accordance with Occam's razor.
