# RADAR-0001 — Agent-Specific Executor Coupling

Date: 2026-08-12
Subject: PX00 execution abstraction
Horizon: H4_CYBER_PHYSICAL_FACTORY
Reversibility: EXPENSIVE
Lock-in risk: HIGH
Blast radius: ORGANIZATION
Maturity trigger: NOW
Recommendation: ABSTRACT_NOW

## Assumption
The current dominant executor type (LLM/agent) will remain representative of all future work.

## Failure mode
If RUN/task/authority contracts embed LLM-specific semantics, later research instruments, robots, industrial devices or humans require parallel management stacks or a core rewrite.

## Treatment
Keep ROLE/RESPONSIBILITY/TASK/CAPABILITY/AUTHORITY/RESULT as stable abstractions. Treat model/agent/device/human identity as executor adapters and snapshots.

## Result
ADR-0046 adopts capability-centric execution before additional agent-specific coupling accumulates.
