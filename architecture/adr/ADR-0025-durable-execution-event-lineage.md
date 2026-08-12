# ADR-0025 — Durable Execution Event Lineage

Status: Accepted
Date: 2026-08-12

## Context
PX00 can pin exact policy profiles to a RUN and bind AuthorityDecision to that snapshot. Material execution events must now preserve the same lineage so an observed effect can be traced back to the exact request, authority decision, grant, and policy snapshot.

## Decision
Every governed material execution event MUST carry RUN/TASK/TRACE context and references to the originating ActionRequest and AuthorityDecision. When execution occurs under a CapabilityGrant, the exact grant MUST be referenced. When authority is snapshot-governed, event policy_snapshot_ref and policy_snapshot_hash MUST equal the AuthorityDecision and RUN lineage.

## Invariants
- event_run_id_must_match_action_request_authority_and_policy_snapshot_run
- event_policy_snapshot_ref_and_hash_must_match_authority_decision
- granted_execution_event_must_reference_the_exact_capability_grant_used
- missing_lineage_is_not_interpreted_as_successful_governed_execution
- event evidence records explicit summaries and identifiers, never hidden chain-of-thought

## Consequences
A future auditor can traverse EVT -> ACTREQ -> AUTH -> POLSNAP -> exact PolicyProfile versions and, for executed operations, EVT -> GRANT -> Tool Boundary. This creates a durable proof path from external effect back to governing authority.
