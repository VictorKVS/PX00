# ADR-0029 — Replay-gated Acceptance

Status: Accepted
Date: 2026-08-12

## Decision
Material execution cannot reach PASS or PASS_WITH_ACTIONS unless a read-only ReplayReport is VERIFIED_RECORD. Replay evidence constrains acceptance but never acts as acceptance authority by itself. Blocking acceptance criteria remain independently decisive.

## Rules
- VERIFIED_RECORD + blocking criteria pass -> PASS or PASS_WITH_ACTIONS.
- VERIFIED_RECORD + blocking criteria fail -> FAIL.
- BROKEN_LINEAGE, TAMPER_DETECTED, POLICY_MISMATCH or INSUFFICIENT_EVIDENCE -> BLOCKED.
- VERIFIED_RECORD does not assert factual truth of the underlying claim.

## Consequence
PX00 now separates execution integrity, replay verification and acceptance authority into distinct layers.
