# DJ-0040 — North-Star Capability Factory

Date: 2026-08-12
Tree_F: TF-0052
ADR: ADR-0046

## Strategic clarification
The present Agent Factory is a stage, not the end-state. PX00/FATHER is being designed as a long-lived management/governance operating system for mixed production organizations.

## Long-term path
1. Agent Factory.
2. Software and Service Factory.
3. Research Factory.
4. Robotic / Cyber-Physical Factory.
5. Generalized governed production organization.

## Architectural implication
Do not bind the management core to LLM-specific concepts. Roles declare responsibilities; tasks require capabilities; executors are replaceable and may eventually be models, humans, software, instruments, robots or machines.

## Architect responsibility
Future design work must proactively surface risks and irreversible decisions before the owner has to know their names. Each significant generation should ask:
- what assumption could fail later?
- what becomes expensive to reverse?
- which future horizon would this design block?
- what should be abstract now versus intentionally deferred?
- what risk may remain inside the current maturity envelope?
- what critical risk must be eliminated immediately?

## New future risk domains to track
Physical safety, resource accounting, energy/material constraints, supply chain, quality/metrology, calibration, maintenance, research reproducibility, digital twins, human-machine coordination, environmental/legal constraints and incident/near-miss learning.

## Current result
The project remains focused on H1 Agent Factory, while the architecture now has an explicit rule that H2-H5 should extend the same governed core rather than force a rewrite.
