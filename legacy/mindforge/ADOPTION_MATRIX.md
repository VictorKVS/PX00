# MindForge -> PX00 Adoption Matrix

Status: INITIAL DRAFT

MindForge is treated as a predecessor and donor of architectural ideas. PX00 does not automatically inherit MindForge implementation choices.

| MindForge concept | PX00 decision | Target |
|---|---|---|
| Orchestrator | ADAPT | PX00 governance/control plane |
| Registry | ADAPT | project/role/protocol/capability registries |
| Audit trail | KEEP + STRENGTHEN | universal event/trace/provenance model |
| Product / Architecture / Engineering separation | KEEP | governance/document lifecycle |
| Specs as source of truth | KEEP | contracts before runtime |
| Architecture Lab / evolution history | KEEP | architecture laboratory and ADR history |
| NormGraph | ADAPT | compliance/knowledge/provenance graph |
| Node/edge weights | ADAPT | confidence + evidence + provenance + contradiction + temporal validity |
| OSINT Hub | MOVE | independent managed OSINT product/project |
| Project Analyzer | MOVE/ADAPT | analytics project/role capability |
| Policy Engine | DEFER / SEPARATE CAPABILITY | governed compliance/policy project if justified |
| Threat Modeler | ADAPT | security role/capability, not core business logic |
| RAG | KEEP AS TECHNIQUE | role/domain/project KB retrieval; not authority by itself |
| Vector store | DEFER IMPLEMENTATION | choose only when requirements justify it |
| Qdrant / FAISS | DEFER IMPLEMENTATION | implementation detail, not baseline invariant |
| Celery / Redis | DEFER | adopt only for proven runtime need |
| Kubernetes | DEFER | deployment option, not core requirement |
| Many specialized agents | REWORK | governed Role Packages with explicit contracts |
| LLM router/providers | ADAPT LATER | replaceable processing providers under role governance |
| Telemetry | KEEP + INTEGRATE | operational telemetry distinct from audit/provenance |
| CI/CD / DevSecOps | KEEP + STRENGTHEN | supply-chain, security, test and release assurance |

## Next review

The matrix is intentionally conceptual. Before code reuse, each candidate component must receive separate source, security, licensing, dependency, test, and architecture review.
