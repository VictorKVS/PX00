# Tree_F — Repository Structure History

`Tree_F` stores concise, reviewable evidence of material PX00 repository-structure changes.

It is not a duplicate of Git history. Git records *what bytes changed*; `Tree_F` records *why the structure changed, what each material file is for, how it participates in the production chain, what dependencies/security implications exist, and how the decision can later be evaluated or reversed*.

## Core rule — accumulate, do not erase

`Tree_F` is an append-only development corpus for normal project evolution.

Accepted `TF-XXXX` files SHALL NOT be deleted, overwritten, renamed for convenience, or reused when the system changes. A new material structural state creates a new record with the next unique number.

```text
TF-0001
  ↓
TF-0002
  ↓
TF-0003
  ↓
...
```

An old record may become superseded, but it remains part of the development lineage. The successor references the earlier record instead of replacing it.

This accumulated corpus is intended to support architecture comparison, production-chain analysis, A/B evaluation, regression-test design, security/DevOps retrospectives, lessons learned and rollback decisions.

The only destructive exception is a formally authorized security/legal sanitation case (for example an accidentally committed secret or protected data). Such sanitation must preserve a public-safe tombstone or incident reference without reproducing the sensitive content.

## Canonical structure evidence

For repository/product structure, the canonical source is the Git-tracked file set, not the raw workstation filesystem.

Use:

```powershell
git ls-files
git status --short
git diff --name-status <base>..<head>
```

`tree /F` may be preserved as supplementary diagnostic evidence, but it SHALL NOT define the canonical PX00 architecture because it can contain `.venv`, caches, package-manager internals and other generated or ignored local state.

This distinction keeps structural history deterministic and comparable across developer machines and CI environments. See `TF-0016_2026-08-12_GIT_TRACKED_STRUCTURE_EVIDENCE.md`.

## Record rule

For every material structural change create one record:

`TF-XXXX_YYYY-MM-DD_SHORT-NAME.md`

and link it from [`../DEVELOPMENT_JOURNAL.md`](../DEVELOPMENT_JOURNAL.md).

TF identifiers are monotonically increasing and never reused.

A `TF` record is append-only by convention after the represented baseline is accepted. Corrections are made by a new record that references the superseded one.

## Minimum content

1. Change ID, date, status and trigger.
2. Structural delta / resulting tree.
3. File dossier for every material created, moved, removed or responsibility-changed file.
4. Data flow and processing/algorithm notes.
5. Libraries/runtime/external dependencies, or explicit `NONE`.
6. DevOps/CI/CD effect.
7. Security/privacy conclusion.
8. Tests/acceptance evidence.
9. Rollback method.
10. Evaluation and decision: `KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT`.

## File dossier fields

For each material file use only fields that add decision value:

- **Purpose** — why the file exists.
- **Trigger** — why it appeared or changed now.
- **Inputs / Outputs** — information consumed and produced.
- **Processing** — algorithm, rule or transformation; `NONE` for pure documentation.
- **Dependencies** — libraries, runtimes, services, standards or referenced contracts.
- **DevOps** — build/test/deploy effect.
- **Security** — threats, controls, data classification and secret handling.
- **Verification** — how to prove the file does what its contract says.
- **Decision** — keep/change/replace/rollback/experiment.

## Materiality rule

Do not create bureaucracy for trivial edits. A new `TF` record is required when a change materially affects at least one of:

- repository/module boundaries;
- role or protocol contracts;
- data model or data flow;
- security/compliance controls;
- runtime/dependency/build path;
- release/distribution structure;
- knowledge/provenance/audit model;
- test/acceptance model.

Formatting-only or typo-only changes remain visible in Git and normally need no `TF` record.

## Security rule

`Tree_F` is safe-to-publish metadata. Never place credentials, API keys, session data, private keys, customer secrets, raw personal data, or protected evidence here. Refer to sensitive evidence by controlled ID/hash/location only.

See [`TF-0002`](TF-0002_2026-08-11_APPEND_ONLY_DEVELOPMENT_CORPUS.md) for the accepted append-only lineage decision.
