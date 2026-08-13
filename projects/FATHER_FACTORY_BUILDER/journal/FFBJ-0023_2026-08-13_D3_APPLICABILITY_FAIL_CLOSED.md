# FFBJ-0023 — D3 Applicability Fail-Closed

Date: 2026-08-13
Status: IMPLEMENTED_PENDING_CI

Factory Builder now has a stronger D3 runtime invariant: a material regulated decision cannot reach PASS merely because an applicability evidence category exists. The underlying applicability conclusion must be explicit.

`APPLICABLE` and `NOT_APPLICABLE` are resolved states. Any other D3 state fails closed as `D3_APPLICABILITY_UNRESOLVED` before review/approval.

This is an enforcement improvement, not a new professional-knowledge model. KNOWLEDGE_CORE remains canonical. `SUMMIT-FFB-02` remains OPEN pending real authorized live-executor evidence.
