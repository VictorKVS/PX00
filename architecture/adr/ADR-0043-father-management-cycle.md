# ADR-0043 — FATHER Management Cycle

Date: 2026-08-12
Status: accepted

## Context
PX00 now has governed goals, projects, task graphs, immutable plans, staffing and routing. FATHER needs an explicit management loop that observes organizational state and chooses the next management transition without becoming the specialist executor.

## Decision
Introduce append-only FATHER_MANAGEMENT_DECISION records and a deterministic reference cycle with six management actions: DISPATCH, WAIT, REQUEST_REVIEW, REPLAN, ESCALATE and CLOSE_PROJECT.

Reference priority is: open replan trigger; failed/blocked work; pending review; ready work; accepted completion; otherwise wait.

## Boundaries
A management decision is not a tool call, capability grant, specialist result or factual claim. DISPATCH hands work to responsibility routing. REQUEST_REVIEW hands work to a reviewer/Socrates role. REPLAN enters governed plan revision. ESCALATE transfers management attention to an authorized human/upper role. Runtime execution remains behind Authority/Grant/Tool Boundary.

## Consequence
FATHER becomes a management control loop over the digital organization while specialist roles remain independently governed and replaceable.
