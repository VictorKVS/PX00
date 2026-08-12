# ADR-0041 — Goal, Project and Dependency-aware Task Graph

Date: 2026-08-12
Status: accepted

## Context
PX00 can route a prepared task to a governed responsibility and pin the exact digital worker into a RUN. FATHER still needs a management layer above routing: objectives must become bounded projects and dependency-aware tasks before execution.

## Decision
Introduce GOAL, PROJECT and TASK_NODE plus a deterministic WorkGraph reference model.

A GOAL expresses desired outcomes and constraints but grants no authority. A PROJECT bounds work around one or more goals. TASK_NODE is the schedulable unit and declares a required duty code, dependencies, expected outputs and acceptance criteria. It never selects a model directly.

## Invariants
- goals are not executable instructions;
- projects reference known goals;
- task dependencies are explicit and acyclic;
- dependencies gate readiness;
- routing occurs by responsibility/duty, not model name;
- task completion requires declared acceptance criteria;
- runtime authority remains in the existing Authority/Grant boundary.

## Consequence
FATHER can begin managing work as an organization: decompose objective → build task graph → release ready tasks → route each task to a governed role/assignment → execute under pinned RUN state.
