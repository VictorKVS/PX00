# PX00 Development Journal

Canonical chronological index of material PX00 development decisions, structure changes, implementation evidence, tests, DevOps/security conclusions and later evaluations.

The journal answers five questions: **what changed, why, from what evidence, how it was verified, and what should happen next**.

Detailed structural dossiers live in [`Tree_F/`](Tree_F/README.md). Git remains the byte-level source of truth; this journal is the production-chain explanation layer.

## Rules

- Record material changes only; trivial formatting/typo edits stay in Git history.
- Link requirements/ADR/TF/test/security/release evidence rather than duplicating it.
- State `NONE` when no algorithm/library/runtime exists; never invent implementation details.
- Never record secrets, session material, private keys, unnecessary personal data or confidential customer content.
- Every material change ends with a lifecycle decision: `KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT`.
- A/B or alternative tests preserve both variants and common acceptance criteria.
- Accepted `Tree_F/TF-xxxx` records accumulate as an append-only development corpus; normal evolution creates new records instead of deleting or overwriting old ones.

---

## DJ-0001 — Repository initialization

**Date:** 2026-08-11  
**Status:** ACCEPTED  
**Decision:** KEEP

**Why:** Separate the governance/control-plane system from OSINT and legacy MindForge implementations and establish the brand-neutral canonical identity `PX-00` before runtime work.

**Evidence / files:**

- [Initialization record](journal/2026-08-11_INITIALIZATION.md)
- [Architecture Baseline 0.1](architecture/BASELINE_0_1.md)
- [FATHER Constitution](governance/FATHER_CONSTITUTION.md)
- [MindForge adoption matrix](legacy/mindforge/ADOPTION_MATRIX.md)

**Processing / libraries:** Documentation and declarative YAML only. No runtime algorithm or application library.

**DevOps:** Git/GitHub history only; runtime CI/CD intentionally absent at this phase.

**Security conclusion:** Public-repository baseline created; no runtime attack surface. `NO CODE BEFORE CONTRACT` remains active.

---

## DJ-0002 — Development production-chain traceability

**Date:** 2026-08-11  
**Status:** ACCEPTED  
**Decision:** KEEP

**Why:** Development itself must be measurable and improvable as a production chain. Git shows byte changes but not sufficient engineering rationale, dependency/security analysis, verification logic or later outcome assessment.

**Decision:** Introduce a root development journal plus `Tree_F` material structure-history records. Avoid total-event bureaucracy: capture material engineering changes only.

**Evidence / files:**

- [ADR-0008 — Development Production Chain and Structure History](architecture/adr/ADR-0008-development-production-chain-and-structure-history.md)
- [Tree_F protocol](Tree_F/README.md)
- [Tree_F template](Tree_F/TEMPLATE.md)
- [TF-0001 — Documentation and Governance Baseline](Tree_F/TF-0001_2026-08-11_DOCUMENTATION_BASELINE.md)

**Production chain:**

```text
Trigger
→ Requirement / Decision
→ Change
→ Tree_F evidence if structure/material responsibility changes
→ Contract/Test design
→ Implementation
→ Verification
→ DevOps/Security evidence
→ Evaluation
→ KEEP / IMPROVE / REPLACE / ROLLBACK / EXPERIMENT
```

**Algorithms / libraries:** No runtime code was added. The active method is a materiality filter plus repeatable evidence fields and coarse 0–5 comparative evaluation. Git and Markdown are the only current mechanisms.

**DevOps:** No CI/CD added yet. Future CI evidence will be referenced from the journal after executable schemas/tests exist.

**Security conclusion:** `PASS_WITH_ACTIONS`. No runtime dependency or attack surface introduced. Public-safe metadata rules are explicit. Before runtime: add evidenced secret scanning/PR controls, dependency/SBOM policy, data classification/retention, and security acceptance tests.

**Evaluation:** Initial TF-0001 scores traceability 5/5, security 4/5, maintainability 4/5. These are coarse decision aids, not statistical claims.

**Next gate:** Define canonical object model and Role Package contract before any application code.

---

## DJ-0003 — Tree_F becomes an append-only development corpus

**Date:** 2026-08-11  
**Status:** ACCEPTED  
**Decision:** KEEP

**Why:** Structural-history snapshots are valuable not only as documentation but as a cumulative dataset of engineering evolution. Deleting an old snapshot when the system changes would destroy the production lineage needed for later comparison, testing, rollback and process improvement.

**Decision:** Accepted `TF-xxxx` records are non-destructive for normal development. Every new material structural state gets the next unique TF identifier. Superseded decisions remain visible and are linked from successors.

**Evidence / files:**

- [TF-0002 — Append-only Development Corpus](Tree_F/TF-0002_2026-08-11_APPEND_ONLY_DEVELOPMENT_CORPUS.md)
- [Tree_F protocol](Tree_F/README.md)
- [ADR-0008](architecture/adr/ADR-0008-development-production-chain-and-structure-history.md)

**Production value:** The accumulated records become a development evidence corpus for architecture generations, A/B alternatives, regression cases, DevOps/IB retrospectives, role/process evaluation, lessons learned and rollback analysis.

**Algorithms / libraries:** `NONE` runtime. Current mechanism is deterministic numbering + Git/Markdown references.

**DevOps:** No build/deployment change. Future automation may generate candidate tree/diff evidence but must not silently rewrite accepted TF records.

**Security conclusion:** `PASS_WITH_EXCEPTION_RULE`. Normal history is append-only. Security/legal sanitation remains a controlled destructive exception for accidentally exposed secrets/protected content; it must leave a safe tombstone/reference without retaining the sensitive value.

**Tests / evaluation:** Verify that later material changes add `TF-0003`, `TF-0004`, ... while `TF-0001` and `TF-0002` remain present and addressable.

**Next gate:** Continue with Canonical Object Model and Role Package Contract; their structural introduction will create the next TF record.

---

## Entry template

```text
DJ-XXXX — title
Date / Status / Decision
Why
Evidence / links
Data & processing
Algorithms / libraries
DevOps
Security conclusion
Tests / evaluation
Next gate
```
