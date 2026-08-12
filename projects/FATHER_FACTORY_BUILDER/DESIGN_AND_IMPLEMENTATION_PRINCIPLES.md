# Design and Implementation Principles

## 1. Build factories around governed capabilities, not technologies
The permanent abstraction is `CAPABILITY`, not model, framework, robot, vendor, language or device. Technology is replaceable implementation.

## 2. Separate designer, operator, executor and auditor
Factory Builder designs the factory. FATHER operates/manages it. Specialist roles execute work. ARGUS and independent reviewers challenge it. No component may quietly collapse these responsibilities into one authority center.

## 3. Start from an authorized need, never from available technology
Sequence: beneficiary/problem -> desired outcome -> constraints -> acceptance -> capabilities -> organization -> executors. Never begin with "we have an LLM/robot, what can it do?" and retrofit the mission around it.

## 4. Reliability before speed at critical boundaries
Identity, authority, safety, provenance, immutable history, emergency stop, recovery and acceptance are designed for correctness first. Performance optimization may not weaken these boundaries.

## 5. Prototype aggressively inside a controlled risk envelope
Fast experiments are encouraged at M1/M2 when side effects are reversible and risks are contained. Prototype shortcuts must be labeled with the maturity level at which they expire.

## 6. S4 risks are not deferred
Critical risks must be eliminated, technically isolated or the affected capability disabled. Schedule pressure is not a treatment plan.

## 7. Every maturity increase pays down the corresponding risk debt
A prototype may carry known S2/S3 debt. A pilot or production system may not inherit that debt merely because the prototype was successful.

## 8. Design for reversibility
Prefer replaceable adapters, versioned contracts, migration paths, feature isolation and reversible deployment. Ask before each material decision: "What will it cost to undo this in two years?"

## 9. Stable identity is separate from physical location
Roles, capabilities, knowledge objects, risks, plans and factory blueprints use stable IDs. Repository, database, vendor and deployment location may change without rewriting history.

## 10. Evidence over authority
No FATHER, architect, reviewer or model is correct because of status. Material claims and maturity decisions require evidence appropriate to their consequence.

## 11. The broad mission never becomes unlimited authority
North Star guides design direction. Every real action is bounded by a concrete authorized goal, beneficiary, jurisdiction, policy, resources, safety envelope and acceptance criteria.

## 12. Treat every executor as fallible and potentially compromised
Agents hallucinate, humans err, software fails, sensors drift, vendors regress and devices can be compromised. Trust is explicit, scoped, revocable and independently verified where impact requires it.

## 13. Simulate before irreversible physical action
For cyber-physical factories, use model/simulation/digital twin, staged commissioning, safe test envelope and independent safety review where technically meaningful before live external effects.

## 14. Safety and security are different but coupled
Security asks who/what can cause an action. Safety asks what happens even when authorized components fail. Both must be modeled.

## 15. Resources are first-class architecture
A plan that ignores money, compute, energy, materials, equipment capacity, maintenance windows, supply chain or human attention is incomplete.

## 16. Quality is designed into the process, not inspected only at the end
Acceptance criteria, measurement method, tolerances, traceability, review and rework loops are created with the factory blueprint.

## 17. Physical factories require metrology and maintenance lineage
Calibration, sensor accuracy, maintenance, wear, component lifetime and configuration state become evidence, not informal operational notes.

## 18. Build for degraded operation and recovery
Specify timeout, retry, idempotency, fail-safe/fail-operational behavior, restart, backup, restore, manual takeover and disaster recovery before production maturity.

## 19. Prevent hidden coupling
No agent, database, prompt, API or machine becomes an undocumented source of truth. Dependencies must be explicit enough to assess blast radius and migration cost.

## 20. Prevent Goodhart failure
Metrics are observations, not the mission. Any KPI used to optimize actors must be reviewed for gaming, displacement of quality, perverse incentives and local optimization harming system outcomes.

## 21. Preserve dissent
Roles have a governed right to challenge, refuse unsafe/unauthorized work and escalate. Independent reviewers cannot be punished or overridden merely because their conclusion delays delivery.

## 22. Learn from weak signals, not only failures
Near-misses, anomalies, repeated manual workarounds, reviewer disagreements, unusual latency/cost, model drift and operator confusion are architecture signals and may become RADAR/RISK entries before an incident occurs.

## 23. Unknown risk is a permanent category
The project must assume important risks have not yet been imagined. Architecture reviews therefore ask what assumptions remain untested and deliberately run adversarial experiments.

## 24. Separate current truth from historical truth
Plans, policies, executor snapshots, knowledge packages, calibration state and factory blueprints are versioned. "What is true now" must never erase "what the system relied on then."

## 25. No production by feature count
A factory reaches M5 only when its required capabilities, risks, controls, recovery, operations, audit and evidence meet gates. More features do not compensate for weak assurance.

## 26. Prefer a smaller proven factory to a larger fragile one
Remove or isolate unproven capabilities rather than forcing a broad production claim.

## 27. Domain expertise is mandatory at the boundary of consequence
Factory Builder may generate structure and proposals, but medicine, industrial safety, civil engineering, energy, finance, law and other consequential domains require applicable specialist review and authorization.

## 28. Continuous architecture, not one-time architecture
Every major ADR, maturity transition, new executor class, new physical effect path, serious incident and material requirement change reruns Architecture Foresight and ARGUS review.

## 29. Design the extraction boundary from day one
This project is incubated inside PX00, but contracts, IDs and interfaces must allow later extraction into dedicated repositories/services without changing organizational meaning.

## 30. The factory must improve without silently redefining its mission
Learning may improve plans, processes, models and organization. Changes to purpose, authority, beneficiary scope or unacceptable-risk threshold require explicit governance, not automatic self-optimization.
