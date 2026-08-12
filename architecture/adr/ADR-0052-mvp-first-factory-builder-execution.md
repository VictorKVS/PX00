# ADR-0052 — MVP-first Factory Builder execution

Status: Accepted
Date: 2026-08-12

## Context
Factory Builder reached an audited M0 concept for the first Agent R&D Factory. Continuing to expand architecture before executing the concept would increase speculative complexity, widen the unfinished surface and make it harder to distinguish necessary controls from imagined future requirements.

## Decision
Freeze an explicit M1 MVP cut and prioritize executable evidence over architectural breadth.

The MVP consists only of the minimum governed path from problem intake to bounded delivery:

`QUALIFY → RESEARCH → ASSESS → DESIGN → SECURITY PRECHECK → BOUNDED PROTOTYPE → VERIFY → SOCRATES → KNOWLEDGE → DELIVERY`.

The first reference implementation is deterministic and synthetic. It does not use live LLM providers, confidential data or material external tools.

## Mandatory MVP gates
- stage order is fail-closed;
- producer and independent verifier assignments differ;
- untrusted content cannot reach prototype execution without an explicit trust gate;
- security precheck must pass before prototype execution;
- verification and Socrates must pass before governed delivery;
- run identifiers and traces are append-only;
- unresolved S4 risk blocks the affected wider M1 path;
- passing M1 does not imply production readiness.

## Scope control
Features outside `FFB-MVP-0001` are backlog by default. They may enter active work only because of:
1. observed user/use-case need;
2. audit finding;
3. measured bottleneck;
4. risk treatment requirement;
5. explicit governed replan.

Convenience, novelty or architectural elegance alone are insufficient reasons to expand the MVP.

## Risk posture
For the current M1 harness, `RISK-0002` is isolated rather than claimed closed: only synthetic or explicitly trust-gated content is allowed and material external action is absent. Wider input/tool scope remains blocked until adversarial trust-gate evidence exists.

## Consequences
Positive:
- executable evidence arrives earlier;
- speculative surface is constrained;
- defects are discovered against running behavior;
- future hardening is driven by observed need and risk.

Tradeoff:
- many desirable platform features remain intentionally absent;
- initial harness is not representative of production scale or live-model behavior.

## Non-goals
This ADR does not authorize production deployment, autonomous tool use, confidential-data processing, multi-tenancy, physical actuation or broad LLM integration.
