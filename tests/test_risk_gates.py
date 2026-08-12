import unittest
from px00.risk_gates import RiskGateInput, RiskMaturityGate


class RiskMaturityGateTests(unittest.TestCase):
    def setUp(self): self.g=RiskMaturityGate()

    def risk(self, rid="RISK-1", severity="S4", status="OPEN", treatment="ISOLATE", verified=True, scope=("PLATFORM",)):
        return RiskGateInput(rid,severity,status,scope,treatment,verified)

    def test_s4_blocks_prototype_even_if_contained(self):
        d=self.g.evaluate(target_maturity="M1_PROTOTYPE",promoted_scope_refs=("PLATFORM",),risks=(self.risk(),))
        self.assertFalse(d.allowed); self.assertIn("RISK-1",d.blockers)

    def test_s4_cannot_be_accepted(self):
        d=self.g.evaluate(target_maturity="M0_CONCEPT",promoted_scope_refs=("PLATFORM",),risks=(self.risk(treatment="ACCEPT"),))
        self.assertFalse(d.allowed)

    def test_unverified_containment_blocks(self):
        d=self.g.evaluate(target_maturity="M2_INTEGRATED_PROTOTYPE",promoted_scope_refs=("PLATFORM",),risks=(self.risk(severity="S3",verified=False),))
        self.assertFalse(d.allowed)

    def test_s3_can_exist_in_integrated_prototype_when_contained(self):
        d=self.g.evaluate(target_maturity="M2_INTEGRATED_PROTOTYPE",promoted_scope_refs=("PLATFORM",),risks=(self.risk(severity="S3"),))
        self.assertTrue(d.allowed)

    def test_s3_blocks_controlled_pilot(self):
        d=self.g.evaluate(target_maturity="M3_CONTROLLED_PILOT",promoted_scope_refs=("PLATFORM",),risks=(self.risk(severity="S3"),))
        self.assertFalse(d.allowed)

    def test_scope_isolation_allows_unrelated_work(self):
        d=self.g.evaluate(target_maturity="M2_INTEGRATED_PROTOTYPE",promoted_scope_refs=("UI",),risks=(self.risk(scope=("KNOWLEDGE",)),))
        self.assertTrue(d.allowed)

    def test_resolved_risk_does_not_block(self):
        d=self.g.evaluate(target_maturity="M5_PRODUCTION",promoted_scope_refs=("PLATFORM",),risks=(self.risk(status="RESOLVED"),))
        self.assertTrue(d.allowed)

if __name__ == "__main__": unittest.main()
