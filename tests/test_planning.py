import unittest
from px00.planning import Plan, PlanStore, ReplanTrigger


class PlanStoreTests(unittest.TestCase):
    def setUp(self):
        self.s=PlanStore(); self.p1=Plan("PLAN-1","PROJ-1",("GOAL-1",),1,"initial decomposition",("TASK-1",),"FATHER",state="ACTIVE"); self.s.add_plan(self.p1)

    def test_revision_requires_trigger(self):
        with self.assertRaisesRegex(ValueError,"REVISION_REQUIRES_TRIGGER"):
            self.s.add_plan(Plan("PLAN-2","PROJ-1",("GOAL-1",),2,"revised",("TASK-1","TASK-2"),"FATHER",supersedes_plan_ref="PLAN-1"))

    def test_replan_preserves_lineage(self):
        t=ReplanTrigger("RPT-1","PROJ-1","PLAN-1","SOCRATES_CHALLENGE","SOCRATES",("EVD-1",),"missing independent evidence",state="ACCEPTED")
        self.s.raise_trigger(t)
        p2=Plan("PLAN-2","PROJ-1",("GOAL-1",),2,"add independent research",("TASK-1","TASK-2"),"FATHER",supersedes_plan_ref="PLAN-1",trigger_ref="RPT-1")
        self.s.add_plan(p2); self.s.activate("PLAN-2")
        self.assertEqual(self.s.lineage("PLAN-2"),("PLAN-2","PLAN-1"))
        self.assertEqual(self.s.plans["PLAN-1"].state,"SUPERSEDED")
        self.assertEqual(self.s.plans["PLAN-2"].state,"ACTIVE")

    def test_cross_project_trigger_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"TRIGGER_PROJECT_MISMATCH"):
            self.s.raise_trigger(ReplanTrigger("RPT-X","PROJ-X","PLAN-1","TASK_FAILURE","FATHER",(),"x"))

    def test_revision_must_be_sequential(self):
        t=ReplanTrigger("RPT-1","PROJ-1","PLAN-1","NEW_EVIDENCE","ANALYST",("EVD-1",),"new evidence",state="ACCEPTED"); self.s.raise_trigger(t)
        with self.assertRaisesRegex(ValueError,"NON_SEQUENTIAL_PLAN_REVISION"):
            self.s.add_plan(Plan("PLAN-3","PROJ-1",("GOAL-1",),3,"skip",("TASK-1",),"FATHER",supersedes_plan_ref="PLAN-1",trigger_ref="RPT-1"))

if __name__ == "__main__": unittest.main()
