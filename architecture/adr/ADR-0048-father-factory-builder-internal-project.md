# ADR-0048 — Establish FATHER Factory Builder as an Internal Meta-Project

Date: 2026-08-12
Status: accepted

## Context
PX00/FATHER is evolving from an AI-agent orchestration system toward a governance and management operating system for many kinds of production organizations. If factory design remains implicit inside FATHER, the runtime manager will gradually accumulate architecture-generation responsibilities, blur accountability and become tightly coupled to the current Agent Factory implementation.

## Decision
Create `PROJECT-FFB-0001 — FATHER Factory Builder` as an explicit internal project under `projects/FATHER_FACTORY_BUILDER/`.

Factory Builder is responsible for designing and maturing factories. FATHER is responsible for managing/operating a constructed factory. Specialist roles execute factory work. ARGUS independently audits architecture/maturity/risk, and Socrates/reviewers challenge work products and evidence.

## Construction doctrine
Factory Builder follows an evidence-gated lifecycle:

`authorized need -> capability map -> organization blueprint -> knowledge/resources/executors -> authority/safety/quality/recovery -> simulation -> prototype -> ARGUS/risk treatment -> controlled pilot -> pre-production -> production -> continuous learning/revision`.

## Risk doctrine
Known risk classes are documented in a living Risk and Failure Atlas, but the project explicitly assumes unknown important risks exist. Near-misses, anomalies, reviewer disagreement, repeated workarounds, drift, irreproducibility and unexplained decisions become architecture signals that may create RADAR/RISK records.

Critical S4 risks are eliminated, technically isolated or the affected capability is disabled. Lower risks may remain inside the maturity envelope but must be paid down before the maturity gate that forbids them.

## Future separation
Factory Builder is incubated inside PX00 to avoid premature fragmentation. It is designed for later extraction without changing stable project, capability, role, risk, audit or historical lineage IDs.

## Consequences
- FATHER runtime does not become the permanent author of its own organizational architecture.
- Factory construction becomes reusable across agent, software, research and cyber-physical domains.
- architecture/risk knowledge discovered while building one factory can become reusable doctrine for future factories.
- future repository/service separation can follow demonstrated boundaries rather than guesses made too early.
