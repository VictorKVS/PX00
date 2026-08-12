# Factory Builder — Knowledge Domain Registry

Date: 2026-08-12
Status: active planning registry
Project: `PROJECT-FFB-0001`

## Rule
The registry names logical knowledge domains required by reusable factory roles. Logical identity is stable; physical storage may migrate or split later.

## Current logical domains
| Knowledge space | Purpose | Typical roles | Current physical strategy |
|---|---|---|---|
| `KB-ARCHITECTURE` | system/enterprise architecture, patterns, ADRs, tradeoffs | Enterprise Architect, Factory Architect | KNOWLEDGE_CORE initially |
| `KB-SECURITY` | security architecture, threat modeling, controls, incidents | Security Architect, CISO, Security Engineer | KNOWLEDGE_CORE initially |
| `KB-PROGRAMMING` | software engineering, languages, libraries, patterns | Developer, Principal Engineer | KNOWLEDGE_CORE initially |
| `KB-DEVSECOPS` | CI/CD, build, supply chain, infrastructure security | DevSecOps Engineer, Platform Engineer | KNOWLEDGE_CORE initially |
| `KB-PRODUCT` | product requirements, users, value, prioritization | Product Manager, Business Analyst | KNOWLEDGE_CORE initially |
| `KB-RESEARCH` | research methods, literature, experiments, reproducibility | Researcher, Scientist | KNOWLEDGE_CORE initially |
| `KB-OSINT` | open-source research and collection methodology | OSINT Analyst | KNOWLEDGE_CORE initially |
| `KB-AI-AGENTS` | model/agent design, orchestration, evaluation | Agent Architect, LLM Engineer | KNOWLEDGE_CORE initially |

## Planned future domains
- `KB-ROBOTICS`
- `KB-MANUFACTURING`
- `KB-METROLOGY`
- `KB-SAFETY`
- `KB-SUPPLY-CHAIN`
- `KB-MAINTENANCE`
- `KB-QUALITY`
- `KB-INDUSTRIAL-AUTOMATION`
- `KB-DIGITAL-TWIN`
- `KB-ENERGY`
- `KB-LOGISTICS`
- `KB-LEGAL-JURISDICTION`

## Extraction criteria
A logical domain may become a separate physical repository when its size, ownership, security boundary, update cadence, validation pipeline or operational independence justifies extraction. Extraction is a routing change, not an identity rewrite.

## Anti-duplication rule
Do not create a role-specific repository merely because a role exists. Prefer shared canonical knowledge spaces with scoped bindings. Create a specialized logical domain only when the knowledge itself forms a distinct governed domain.

## Future structure
A mature Factory Builder should maintain reusable mappings:

`ROLE -> RESPONSIBILITIES -> CAPABILITIES -> PROTOCOLS -> KNOWLEDGE_BINDINGS -> EVALUATIONS -> RISKS`

This mapping becomes a component catalog for assembling new factories without copy-pasting old organizations.
