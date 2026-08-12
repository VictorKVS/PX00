# Risk and Failure Atlas

This atlas is intentionally incomplete. Its purpose is to make major risk classes visible and to define signals that reveal additional unknown risks during operation.

## A. Mission and beneficiary failure
Failure modes:
- wrong problem solved well;
- vague "human benefit" converted into uncontrolled optimization;
- hidden conflict between beneficiary groups;
- local benefit with unacceptable externality.

Detection:
- beneficiary review;
- scope challenge;
- externality analysis;
- outcome metrics vs activity metrics;
- ARGUS skeptic review.

## B. Architecture and abstraction failure
Failure modes:
- overengineering;
- premature generic platform;
- hidden coupling;
- single source of truth ambiguity;
- abstraction that fits agents but blocks robots/research later;
- irreversible schema/API decision.

Detection:
- reversibility test;
- dependency graph/blast-radius review;
- alternate implementation exercise;
- migration rehearsal;
- architecture radar.

## C. Organizational failure
Failure modes:
- responsibility without authority;
- authority without accountability;
- circular handoff;
- self-review;
- nobody owns failure;
- KPI gaming;
- agents hide uncertainty to satisfy FATHER.

Detection:
- RACI/responsibility audit;
- segregation-of-duties test;
- escalation drill;
- incentive review;
- disagreement/appeal telemetry.

## D. Executor/model failure
Failure modes:
- hallucination;
- prompt injection;
- compromised executor;
- provider behavior drift;
- model upgrade regression;
- hidden system-prompt/config change;
- inappropriate model chosen for capability.

Detection:
- exact executor snapshot;
- benchmark/regression suite;
- adversarial prompts;
- independent verifier;
- provider/model diversity for critical review;
- drift monitoring.

## E. Knowledge/data failure
Failure modes:
- poisoned source;
- stale knowledge;
- mutable content behind stable ID;
- provenance loss;
- copied sources mistaken for independent corroboration;
- data leakage/classification violation.

Detection:
- immutable version/digest;
- source/evidence assessments;
- independence groups;
- freshness gates;
- taint propagation;
- access/classification audit.

## F. Software/runtime failure
Failure modes:
- race conditions;
- duplicate execution;
- partial transaction;
- replay mismatch;
- state lost after restart;
- unbounded retry;
- silent exception;
- incompatible migration.

Detection:
- idempotency tests;
- concurrency/failure injection;
- crash/restart drills;
- migration/rollback rehearsal;
- trace completeness checks.

## G. Security failure
Failure modes:
- privilege escalation;
- confused deputy;
- forged identity;
- secret leakage;
- malicious dependency/vendor;
- tool abuse;
- audit tampering;
- lateral movement across agents/factories.

Detection:
- least privilege;
- independent authority boundary;
- SBOM/provenance;
- secret scanning;
- adversarial red-team tests;
- immutable trace verification;
- segmented blast radius.

## H. Safety and cyber-physical failure
Failure modes:
- authorized but unsafe action;
- sensor failure/drift;
- actuator runaway;
- stale world model;
- emergency-stop failure;
- unsafe recovery after network/power loss;
- human unexpectedly inside hazard zone.

Detection:
- hazard analysis;
- digital twin/simulation;
- interlocks;
- redundant sensing where consequence warrants;
- fail-safe design;
- emergency-stop tests;
- staged commissioning;
- domain safety expert approval.

## I. Resource/economic failure
Failure modes:
- plan technically works but is uneconomic;
- runaway API/compute cost;
- energy/material bottleneck;
- scarce equipment contention;
- maintenance cost omitted;
- critical vendor monopoly.

Detection:
- resource budget per plan/run;
- cost/energy telemetry;
- capacity model;
- alternate supplier analysis;
- lifecycle cost review.

## J. Supply-chain failure
Failure modes:
- unavailable critical component;
- counterfeit/unverified part;
- vendor discontinuation;
- malicious dependency/update;
- geopolitical/jurisdiction disruption.

Detection:
- supplier provenance;
- approved alternatives;
- inventory/lead-time monitoring;
- dependency lock/hash/SBOM;
- substitution testing.

## K. Quality/metrology failure
Failure modes:
- acceptance test does not measure real need;
- instrument calibration drift;
- tolerance stack missed;
- sampling hides rare defects;
- test environment differs from production.

Detection:
- measurement-system analysis;
- calibration lineage;
- independent QA;
- golden samples/fixtures;
- field-vs-test outcome comparison.

## L. Operations and maintenance failure
Failure modes:
- nobody knows how to recover;
- undocumented manual workaround becomes permanent;
- configuration drift;
- maintenance overdue;
- key operator dependency;
- alarm fatigue.

Detection:
- runbook exercises;
- configuration/version inventory;
- maintenance schedule;
- operator handover drills;
- alert precision metrics;
- workaround register.

## M. Legal, ethical and social failure
Failure modes:
- unauthorized processing/action;
- wrong jurisdiction assumption;
- unsafe/unfair allocation;
- hidden externality;
- automation removes accountable human decision point where required.

Detection:
- jurisdiction profile;
- legal/compliance review;
- beneficiary/impact analysis;
- explicit human accountability map;
- change monitoring.

## N. Self-improvement/control failure
Failure modes:
- factory changes its own objective;
- optimizer removes controls as "inefficient";
- learned policy widens authority;
- feedback loop amplifies bad metric;
- self-generated evidence validates self-generated claim.

Detection:
- immutable mission/authority boundary;
- change approval separation;
- anti-Goodhart review;
- independent evidence sources;
- no self-approval of critical changes.

# Unknown-risk discovery signals
Create a RADAR entry when any of the following appears repeatedly or materially:
- manual workaround;
- unexplained variance;
- near-miss;
- reviewer disagreement;
- repeated retry/rework;
- unexpected cost/latency spike;
- operator confusion;
- source contradiction;
- model/provider regression;
- unowned exception;
- test that passes while real outcome degrades;
- undocumented dependency;
- a component described as "temporary" beyond its expiry maturity;
- inability to reproduce an old result;
- inability to explain why the factory made a decision.

# Escalation doctrine
- S4: eliminate/isolate/disable now.
- S3: treat before maturity gate that forbids it; prototype may continue only inside bounded envelope.
- S2: track, assign owner and deadline/maturity trigger.
- S1/S0: improve/observe, but promote if recurrence or impact rises.

The atlas is versioned and expected to grow from incidents, audits, research and new factory domains.
