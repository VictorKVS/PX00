# PX00 Knowledge Admission Contract — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1

## Purpose

PX00 separates information retrieval from governed knowledge. RAG, search, LLM output and analyst text may help produce findings, but none of them becomes `KN-*` merely because it was retrieved or generated.

> **No material knowledge without evidence, provenance, applicability and review status.**

## Admission chain

```text
SRC / ART
   ↓
EVD
   ↓
FIND
   ↓
contradiction + applicability + provenance review
   ↓
Knowledge Gate
   ├─ REJECT / REQUEST_MORE_EVIDENCE
   └─ ADMIT
        ↓
       KN
```

For material/high-risk knowledge the protocol may require an independent reviewer or Socrates-style critical review before admission.

## Evidence rule

A knowledge object SHALL reference an admitted evidence chain sufficient for its claim and scope.

LLM output, RAG retrieval ranking or model confidence alone is not `EVD-*`.

A model-generated statement may become a `FIND-*` proposal, but it requires external or governed source/evidence support before knowledge admission.

## Required properties of admitted knowledge

Every `KN-*` SHALL define:

- immutable knowledge ID;
- knowledge type;
- canonical statement/concept;
- scope/applicability;
- provenance/evidence references;
- supporting and contradictory findings/evidence where material;
- confidence assessment and basis;
- temporal validity when applicable;
- jurisdiction/industry/project scope when applicable;
- admission protocol/version;
- admitting role/authority;
- review status;
- lifecycle state;
- supersession links when replaced.

## Knowledge types

Initial minimum vocabulary:

- `FACT` — evidence-supported claim about a state/event;
- `RULE` — governed normative/organizational rule;
- `CONCEPT` — defined concept/meaning;
- `METHOD` — accepted way to perform/evaluate work;
- `PATTERN` — repeatable observed relationship with stated limits;
- `HYPOTHESIS` — useful but not admitted as fact; may be stored only when clearly marked and protocols allow it.

A hypothesis SHALL NOT silently become a fact because it is repeated by later roles/models.

## Confidence policy

Confidence is explainable, not decorative precision.

Default confidence levels:

`LOW | MEDIUM | HIGH`

A numeric score may be added only when a named evaluation method defines how it is calculated and interpreted. Unexplained decimals are prohibited for material knowledge.

Confidence SHALL consider, where relevant:

- source quality/authority;
- evidence independence;
- directness of support;
- contradictions;
- temporal freshness;
- applicability match;
- reproducibility/verification.

## Contradiction policy

Contradictory evidence is not deleted to make the knowledge graph cleaner.

The gate may:

- lower confidence;
- narrow scope;
- mark knowledge `DISPUTED`;
- request additional OSINT/research;
- supersede prior knowledge;
- reject admission.

## Temporal and regulatory policy

Knowledge whose truth/applicability changes over time SHALL have validity metadata. Regulatory/normative knowledge additionally references authority, jurisdiction, edition/version and effective period where available.

A newer source does not silently overwrite historical knowledge. Replacement uses explicit lifecycle/supersession links so PX00 can reconstruct what knowledge was valid/available at a past decision time.

## Retrieval / RAG policy

RAG is a retrieval mechanism. Retrieval results SHALL preserve source identity, version and classification where available.

Retrieval SHALL NOT:

- grant evidence status automatically;
- remove contradictory context silently;
- bypass access/classification controls;
- replace knowledge-gate review;
- convert customer/private knowledge into shared/global knowledge without authority.

## Lifecycle

Initial lifecycle states:

`ACTIVE | DISPUTED | SUPERSEDED | RETIRED`

Rejected proposals remain represented by their source/evidence/finding/decision records rather than creating a misleading active `KN-*`.

## Admission outcomes

Knowledge Gate result:

`ADMIT | REJECT | REQUEST_MORE_EVIDENCE | ESCALATE`

The result SHALL preserve concise rationale, evidence references, protocol/version, role/authority and trace.

## Security and privacy

Knowledge classification cannot be lower than permitted by its protected inputs merely for convenience. Sensitive/raw content should be referenced from controlled storage rather than duplicated into governance records.

Knowledge promotion across organization/project/jurisdiction boundaries requires explicit authority and policy checks.

## Minimum acceptance tests before runtime

1. LLM-only statement cannot become evidence/active knowledge;
2. missing provenance blocks admission;
3. contradictory evidence remains addressable;
4. expired/superseded regulatory knowledge is not returned as currently active without warning;
5. project-private knowledge cannot be promoted globally without authority;
6. admitted knowledge records role/protocol/version and trace;
7. re-evaluation can supersede knowledge without deleting the old record.

## Current disposition

`KEEP / validate with first Analyst and Socrates Role Packages before production use`.
