# DJ-0038 — Long-Lived Architectural Risk Memory

Date: 2026-08-12
Tree_F: TF-0049
ADR: ADR-0044

## Completed
Created the first durable self-audit memory for PX00. Independent review findings can be promoted into stable `RISK-*` objects with ownership, likelihood, impact, severity, mitigation, verification, review cadence and append-only history.

## Why it matters
PX00 is expected to evolve for years. A weakness found in 2026 may still matter after a repository split, model replacement or major architecture revision. The system must remember not only what it decided, but what previously failed, what was merely accepted, what was mitigated but not proven fixed, and what risks have returned.

## Reliability rules
- no deletion of open findings;
- risk acceptance requires named accountability and rationale;
- resolution requires verification evidence;
- previously resolved risks can be reopened;
- mitigation is never automatically treated as resolution;
- physical relocation does not change logical risk identity.

## Progress impact
Future dashboards must show at least three different measures: implementation progress, audited progress, and unresolved material risk. A high implementation percentage must never hide a low audited maturity or accumulated critical findings.

## Next
ARGUS audit governance, auditor mandates, audit package snapshots, multi-reviewer verdict aggregation and milestone gates linked to this register.
