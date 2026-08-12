from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProjectObservation:
    observation_id: str
    project_ref: str
    plan_ref: str
    ready_task_refs: tuple[str, ...] = ()
    running_task_refs: tuple[str, ...] = ()
    blocked_task_refs: tuple[str, ...] = ()
    review_task_refs: tuple[str, ...] = ()
    failed_task_refs: tuple[str, ...] = ()
    open_replan_trigger_refs: tuple[str, ...] = ()
    all_required_tasks_accepted: bool = False


@dataclass(frozen=True)
class ManagementDecision:
    decision_id: str
    project_ref: str
    plan_ref: str
    observation_refs: tuple[str, ...]
    decision_type: str
    rationale: str
    task_refs: tuple[str, ...] = ()
    review_target_refs: tuple[str, ...] = ()
    replan_trigger_ref: str | None = None
    escalation_target_ref: str | None = None
    closure_reason: str | None = None


@dataclass
class FatherManagementCycle:
    decisions: dict[str, ManagementDecision] = field(default_factory=dict)

    def decide(self, decision_id: str, obs: ProjectObservation, human_target: str = "HUMAN-OWNER") -> ManagementDecision:
        if decision_id in self.decisions: raise ValueError("DECISION_ID_REUSE")
        if obs.open_replan_trigger_refs:
            d=ManagementDecision(decision_id,obs.project_ref,obs.plan_ref,(obs.observation_id,),"REPLAN","open governed replan trigger",replan_trigger_ref=obs.open_replan_trigger_refs[0])
        elif obs.failed_task_refs or obs.blocked_task_refs:
            targets=obs.failed_task_refs + obs.blocked_task_refs
            d=ManagementDecision(decision_id,obs.project_ref,obs.plan_ref,(obs.observation_id,),"ESCALATE","failed or blocked work requires management attention",task_refs=targets,escalation_target_ref=human_target)
        elif obs.review_task_refs:
            d=ManagementDecision(decision_id,obs.project_ref,obs.plan_ref,(obs.observation_id,),"REQUEST_REVIEW","work is awaiting independent review",review_target_refs=obs.review_task_refs)
        elif obs.ready_task_refs:
            d=ManagementDecision(decision_id,obs.project_ref,obs.plan_ref,(obs.observation_id,),"DISPATCH","governed tasks are ready for responsibility routing",task_refs=obs.ready_task_refs)
        elif obs.all_required_tasks_accepted:
            d=ManagementDecision(decision_id,obs.project_ref,obs.plan_ref,(obs.observation_id,),"CLOSE_PROJECT","all required tasks have passed acceptance",closure_reason="GOAL_WORK_ACCEPTED")
        else:
            d=ManagementDecision(decision_id,obs.project_ref,obs.plan_ref,(obs.observation_id,),"WAIT","no governed management transition is currently available")
        self.decisions[decision_id]=d
        return d
