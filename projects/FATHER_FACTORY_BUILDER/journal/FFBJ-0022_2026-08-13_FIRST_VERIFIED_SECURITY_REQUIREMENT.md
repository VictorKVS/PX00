# FFBJ-0022 — First VERIFIED Security Requirement

Date: 2026-08-13
Tree_F: `TF-0075`

Canonical Security Knowledge now contains its first strict VERIFIED D3-capable atomic legal requirement: Federal Law 152-FZ, Article 22 part 1, with exact locator, primary-source quote, bounded applicability, evidence expectations and Order 180 form mapping.

Building the atom exposed a proof-model defect in the source-pack validator: a VERIFIED legacy federal law could not use the official consolidated text channel at `ips.pravo.gov.ru`. The gate was corrected to distinguish official publication metadata from official consolidated text, and regression tests now accept the official IPS host while rejecting arbitrary mirrors.

This closes only the zero-VERIFIED-atom blocker for a narrow test slice. It does not make the Security KB EXPERT_READY and does not authorize a concrete no-notification conclusion without resolving Article 22 part 2 exceptions.

Next: use the atom in one bounded D3 professional decision and verify that unresolved exceptions fail closed. `SUMMIT-FFB-02` remains independently OPEN pending one authorized PUBLIC Gemini inference.
