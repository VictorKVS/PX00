# DJ-0065 — TF-0077 Security Source Registry CI Gate

Date: 2026-08-13
Status: IMPLEMENTED_PENDING_PX00_CI

Closed the current KNOWLEDGE_CORE repository-acceptance gap for newly registered Security Knowledge P0 source registries. A dedicated fail-closed validator now enforces alignment with the master source inventory, authoritative-host evidence rules, dynamic snapshot semantics, timestamped VERIFIED observations, and explicit red-team limitations.

The first CI run was preserved as failed evidence and exposed a real risk-registry defect: `STATUS_VERIFIED_METADATA_ONLY` had been asserted for the 27001 source without `status_observed`. The new invariant also exposed three dynamic BDU VERIFIED observations lacking `observed_at`. Both were repaired before merge.

The gate does not promote knowledge maturity merely because YAML is valid. All 12 P0 families are now registered, but the conservative overall maturity remains 10% and Security Knowledge remains NOT EXPERT_READY. PX00 remains a consumer/governor; canonical professional knowledge stays in KNOWLEDGE_CORE.
