from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Goal:
    goal_id: str
    owner_ref: str
    statement: str
    desired_outcomes: tuple[str, ...]
    constraints: tuple[str, ...] = ()
    acceptance_criteria_refs: tuple[str, ...] = ()
    priority: str = "NORMAL"
    state: str = "ACTIVE"


@dataclass(frozen=True)
class Project:
    project_id: str
    goal_refs: tuple[str, ...]
    owner_ref: str
    scope_in: tuple[str, ...]
    scope_out: tuple[str, ...] = ()
    state: str = "PLANNED"


@dataclass(frozen=True)
class TaskNode:
    task_id: str
    project_ref: str
    title: str
    required_duty_code: str
    dependency_refs: tuple[str, ...] = ()
    required_input_refs: tuple[str, ...] = ()
    expected_output_types: tuple[str, ...] = ()
    acceptance_criteria_refs: tuple[str, ...] = ()
    priority: str = "NORMAL"
    state: str = "PLANNED"


@dataclass
class WorkGraph:
    goals: dict[str, Goal] = field(default_factory=dict)
    projects: dict[str, Project] = field(default_factory=dict)
    tasks: dict[str, TaskNode] = field(default_factory=dict)

    def add_goal(self, goal: Goal) -> None:
        if goal.goal_id in self.goals:
            raise ValueError("GOAL_ID_REUSE")
        if not goal.statement.strip() or not goal.desired_outcomes:
            raise ValueError("GOAL_INCOMPLETE")
        self.goals[goal.goal_id] = goal

    def add_project(self, project: Project) -> None:
        if project.project_id in self.projects:
            raise ValueError("PROJECT_ID_REUSE")
        if not project.goal_refs:
            raise ValueError("PROJECT_WITHOUT_GOAL")
        if any(ref not in self.goals for ref in project.goal_refs):
            raise ValueError("UNKNOWN_GOAL_REF")
        self.projects[project.project_id] = project

    def add_task(self, task: TaskNode) -> None:
        if task.task_id in self.tasks:
            raise ValueError("TASK_ID_REUSE")
        if task.project_ref not in self.projects:
            raise ValueError("UNKNOWN_PROJECT_REF")
        if any(ref not in self.tasks for ref in task.dependency_refs):
            raise ValueError("UNKNOWN_TASK_DEPENDENCY")
        self.tasks[task.task_id] = task
        if self._has_cycle():
            del self.tasks[task.task_id]
            raise ValueError("TASK_GRAPH_CYCLE")

    def _has_cycle(self) -> bool:
        visiting: set[str] = set(); visited: set[str] = set()
        def visit(task_id: str) -> bool:
            if task_id in visiting: return True
            if task_id in visited: return False
            visiting.add(task_id)
            for dep in self.tasks[task_id].dependency_refs:
                if visit(dep): return True
            visiting.remove(task_id); visited.add(task_id); return False
        return any(visit(task_id) for task_id in self.tasks)

    def ready_tasks(self) -> tuple[TaskNode, ...]:
        ready=[]
        for task in self.tasks.values():
            if task.state not in {"PLANNED", "READY"}: continue
            if all(self.tasks[ref].state == "COMPLETED" for ref in task.dependency_refs): ready.append(task)
        return tuple(sorted(ready, key=lambda item: item.task_id))

    def replace_task_state(self, task_id: str, state: str) -> None:
        from dataclasses import replace
        if task_id not in self.tasks: raise ValueError("UNKNOWN_TASK_REF")
        allowed={"PLANNED","READY","ASSIGNED","RUNNING","BLOCKED","REVIEW","COMPLETED","FAILED","CANCELLED"}
        if state not in allowed: raise ValueError("UNKNOWN_TASK_STATE")
        task=self.tasks[task_id]
        if state == "COMPLETED" and not task.acceptance_criteria_refs:
            raise ValueError("COMPLETION_WITHOUT_ACCEPTANCE_CRITERIA")
        self.tasks[task_id]=replace(task,state=state)
