# TF-0005 — Knowledge Admission and Decision Evaluation

**Date:** 2026-08-11  
**Status:** ACCEPTED FOR BASELINE VALIDATION  
**Trigger:** DJ-0005 next gate; PX00 required governed knowledge admission and measurable decision improvement before role instantiation.  
**Decision:** KEEP / VALIDATE

## Structural delta

New material files:

```text
knowledge/
└── KNOWLEDGE_ADMISSION_CONTRACT.md

assurance/
└── DECISION_EVALUATION_CONTRACT.md

schemas/
├── KNOWLEDGE_RECORD.yaml
├── DECISION_RECORD.yaml
└── EVALUATION_RECORD.yaml

architecture/adr/
└── ADR-0011-knowledge-admission-and-decision-evaluation.md
```

Prior `TF-0001..TF-0004` records remain unchanged and addressable.

## Production chain introduced

```text
SRC/ART → EVD → FIND → Knowledge Gate → KN
                                  ↓
                               role/task
                                  ↓
                                 DEC
                                  ↓
                             action/result
                                  ↓
                                 EVAL
                                  ↓
                   governed improvement proposal
```

## File dossiers

### `knowledge/KNOWLEDGE_ADMISSION_CONTRACT.md`

**Purpose:** Defines when information becomes governed knowledge.  
**Trigger:** RAG/search/LLM output must not silently become institutional truth.  
**Inputs:** Sources, artifacts, evidence, findings, contradiction/applicability data.  
**Outputs:** `ADMIT | REJECT | REQUEST_MORE_EVIDENCE | ESCALATE` and governed `KN-*` when admitted.  
**Processing:** Provenance gate, contradiction review, temporal/scope check, explainable confidence.  
**Dependencies:** Canonical object model, authority/trace contracts; no runtime library.  
**DevOps:** Future RAG/vector/search technology remains outside the contract until justified.  
**Security:** Reduces hallucination-as-fact, stale regulation and cross-scope knowledge promotion risk; runtime must handle poisoning/access isolation.  
**Verification:** LLM-only claim cannot become active knowledge; supersession preserves history.  
**Decision:** KEEP / VALIDATE.

### `schemas/KNOWLEDGE_RECORD.yaml`

**Purpose:** Machine-readable metadata for admitted `KN-*`.  
**Trigger:** Knowledge lifecycle, provenance and confidence require testable fields.  
**Inputs:** Evidence/findings, scope, admission role/protocol/trace.  
**Outputs:** Versioned knowledge record.  
**Processing:** Declarative invariants; no executable validator selected.  
**Dependencies:** YAML/canonical IDs only.  
**DevOps:** Future schema validation candidate.  
**Security:** Classification/scope retained; protected content should be referenced rather than duplicated.  
**Verification:** Negative fixtures for missing evidence, unexplained numeric confidence and scope expansion.  
**Decision:** KEEP / VALIDATE.

### `assurance/DECISION_EVALUATION_CONTRACT.md`

**Purpose:** Makes decision quality measurable before action and after observed outcome.  
**Trigger:** PX00 needs a feedback loop capable of improving roles/protocols/KB from evidence.  
**Inputs:** Decision, evidence, rubric, evaluator, observed outcomes.  
**Outputs:** `EVAL-*`, lifecycle recommendation and improvement proposal references.  
**Processing:** Ex-ante/ex-post separation, dimension scoring 0–5/N/A, blocking criteria, A/B comparison rules.  
**Dependencies:** Canonical objects, authority/trace contracts. No scoring library.  
**DevOps:** Future benchmark/regression automation can consume the same contract.  
**Security:** Prevents security failures being averaged away; evaluation data must respect classification.  
**Verification:** Rubric version and negative outcomes remain immutable/addressable.  
**Decision:** KEEP / VALIDATE.

### `schemas/DECISION_RECORD.yaml`

**Purpose:** Canonical material decision record.  
**Trigger:** Decisions need authority, rationale, evidence, intended outcome and rollback/supersession links.  
**Inputs:** Requirements, evidence, knowledge, authority, risks/approvals.  
**Outputs:** `DEC-*` lifecycle record.  
**Processing:** Declarative contract only.  
**Dependencies:** YAML/canonical IDs.  
**DevOps:** Future decision-gate validator.  
**Security:** Material decisions cannot omit authority; sensitive rationale uses minimum necessary content.  
**Verification:** Missing authority/evidence blocks approval in future validator.  
**Decision:** KEEP / VALIDATE.

### `schemas/EVALUATION_RECORD.yaml`

**Purpose:** Comparable evaluation record for decisions/roles/runs/outcomes.  
**Trigger:** Scores need evidence, rubric version and anti-gaming constraints.  
**Inputs:** Target, rubric, evaluator, evidence/outcome.  
**Outputs:** `EVAL-*` plus lifecycle recommendation.  
**Processing:** Dimension score + basis; optional aggregate only with declared method.  
**Dependencies:** YAML/canonical IDs.  
**DevOps:** Future benchmark/regression result format.  
**Security:** Blocking security/compliance failures cannot be hidden by averages.  
**Verification:** A/B variants and failed results remain separately traceable.  
**Decision:** KEEP / VALIDATE.

### `architecture/adr/ADR-0011-knowledge-admission-and-decision-evaluation.md`

**Purpose:** Accepts the knowledge/evaluation feedback loop as a core architecture decision.  
**Trigger:** These contracts materially govern all future role learning and KB behavior.  
**Inputs:** Canonical object, authority and trace baselines.  
**Outputs:** Core invariants and deferred technology choices.  
**Processing:** ADR only.  
**Dependencies:** Repository contracts only.  
**DevOps:** Explicitly defers vector DB/RAG/evaluation platform selection.  
**Security:** Records poisoning, cross-tenant leakage, stale cache and rubric-gaming risks for runtime controls.  
**Verification:** First Analyst/Socrates pilots must fit without ad-hoc knowledge semantics.  
**Decision:** KEEP.

## Algorithms and libraries

Runtime implementation: `NONE`.

Contract algorithms/rules:

1. `SRC/ART → EVD → FIND → gate → KN`;
2. contradiction/scope/temporal checks before knowledge admission;
3. qualitative confidence by default; numeric only with named method;
4. `DEC → outcome → EVAL → governed improvement proposal`;
5. ex-ante and ex-post evaluation remain separate;
6. blocking security/compliance criteria cannot be averaged away.

Third-party libraries introduced: `NONE`.

## DevOps conclusion

No runtime/CI dependency added. This gate deliberately avoids premature selection of vector databases, embedding/RAG frameworks and evaluation services.

## Security / privacy conclusion

**Result:** `PASS_WITH_ACTIONS`.

Controls improved:

- evidence required before material knowledge admission;
- contradiction preservation;
- scoped/temporal knowledge lifecycle;
- explicit authority and trace on decisions;
- evaluation anti-gaming rules;
- sensitive-data minimization.

Required before runtime:

- source trust/poisoning controls;
- tenant/project KB isolation;
- cache freshness/invalidation;
- evaluator separation where required;
- schema/fixture tests;
- access-control enforcement around retrieval and promotion.

## Evaluation

Coarse baseline score (0–5):

- Correctness/contract coherence: 4/5
- Traceability: 5/5
- Security-by-design: 5/5
- Maintainability: 4/5
- Reproducibility: 4/5
- Complexity/cost: 4/5

Main uncertainty: no real Role Package has yet exercised the full chain.

## Rollback

Preserve this TF record. Any replacement creates successor ADR/TF records and explicit supersession links.

## Next gate

Define Protocol Execution Contract + Acceptance Model/fixtures, then instantiate Analyst and Socrates pilot Role Packages to validate the architecture before runtime code is broadly allowed.
