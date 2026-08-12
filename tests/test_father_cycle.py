import unittest
from px00.father_cycle import FatherManagementCycle, ProjectObservation


class FatherCycleTests(unittest.TestCase):
    def setUp(self): self.c=FatherManagementCycle()
    def obs(self, **kw): return ProjectObservation("OBS-1","PROJ-1","PLAN-1",**kw)

    def test_dispatch_ready_work(self):
        d=self.c.decide("MD-1",self.obs(ready_task_refs=("TASK-1",)))
        self.assertEqual(d.decision_type,"DISPATCH")

    def test_replan_has_priority_over_dispatch(self):
        d=self.c.decide("MD-1",self.obs(ready_task_refs=("TASK-1",),open_replan_trigger_refs=("RPT-1",)))
        self.assertEqual(d.decision_type,"REPLAN"); self.assertEqual(d.replan_trigger_ref,"RPT-1")

    def test_blocked_work_escalates(self):
        d=self.c.decide("MD-1",self.obs(blocked_task_refs=("TASK-2",)))
        self.assertEqual(d.decision_type,"ESCALATE"); self.assertTrue(d.escalation_target_ref)

    def test_review_precedes_new_dispatch(self):
        d=self.c.decide("MD-1",self.obs(ready_task_refs=("TASK-2",),review_task_refs=("TASK-1",)))
        self.assertEqual(d.decision_type,"REQUEST_REVIEW")

    def test_close_only_when_accepted_and_no_other_transition(self):
        d=self.c.decide("MD-1",self.obs(all_required_tasks_accepted=True))
        self.assertEqual(d.decision_type,"CLOSE_PROJECT")

    def test_wait_when_nothing_actionable(self):
        self.assertEqual(self.c.decide("MD-1",self.obs()).decision_type,"WAIT")

    def test_decision_ids_are_append_only(self):
        self.c.decide("MD-1",self.obs())
        with self.assertRaisesRegex(ValueError,"DECISION_ID_REUSE"): self.c.decide("MD-1",self.obs())

if __name__ == "__main__": unittest.main()
