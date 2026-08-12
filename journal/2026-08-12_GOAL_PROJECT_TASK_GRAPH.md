# DJ-0035 — Goal / Project / Task Graph

Date: 2026-08-12
Tree_F: TF-0046
ADR: ADR-0041

## Completed
FATHER now has a reference management layer above the corporate dispatcher. Objectives are represented as GOAL objects, bounded into PROJECT objects and decomposed into TASK_NODE graphs with explicit dependencies, duty requirements, outputs and acceptance criteria.

## Important boundary
A user's goal is not treated as runtime authority. A task becoming READY does not authorize tools. Existing Policy/Authority/Grant controls remain mandatory at execution time.

## Organizational meaning
FATHER can now ask `what work is ready?` before deciding `which governed role is responsible?`. This separates management scheduling from staffing and from runtime authority.

## Next
PLAN and DECOMPOSITION lineage: preserve why tasks were created, allow revisions/supersession, and make replanning auditable rather than silently mutating the task graph.
