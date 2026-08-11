# PX00 / FATHER Constitution

Status: **DRAFT — Architecture Baseline 0.1**

## 1. Purpose

PX00 is a governance and control-plane system for managing AI-assisted roles, projects, knowledge, decisions, evidence, risk, compliance, assurance, and product distributions.

PX00 shall not treat an LLM as an authority, legal basis, source of evidence, or substitute for accountable human or organizational responsibility.

## 2. Immutable principles

1. No code before contract.
2. Reliability takes priority over performance and convenience.
3. Security, privacy, compliance, auditability, and recoverability are cross-cutting requirements.
4. Global by architecture, regional by policy.
5. Canonical technical identity is independent from commercial branding.
6. LLM output is never evidence by itself.
7. Material knowledge requires provenance and lifecycle state.
8. Material decisions require traceability to requirements, evidence, applicable rules, roles, protocols, and approvals.
9. Autonomous actions require explicit authority and bounded scope.
10. Material decisions shall be evaluated before execution and, where outcomes are observable, after execution.
11. Material disagreement, uncertainty, exception, or normative conflict shall be represented explicitly rather than silently resolved.
12. Rebranding shall not alter provenance, licensing, audit, security identity, SBOM, or supply-chain records.
13. Customer differentiation shall use controlled profiles and extensions instead of uncontrolled forks.
14. Regional, industry, organization, and project rules extend the global core without silently rewriting historical records.
15. Superseded knowledge, rules, decisions, and controls remain traceable.

## 3. Governance hierarchy

PX00 shall distinguish at least the following layers:

`Global Core -> Global Standards Profile -> Jurisdiction Profile -> Industry Profile -> Organization Profile -> Project Profile -> Task Context`.

Applicability is determined explicitly. A rule being present in a knowledge base does not by itself make it applicable.

## 4. Roles

A role is not merely a prompt. A governed Role Package shall contain or reference:

- canonical role identity and version;
- purpose, authority, duties, and prohibitions;
- system prompt/instruction set;
- role-specific knowledge base;
- permitted shared/domain/project knowledge bases;
- protocols and decision gates;
- tools and access policy;
- input/output schemas;
- evaluation rubric and regression cases;
- journal/audit requirements;
- escalation and human-approval rules.

The underlying LLM/provider is a replaceable processing component of the role.

## 5. Knowledge

Knowledge shall have identity, source/provenance, type, status, validity/lifecycle state, authoring role, review state, and links to supporting and contradicting evidence where applicable.

Raw source, evidence, analysis, hypothesis, decision, and approved knowledge are separate object classes.

## 6. Decisions

A material decision shall record at least:

- decision identity;
- requirement/problem being addressed;
- creator role and version;
- applicable protocol and version;
- evidence and authoritative sources;
- alternatives considered;
- declared assumptions and uncertainty;
- risks and exceptions;
- approval/authority state;
- resulting actions/artifacts;
- pre-decision evaluation;
- later outcome evaluation where meaningful.

PX00 records formalized rationale and evidence references. It does not depend on hidden model chain-of-thought for auditability.

## 7. Traceability and provenance

Material actions and artifacts shall be attributable, timestamped, linked by trace/provenance identifiers, and governed by retention/classification policy.

Technical logs, operation traces, and artifact/decision provenance are separate concerns even when implemented on shared infrastructure.

## 8. Compliance and standards

PX00 may be mapped to laws, regulations, standards, corporate policies, and contractual requirements. Mapping is not equivalent to certification.

Normative objects shall carry edition/version, authority, jurisdiction, effective dates, status, source class, and applicability rules.

Conflicts between applicable rules generate an explicit conflict object and escalation; they are not silently resolved by an LLM.

## 9. Product identity and distribution

Canonical product/module identifiers remain stable across branding and customer distributions.

Customer-facing names, visual identity, terminology, documentation covers, installer display names, and approved feature profiles may be composed at distribution time.

Each material distribution shall remain traceable to its core version, source commit, configuration/profile set, security evidence, license obligations, and SBOM/provenance records.

## 10. Improvement

PX00 shall support institutional learning through:

`Action -> Result -> Evaluation -> Lesson -> Knowledge/Role/Protocol Change Proposal -> Regression Test -> Governed Release`.

A role or protocol is not improved merely because its prompt was edited. Changes require versioning and evaluation.

## 11. Human accountability

Where law, regulation, contract, risk, or organizational policy requires accountable human authority, PX00 shall make that authority explicit and shall not simulate or bypass it.
