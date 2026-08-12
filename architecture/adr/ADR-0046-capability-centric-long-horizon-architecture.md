# ADR-0046 — Capability-Centric Long-Horizon Architecture

Date: 2026-08-12
Status: accepted

## Context
PX00 is currently implementing an agent factory, but the intended system may later coordinate software services, research workflows, laboratory instruments, robots and industrial machinery. Binding the management model to LLM/agent concepts would create a strategic dead end.

## Decision
Make `CAPABILITY` and governed `EXECUTOR` the long-lived execution abstractions. Roles own responsibilities; tasks declare required capabilities; eligible executors may be human, AI/model, software, simulator, instrument, robot or machine. Executor-specific behavior belongs behind adapters and domain safety profiles.

The management core remains centered on GOAL/PROJECT/PLAN/TASK/RESPONSIBILITY/ROLE/AUTHORITY/RESULT/EVIDENCE/REVIEW rather than any particular executor technology.

## Consequences
- Current agent implementations become one executor class, not the system identity.
- Future physical systems can reuse governance, planning, risk, audit and acceptance primitives.
- Cyber-physical expansion requires additional safety, simulation, asset, calibration, maintenance, resource and emergency-stop contracts before real-world autonomy.
- Broad mission statements never imply broad authority; material action remains bounded by explicit goal, policy, jurisdiction, risk and safety envelopes.
