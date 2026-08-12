# RISK-0008 — Development Identity / Numbering Collision Risk

Status: OPEN
Severity: S2
Category: PROCESS / GOVERNANCE
Source: ARGUS-GOV-001
Owner: ROLE-PRINCIPAL-ENGINEER

## Risk
Rapid development has already reused Tree_F numbers. If stable development IDs are not machine-enforced, historical references can become ambiguous over years.

## Required mitigation
Add repository-wide CI uniqueness checks for TF/DJ/ADR/RISK/AUDIT identifiers and a migration policy for previously collided IDs without deleting history.
