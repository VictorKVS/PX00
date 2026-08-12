# Extraction Plan

Factory Builder is incubated inside PX00 but is expected to become separately deployable and possibly split into multiple repositories/services as maturity grows.

## Why incubate inside PX00 now
- reuse governance, risk, audit, role and knowledge contracts;
- evolve quickly while boundaries are still being discovered;
- avoid premature repository/service fragmentation;
- keep design decisions close to FATHER until interfaces stabilize.

## Why extract later
Factory construction, factory operation, assurance, knowledge and domain adapters will eventually have different release cadences, teams, risk profiles and deployment boundaries.

## Stable interfaces that must survive extraction
- `PROJECT-FFB-0001` identity;
- FACTORY/BLUEPRINT stable IDs when introduced;
- capability IDs;
- role/responsibility/protocol references;
- risk/audit lineage;
- knowledge-space logical IDs;
- executor eligibility contracts;
- maturity and acceptance records.

## Proposed future split
Potential structure, only when justified by evidence:

```text
FACTORY_BUILDER_CORE
  requirements
  capability architecture
  organization blueprint
  blueprint versioning

FACTORY_ASSURANCE
  ARGUS
  maturity gates
  risk treatment
  safety/security review

FACTORY_KNOWLEDGE
  templates
  patterns
  lessons
  prior risks
  domain construction knowledge

FACTORY_EXECUTOR_ADAPTERS
  AI/software
  simulation
  robotics
  industrial equipment

FACTORY_OPERATIONS
  handed-off runtime integration with FATHER
```

## Extraction triggers
Do not split merely because directories are large. Consider extraction when at least one is true:
- independent release cadence is repeatedly required;
- security/trust boundary requires physical separation;
- different teams own the domains;
- deployment/scaling characteristics materially differ;
- domain adapters create dependency conflicts;
- repository governance becomes a bottleneck;
- stable interfaces have been demonstrated by at least two implementations.

## Anti-patterns
- premature microservices;
- one repository per abstract concept;
- copying contracts instead of versioned dependencies;
- changing stable IDs during move;
- losing historical links when files move;
- making FATHER depend on a physical GitHub path.

## Migration rule
Physical separation is a routing/configuration event, not an identity rewrite.

Historical records must continue to resolve the exact contract/version they used at the time.
