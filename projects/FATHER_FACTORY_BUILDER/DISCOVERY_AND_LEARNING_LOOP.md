# Discovery and Learning Loop

Factory Builder must expect important failures to be discovered only after design starts. The goal is not to pretend all risks are known; the goal is to discover them early, contain them, preserve the lesson and prevent recurrence.

## Loop

```text
DESIGN ASSUMPTION
      ↓
PROTOTYPE / SIMULATION / PILOT
      ↓
OBSERVATION
      ├─ expected
      ├─ anomaly
      ├─ near-miss
      ├─ failure
      └─ reviewer disagreement
      ↓
RADAR ENTRY
      ↓
RISK / DEFECT / ARCHITECTURAL TENSION / LESSON
      ↓
TREATMENT
      ↓
TEST / VERIFICATION
      ↓
FACTORY REVISION
      ↓
INSTITUTIONAL MEMORY
```

## Mandatory capture
Capture not only incidents but also:
- near-misses;
- assumptions disproved;
- surprising success that reveals an undocumented dependency;
- repeated human workaround;
- repeated reviewer disagreement;
- false positive/false negative controls;
- performance/cost/resource drift;
- safety/security control bypass attempts;
- supplier/model/API behavior change;
- difficult rollback or recovery;
- areas where operators cannot explain system behavior.

## Classification of discoveries
- `RISK` — uncertain future harm requiring treatment;
- `DEFECT` — demonstrated implementation error;
- `ARCHITECTURAL_TENSION` — two valid goals/constraints in conflict;
- `ASSUMPTION_FAILURE` — premise was false or unproven;
- `NEAR_MISS` — harmful outcome narrowly avoided;
- `LESSON` — reusable design/operational knowledge;
- `OPPORTUNITY` — observation that can simplify or improve the factory.

## Memory rule
A resolved problem remains searchable. Closure changes current status; it does not erase the event, root cause, treatment or evidence.

## Recurrence rule
When a similar event appears in another factory, Factory Builder must search prior lessons/risks before inventing a new treatment from scratch.

## Pattern promotion
Repeated local findings are promoted into global Factory Builder doctrine when evidence shows a cross-factory pattern.

Example:
1. Factory A suffers duplicate task execution.
2. Factory B later shows the same pattern.
3. ARGUS identifies shared cause: missing idempotency contract.
4. The lesson is promoted into the universal construction lifecycle/gate.
5. New factories receive the control by default.

## Feedback boundaries
Learning may change implementation, architecture and procedures. It may not automatically change:
- mission;
- beneficiary scope;
- legal authority;
- unacceptable-risk threshold;
- safety boundary;
- human accountability model.

Those require explicit governed decisions.

## Review cadence
- continuous for S4/S3 signals;
- at each TF/material architecture generation for local findings;
- at each SUMMIT for accumulated project risk;
- at every maturity transition;
- periodic retrospective audit even without an incident.
