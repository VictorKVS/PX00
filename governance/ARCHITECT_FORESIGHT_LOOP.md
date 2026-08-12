# Architect Foresight Loop

Date: 2026-08-12
Status: active governance practice

## Purpose
PX00 must not depend on the owner already knowing every architectural, operational, security or organizational risk. The architect function is responsible for proactively surfacing failure modes, lock-in, irreversible choices and future-horizon conflicts before they become expensive.

## Mandatory triggers
Run the foresight loop:
- for every material ADR;
- before every SUMMIT acceptance;
- before every maturity transition M1->M2, M2->M3, M3->M4 and M4->M5;
- before introducing a new executor class, persistent store, critical vendor/provider, physical device class or external side-effect path;
- after a serious incident, near-miss, audit S3/S4 finding or major requirement change;
- periodically on long-lived architecture even when no incident occurred.

## Questions
1. Which assumption is being treated as true without proof?
2. What fails if that assumption is false?
3. What becomes expensive or impossible to reverse later?
4. Does the decision create model/provider/vendor/device/data-format lock-in?
5. Does it block H2, H3, H4 or H5 expansion?
6. What is the blast radius if this component is wrong or compromised?
7. What must be abstracted now, and what should deliberately remain concrete until evidence exists?
8. Which risks are acceptable inside the current maturity envelope?
9. Which risks must be eliminated or isolated now?
10. What evidence would prove the decision is safe enough for the next maturity level?
11. What new operational burden will appear: maintenance, calibration, backups, staffing, supply chain, cost, energy, legal/compliance, incident response?
12. How can this design fail socially or organizationally even if the code works?

## Required outputs
Each material review produces zero or more `ARCHITECTURE_RADAR_ENTRY` records with one of:
- KEEP
- EXPERIMENT
- ABSTRACT_NOW
- DEFER_WITH_GUARD
- REPLACE
- STOP

Radar findings may create or update `RISK-*` entries. A radar item is not itself a risk unless uncertainty/failure consequence justifies risk treatment.

## Long-horizon rule
Current implementation convenience must not silently redefine the permanent architecture. Reference implementation shortcuts must remain explicitly labeled with the maturity level at which they must be replaced.

## Physical-world escalation
Any future design with `PHYSICAL_EXTERNAL` blast radius must add domain-specific safety review, simulation/digital-twin validation where meaningful, independent verification, emergency-stop/override strategy, incident response and evidence of safe failure before real-world autonomous execution.

## Architect accountability
The architect is evaluated not only by how much was designed, but by:
- critical failures prevented;
- costly rewrites avoided;
- risks discovered before maturity gates;
- quality of reversibility and migration paths;
- preservation of stable organizational contracts across technology changes.
