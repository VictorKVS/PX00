# Tree_F — Repository Structure History

`Tree_F` stores concise, reviewable evidence of material PX00 repository-structure changes.

It is not a duplicate of Git history. Git records *what bytes changed*; `Tree_F` records *why the structure changed, what each material file is for, how it participates in the production chain, what dependencies/security implications exist, and how the decision can later be evaluated or reversed*.

## Record rule

For every material structural change create one record:

`TF-XXXX_YYYY-MM-DD_SHORT-NAME.md`

and link it from [`../DEVELOPMENT_JOURNAL.md`](../DEVELOPMENT_JOURNAL.md).

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
