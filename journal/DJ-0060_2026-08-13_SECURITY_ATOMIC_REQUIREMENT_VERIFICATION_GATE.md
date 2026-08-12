# DJ-0060 — Security Atomic Requirement Verification Gate

Date: 2026-08-13
Tree_F: `TF-0072`

## Change

Attempting the first professional D3 Security RUN exposed a canonical knowledge quality gap before runtime execution.

FSTEK-31 atomic records used `verification: VERIFIED` with locators but no `source_quote`, despite the existing Security requirement schema requiring a quote for VERIFIED status.

The records were not discarded. Their verification state was corrected to `REVIEWED` while preserving atomization and locators.

## Enforcement

KNOWLEDGE_CORE now contains an executable Security atomic requirement gate and regression tests.

`VERIFIED` requires:
- requirement identity;
- source document identity;
- exact locator;
- source quote.

Absent verification state is interpreted as `UNVERIFIED`, not as an error and never as implicit verification.

## Measured baseline

The first full scan reports:
- 9 requirement files;
- 82 atomic requirements;
- 0 requirements currently satisfying the new strict VERIFIED proof floor.

This is an honest maturity baseline, not a failure of the project.

## Consequence

Professional D3 Security reasoning remains blocked until the first real VERIFIED atomic requirement exists. The live-provider summit remains independent and may proceed in parallel.

First promotion target: `FSTEK31-REQ-001` at p. 10.

## Lesson

A data field named VERIFIED is not evidence. Verification promotion itself must have executable admission conditions.
