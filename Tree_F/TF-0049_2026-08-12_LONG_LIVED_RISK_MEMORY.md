# TF-0049 — Long-Lived Architectural Risk Memory

Date: 2026-08-12
Status: implemented; CI pending
ADR: ADR-0044

## Generation
Added a durable institutional memory for architecture, organization, implementation, governance and security risks discovered during PX00 evolution.

## Surfaces
- `schemas/ARCHITECTURAL_RISK_REGISTER_ENTRY.yaml`
- `schemas/AUDIT_FINDING.yaml`
- `px00/risk_register.py`
- `tests/test_risk_register.py`
- `architecture/adr/ADR-0044-long-lived-risk-memory.md`

## Core rule
A risk is a stable logical object. Refactoring code, moving repositories, replacing models or changing organizational structure does not erase its history.

## Lifecycle
OPEN -> MITIGATING / MONITORING / ACCEPTED -> RESOLVED, with REOPENED when new evidence invalidates a prior resolution.

## Next
Build ARGUS audit governance and retrospective audit packs so reviewer findings automatically enter the durable risk register and project dashboards can expose `project progress` separately from `audited progress` and `known unresolved risk`.
