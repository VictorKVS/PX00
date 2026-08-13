# DJ-0064 — TF-0076 Applicability Fail-Closed

Date: 2026-08-13
Status: IMPLEMENTED_PENDING_CI

Closed a concrete D3 false-positive path in the decision materiality gate: evidence-category presence can no longer substitute for an explicit applicability determination.

The change is deliberately narrow. It adds a resolved/unresolved applicability state to the existing D3 evidence floor and returns `INSUFFICIENT_EVIDENCE` with reason `D3_APPLICABILITY_UNRESOLVED` before review or approval can produce PASS.

The canonical Security Knowledge source remains in KNOWLEDGE_CORE; PX00 stores only the governance behavior. No duplicate professional knowledge and no simulated live-provider evidence were introduced.
