import unittest
from px00.work_management import Goal, Project, TaskNode, WorkGraph


class WorkGraphTests(unittest.TestCase):
    def setUp(self):
        self.g=WorkGraph(); self.g.add_goal(Goal("GOAL-1","OWNER-1","Prepare governed result",("accepted result",),acceptance_criteria_refs=("ACC-1",)))
        self.g.add_project(Project("PROJ-1",("GOAL-1",),"OWNER-1",("research",)))

    def test_project_requires_known_goal(self):
        with self.assertRaisesRegex(ValueError,"UNKNOWN_GOAL_REF"):
            self.g.add_project(Project("PROJ-X",("GOAL-X",),"OWNER-1",("x",)))

    def test_dependencies_gate_readiness(self):
        self.g.add_task(TaskNode("TASK-1","PROJ-1","Research","RESEARCH",acceptance_criteria_refs=("ACC-1",)))
        self.g.add_task(TaskNode("TASK-2","PROJ-1","Analyze","ANALYZE",dependency_refs=("TASK-1",),acceptance_criteria_refs=("ACC-2",)))
        self.assertEqual(tuple(x.task_id for x in self.g.ready_tasks()),("TASK-1",))
        self.g.replace_task_state("TASK-1","COMPLETED")
        self.assertEqual(tuple(x.task_id for x in self.g.ready_tasks()),("TASK-2",))

    def test_unknown_dependency_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"UNKNOWN_TASK_DEPENDENCY"):
            self.g.add_task(TaskNode("TASK-2","PROJ-1","Analyze","ANALYZE",dependency_refs=("TASK-X",)))

    def test_completion_requires_acceptance_criteria(self):
        self.g.add_task(TaskNode("TASK-1","PROJ-1","Research","RESEARCH"))
        with self.assertRaisesRegex(ValueError,"COMPLETION_WITHOUT_ACCEPTANCE_CRITERIA"):
            self.g.replace_task_state("TASK-1","COMPLETED")

    def test_task_declares_duty_not_model(self):
        self.g.add_task(TaskNode("TASK-1","PROJ-1","Analyze evidence","ANALYZE_EVIDENCE",acceptance_criteria_refs=("ACC-1",)))
        self.assertEqual(self.g.tasks["TASK-1"].required_duty_code,"ANALYZE_EVIDENCE")

if __name__ == "__main__": unittest.main()
