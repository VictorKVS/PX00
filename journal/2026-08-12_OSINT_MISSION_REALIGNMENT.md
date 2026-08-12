# DJ-0029 — OSINT Mission Realignment

Date: 2026-08-12
Tree_F: TF-0040
ADR: ADR-0035

## Audit result
The preceding generations built a strong governance, audit, replay, provenance and epistemic foundation, but the roadmap risked drifting toward a generic agent/knowledge platform.

The project goal is now explicitly restated: PX00/FATHER is a governed OSINT system focused on information search and collection, event monitoring, evidence research, and delivery of structured material to analysts.

## What existing work is for
- Authority/Policy/Tool Boundary: govern collectors and external access.
- RUN/EVT/Replay: prove what collectors and processors actually did.
- Source/Evidence/Claim graph: preserve provenance and investigative reasoning.
- Quality/Challenge/Socrates: challenge weak sources, contradictions and conclusions.

These mechanisms support OSINT operations; they are not independent product goals.

## Immediate development direction
Stop adding generic orchestration abstractions unless required by an OSINT scenario. Build the operational OSINT spine next: intelligence requirements, collection planning/jobs, source discovery/registry, raw capture, normalization/deduplication, entity/event extraction, monitoring, analyst handoff, research cases and an end-to-end OSINT pilot.
