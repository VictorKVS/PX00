from __future__ import annotations
from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class Plan:
    plan_id: str
    project_ref: str
    goal_refs: tuple[str, ...]
    revision: int
    rationale: str
    task_refs: tuple[str, ...]
    created_by: str
    state: str = "PROPOSED"
    supersedes_plan_ref: str | None = None
    trigger_ref: str | None = None


@dataclass(frozen=True)
class ReplanTrigger:
    trigger_id: str
    project_ref: str
    plan_ref: str
    reason_code: str
    raised_by: str
    evidence_refs: tuple[str, ...]
    description: str
    state: str = "OPEN"


@dataclass
class PlanStore:
    plans: dict[str, Plan] = field(default_factory=dict)
    triggers: dict[str, ReplanTrigger] = field(default_factory=dict)

    def add_plan(self, plan: Plan) -> None:
        if plan.plan_id in self.plans: raise ValueError("PLAN_ID_REUSE")
        if plan.revision < 1: raise ValueError("INVALID_PLAN_REVISION")
        if plan.revision == 1 and plan.supersedes_plan_ref is not None: raise ValueError("INITIAL_PLAN_CANNOT_SUPERSEDE")
        if plan.revision > 1:
            if not plan.supersedes_plan_ref: raise ValueError("REVISION_REQUIRES_SUPERSEDED_PLAN")
            prior=self.plans.get(plan.supersedes_plan_ref)
            if prior is None: raise ValueError("UNKNOWN_SUPERSEDED_PLAN")
            if prior.project_ref != plan.project_ref: raise ValueError("PLAN_PROJECT_MISMATCH")
            if plan.revision != prior.revision + 1: raise ValueError("NON_SEQUENTIAL_PLAN_REVISION")
            if not plan.trigger_ref or plan.trigger_ref not in self.triggers: raise ValueError("REVISION_REQUIRES_TRIGGER")
            trigger=self.triggers[plan.trigger_ref]
            if trigger.plan_ref != prior.plan_id or trigger.project_ref != plan.project_ref: raise ValueError("TRIGGER_PLAN_MISMATCH")
        self.plans[plan.plan_id]=plan

    def raise_trigger(self, trigger: ReplanTrigger) -> None:
        if trigger.trigger_id in self.triggers: raise ValueError("TRIGGER_ID_REUSE")
        plan=self.plans.get(trigger.plan_ref)
        if plan is None: raise ValueError("UNKNOWN_PLAN_REF")
        if plan.project_ref != trigger.project_ref: raise ValueError("TRIGGER_PROJECT_MISMATCH")
        self.triggers[trigger.trigger_id]=trigger

    def activate(self, plan_id: str) -> None:
        plan=self.plans.get(plan_id)
        if plan is None: raise ValueError("UNKNOWN_PLAN_REF")
        for pid,p in tuple(self.plans.items()):
            if p.project_ref == plan.project_ref and p.state == "ACTIVE" and pid != plan_id:
                self.plans[pid]=replace(p,state="SUPERSEDED")
        self.plans[plan_id]=replace(plan,state="ACTIVE")

    def lineage(self, plan_id: str) -> tuple[str, ...]:
        out=[]; current=self.plans.get(plan_id)
        if current is None: raise ValueError("UNKNOWN_PLAN_REF")
        while current:
            out.append(current.plan_id)
            current=self.plans.get(current.supersedes_plan_ref) if current.supersedes_plan_ref else None
        return tuple(out)
