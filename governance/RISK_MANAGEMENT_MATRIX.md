# PX00 Risk Management Matrix

Date: 2026-08-12
Status: active governance baseline

## Principle
Reliability outranks speed at critical boundaries. Prototype velocity is allowed only inside an explicit risk envelope.

Each risk has two treatments:
1. **Immediate containment** — prevents the risk from causing unacceptable harm now.
2. **Final remediation** — removes/reduces the root cause before the maturity gate where the risk becomes unacceptable.

## Maturity levels
- M0 CONCEPT — contracts/architecture only; no material external effects.
- M1 PROTOTYPE — isolated executable reference models; synthetic/non-critical data.
- M2 INTEGRATED_PROTOTYPE — components connected; still sandboxed and reversible.
- M3 CONTROLLED_PILOT — bounded real use, human supervision, limited blast radius.
- M4 PRE_PRODUCTION — production-like persistence, recovery, security and operations controls.
- M5 PRODUCTION — durable enterprise operation and declared SLO/security posture.

## Severity gates
| Severity | Unresolved risk may progress through | Required treatment |
|---|---|---|
| S4 Critical | M0 only. Existing M1/M2 affected path must be quarantined immediately. | ELIMINATE or ISOLATE/DISABLE; acceptance is forbidden. |
| S3 Major | M2 with explicit containment and owner. | Must be reduced/closed before M3. |
| S2 Important | M3 with monitoring and treatment plan. | Must be reduced/accepted before M4. |
| S1 Improvement | M4 with owner and review date. | Resolve/accept before M5. |
| S0 Observation | Any, if tracked. | Monitor/document. |

A risk gate is **scope-aware**: a critical risk in one subsystem blocks that subsystem's maturity promotion, not unrelated work. However, a risk affecting Authority, identity, audit integrity, context integrity, persistence-of-record, or emergency control is a platform risk and may block the whole platform maturity claim.

## Treatment types
- ELIMINATE — remove root cause.
- REDUCE — reduce likelihood/impact with verified controls.
- ISOLATE — prevent the affected path from reaching higher-trust/material operations.
- DISABLE — turn off the unsafe capability.
- TRANSFER — move accountable operational exposure under an explicit external control/SLA; never transfers architectural accountability.
- ACCEPT — consciously accept residual risk; forbidden for S4.
- MONITOR — track evidence/trend; never sufficient alone for S3/S4.

## Current ARGUS-0001 matrix
| Risk | Sev | Immediate containment | Final remediation | Latest unresolved maturity | Current decision |
|---|---|---|---|---|---|
| RISK-0001 Knowledge context reproducibility | S4 | Do not claim historical semantic replay from ID-only Context Packages. Gate material replay/acceptance on versioned content digests. | Immutable `KNOWLEDGE_OBJECT_VERSION`; pin `version_id + content_digest` into Context Package hash and RUN. | M0 | FIX NOW |
| RISK-0002 Compromised agent/context poisoning | S4 | Treat external/model/tool/KB-derived content as UNTRUSTED; forbid untrusted context from creating authority/grants; sensitive actions require independent verification; retain emergency revoke. | Formal trust/taint model, provenance enforcement, injection defenses, independent verifier constraints, revocation/kill-switch tests. | M0 | CONTAIN NOW + REMEDIATE |
| RISK-0003 In-memory reference stores | S3 | Label as NON_PRODUCTION; synthetic/recoverable prototype state only. | Durable transactional system of record, migrations, backup/restore, RPO/RTO. | M2 | PROTOTYPE ALLOWED |
| RISK-0004 Concurrency/idempotency undefined | S3 | Single-writer/reference execution for prototype state changes. | object revision/etag, idempotency keys, transition preconditions, atomic transactions, race tests. | M2 | PROTOTYPE ALLOWED |
| RISK-0005 Executor snapshot incomplete | S3 | No strong reproducibility claim beyond pinned current fields. | `EXECUTOR_SNAPSHOT`: provider/build, system/role prompt version, tool profile, adapter, runtime parameters, digest pinned in RUN. | M2 | PROTOTYPE ALLOWED |
| RISK-0006 Reviewer independence not enforced | S3 | Human/manual independent review for critical prototype decisions. | reviewer eligibility, producer != reviewer assignment, independence groups/provider diversity where required, conflict-of-interest rules. | M2 | PROTOTYPE ALLOWED |
| RISK-0007 Incentive/Goodhart risk | S2 | Do not optimize agents on simplistic productivity KPIs. | Corporate Culture Charter: challenge/refusal/escalation rights, outcome metrics, no-fault reporting, anti-gaming controls. | M3 | TRACK |
| RISK-0008 Development ID collisions | S2 | Manual unique-ID check before new canonical artifacts. | CI uniqueness invariant for TF/DJ/ADR/RISK/AUDIT and canonical IDs. | M3 | FIX EARLY |

## Promotion gate
A component may be promoted from maturity `Mx` to `Mx+1` only when:
- no unresolved S4 affects the promoted scope;
- every S3/S2/S1 satisfies its severity maturity rule;
- containment controls have verification evidence;
- owner and next review date exist for remaining risk;
- ARGUS or designated independent reviewer signs the promotion package.

## Reliability rule
When two implementation choices meet the same functional requirement, prefer the design with stronger determinism, recoverability, auditability, isolation and failure containment, even if implementation is slower. Speed is an optimization only after the safety/reliability floor is satisfied.
