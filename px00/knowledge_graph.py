from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class SourceNode:
    source_id: str
    source_type: str
    locator: str
    independence_group: str
    parent_source_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvidenceNode:
    evidence_id: str
    source_ref: str
    stance: str
    independence_group: str
    parent_evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ClaimNode:
    claim_id: str
    statement: str
    supersedes: str | None = None


@dataclass
class ClaimEvidenceGraph:
    sources: Dict[str, SourceNode] = field(default_factory=dict)
    evidence: Dict[str, EvidenceNode] = field(default_factory=dict)
    claims: Dict[str, ClaimNode] = field(default_factory=dict)
    support_edges: set[tuple[str, str]] = field(default_factory=set)
    contradiction_edges: set[tuple[str, str]] = field(default_factory=set)

    def add_source(self, node: SourceNode) -> None:
        if node.source_id in self.sources:
            raise ValueError("SOURCE_ID_REUSE")
        for parent in node.parent_source_refs:
            if parent not in self.sources:
                raise ValueError("UNKNOWN_PARENT_SOURCE")
        self.sources[node.source_id] = node

    def add_evidence(self, node: EvidenceNode) -> None:
        if node.evidence_id in self.evidence:
            raise ValueError("EVIDENCE_ID_REUSE")
        if node.source_ref not in self.sources:
            raise ValueError("UNKNOWN_SOURCE_REF")
        if node.stance not in {"SUPPORT", "CONTRADICT"}:
            raise ValueError("UNKNOWN_EVIDENCE_STANCE")
        for parent in node.parent_evidence_refs:
            if parent not in self.evidence:
                raise ValueError("UNKNOWN_PARENT_EVIDENCE")
        source = self.sources[node.source_ref]
        if source.independence_group != node.independence_group:
            raise ValueError("INDEPENDENCE_GROUP_MISMATCH")
        self.evidence[node.evidence_id] = node

    def add_claim(self, node: ClaimNode) -> None:
        if node.claim_id in self.claims:
            raise ValueError("CLAIM_ID_REUSE")
        if node.supersedes is not None:
            if node.supersedes not in self.claims:
                raise ValueError("UNKNOWN_SUPERSEDED_CLAIM")
            cursor = node.supersedes
            seen = {node.claim_id}
            while cursor is not None:
                if cursor in seen:
                    raise ValueError("CLAIM_SUPERSESSION_CYCLE")
                seen.add(cursor)
                cursor = self.claims[cursor].supersedes
        self.claims[node.claim_id] = node

    def link_evidence(self, claim_id: str, evidence_id: str) -> None:
        if claim_id not in self.claims:
            raise ValueError("UNKNOWN_CLAIM_REF")
        if evidence_id not in self.evidence:
            raise ValueError("UNKNOWN_EVIDENCE_REF")
        node = self.evidence[evidence_id]
        edge = (claim_id, evidence_id)
        if node.stance == "SUPPORT":
            self.support_edges.add(edge)
        else:
            self.contradiction_edges.add(edge)

    def evidence_for_claim(self, claim_id: str) -> Tuple[EvidenceNode, ...]:
        if claim_id not in self.claims:
            raise ValueError("UNKNOWN_CLAIM_REF")
        refs = [eid for cid, eid in self.support_edges | self.contradiction_edges if cid == claim_id]
        return tuple(self.evidence[eid] for eid in sorted(refs))

    def claim_lineage(self, claim_id: str) -> tuple[str, ...]:
        if claim_id not in self.claims:
            raise ValueError("UNKNOWN_CLAIM_REF")
        lineage = []
        cursor: str | None = claim_id
        while cursor is not None:
            lineage.append(cursor)
            cursor = self.claims[cursor].supersedes
        return tuple(lineage)
