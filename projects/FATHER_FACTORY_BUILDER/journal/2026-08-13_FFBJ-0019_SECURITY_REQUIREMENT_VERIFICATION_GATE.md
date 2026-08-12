# FFBJ-0019 — Security Requirement Verification Gate

Date: 2026-08-13
Tree_F: `TF-0072`

## Trigger

Factory Builder attempted to move from provenance mechanics to the first professional D3 Security decision. The canonical Security corpus exposed a proof-state inconsistency before the RUN began: FSTEK-31 atomic requirements were labeled VERIFIED while lacking the `source_quote` required by their own schema.

## Action

Factory Builder did not consume the inflated state.

KNOWLEDGE_CORE corrected affected requirements to REVIEWED and introduced a CI gate that makes VERIFIED an earned state requiring source document identity, exact locator and source quote.

## Measured result

Current strict corpus baseline:
- 9 requirement files;
- 82 atomic requirements;
- 0 strict VERIFIED requirements.

## Factory Builder implication

A factory/role may not lower a domain knowledge proof floor merely to unblock execution.

`ROLE NEEDS VERIFIED KNOWLEDGE` can legitimately produce:
`BLOCKED_BY_KNOWLEDGE_PROOF_FLOOR`.

That is a correct governed outcome, not a reason to reinterpret REVIEWED as VERIFIED.

## Next

- Security Knowledge independently promotes the first real atomic VERIFIED item (`FSTEK31-REQ-001` is the first target).
- Factory Builder independently continues `SUMMIT-FFB-02` live-executor work.
- First closed professional Security loop requires both prerequisites.
