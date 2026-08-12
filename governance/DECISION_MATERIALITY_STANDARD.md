# PX00 / FATHER — Decision Materiality Standard

Status: **ACTIVE PROJECT NORM**
Norm ID: `PX00-NORM-DM-0001`
Scope: PX00, FATHER, Factory Builder, all governed roles, all professional domains consumed from KNOWLEDGE_CORE, and future digital/physical factories.

## 1. Constitutional rule

> **The higher the cost of error, irreversibility, uncertainty and risk of a decision, the stronger the mandatory evidentiary basis, independent review and approval must be.**

This is a project invariant, not optional guidance.

A role, agent, model, engineer, architect or manager may not reduce required evidence merely because a decision feels obvious, is called a "best practice", is common in the industry, is recommended by a vendor, or was suggested by an LLM.

## 2. Why this norm exists

Not every decision deserves the same process.

Requiring a full research dossier for a local variable name would create bureaucracy. Allowing a safety, security, architecture, legal or high-cost decision to proceed on intuition would create uncontrolled risk.

PX00 therefore uses a **decision materiality class** to scale governance effort to consequence.

`DECISION MATERIALITY != RISK SEVERITY != SYSTEM MATURITY != DELIVERY STAGE`.

Materiality answers: **how strong must the justification and review of this particular decision be?**

## 3. Materiality classes

### D0 — LOCAL / CONVENTIONAL
Typical examples:
- local variable naming;
- formatting;
- non-material refactor;
- reversible local implementation preference.

Minimum evidence:
- project/team convention, style guide, formatter/linter or explicit local rule.

Independent review: not required by materiality alone.

### D1 — IMPLEMENTATION
Typical examples:
- library/API usage;
- data structure choice inside a bounded component;
- retry or timeout policy with limited blast radius;
- test strategy for a component.

Minimum evidence:
- official/admitted technical reference;
- compatibility/version constraints;
- relevant project standard;
- executable test, measurement or other verification where material;
- known failure modes/limitations.

Independent review: risk-based.

### D2 — ARCHITECTURE / PRODUCT
Typical examples:
- database or storage model;
- service boundary;
- consistency model;
- cloud topology;
- build-vs-buy;
- metric family or threshold that drives business/technical action;
- reliability-vs-latency or cost-vs-performance trade-off;
- material dependency/vendor selection.

Minimum evidence:
- explicit requirements and hard constraints;
- assumptions separated from verified facts;
- viable alternatives where alternatives exist;
- explanation when only one feasible option remains;
- measurable decision criteria and rationale for those criteria;
- cost/resource view;
- risk/failure-mode view;
- authoritative/admitted technical sources;
- rejected-option rationale;
- verification/acceptance plan.

Independent review: normally required.

### D3 — REGULATED / SAFETY / CRITICAL
Typical examples:
- legal/regulatory compliance;
- safety envelope;
- cryptographic/security architecture with material impact;
- medical, industrial, financial or other critical decisions;
- irreversible material external effect;
- decisions with catastrophic or legally prohibited failure modes.

Minimum evidence:
- all applicable D2 evidence;
- admitted primary/normative sources with exact locators where applicable;
- explicit applicability determination;
- calculations/measurements where relevant;
- residual-risk statement;
- qualified independent review;
- explicit accountable approval/authority where required;
- unresolved S4 on the affected path blocks advancement unless eliminated or isolated under the existing risk policy.

Independent review: mandatory.

## 4. Classification dimensions

The declared class must consider at least:
- **cost of error / consequence** — money, harm, legal exposure, service loss, data loss, reputational or strategic damage;
- **reversibility** — how easily and safely the decision can be undone;
- **uncertainty** — quality/completeness of evidence and sensitivity to assumptions;
- **blast radius** — local, team, system, organization, customer/public, physical world;
- **regulatory/contractual criticality**;
- **security/safety criticality**;
- **dependency duration / lock-in**;
- **external material effect**.

The highest material dimension sets a floor. A low score in another dimension cannot average it away.

## 5. Risk-floor bridge

Risk severity and decision materiality remain separate, but risk can impose a minimum materiality:

- `S0–S1` do not by themselves raise the floor;
- `S2` normally requires at least D1 when the decision changes behavior;
- `S3` requires at least D2 on the affected decision path;
- `S4` requires D3 and retains the existing veto semantics.

A favorable expected-loss calculation cannot downgrade an S4/D3 obligation.

## 6. Promotion rule

A low-level decision is promoted when it can materially affect a higher-level property.

Examples:
- a variable name remains D0;
- choosing an unsafe deserialization function may become D2/D3 because security impact dominates the local code scope;
- a timeout constant may be D1 locally, but D2 if it determines an SLA or financial transaction outcome;
- an algorithm may be D1 in a toy tool, D2 in a high-load service, and D3 in a regulated/safety-critical control path.

## 7. Required decision derivation

For D2/D3, the normal derivation is:

`PROBLEM/GOAL → REQUIREMENTS → CONSTRAINTS → FACTS/ASSUMPTIONS → OPTIONS → METRICS/CRITERIA → EVIDENCE → CALCULATIONS/EXPERIMENTS → TRADE-OFF → DECISION → VERIFICATION → OUTCOME/LESSON`

Hard constraints eliminate options before preference scoring.

If 1,000 requirements reduce the feasible solution set to 3–5 options or one option, that is a valid result. The system must preserve why alternatives were eliminated.

The correct disposition may also be:
- `REQUEST_MORE_EVIDENCE`;
- `MULTIPLE_VALID_OPTIONS`;
- `ESCALATE`;
- `NO_GO`.

## 8. Anti-bureaucracy rule

Evidence depth must be **proportional**, not maximal.

Do not demand D3 ceremony for D0 work.
Do not use D0 convenience to hide a D2/D3 decision.

The purpose of this norm is to spend assurance effort where the cost of being wrong justifies it.

## 9. Anti-patterns

The following are never sufficient as the sole justification for a material D2/D3 decision:
- "best practice";
- "industry standard" without identifying the source;
- "everyone does it";
- "the architect/programmer prefers it";
- "the model recommended it";
- vendor marketing treated as independent proof;
- weighted scoring without rationale for weights;
- benchmark results from an irrelevant workload;
- precise estimates unsupported by source quality;
- copying an old decision without checking applicability/freshness.

## 10. Runtime / audit obligations

For material governed decisions PX00 shall preserve:
- declared materiality class;
- materiality rationale and triggering dimensions;
- evidence obligations and completion state;
- requirements/constraints and alternatives;
- knowledge/evidence snapshot references;
- creator/assignment;
- independent reviewer where required;
- approval/authority where required;
- verification plan and later outcome when observable.

Historical replay uses the evidence available at decision time. Reassessment under newer evidence creates a new/superseding decision; it does not rewrite history.

## 11. Factory Builder obligation

Factory Builder must assign evidence/review requirements when designing a role, protocol or factory. It may not defer materiality determination to an LLM at the final moment.

Every material role must know:
- which decisions it may make;
- typical materiality range;
- when to promote materiality;
- which evidence sources are acceptable;
- when independent review/approval is mandatory.

## 12. KNOWLEDGE_CORE relationship

Professional domains define **what counts as evidence** for that profession: laws, standards, vendor documentation, experiments, benchmarks, operating history, methodologies, metrics, calculations, etc.

PX00 owns the governance requirement for **how much evidence/review is required for a decision of a given materiality**.

Security Knowledge is the first reference implementation; the same evidence-first principle will be applied to architecture, software engineering, analytics, DevOps/SRE, AI/ML, finance, legal, construction, electrical engineering, safety, research and future manufacturing domains.

## 13. Enforcement

Machine-readable contract: `schemas/DECISION_MATERIALITY.yaml`.
Reference runtime gate: `px00/decision_materiality.py`.

A material decision that does not satisfy the minimum evidence/review floor must return a fail-closed disposition such as `INSUFFICIENT_EVIDENCE`, `REVIEW_REQUIRED`, or `BLOCKED_BY_RISK_FLOOR`; it must not silently proceed as accepted.
