# DJ-0037 — FATHER Management Cycle

Date: 2026-08-12
Tree_F: TF-0048
ADR: ADR-0043

## Completed
FATHER now has a reference management state cycle. It observes project state and records an append-only decision to dispatch ready work, wait, request review, replan, escalate blocked/failed work, or close accepted work.

## Corporate meaning
This is the first explicit director-level loop in PX00. FATHER does not perform the specialist task itself; it decides which governed organizational transition should happen next.

## Safety/governance boundary
A management decision cannot manufacture runtime authority. All material execution remains behind responsibility routing, pinned RUN state, AuthorityDecision, CapabilityGrant and Tool Boundary.

## Next
SOCRATES/reviewer operating model: review mandate, independence rules, finding severity, disposition, rework handoff and acceptance interaction.
