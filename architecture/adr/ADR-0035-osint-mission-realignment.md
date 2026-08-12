# ADR-0035 — PX00 OSINT Mission Realignment

Date: 2026-08-12
Status: accepted

## Primary mission
PX00/FATHER is a governed OSINT system. Its primary purpose is to collect open-source information, monitor events, preserve provenance/evidence, and deliver structured material to analysts for investigation and assessment.

## Core operational outcomes
1. Search and collect information from authorized open sources.
2. Normalize and preserve source/provenance metadata.
3. Detect, correlate, and monitor events over time.
4. Build evidence packages and claim/evidence graphs.
5. Route collected material to analysts with explicit uncertainty and provenance.
6. Support research workflows: hypotheses, competing explanations, evidence gaps, contradiction handling, and reassessment.
7. Maintain governed execution, auditability, and reproducibility of collection/analysis actions.

## Supporting, not primary, subsystems
Governance, authority, replay, acceptance, epistemic assessment, Socrates review, and tool control exist to make OSINT collection and analysis safer, traceable, and reliable. They are not the product goal by themselves.

## Non-goals for the current roadmap
- generic autonomous-agent platform unrelated to OSINT
- broad enterprise workflow automation
- arbitrary tool orchestration without an OSINT collection/analysis purpose
- metaphysical truth engine
- replacing the human analyst as final accountable decision-maker

## Target OSINT pipeline
`INTELLIGENCE_REQUIREMENT -> COLLECTION_PLAN -> SOURCE_DISCOVERY -> COLLECTION -> NORMALIZATION -> EVENT/ENTITY EXTRACTION -> PROVENANCE/EVIDENCE -> ANALYST PACKAGE -> ANALYSIS -> REVIEW/SOCRATES -> FINDING/ASSESSMENT -> MONITORING/REASSESSMENT`

## Architecture consequence
Roadmap priority shifts from deeper generic governance/epistemic abstractions to the operational OSINT spine: requirements, collectors, source registry, collection jobs, normalization, event/entity model, monitoring, analyst handoff, research cases, and evidence packages. Existing governance/evidence work remains the control and assurance layer under that spine.
