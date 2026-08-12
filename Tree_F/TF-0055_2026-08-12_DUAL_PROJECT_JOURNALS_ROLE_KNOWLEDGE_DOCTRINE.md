# TF-0055 — Dual Project Journals + Role/Knowledge Doctrine

Date: 2026-08-12
Status: implemented
Projects: PX00/FATHER + PROJECT-FFB-0001

## Generation
Formalized the two-project operating model:
- PX00/FATHER keeps its own development journal and runtime/governance roadmap.
- FATHER Factory Builder keeps a separate `DEVELOPMENT_JOURNAL.md` and its own milestones.

Added Factory Builder doctrine for designing roles as reusable organizational modules with carefully bounded responsibilities, authority, handoffs, independence constraints, performance/anti-Goodhart controls and governed knowledge bindings.

## New surfaces
- `projects/FATHER_FACTORY_BUILDER/DEVELOPMENT_JOURNAL.md`
- `projects/FATHER_FACTORY_BUILDER/ROLE_AND_KNOWLEDGE_DESIGN_DOCTRINE.md`
- `projects/FATHER_FACTORY_BUILDER/contracts/FACTORY_ROLE_BLUEPRINT.yaml`
- `projects/FATHER_FACTORY_BUILDER/KNOWLEDGE_DOMAIN_REGISTRY.md`

## Core invariants
- `ROLE != AGENT != MODEL != DEVICE != KNOWLEDGE_SPACE`.
- knowledge is organizational infrastructure, not private executor memory.
- knowledge bindings reference stable logical spaces, not physical repository paths.
- role creation must be justified by a stable responsibility/capability boundary.
- physical KB extraction may happen later without rewriting canonical IDs or history.

## Next
Create the first reusable Factory Builder role set for `SUMMIT-FFB-01` and connect role blueprints to capability requirements and factory blueprint generation.
