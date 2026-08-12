# DJ-0036 — Immutable Plan and Governed Replanning

Date: 2026-08-12
Tree_F: TF-0047
ADR: ADR-0042

## Completed
FATHER planning is now revision-aware. Plans are immutable records; changes are represented as a new revision caused by an explicit REPLAN_TRIGGER. Socrates challenge, new evidence, task failure, policy/resource/requirement changes and human direction are first-class triggers.

## Management meaning
The system can preserve the distinction between `what FATHER planned then` and `what FATHER plans now`. A new plan supersedes rather than erases the old one.

## Authority boundary
A replan changes management intent and task structure only. It does not create tool authority; execution still requires the existing governed RUN/Authority/Grant path.

## Next
FATHER management-cycle state machine: DISPATCH, WAIT, REPLAN, ESCALATE, REQUEST_REVIEW and CLOSE_PROJECT decisions over the governed project state.
