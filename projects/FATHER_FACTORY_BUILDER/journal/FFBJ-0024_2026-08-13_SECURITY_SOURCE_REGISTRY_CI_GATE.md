# FFBJ-0024 — Security Source Registry CI Gate

Date: 2026-08-13
Status: IMPLEMENTED_PENDING_PX00_CI

Factory Builder now has a stronger external-knowledge dependency contract: newly registered Security Knowledge source-family registries are protected by a dedicated repository-level CI gate before PX00 treats their inventory state as trustworthy routing metadata.

The gate caught two pre-existing evidence defects: missing `observed_at` on three VERIFIED dynamic BDU records and missing `status_observed` on a 27001 metadata-only verified source card. Both were repaired before the KNOWLEDGE_CORE change was merged.

This does not grant runtime authority, does not turn registry metadata into VERIFIED requirements, and does not change `SUMMIT-FFB-02`: the first real authorized Gemini inference is still outstanding.
