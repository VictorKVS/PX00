# FFBJ-0022 — Security Primary-Source Proof-Channel Hardening

Date: 2026-08-13
Tree_F: `TF-0075`

The durable result of this generation is proof-channel hardening, not creation of the first VERIFIED requirement. During the run KNOWLEDGE_CORE concurrently gained a broader canonical 152-FZ requirement slice with 19 VERIFIED atoms, including Article 22 part 1. A one-atom source pack created earlier in this run became redundant and older, so it was removed to avoid split truth.

The source-pack gate now explicitly distinguishes official publication records at `publication.pravo.gov.ru` from official consolidated legal text at `ips.pravo.gov.ru` with `edition_as_of`. Regression tests accept the official IPS channel and reject arbitrary hosts.

Full CI also exposed invalid YAML in the run-02 Security coverage scorecard; that failure was preserved and the YAML was repaired rather than ignored.

Maturity remains conservative: the Security KB is still not EXPERT_READY; Article 22 part 2 exception logic and exact KoAP mappings remain open. `SUMMIT-FFB-02` remains independently OPEN pending one authorized PUBLIC Gemini inference.

Next: bounded D3 professional decision on the current canonical VERIFIED 152-FZ slice, with an explicit fail-closed unresolved-exception case.
