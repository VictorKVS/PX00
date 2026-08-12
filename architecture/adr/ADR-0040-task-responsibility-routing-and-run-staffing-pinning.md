# ADR-0040 — Task-to-Responsibility Routing and RUN Staffing Pinning

Date: 2026-08-12
Status: accepted

## Context
PX00 has governed roles, responsibilities, agent assignments, knowledge bindings, and context packages. FATHER now needs a deterministic boundary that routes work to a duty-bearing role and pins the exact executor configuration used for a RUN.

## Decision
Tasks are routed by declared responsibility/duty code, not by hardcoded agent or model names. The selected responsibility determines the eligible role and protocol. Only ACTIVE agent assignments belonging to that role/department and carrying the required knowledge bindings are eligible.

Before material execution, the RUN pins:
- responsibility_ref
- role_id/version
- assignment_ref
- agent_id
- executor_type
- model_ref
- context_package_ref/hash

Later staffing/model changes MUST NOT rewrite active or historical RUN records.

## Critical boundaries
- routing does not grant tool authority
- responsibility does not select a provider directly
- assignment cannot expand role authority or knowledge scope
- context package must match RUN/ROLE/ASSIGNMENT lineage
- suspended/retired assignments cannot start new RUNs

## Consequences
FATHER can reason in organizational terms ("who is accountable for this duty?") while preserving exact technical reproducibility ("which model/agent actually executed this RUN?").
