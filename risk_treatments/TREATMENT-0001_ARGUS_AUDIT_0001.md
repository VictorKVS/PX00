# TREATMENT-0001 — ARGUS AUDIT-0001 Risk Treatment Program

Date: 2026-08-12
Status: ACTIVE
Source audit: ARGUS_AUDIT_0001
Policy: `governance/RISK_MANAGEMENT_MATRIX.md`

## RISK-0001 — Knowledge context reproducibility — S4
Immediate: block ID-only historical semantic replay.
Implemented now: Context Package v0.2 pins object ID, version ID and SHA-256 content digest; tests cover same-ID content/version changes.
Final closure: CI green + immutable version semantics guaranteed by KB integration.
Target maturity: close before M1 for affected replay path.

## RISK-0002 — Compromised agent/context poisoning — S4
Immediate: context trust labels and fail-closed gate; context cannot create authority; tainted/untrusted content cannot directly drive sensitive material action.
Final closure: full threat model, taint propagation, injection handling, independent verifier, kill switch, quarantine/recovery, adversarial E2E tests.
Target maturity: verified isolation before M1 on material-action path; full residual-risk reduction before controlled pilot.

## RISK-0003 — In-memory reference stores — S3
Immediate: declare stores NON_PRODUCTION and use only synthetic/recoverable state.
Final closure: durable event/state store with transactions, migrations, backup/restore, RPO/RTO and recovery tests.
Preferred solution: PostgreSQL for authoritative multi-process state plus append-only event/audit storage; SQLite may be used only for local single-user development fixtures.
Target maturity: before M3 CONTROLLED_PILOT.

## RISK-0004 — Concurrency/idempotency — S3
Immediate: single-writer mode for prototype mutations.
Final closure: revision/etag on mutable aggregates, idempotency keys on commands, compare-and-swap preconditions, transaction boundaries, duplicate-delivery and race tests.
Target maturity: before M3.

## RISK-0005 — Executor snapshot incomplete — S3
Immediate: do not claim strong model replay beyond currently pinned fields.
Final closure: immutable EXECUTOR_SNAPSHOT containing provider, exact model/build, role/system prompt package version, adapter/tool profile versions, decoding/runtime parameters and snapshot digest pinned in RUN.
Target maturity: before M3.

## RISK-0006 — Reviewer independence — S3
Immediate: require manual/human independent review for critical prototype decisions.
Final closure: runtime eligibility gate requiring producer assignment != reviewer assignment, conflict-of-interest declaration, independence groups, and provider/model diversity for critical classes where justified.
Target maturity: before M3.

## RISK-0007 — Incentive / Goodhart — S2
Immediate: no optimization on simplistic task-count/speed KPIs.
Final closure: Corporate Culture Charter with right to challenge/refuse/escalate, no-fault reporting, outcome/evidence metrics, anti-gaming review and metric sunset rules.
Target maturity: before M4.

## RISK-0008 — Development ID collisions — S2
Immediate: manual ID search/check before canonical artifact creation.
Final closure: repository-wide CI scanner for globally unique TF/DJ/ADR/RISK/AUDIT IDs and stable canonical IDs; fail build on collision.
Target maturity: early, no later than M3.

## Priority order
1. RISK-0001 — eliminate now.
2. RISK-0002 — isolate now, then eliminate/reduce root causes.
3. RISK-0008 — cheap structural control; fix early to protect long-lived history.
4. RISK-0004 — transaction semantics before persistence implementation locks in bad assumptions.
5. RISK-0003 — durable persistence built on defined transaction semantics.
6. RISK-0005 — executor snapshot before serious replay claims.
7. RISK-0006 — independent review before autonomous pilot.
8. RISK-0007 — culture/KPI charter before optimization loops.

## Operating rule
Development continues on unrelated or safely contained prototype scopes. No component is promoted above its risk gate. Critical risk treatment takes precedence over feature velocity.
