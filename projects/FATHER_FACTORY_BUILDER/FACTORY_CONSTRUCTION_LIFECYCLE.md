# Factory Construction Lifecycle

A factory is built in stages. Skipping a stage requires a recorded exception and may never bypass mandatory S4, authority, safety or legal gates.

## Stage 0 — Need and authorization
**Question:** what useful outcome is requested, for whom, by whom, under what authority?

Required outputs:
- beneficiary/problem statement;
- authorized goal;
- scope-in/scope-out;
- jurisdiction/policy constraints;
- harm/externality scan;
- measurable acceptance outcomes.

Gate: no factory design begins from a vague universal mission alone.

## Stage 1 — Capability decomposition
Translate outcomes into capabilities independent of implementation.

Examples: research, design, verification, procurement, manufacturing, testing, security review, logistics, support.

Required outputs:
- capability map;
- criticality classification;
- dependencies;
- required evidence and quality levels;
- capability failure consequences.

Gate: no executor/vendor selection before capability requirements exist.

## Stage 2 — Organization blueprint
Design departments, roles, responsibilities, segregation of duties, escalation and handoffs.

Required outputs:
- organization graph;
- role/responsibility matrix;
- review independence model;
- authority boundaries;
- human accountability points.

Gate: eliminate unowned responsibility and circular accountability.

## Stage 3 — Knowledge, resource and executor architecture
Bind knowledge spaces, data, budgets, materials, compute, equipment and eligible executor classes.

Required outputs:
- knowledge bindings;
- resource model;
- executor eligibility criteria;
- supply/vendor dependencies;
- trust levels and provenance.

Gate: role identity must remain independent of executor/vendor/device.

## Stage 4 — Safety, security, quality and recovery design
Before live execution, define how the factory fails safely and how results are proven.

Required outputs:
- threat and abuse cases;
- hazard analysis where applicable;
- security boundaries;
- emergency stop/manual override for applicable physical systems;
- quality plan and acceptance tests;
- backup/restore/recovery model;
- incident/near-miss process.

Gate: unresolved S4 means eliminate/isolate/disable affected path.

## Stage 5 — Simulation / dry run
Execute the factory logic using synthetic, sandboxed or simulated inputs and no unapproved external side effects.

Required outputs:
- traces;
- failure injection results;
- adversarial tests;
- performance/cost observations;
- discovered assumptions;
- new RADAR/RISK entries.

Gate: prototype only if critical controls behave as designed.

## Stage 6 — M1 prototype
Prove the minimum end-to-end production loop with reversible effects.

Objective: learn architecture, not maximize features.

Gate: all shortcuts explicitly tagged with expiry maturity.

## Stage 7 — M2 integrated prototype
Integrate real subsystems, models/providers and realistic data while staying inside controlled blast radius.

Required additions:
- idempotency/concurrency strategy;
- exact executor/configuration snapshots;
- durable-enough evidence lineage;
- independent review;
- cost/resource telemetry.

Gate: S3 debt may remain only where M2 policy allows it.

## Stage 8 — ARGUS summit audit
Independent architecture/security/software/organization skepticism.

Outputs:
- verdicts;
- findings;
- tensions/disagreements;
- risk treatments;
- audited maturity score.

Gate: implementation progress cannot substitute for audit.

## Stage 9 — M3 controlled pilot
Limited real users/beneficiaries/resources with explicit operational supervision and rollback.

Required additions:
- durable persistence;
- operational runbooks;
- recovery exercises;
- monitoring/alerting;
- support/escalation;
- approved residual risk.

Gate: S3 risks that exceed the M3 envelope block promotion.

## Stage 10 — M4 pre-production
Production-like scale and failure modes.

Required additions:
- capacity and load evidence;
- disaster recovery exercise;
- security testing;
- supply-chain review;
- compliance evidence where applicable;
- change/release governance;
- operational staffing model.

## Stage 11 — M5 production
Only after evidence-backed acceptance of capability, safety/security, quality, recoverability, audit and residual-risk ownership.

## Stage 12 — Continuous factory learning
Production is not the end.

Observe:
- outcomes vs intended need;
- quality and defects;
- incidents and near-misses;
- cost/energy/material efficiency;
- model/vendor drift;
- maintenance/calibration drift;
- human workarounds;
- reviewer disagreement;
- legal/environmental changes.

Outputs feed `FACTORY_REVISION`, PLAN revision, RADAR and RISK registers.

## Promotion rule
A factory advances by evidence and risk posture, never by calendar pressure or feature count.
