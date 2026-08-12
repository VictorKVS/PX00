# DJ-0044 — Factory Builder Core Staff

Date: 2026-08-12
Tree_F: TF-0056
ADR: ADR-0049
Project: PROJECT-FFB-0001

## Completed
Created the first governed Factory Builder architecture team with five reusable role blueprints, a role registry, organization seed and role-to-knowledge binding matrix.

## Why it matters
Factory Builder is no longer modeled as one general-purpose architect. Factory design is deliberately decomposed into structural architecture, organization design, knowledge architecture and security/risk with a Chief Factory Architect responsible for synthesis rather than replacing the specialists.

## Governance boundaries
- role identity is independent of model/provider/device;
- knowledge binding never grants runtime authority;
- Chief Factory Architect cannot independently certify its own blueprint;
- Security/Risk cannot accept S4 risk;
- dissent, open tensions and unresolved risks must survive handoff;
- roles remain PROPOSED until protocols/evals and independent review are added.

## Knowledge direction
Logical role knowledge spaces are treated as reusable organizational infrastructure. Physical repositories may later split without changing logical knowledge identities or historical bindings.

## Next
Complete the minimum Factory Builder staff with Principal Software Engineer, Quality/Assurance Architect and Capability Architect, then build the first explicit collaboration protocol for producing and reviewing an Agent Factory Blueprint.
