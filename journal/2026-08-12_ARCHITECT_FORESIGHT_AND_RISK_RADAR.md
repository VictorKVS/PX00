# DJ-0041 — Architect Foresight and Risk Radar

Date: 2026-08-12
Tree_F: TF-0053
ADR: ADR-0047

## Completed
Architectural foresight is now an explicit project function. PX00 will no longer depend on the owner already knowing which risks or future constraints to ask about.

## Operating principle
For material architecture decisions, the architect must inspect assumptions, failure modes, reversibility, technology/vendor/device lock-in, blast radius, future-horizon conflicts and maturity deadlines.

## Required architect behavior
Proactively propose risks, alternatives and migration paths. Distinguish what should be abstracted now from what should remain intentionally concrete during prototyping. Critical/irreversible boundaries receive earlier scrutiny than reversible prototype internals.

## Link to risk management
Material radar findings become durable `RISK-*` entries and are governed by maturity gates. ARGUS remains the independent skeptical audit; the architect foresight loop is proactive design-time prevention. These are complementary, not substitutes.

## Long-term implication
As PX00 expands from Agent Factory toward software/service, research and cyber-physical factories, the same foresight mechanism will raise new domains automatically: physical safety, resources, supply chain, metrology, maintenance, environmental/legal constraints and human-machine coordination.
