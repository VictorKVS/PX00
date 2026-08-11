# PX00 Decision Evaluation Contract — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1

## Purpose

PX00 must be able to improve decisions, roles, protocols and knowledge using outcomes rather than intuition. Every material decision therefore carries explicit rationale and may be evaluated both before execution and after observed outcome.

The evaluation system is designed for comparison and learning, not decorative scoring.

## Decision record rule

Every material `DEC-*` SHALL identify:

- decision statement;
- decision owner/authority;
- task/project/trace context;
- requirement/problem being addressed;
- evidence and knowledge references;
- alternatives considered where material;
- rationale summary;
- assumptions and uncertainty;
- risks/constraints;
- approvals when required;
- intended outcome / acceptance criteria;
- lifecycle status and supersession links.

Hidden chain-of-thought is not required. The record preserves explicit decision rationale sufficient for review.

## Two evaluation moments

### Ex-ante evaluation

Performed before execution when required by protocol/risk.

Typical dimensions:

- evidence sufficiency;
- source/knowledge quality;
- alternatives coverage;
- requirement fit;
- security/compliance;
- uncertainty handling;
- reversibility/rollback readiness;
- expected operational cost/complexity;
- traceability/reproducibility.

### Ex-post evaluation

Performed after enough outcome evidence exists.

Typical dimensions:

- intended outcome achieved;
- defects/incidents/rework;
- unexpected side effects;
- estimate accuracy where applicable;
- security/compliance outcome;
- operational cost;
- maintainability;
- user/business effect;
- need to change role/knowledge/protocol/test.

## Scoring policy

Default comparable scale:

`0 | 1 | 2 | 3 | 4 | 5 | N/A`

Every score SHALL have either evidence/reference or a short stated basis. A single aggregate score SHALL NOT hide materially weak dimensions.

Weighted scoring is allowed only when the rubric declares weights before comparison. Post-hoc weight changes must be versioned.

Scores are decision aids, not claims of statistical certainty.

## Decision lifecycle

Initial states:

`PROPOSED | APPROVED | REJECTED | EXECUTED | SUPERSEDED | ROLLED_BACK | CLOSED`

Execution does not mean the decision was good. Outcome evaluation remains a separate `EVAL-*` object.

## Learning loop

```text
DEC
 ↓
implementation / action
 ↓
observed outcome
 ↓
EVAL
 ↓
LESSON candidate
 ├─ knowledge update
 ├─ role update
 ├─ protocol update
 ├─ test/regression update
 └─ no change
```

PX00 shall not silently modify a role or knowledge base because an evaluation score was low. Improvement proposals follow normal governed change/admission gates.

## A/B and alternatives

When controlled variants are useful:

- variants are explicit (`A`, `B`, ...);
- comparable acceptance criteria are declared before execution where possible;
- both result sets are retained;
- chosen/rejected variants remain traceable;
- customer/user exposure follows authority, privacy and safety rules;
- no variant silently replaces the baseline.

## Evaluator independence

Protocols may require a different role/reviewer from the decision creator for material/high-risk decisions. Self-evaluation is allowed only where policy permits and shall be marked as such.

## Calibration and anti-gaming

Evaluation quality itself is reviewable. PX00 should later compare predicted/ex-ante assessments with ex-post outcomes to detect systematic optimism, pessimism or rubric gaming.

No role may improve its own formal score by removing failed runs, contradictory evidence or negative outcome records.

## Security and compliance

Evaluation records may expose sensitive weaknesses, incidents or customer data. Store references/minimum necessary content under classification/retention rules.

Security/compliance failures cannot be averaged away by strong convenience/performance scores where policy defines them as blocking criteria.

## Minimum acceptance tests before runtime

1. material decision cannot be approved without required authority/evidence fields;
2. ex-ante and ex-post evaluations are distinguishable;
3. weak blocking security score cannot be hidden by aggregate average;
4. rubric version is preserved with each evaluation;
5. A/B results preserve both variants;
6. rollback/supersession preserves original decision/evaluation;
7. low score proposes improvement but does not silently mutate role/knowledge/protocol;
8. evaluator identity and trace are recorded.

## Current disposition

`KEEP / validate using first architecture decision and first governed role benchmark set`.
