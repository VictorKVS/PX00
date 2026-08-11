# TF-0002 — Append-only Development Corpus

**Date:** 2026-08-11  
**Status:** ACCEPTED  
**Trigger:** Owner decision that structural-history files must accumulate rather than be replaced, forming a development evidence base.

## Decision

`Tree_F/` is an append-only development corpus for normal project evolution.

Accepted `TF-xxxx` records SHALL NOT be deleted, overwritten, or reused merely because the repository structure later changes. Each material structural state is represented by a new monotonically numbered record.

Normal sequence:

```text
TF-0001 baseline
   ↓
material change
   ↓
TF-0002
   ↓
material change
   ↓
TF-0003
   ↓
...
```

A later record may supersede an earlier engineering decision, but it does not erase the earlier record. The new record SHALL reference the predecessor/superseded record when relevant.

## Why

The accumulated records form a compact development evidence corpus suitable for:

- reconstructing the production chain;
- comparing architecture generations;
- evaluating why files/modules appeared or disappeared;
- A/B and alternative-design comparison;
- regression-test design;
- security and DevOps retrospectives;
- role/process evaluation;
- lessons learned and future improvement;
- rollback and historical audit.

Git remains the byte-level history. `Tree_F` is the engineering explanation and evaluation layer.

## Data model

Every record has a stable `TF-xxxx` identifier. Numbers are never reused.

A record may reference:

- previous TF record(s);
- ADR/requirement/decision;
- files created, moved, retired or responsibility-changed;
- tests and security evidence;
- evaluation result;
- successor/superseding TF record.

This creates a chronological lineage rather than a single mutable snapshot.

## Processing / algorithms

No runtime algorithm is introduced. The current method is deterministic document governance:

1. detect a material structural change;
2. allocate the next TF identifier;
3. capture structure/delta and file dossiers;
4. link evidence, tests and security conclusions;
5. evaluate the change;
6. preserve the record permanently for normal engineering history.

## Libraries / runtime

`NONE`. Markdown + Git/GitHub only.

## DevOps

No new runtime or CI/CD dependency. Future automation MAY generate candidate tree snapshots, diffs and links, but accepted records remain reviewable text artifacts committed to Git.

## Security conclusion

**PASS WITH EXCEPTION RULE.** Append-only history improves accountability and forensic reconstruction, but public repositories must not retain exposed secrets, protected personal data or material that must legally be removed.

Therefore the only permitted destructive exception is a documented security/legal sanitation event. If deletion or history rewriting is required, the sensitive value itself must not be copied into the replacement record. A public-safe tombstone/incident reference SHALL preserve the fact that sanitation occurred, why it was authorized, and what non-sensitive lineage remains.

## Verification

- prior accepted TF records remain present after later structural changes;
- each new material structural change receives the next unique TF number;
- journal links identify the corresponding TF record;
- supersession is represented by references, not deletion;
- security/legal sanitation follows the exception rule.

## Evaluation

- Traceability: **5/5**
- Reproducibility: **5/5**
- Maintainability: **4/5**
- Security: **4/5** until automated checks and retention/classification controls exist
- Complexity: **low** while materiality filtering is enforced

**Lifecycle decision:** `KEEP`
