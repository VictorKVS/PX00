from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class RequestLike(Protocol):
    action_request_id: str
    capability: str
    target_ref: str
    classification: str
    side_effect_class: str
    payload: dict[str, Any]


class GrantLike(Protocol):
    action_request_id: str
    capability: str
    target_scope: str
    side_effect_ceiling: str
    data_classification_ceiling: str
    operation_count_limit: int
    one_time: bool
    status: str


@dataclass(frozen=True)
class BoundaryViolation(Exception):
    code: str

    def __str__(self) -> str:
        return self.code


class DeterministicMathTool:
    """Synthetic S0 tool used only to prove the PX00 boundary contract."""

    CAPABILITY = "math.multiply"
    TARGET = "synthetic://math.multiply"

    def execute(self, request: RequestLike, grant: GrantLike) -> int | float:
        if grant.status != "ACTIVE":
            raise BoundaryViolation("GRANT_NOT_ACTIVE")
        if grant.action_request_id != request.action_request_id:
            raise BoundaryViolation("GRANT_REQUEST_MISMATCH")
        if grant.capability != request.capability:
            raise BoundaryViolation("GRANT_CAPABILITY_MISMATCH")
        if grant.target_scope != request.target_ref:
            raise BoundaryViolation("GRANT_TARGET_MISMATCH")
        if request.capability != self.CAPABILITY or request.target_ref != self.TARGET:
            raise BoundaryViolation("UNSUPPORTED_SYNTHETIC_CAPABILITY")
        if request.side_effect_class != "S0" or grant.side_effect_ceiling != "S0":
            raise BoundaryViolation("SIDE_EFFECT_CEILING_EXCEEDED")
        if request.classification != "PUBLIC" or grant.data_classification_ceiling != "PUBLIC":
            raise BoundaryViolation("DATA_CLASSIFICATION_CEILING_EXCEEDED")
        if grant.operation_count_limit != 1:
            raise BoundaryViolation("INVALID_OPERATION_LIMIT")

        left = request.payload.get("left")
        right = request.payload.get("right")
        if isinstance(left, bool) or isinstance(right, bool):
            raise BoundaryViolation("INVALID_OPERAND")
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise BoundaryViolation("INVALID_OPERAND")
        return left * right
