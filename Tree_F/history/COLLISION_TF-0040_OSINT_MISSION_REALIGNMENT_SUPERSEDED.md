# Historical collision record — former duplicate TF-0040 OSINT Mission Realignment

Original date: 2026-08-12
Original ID used: TF-0040 (duplicate)
Canonical status: SUPERSEDED / NON-CANONICAL
Reason for archival: rapid development reused TF-0040, violating Tree_F identity invariants. The OSINT-only mission realignment was subsequently rejected; OSINT remains an application domain of PX00/FATHER rather than the boundary of the whole system.

## Preserved original content

# TF-0040 — OSINT Mission Realignment

Date: 2026-08-12
Status: accepted
ADR: ADR-0035

## Decision
PX00/FATHER is explicitly realigned to its primary mission: governed OSINT collection, event monitoring, evidence research, and analyst handoff.

## Primary OSINT spine
1. INTELLIGENCE_REQUIREMENT
2. COLLECTION_PLAN
3. SOURCE_DISCOVERY
4. COLLECTION_JOB
5. RAW_SOURCE_CAPTURE
6. NORMALIZATION
7. ENTITY / EVENT EXTRACTION
8. PROVENANCE / EVIDENCE PACKAGE
9. ANALYST_HANDOFF
10. ANALYSIS / SOCRATES REVIEW
11. FINDING / ASSESSMENT
12. MONITORING / REASSESSMENT

## Existing work retained as assurance layer
- Policy / Authority / Tool Boundary
- RUN / EVT / Trace / Replay
- Source / Evidence / Claim provenance
- Claim and quality assessments
- Challenge / Review / Supersession

## Roadmap priority
Next generations must build the OSINT operational spine rather than deepen generic agent-platform abstractions.

## Immediate sequence
- TF-0041 Intelligence Requirement contract
- TF-0042 Collection Plan and Collection Job
- TF-0043 Source Registry / Discovery
- TF-0044 Raw Capture + provenance
- TF-0045 Normalization + deduplication
- TF-0046 Entity/Event extraction model
- TF-0047 Event monitoring / change detection
- TF-0048 Analyst Handoff Package
- TF-0049 Research Case / hypothesis-evidence matrix
- TF-0050 End-to-end OSINT pilot
