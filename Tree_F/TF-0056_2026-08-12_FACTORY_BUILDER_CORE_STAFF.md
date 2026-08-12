# TF-0056 — Factory Builder Core Staff

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0049
Project: PROJECT-FFB-0001

## Generation
Factory Builder now has a minimal governed architecture staff instead of an undifferentiated design prompt.

## Roles
- FFB-ROLE-0001 Chief Factory Architect
- FFB-ROLE-0002 Enterprise and Systems Architect
- FFB-ROLE-0003 Organization Architect
- FFB-ROLE-0004 Knowledge Architect
- FFB-ROLE-0005 Security and Risk Architect

## Supporting structure
- role registry;
- initial department/reporting seed;
- role-to-knowledge binding matrix;
- explicit role authority, non-responsibility, escalation, evidence, independence, anti-Goodhart, failure and continuity requirements.

## Boundary
Role identity is stable. Agent/model/provider/device assignment is replaceable. Knowledge binding grants context, never authority. Independent Socrates/ARGUS review remains separate from the producer chain.

## Next
Add Principal Software Engineer, Quality/Assurance Architect and Capability Architect, then define collaboration and review protocols required for SUMMIT-FFB-01 Agent Factory Blueprint.
