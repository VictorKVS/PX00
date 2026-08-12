# ADR-0049 — Factory Builder Core Staff and Role/Knowledge Doctrine

Date: 2026-08-12
Status: accepted
Project: PROJECT-FFB-0001

## Context
Factory Builder cannot reliably design future factories as a single undifferentiated architect prompt. Factory design spans structural architecture, organization, knowledge, security/risk and later implementation/quality domains. The project therefore needs explicit professional roles whose responsibilities, authority, independence and knowledge are governed separately from any model assigned to them.

## Decision
Establish the initial Factory Builder staff:
- FFB-ROLE-0001 Chief Factory Architect;
- FFB-ROLE-0002 Enterprise and Systems Architect;
- FFB-ROLE-0003 Organization Architect;
- FFB-ROLE-0004 Knowledge Architect;
- FFB-ROLE-0005 Security and Risk Architect.

Each role is a reusable governed Role Blueprint, not a prompt or model identity. Each role has explicit non-responsibilities, authority ceiling, escalation, handoffs, evidence obligations, independence constraints, anti-Goodhart controls, known failure modes and continuity rules.

## Knowledge decision
Roles bind to stable logical knowledge spaces. A role may use several spaces and one space may serve several roles. Physical repositories may later split or migrate without changing logical knowledge-space IDs, object IDs, provenance or historical role bindings.

## Independence
The Chief Factory Architect integrates specialist outputs but cannot independently certify its own blueprint. Independent Socrates/ARGUS review remains outside the producer chain. Security/Risk may block an affected maturity path for unresolved S4 risk but cannot accept S4 risk.

## Consequences
Factory Builder can now evolve as an organization of replaceable specialists. Later model/provider changes do not rewrite professional responsibility. The next generation must add implementation/quality/capability roles and explicit collaboration protocols before SUMMIT-FFB-01 can be audited.
