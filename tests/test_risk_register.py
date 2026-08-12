import unittest
from px00.risk_register import ArchitecturalRisk, RiskEvent, RiskRegister


class RiskRegisterTests(unittest.TestCase):
    def risk(self, **kw):
        base=dict(risk_id="RISK-1", title="example", category="ARCHITECTURE", source_refs=("ARGUS-1",), affected_component_refs=("PX00",), description="risk", causal_hypothesis="cause", likelihood="POSSIBLE", impact="MAJOR", severity="S3", status="OPEN", owner_ref="ROLE-ARCH", discovered_at="2026-08-12T00:00:00+00:00", last_reviewed_at="2026-08-12T00:00:00+00:00", next_review_at="2026-09-01T00:00:00+00:00")
        base.update(kw); return ArchitecturalRisk(**base)

    def test_ids_are_stable(self):
        r=RiskRegister(); r.add(self.risk())
        with self.assertRaisesRegex(ValueError,"RISK_ID_REUSE"): r.add(self.risk())

    def test_acceptance_requires_accountable_actor_and_reason(self):
        r=RiskRegister(); r.add(self.risk())
        with self.assertRaisesRegex(ValueError,"RISK_ACCEPTANCE_REQUIRES_ACCOUNTABILITY"):
            r.transition("RISK-1","ACCEPTED",actor_ref="OWNER",note="accept",event_id="RE-1")

    def test_resolution_requires_verification(self):
        r=RiskRegister(); r.add(self.risk())
        with self.assertRaisesRegex(ValueError,"RESOLUTION_REQUIRES_VERIFICATION"):
            r.transition("RISK-1","RESOLVED",actor_ref="ARGUS",note="fixed",event_id="RE-1")

    def test_history_is_append_only(self):
        r=RiskRegister(); r.add(self.risk()); r.record_event(RiskEvent("RE-1","RISK-1","OBSERVED","ARGUS","first","2026-08-12T01:00:00+00:00"))
        r.record_event(RiskEvent("RE-2","RISK-1","MITIGATING","ARCH","second","2026-08-12T02:00:00+00:00"))
        self.assertEqual(r.risks["RISK-1"].history_refs,("RE-1","RE-2"))

    def test_due_review_excludes_resolved(self):
        r=RiskRegister(); r.add(self.risk())
        self.assertEqual(tuple(x.risk_id for x in r.due_for_review("2026-09-02T00:00:00+00:00")),("RISK-1",))
        r.transition("RISK-1","RESOLVED",actor_ref="ARGUS",note="verified",event_id="RE-1",verification_refs=("TEST-1",))
        self.assertEqual(r.due_for_review("2026-09-02T00:00:00+00:00"),())

if __name__ == "__main__": unittest.main()
