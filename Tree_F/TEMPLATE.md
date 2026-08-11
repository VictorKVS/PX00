# TF-XXXX — <short name>

**Date:** YYYY-MM-DD  
**Status:** PROPOSED | ACTIVE | SUPERSEDED | ROLLED_BACK  
**Decision:** KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT  
**Parent decision / requirement:** <ID or link>

## 1. Trigger

What changed and why now.

## 2. Structural delta

```text
before
→
after
```

## 3. File dossier

### `path/to/file`
- **Purpose:**
- **Trigger:**
- **Inputs / Outputs:**
- **Processing:** NONE | algorithm/rules
- **Dependencies:** NONE | libraries/services/contracts
- **DevOps:** NONE | build/test/deploy effect
- **Security:** classification, threats, controls, secrets rule
- **Verification:** test/review/evidence
- **Decision:** KEEP | IMPROVE | REPLACE | ROLLBACK | EXPERIMENT

Repeat only for material files.

## 4. Production-chain view

```text
Trigger → Requirement/Decision → Change → Verification → Security review → Evaluation → Outcome
```

## 5. Tests / acceptance

- Contract test:
- Regression test:
- Security test:
- Reproducibility check:

## 6. Evaluation

| Criterion | Before 0–5 | After 0–5 | Evidence |
|---|---:|---:|---|
| Correctness | | | |
| Traceability | | | |
| Security | | | |
| Maintainability | | | |
| Reproducibility | | | |
| Complexity/cost | | | |

Scores are comparison aids, not pseudo-precision.

## 7. Experiment, if any

**Experiment ID:** EXP-XXXX  
**Variant A:**  
**Variant B:**  
**Common acceptance criteria:**  
**Result:**  
**Selected variant:**

## 8. Rollback

Exact restoration path or reference to the prior accepted `TF` baseline.

## 9. Security conclusion

`PASS | PASS_WITH_ACTIONS | FAIL | NOT_APPLICABLE`

Short rationale and open actions.
