# DJ-0031 — Governed Staffing and Handoff

Date: 2026-08-12
Tree_F: TF-0042
ADR: ADR-0037

## Completed
Added formal role responsibility, agent assignment and handoff package contracts. Implemented reference staffing registry and negative tests for knowledge-binding overflow, suspended assignments, missing bilateral handoff protocol, READY packages with blocking findings, and accidental authority transfer.

## Organizational interpretation
PX00/FATHER now treats ROLE as the stable job position, AGENT/MODEL as a replaceable employee assigned to that position, and HANDOFF_PACKAGE as a governed work-transfer document. Knowledge remains in KNOWLEDGE_CORE and is attached by binding, not copied into the model.

## Next gate
Pin exact AGENT_ASSIGNMENT/model to RUN and add task-to-responsibility routing so FATHER can choose an eligible role/agent from declared duties rather than hardcoded role names.
