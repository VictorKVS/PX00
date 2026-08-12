import unittest
from px00.trust_gate import ContextTrustAssessment, ContextTrustGate


class ContextTrustGateTests(unittest.TestCase):
    def setUp(self): self.g=ContextTrustGate()

    def a(self,label,verified=()):
        return ContextTrustAssessment("CTA-1","CTX-1",label,("PROV-1",),verified)

    def test_tainted_context_may_be_analyzed_but_not_act(self):
        a=self.a("TAINTED")
        self.assertTrue(self.g.allow_use(a,use_type="ANALYSIS_ONLY"))
        self.assertFalse(self.g.allow_use(a,use_type="MATERIAL_REVERSIBLE"))
        self.assertFalse(self.g.allow_use(a,use_type="MATERIAL_SENSITIVE"))

    def test_untrusted_external_requires_independent_verification_for_material_use(self):
        self.assertFalse(self.g.allow_use(self.a("UNTRUSTED_EXTERNAL"),use_type="MATERIAL_REVERSIBLE"))
        self.assertTrue(self.g.allow_use(self.a("UNTRUSTED_EXTERNAL",("VERIFY-1",)),use_type="MATERIAL_REVERSIBLE"))

    def test_verified_external_still_requires_independent_verification_for_sensitive_use(self):
        self.assertFalse(self.g.allow_use(self.a("VERIFIED_EXTERNAL"),use_type="MATERIAL_SENSITIVE"))
        self.assertTrue(self.g.allow_use(self.a("VERIFIED_EXTERNAL",("VERIFY-1",)),use_type="MATERIAL_SENSITIVE"))

    def test_context_never_manufactures_authority(self):
        self.assertFalse(self.g.may_influence_authority(self.a("TRUSTED_INTERNAL")))

    def test_unknown_label_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"UNKNOWN_CONTEXT_TRUST_LABEL"):
            self.g.allow_use(self.a("MAGIC"),use_type="ANALYSIS_ONLY")

if __name__ == "__main__": unittest.main()
