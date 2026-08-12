# ADR-0042 — Immutable Plan and Governed Replanning Lineage

Date: 2026-08-12
Status: accepted

## Context
FATHER can represent goals/projects/tasks and route ready work. Plans must evolve when evidence, policy, resources, requirements or critical review change, but silent mutation would destroy auditability.

## Decision
Introduce immutable PLAN revisions and explicit REPLAN_TRIGGER objects. A revision greater than one must identify the exact prior plan and the trigger that caused reconsideration. Activating a new revision supersedes the prior active plan without deleting it.

## Replan sources
NEW_EVIDENCE, TASK_FAILURE, BLOCKING_FINDING, REQUIREMENT_CHANGE, RESOURCE_CHANGE, POLICY_CHANGE, SOCRATES_CHALLENGE and HUMAN_DIRECTION.

## Invariants
- no in-place plan rewrite;
- revision lineage is sequential;
- cross-project supersession is forbidden;
- replanning does not grant runtime authority;
- evidence/reason for replanning remains inspectable.

## Consequence
FATHER can now answer not only what the current plan is, but why it changed and which earlier plan was active before the change.
