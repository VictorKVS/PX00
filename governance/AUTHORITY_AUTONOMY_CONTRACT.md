# PX00 Authority and Autonomy Contract — Baseline 0.1

**Status:** DRAFT FOR BASELINE 0.1  
**Parent decisions:** ADR-0004, ADR-0009

## Purpose

PX00 separates professional capability from authority. A role, model, tool or protocol may be technically capable of an action and still have no authority to perform it.

The default rule is fail-closed:

> **Absence of explicit authority means no authority.**

## Effective authority

A material action is permitted only when all applicable scopes allow it:

```text
Role authority
∩ Protocol authority
∩ Project authority
∩ Organization policy
∩ Jurisdiction / regulatory constraints
∩ Tool permission
∩ Data-classification permission
∩ Required human approval
= Effective authority
```

No layer may silently expand authority granted by a stricter layer.

## Autonomy levels

### A0 — ADVISE

May analyze, explain, recommend and identify options.  
May not create an externally effective change.

Typical use: analysis, planning, critique, risk identification.

### A1 — PREPARE

May prepare drafts, plans, patches, documents, commands or proposed transactions.  
May not make them externally effective.

Typical use: draft contract, proposed configuration, code patch, proposed email.

### A2 — EXECUTE AFTER APPROVAL

May perform the explicitly approved action after a required human or governed approval is present and valid.

Approval must identify the governed object/action, scope and expiry or one-time nature where applicable.

### A3 — BOUNDED AUTONOMY

May execute automatically only inside a pre-approved, explicitly bounded and testable action class.

Required characteristics:

- defined scope and resource limits;
- reversible or safely compensatable where feasible;
- bounded retries/loops/time;
- explicit allowed tools and data classes;
- event/trace recording;
- failure escalation;
- no silent privilege expansion.

Typical use: approved repository linting, bounded information collection, low-risk housekeeping, scheduled verification.

### A4 — DELEGATED MATERIAL AUTONOMY

May perform material externally effective actions without per-action prior approval only when a separate governance decision explicitly delegates that authority.

A4 requires:

- named owner/accountable authority;
- documented legal/organizational basis;
- defined risk limits;
- continuous or periodic assurance;
- explicit stop/revoke mechanism;
- post-action review where required;
- immutable trace/provenance for material actions.

A4 is exceptional, not the default production level.

## Action risk and autonomy are separate

Autonomy level does not by itself determine whether an action is safe. Each material action also has a risk/impact classification determined by the applicable protocol.

A project or jurisdiction profile may cap autonomy below the role's package maximum.

Example:

```text
Role maximum: A3
Project maximum: A2
Protocol requires human approval: yes
Effective autonomy: A2
```

## Required authority decision

Before every material tool/action execution, the governing runtime SHALL be able to produce an authority decision containing:

- actor and role/version;
- requested action class;
- target/object;
- project/context;
- requested autonomy level;
- applicable role/protocol/project/policy constraints;
- data classification scope;
- approval references when required;
- result: `ALLOW | DENY | ESCALATE`;
- reason code and concise rationale;
- trace/event reference.

The decision records explicit rationale and evidence references, not hidden chain-of-thought.

## Deny / escalate conditions

The action SHALL be denied or escalated when any of the following applies:

- authority is absent or ambiguous;
- required approval is absent, expired or mismatched;
- the action exceeds role/project/protocol scope;
- data classification exceeds permission;
- applicable legal/policy constraints conflict;
- tool permission is unavailable;
- requested action cannot be bounded as required;
- required trace/provenance cannot be produced;
- a security or compliance gate blocks execution.

## Revocation and emergency stop

Authority must be revocable. A role, tool, project or autonomy grant can be suspended without changing canonical identity.

Emergency stop/revocation events are material assurance events and SHALL be traced.

## Provider/model rule

Model/provider capability never grants authority. A more capable model receives exactly the authority explicitly granted to the governed role and execution context.

## Acceptance tests before runtime

At minimum the future runtime must demonstrate:

1. missing authority → `DENY`;
2. missing required approval → `DENY` or `ESCALATE`;
3. stricter project cap overrides broader role grant;
4. data-classification mismatch blocks action;
5. A3 loop/resource bounds are enforced;
6. revocation takes effect without role-ID reuse;
7. every material authority decision is linked to the execution trace.

## Current disposition

`KEEP / validate with first instantiated roles and protocol tests before runtime autonomy is enabled`.
