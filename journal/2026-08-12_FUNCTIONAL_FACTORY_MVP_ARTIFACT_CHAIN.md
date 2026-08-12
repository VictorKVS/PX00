# DJ-0048 — Functional Factory MVP artifact chain

Date: 2026-08-12
Projects: PX00/FATHER + PROJECT-FFB-0001
Generation: TF-0060
ADR: ADR-0053

## Achievement
Factory Builder has moved from an executable control-flow skeleton to its first useful audited functional reference MVP.

`MVP-FUNC-RUN-0001` completed the full bounded R&D chain from problem qualification through research, claims, design, security precheck, prototype, independent verification, Socrates review, knowledge-admission candidate and governed delivery.

## New evidence discipline
Each stage now requires a typed immutable artifact. The M1 reference runtime enforces:
- append-only artifact identity;
- deterministic payload SHA-256;
- strict stage/artifact type matching;
- explicit immediate-parent lineage;
- pinned verifier assignment for verification evidence;
- independent Socrates assignment;
- runtime outcome consistency with assurance-artifact verdict;
- terminal successful delivery.

## Useful result
The first case designed and independently verified a deterministic idempotency identity based on SHA-256 of canonical JSON `[run_id, operation, target]`.

The final package intentionally preserves the limitation that an idempotency identity is not exactly-once execution. Durable uniqueness and atomic state transition remain separate future controls.

## Criticism converted into work
The functional audit found two implementation defects before acceptance:
1. delimiter-based tuple encoding was ambiguous;
2. evidence could previously declare FAIL while runtime accepted PASS.

Both were corrected and covered by negative tests before the M1 functional acceptance decision.

ARGUS also identified a new longer-horizon evidence risk: `RISK-0009 — Artifact Envelope Integrity Gap`. Current payload hashing does not yet bind the entire run/stage/type/producer/lineage envelope. This is acceptable only inside the local in-memory M1 reference scope.

## Verdict
Socrates: `PASS_WITH_FINDINGS`.
ARGUS: `PASS_WITH_RESTRICTIONS`.
Acceptance: `FFB-ACCEPT-FUNC-MVP-0001`.

Allowed claim: `M1 FUNCTIONAL REFERENCE MVP`.

Not allowed: production-ready, live autonomous-agent factory, arbitrary external-content safety, durable/exactly-once operation, or material external execution.

## Open risk debt
- `RISK-0002`: adversarial/untrusted context — isolated, not closed;
- `RISK-0003`: in-memory stores;
- `RISK-0004`: durable transaction/idempotency semantics;
- `RISK-0009`: full artifact-envelope integrity.

## Next summit
Prove that the workflow is reusable rather than tailored to one case: run several different bounded problems through the same artifact contract and record failure/rework patterns. Then substitute exactly one deterministic producer stage with a governed executor adapter without weakening the existing gates.
