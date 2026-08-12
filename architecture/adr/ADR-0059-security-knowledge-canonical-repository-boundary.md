# ADR-0059 — Security Knowledge Canonical Repository Boundary

Date: 2026-08-12
Status: ACCEPTED

## Context
PX00/FATHER and KNOWLEDGE_CORE are separate projects with different responsibilities. `SEC-PROD-0001 Security Knowledge Base` already exists in `VictorKVS/KNOWLEDGE_CORE`, with its primary product tree under `security-knowledge/`, professional-domain registry under `father/domain-knowledge/`, and product roadmap under `father/product-roadmap/`.

During portfolio integration, duplicate Security Knowledge product/gate/coverage artifacts were briefly introduced in PX00. Keeping them would create two competing sources of product truth and a long-term drift risk.

## Decision
`VictorKVS/KNOWLEDGE_CORE` is the canonical repository for Security Knowledge product/domain truth.

Canonical ownership:
- `security-knowledge/` — Security Knowledge source/version/requirement/applicability/control/check/evidence/expert-review graph;
- `father/domain-knowledge/` — professional-domain registry and domain knowledge contracts;
- `father/product-roadmap/` — canonical product manufacturing roadmap.

PX00/FATHER owns:
- GOAL/PROJECT/PLAN/TASK orchestration;
- role/agent assignment;
- governed context requests;
- authority/capability/tool boundaries;
- RUN execution and trace;
- independent review/rework/acceptance;
- runtime risk/assurance evidence;
- Factory Builder organization/factory design.

PX00 SHALL NOT maintain a second Security Knowledge corpus, source backlog, coverage truth, VERIFIED state or expert-readiness truth.

## Canonical Security Knowledge pipeline
`SOURCE → VERSION → CHUNK → ATOMIC CLAIM/REQUIREMENT → APPLICABILITY → RELATIONS → CONTROL → CHECK → EVIDENCE → EXPERT REVIEW`

`VERIFIED` requires an admitted primary source and exact locator. Retrieval, RAG output, model memory or generated explanation cannot independently create VERIFIED knowledge.

## Parallel development rule
`SUMMIT-FFB-02 — first governed live AI executor` may proceed in parallel with Security Knowledge corpus population.

Live-provider readiness is not a blocker for `SEC-PROD-0001`.

If live models are later used for extraction, normalization or interpretation, their output remains candidate knowledge until it passes the canonical Security Knowledge provenance/review pipeline.

## Product architecture rule
Security Knowledge is explicitly **not ordinary RAG over PDFs**. Retrieval is a lower layer. Product value is the evidence-linked graph:

`requirement ↔ applicability ↔ control ↔ implementation ↔ check ↔ evidence ↔ risk`

plus expert evaluation and source-to-decision traceability.

## Cross-repository routing
PX00 keeps route-only records that resolve stable logical product/domain identifiers to canonical repository paths. Historical RUN/context records must pin the resolved version/content identity required for reproducibility.

`LOGICAL IDENTITY ≠ PHYSICAL LOCATION` remains valid if Security Knowledge is moved again later.

## Correction performed
Duplicate PX00 Security Knowledge coverage/readiness/source-backlog artifacts and duplicate runtime gate were removed. PX00 product/roadmap files were converted to route-only records. The canonical master roadmap now lives alongside the domain product roadmap in KNOWLEDGE_CORE.

## Consequences
Positive:
- one source of product/domain truth;
- no roadmap drift between repositories;
- FATHER can evolve independently from corpus ingestion;
- Security Knowledge can continue high-volume normative population without waiting for live AI integration;
- future roles can bind `KB-SECURITY` without hard-coding physical repository assumptions.

Cost:
- cross-repository version/routing integrity becomes an explicit integration concern;
- PX00 cannot infer product maturity from stale local copies;
- future automated context packaging must resolve and pin canonical KNOWLEDGE_CORE object/version identities.
